"""
Run gcloud auth application-default login 
"""
from google.cloud import geminidataanalytics as geminidataanalytics

PROJECT_ID = "509008414646"
LOCATION = "us"
AGENT_ID = "agent_cad6411c-7fbb-48bb-8d06-18fa3542feb5"

def test_data_agent():
    # 1. Initialize the regional client
    client_options = {"api_endpoint": "geminidataanalytics.us.rep.googleapis.com"}
    chat_client = geminidataanalytics.DataChatServiceClient(client_options=client_options)
    
    parent_path = f"projects/{PROJECT_ID}/locations/{LOCATION}"
    agent_path = f"projects/{PROJECT_ID}/locations/{LOCATION}/dataAgents/{AGENT_ID}"
    
    # 2. Define the Conversation object with your agent registered
    print("Preparing conversation session...")
    conversation_payload = geminidataanalytics.Conversation(
        agents=[agent_path]
    )
    
    # 3. Create the conversation request
    request_create = geminidataanalytics.CreateConversationRequest(
        parent=parent_path,
        conversation=conversation_payload
    )
    
    print("Creating conversation session on GCP...")
    conversation = chat_client.create_conversation(request=request_create)
    conversation_name = conversation.name
    print(f"Conversation created successfully: {conversation_name}\n")
    
    # 4. Construct the ConversationReference for chatting
    conversation_ref = geminidataanalytics.ConversationReference(
        conversation=conversation_name,
        data_agent_context=geminidataanalytics.DataAgentContext(
            data_agent=agent_path
        )
    )
    
    user_message = geminidataanalytics.Message(
        user_message=geminidataanalytics.UserMessage(
            text="Provide a summary of the data tables you can query."
        )
    )
    
    chat_request = geminidataanalytics.ChatRequest(
        parent=parent_path,
        messages=[user_message],
        conversation_reference=conversation_ref
    )
    
    print("Asking Agent: 'Provide a summary of the data tables you can query.'")
    print("-" * 50)
    
    # 5. Stream and print the response
    stream = chat_client.chat(request=chat_request)
    for response_chunk in stream:
        if response_chunk.system_message:
            sys_msg = response_chunk.system_message
            if sys_msg.text:
                if hasattr(sys_msg.text, "content"):
                    print(sys_msg.text.content, end="", flush=True)
                else:
                    print(sys_msg.text, end="", flush=True)
            
    print("\n" + "-" * 50)

if __name__ == "__main__":
    test_data_agent()
