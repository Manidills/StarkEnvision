import base64
import io
import os
import PyPDF2
import tempfile
from PIL import Image
from classes import classes
from contracts import contracts
from dashboards import dash
from events import events
from prediction import pred
import streamlit as st
import requests
from tokens import tokens
from transactions import trans
from wallet_connect import wallet_connect
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import io


st.set_page_config(
    page_title="StarkEnvision",
    page_icon="❄️️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "This app generates scripts for data clean rooms!"
    }
)


st.sidebar.image("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZDFjb2UzaWFwMnZqZWE1b2N3Yjc5OTltYzdxM2h5YXY2MWd6MXBxbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/UAragLbg9oKRfZLThq/giphy.webp")
action = st.sidebar.radio("What action would you like to take?", ("Dashboards","Predictive_Analysis", "Tokens", "Contracts", "Events", "Transactions", "Classes"))


response = requests.get("https://www.starknet.io/wp-content/uploads/2024/04/sn_logo_banner.png")
img = Image.open(io.BytesIO(response.content))
new_image = img.resize((1500, 400))


def wallet_con():
    with st.sidebar:
        st.markdown('##')
        wallet =  wallet_connect(
            label="login", 
            key="login", 
            message="Login", 
            auth_token_contract_address="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            chain_name="ethereum", 
            contract_type="ERC20",
            num_tokens="0"
            )
        return wallet
    


if action == "Dashboards":
    st.image(new_image)
    dash()
elif action == "Predictive_Analysis":
    pred()
elif action == "Tokens":
    tokens()
elif action == "Contracts":
    contracts()
elif action == "Classes":
    classes()
elif action == "Transactions":
   trans()
elif action == "Events":
    events()


    

