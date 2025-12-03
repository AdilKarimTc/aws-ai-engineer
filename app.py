import streamlit as st
import boto3
from botocore.exceptions import ClientError
import json
from bedrock_utils import query_knowledge_base, generate_response, valid_prompt


# Streamlit UI
st.title("Bedrock Chat Application")

# Sidebar for configurations
st.sidebar.header("Configuration")
model_id = st.sidebar.selectbox("Select LLM Model", ["anthropic.claude-3-haiku-20240307-v1:0", "anthropic.claude-3-5-sonnet-20240620-v1:0"])
kb_id = st.sidebar.text_input("Knowledge Base ID", "DU9AYF1KM2")
temperature = st.sidebar.select_slider("Temperature", [i/10 for i in range(0,11)],1)
top_p = st.sidebar.select_slider("Top_P", [i/1000 for i in range(0,1001)], 1)
debug_mode = st.sidebar.checkbox("Debug Mode", value=False)

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

    try:
        validation_result = valid_prompt(prompt, model_id)
        if debug_mode:
            st.sidebar.write(f"🔍 Debug: Validation result = {validation_result}")
        
        if validation_result:
            # Check if Knowledge Base ID is configured
            if kb_id == "your-knowledge-base-id" or not kb_id:
                response = "⚠️ Please configure your Knowledge Base ID in the sidebar."
            else:
                # Query Knowledge Base
                kb_results = query_knowledge_base(prompt, kb_id)
                if debug_mode:
                    st.sidebar.write(f"🔍 Debug: Found {len(kb_results)} KB results")
                
                # Prepare context from Knowledge Base results
                if kb_results:
                    context = "\n".join([
                        result.get('content', {}).get('text', '') 
                        for result in kb_results 
                        if result.get('content', {}).get('text')
                    ])
                    
                    if context:
                        # Generate response using LLM with context
                        full_prompt = f"Context: {context}\n\nUser: {prompt}\n\nAssistant:"
                        response = generate_response(full_prompt, model_id, temperature, top_p)
                        if not response:
                            response = "⚠️ Error generating response. Please check your AWS credentials and model configuration."
                    else:
                        response = "I couldn't find relevant information in the knowledge base. Please try rephrasing your question."
                else:
                    response = "I couldn't find relevant information in the knowledge base. Please try rephrasing your question."
        else:
            response = "I'm unable to answer this question. Please ask about heavy machinery specifications, features, or related topics."
            if debug_mode:
                st.sidebar.warning("🔍 Debug: Prompt validation failed. Check terminal for category classification.")
    except Exception as e:
        error_msg = str(e)
        if "credentials" in error_msg.lower() or "profile" in error_msg.lower():
            response = f"⚠️ AWS Credentials Error: {error_msg}\n\nPlease configure your AWS credentials using:\n- AWS CLI: `aws configure`\n- Environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY\n- Or update your AWS credentials file."
        else:
            response = f"⚠️ Error: {error_msg}"
        if debug_mode:
            st.sidebar.error(f"🔍 Debug Error: {error_msg}")
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})