import streamlit as st
import openai
import pandas as pd
import os
from PIL import Image
from langchain.callbacks import StreamlitCallbackHandler
from dotenv import load_dotenv

load_dotenv()
ss = st.session_state

st.title("Expert AI")
st.write('''### Extract structure-function relationships from your data!

This is a simple app which helps you to extract human interpretable relationships
in your dataset. ''')

# Set width of sidebar
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"]{
        min-width: 450px;
        max-width: 450px;
    }
    """,
    unsafe_allow_html=True,
)

def on_api_key_change():
    api_key = ss.get('api_key') or os.getenv('OPENAI_API_KEY')
    #api_key = os.getenv('OPENAI_API_KEY')
    os.environ["OPENAI_API_KEY"] = api_key
    from expert_ai.tools import tools
    from expert_ai.agent import ExpertAI
    global agent    
    agent = ExpertAI(verbose=True)


# sidebar
with st.sidebar:
    logo = Image.open('assets/logo.png')
    st.image(logo)

    # Input OpenAI api key
    st.markdown('Input your OpenAI API key.')
    api_key = st.text_input('OpenAI API key', type='password', key='api_key',  
                  on_change=on_api_key_change, label_visibility="visible")   
    if api_key:
        on_api_key_change() 
    st.markdown('Upload your input files')
    input_file = st.file_uploader("Upload dataset here:")
    lit_dir = st.file_uploader("Upload your literature library here:", 
                               accept_multiple_files=True)
    

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    if input_file is not None:
        prompt += f'datapath:{input_file}'
    
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        try:
         response = agent.run(query=prompt)
        ## TEST THIS LATER
        except Exception as e:
            response = str(e)
            if response.startswith("Could not parse LLM output: `"):
                response = response.removeprefix("Could not parse LLM output: `").removesuffix("`")
                print(response)
    
        st.write(response)
