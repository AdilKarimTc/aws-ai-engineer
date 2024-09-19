import streamlit as st
import boto3
from botocore.exceptions import ClientError
import json

# Initialize AWS Bedrock client
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-west-2'  # Replace with your AWS region
)

# Initialize Bedrock Knowledge Base client
bedrock_kb = boto3.client(
    service_name='bedrock-agent-runtime',
    region_name='us-west-2'  # Replace with your AWS region
)

def query_knowledge_base(query, kb_id):
    try:
        response = bedrock_kb.retrieve(
            knowledgeBaseId=kb_id,
            retrievalQuery={
                'text': query
            },
            retrievalConfiguration={
                'vectorSearchConfiguration': {
                    'numberOfResults': 3
                }
            }
        )
        return response['retrievalResults']
    except ClientError as e:
        st.error(f"Error querying Knowledge Base: {e}")
        return []

def generate_response(prompt, model_id):
    try:
        response = bedrock.invoke_model(
            modelId=model_id,
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                "prompt": prompt,
                "max_tokens_to_sample": 300,
                "temperature": 0.7,
                "top_p": 0.9,
            })
        )
        return json.loads(response['body'].read())['completion']
    except ClientError as e:
        st.error(f"Error generating response: {e}")
        return ""

# Streamlit UI
st.title("Bedrock Chat Application")

# Sidebar for configurations
st.sidebar.header("Configuration")
model_id = st.sidebar.selectbox("Select LLM Model", ["anthropic.claude-v2", "ai21.j2-ultra", "amazon.titan-text-express-v1"])
kb_id = st.sidebar.text_input("Knowledge Base ID", "your-knowledge-base-id")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Query Knowledge Base
    kb_results = query_knowledge_base(prompt, kb_id)
    
    # Prepare context from Knowledge Base results
    context = "\n".join([result['content']['text'] for result in kb_results])
    
    # Generate response using LLM
    full_prompt = f"Human:Context: {context}\n\nUser: {prompt}\n\nAssistant:"
    response = generate_response(full_prompt, model_id)
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})