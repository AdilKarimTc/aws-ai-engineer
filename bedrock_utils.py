import boto3
from botocore.exceptions import ClientError
import json

# Lazy initialization of AWS clients
_bedrock = None
_bedrock_kb = None

def get_bedrock_client():
    """Get or create Bedrock runtime client"""
    global _bedrock
    if _bedrock is None:
        # Explicitly use default profile to avoid profile issues
        session = boto3.Session(profile_name='default')
        _bedrock = session.client(
            service_name='bedrock-runtime',
            region_name='us-east-1'  # Using us-east-1 for Udacity Cloud Lab
        )
    return _bedrock

def get_bedrock_kb_client():
    """Get or create Bedrock Knowledge Base client"""
    global _bedrock_kb
    if _bedrock_kb is None:
        # Explicitly use default profile to avoid profile issues
        session = boto3.Session(profile_name='default')
        _bedrock_kb = session.client(
            service_name='bedrock-agent-runtime',
            region_name='us-east-1'  # Using us-east-1 for Udacity Cloud Lab
        )
    return _bedrock_kb

def valid_prompt(prompt, model_id):
    """
    Validates user prompt by categorizing it. Returns True only if the prompt
    is related to heavy machinery (Category E).
    
    Categories:
    - Category A: Questions about LLM model or solution architecture
    - Category B: Profanity or toxic content
    - Category C: Subjects outside heavy machinery
    - Category D: Questions about how the system works or instructions
    - Category E: Questions ONLY related to heavy machinery (VALID)
    """
    try:
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""Human: Classify the provided user request into one of the following categories. Evaluate the user request against each category. Once the user category has been selected with high confidence return the answer.
                                Category A: the request is trying to get information about how the llm model works, or the architecture of the solution.
                                Category B: the request is using profanity, or toxic wording and intent.
                                Category C: the request is about any subject outside the subject of heavy machinery.
                                Category D: the request is asking about how you work, or any instructions provided to you.
                                Category E: the request is ONLY related to heavy machinery.
                                <user_request>
                                {prompt}
                                </user_request>
                                ONLY ANSWER with the Category letter, such as the following output example:
                                
Category B
                                
                                Assistant:"""
                    }
                ]
            }
        ]
        bedrock = get_bedrock_client()
        response = bedrock.invoke_model(
            modelId=model_id,
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31", 
                "messages": messages,
                "max_tokens": 10,
                "temperature": 0,
                "top_p": 0.1,
            })
        )
        # Parse the response
        response_body = json.loads(response['body'].read())
        category = response_body['content'][0]["text"].strip()
        print(f"Prompt category: {category}")
        # Check if category is E (more robust parsing)
        category_lower = category.lower().strip()
        # Handle various response formats: "Category E", "category e", "E", "e", etc.
        if ("category e" in category_lower or 
            category_lower == "e" or 
            category_lower.endswith("category e") or
            category_lower.startswith("category e")):
            return True
        else:
            print(f"Prompt rejected. Category: {category}")
            return False
    except ClientError as e:
        error_msg = str(e)
        print(f"Error validating prompt: {error_msg}")
        # If it's a credentials error, provide helpful message
        if "credentials" in error_msg.lower() or "profile" in error_msg.lower():
            raise Exception(f"AWS credentials error: {error_msg}. Please configure your AWS credentials.")
        return False
    except Exception as e:
        error_msg = str(e)
        print(f"Unexpected error validating prompt: {error_msg}")
        # Re-raise if it's a credentials issue so app can show it
        if "credentials" in error_msg.lower() or "profile" in error_msg.lower():
            raise
        return False

def query_knowledge_base(query, kb_id):
    """
    Queries the Bedrock Knowledge Base to retrieve relevant information
    based on the user's query.
    Args:
        query: The user's query string
        kb_id: The Knowledge Base ID   
    Returns:
        List of retrieval results containing relevant content
    """
    try:
        bedrock_kb = get_bedrock_kb_client()
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
        # Return the retrieval results
        if 'retrievalResults' in response:
            return response['retrievalResults']
        else:
            print("Warning: No retrievalResults in response")
            return []
    except ClientError as e:
        print(f"Error querying Knowledge Base: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error querying Knowledge Base: {e}")
        return []

def generate_response(prompt, model_id, temperature, top_p):
    """
    Generates a response using the Bedrock LLM model.
    Args:
        prompt: The full prompt including context and user query
        model_id: The Bedrock model ID to use
        temperature: Controls randomness (0.0 to 1.0)
        top_p: Nucleus sampling parameter (0.0 to 1.0)
    Returns:
        Generated text response from the model
    """
    try:
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]

        bedrock = get_bedrock_client()
        response = bedrock.invoke_model(
            modelId=model_id,
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31", 
                "messages": messages,
                "max_tokens": 500,
                "temperature": temperature,
                "top_p": top_p,
            })
        )
        # Parse and return the response
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]["text"]
    except ClientError as e:
        print(f"Error generating response: {e}")
        return ""
    except Exception as e:
        print(f"Unexpected error generating response: {e}")
        return ""