"""
Run gcloud auth application-default login
"""
import json
from google.cloud import geminidataanalytics as geminidataanalytics
from google.protobuf.json_format import MessageToDict
 
PROJECT_ID = "509008414646"
LOCATION = "us"
AGENT_ID = "agent_cad6411c-7fbb-48bb-8d06-18fa3542feb5"
 
 
def ask_data_agent(question: str) -> dict:
    """
    Sends `question` to the registered Data Agent and returns the FULL
    response as a JSON-serializable dict (no incremental printing).
 
    Returns a dict shaped like:
    {
        "question": "...",
        "conversation": "projects/.../conversations/...",
        "answer": "<concatenated text answer>",
        "messages": [ {...raw-ish parsed chunk...}, ... ]
    }
    """
    # 1. Initialize the regional client
    client_options = {"api_endpoint": "geminidataanalytics.us.rep.googleapis.com"}
    chat_client = geminidataanalytics.DataChatServiceClient(client_options=client_options)
 
    parent_path = f"projects/{PROJECT_ID}/locations/{LOCATION}"
    agent_path = f"projects/{PROJECT_ID}/locations/{LOCATION}/dataAgents/{AGENT_ID}"
 
    # 2. Create the conversation session
    conversation_payload = geminidataanalytics.Conversation(agents=[agent_path])
    request_create = geminidataanalytics.CreateConversationRequest(
        parent=parent_path,
        conversation=conversation_payload,
    )
    conversation = chat_client.create_conversation(request=request_create)
    conversation_name = conversation.name
 
    # 3. Build the chat request
    conversation_ref = geminidataanalytics.ConversationReference(
        conversation=conversation_name,
        data_agent_context=geminidataanalytics.DataAgentContext(
            data_agent=agent_path
        ),
    )
 
    user_message = geminidataanalytics.Message(
        user_message=geminidataanalytics.UserMessage(text=question)
    )
 
    chat_request = geminidataanalytics.ChatRequest(
        parent=parent_path,
        messages=[user_message],
        conversation_reference=conversation_ref,
    )
 
    # 4. Consume the stream silently, converting every chunk to a plain dict.
    #    We do NOT guess field names here — MessageToDict gives us whatever
    #    the server actually sent, so nothing gets silently dropped.
    answer_parts = []
    raw_messages = []
 
    stream = chat_client.chat(request=chat_request)
    for response_chunk in stream:
        try:
            # protobuf >= 5.x
            chunk_dict = MessageToDict(
                response_chunk._pb,
                preserving_proto_field_name=True,
                always_print_fields_with_no_presence=True,
            )
        except TypeError:
            # protobuf < 5.x uses the older kwarg name
            chunk_dict = MessageToDict(
                response_chunk._pb,
                preserving_proto_field_name=True,
                including_default_value_fields=True,
            )
        raw_messages.append(chunk_dict)
 
        # Walk the dict looking for text content, regardless of exact shape
        # (observed shapes: systemMessage.text.parts [list] or .content [str]).
        sys_msg = chunk_dict.get("system_message", {})
        text_block = sys_msg.get("text")
        if text_block:
            if isinstance(text_block, str):
                answer_parts.append(text_block)
            elif isinstance(text_block, dict):
                parts = text_block.get("parts") or text_block.get("content")
                if isinstance(parts, list):
                    answer_parts.extend(str(p) for p in parts)
                elif isinstance(parts, str):
                    answer_parts.append(parts)
 
    result = {
        "question": question,
        "conversation": conversation_name,
        "answer": "".join(answer_parts).strip(),
        "messages": raw_messages,
    }
    return result
 
 
if __name__ == "__main__":
    output = ask_data_agent("Provide a summary of the data tables you can query.")
    # Only the final JSON is printed — nothing streamed incrementally.
    print(json.dumps(output, indent=2, default=str))