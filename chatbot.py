import streamlit as st
from openai import OpenAI

    
st.set_page_config(page_title="Ecommerce Chatbot")
with st.sidebar:
    st.title('Mumbai Marines : Ecommerce Product Search and Image Captioning')

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def get_openai_context(prompt:str, chat_history:str, max_tokens) -> str:
    """Get context from OpenAI model."""
    response=client.chat.completions.create(
        model="model-identifier",
        messages=[
            # {"role": "system", "content": prompt},
            # {"role": "user", "content": chat_history}
            {"role": "system", "content": "Always answer in rhymes."},
            {"role": "user", "content": "Introduce yourself."}
        ],
        temperature=0.5,
    )
    return response.choices[0].message.content

# Function for generating LLM response
def generate_response(input,max_tokens):
    result = get_openai_context("",input,max_tokens)
    return result

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Hello there!, i am your search assisstant, How can i help you? 😊"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def extract_details(prompt):
    # Define prompts for LLM to determine gender and occasion
    gender_prompt = f"Identify the gender for this fashion query [men/women/boy/girl]: {prompt}"
    occasion_prompt = f"This query is about a particular type of product: {prompt}"
    gender=generate_response(gender_prompt,200)
    occasion=generate_response(occasion_prompt,200)
    return gender



def check_context(prompt):
    greeting=False
    genderspecific=False
    occasionspecified=False
    gender=""
    occasion=""
    
    isgender_prompt = f"This is about internal product search. Does this prompt gives enough context to understand to a specic gender the product search is for? answer with yes or no: {prompt}"
    findingoccasion = f"Does this prompt provide enough context to identify for which occasion they are finding clothes for or they are specific about which product to buy reply with yes or no :{prompt}"

    if generate_response(isgender_prompt,1).lower=="true":
        genderspecific = True
    if generate_response(findingoccasion,1).lower=="true":
        occasionspecified = True
    while not genderspecific or not occasionspecified:
        if not genderspecific:
            response=generate_response("As the gender is not specific in the previous prompt. Ask for the specific gender for which they wish to buy fashion products for.",50)
        elif not occasionspecified:
            response=generate_response("As the occasion is not specific in the previous prompt. Ask for the specific occasion or specific clothes they have in mind for which they wish to buy fashion products for.",50)
        else:
            gender=extract_details(prompt)
    return response
            
# User-provided prompt
if input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": input})
    with st.chat_message("user"):
        st.write(input)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            response = check_context(input)
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)