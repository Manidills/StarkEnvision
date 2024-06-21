import asyncio
import yfinance as yf
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import MinMaxScaler
from torch.utils.data import DataLoader, TensorDataset
import streamlit as st
import pandas_datareader as web
import matplotlib.pyplot as plt
import mplfinance as mpf
import datetime as dt
import altair as alt

from starknet_py.net.models import StarknetChainId
from starknet_py.net.account.account import Account
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet.helpers import swap_eth_to_usdc, get_balance, swap_usdc_to_eth


ADDRESSES = {
    "ETH": {
        "SN_MAIN" : "0x49d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7"
    },
    "USDC": {
        "SN_MAIN" : "0x053c91253bc9682c04929ca02ed00b3e423f6710d2ee7e0d5ebb06f3ecf368a8"
    },
    "AVNU_EXCHANGE": {
        "SN_MAIN" : "0x04270219d365d6b017231b52e92b3fb5d7c8378b05e9abc97724537a80e93b0f"
    },
}


async def create_model_(private_key,address,next_price,current_price):

    client = FullNodeClient(node_url='https://starknet-mainnet.public.blastapi.io')
    account = Account(
        client=client,
        address=address,
        key_pair=KeyPair.from_private_key(private_key),
        chain=StarknetChainId.MAINNET,
    )

    if next_price > current_price * 1.01:
        usdc_balance = await get_balance(account, '0x053c91253bc9682c04929ca02ed00b3e423f6710d2ee7e0d5ebb06f3ecf368a8') 
        usdc_balance = usdc_balance / 10**6   
        st.info(f"Your USDC balance: {usdc_balance:.2f}")
        if usdc_balance > 0.2:
                st.info("Buying ETH with 0.1 USDC....")
                tx_hash = await swap_usdc_to_eth(account, 0.1)
                st.info(f"Transaction hash: {tx_hash}")
        else:
                st.info("Insufficient USDC balance to buy ETH")
        
    elif next_price < current_price * 0.99:
        eth_balance = await get_balance(account, '0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7')
        eth_balance = eth_balance / 10**18
        print(eth_balance)
        st.info(f"ETH balance: {eth_balance:.18f}")
        if eth_balance > 0:
            st.info("Selling ETH for USDC....")
            tx_hash = await swap_eth_to_usdc(account, eth_balance, address)
            st.info(f"Transaction hash: {tx_hash}")
        else:
            st.info("No ETH balance to sell")

# Step 1: Fetch Historical Price Data
def fetch_data(ticker, start_date):
    data = yf.download(ticker, start=start_date)
    return data['Close'].values.reshape(-1, 1)

# Step 2: Preprocess Data
def preprocess_data(data, window_size):
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)
    
    X = []
    y = []
    for i in range(window_size, len(data_scaled)):
        X.append(data_scaled[i-window_size:i, 0])
        y.append(data_scaled[i, 0])
    
    X = np.array(X)
    y = np.array(y)
    
    return X, y, scaler

# Step 3: Build the Neural Network Model
class PricePredictor(nn.Module):
    def __init__(self, input_size):
        super(PricePredictor, self).__init__()
        self.fc1 = nn.Linear(input_size, 50)
        self.fc2 = nn.Linear(50, 25)
        self.fc3 = nn.Linear(25, 1)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# Step 4: Train the Model
def train_model(model, dataloader, criterion, optimizer, epochs=50):
    model.train()
    for epoch in range(epochs):
        for inputs, targets in dataloader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

# Step 5: Predict the Next Price
def predict_next_price(model, data, window_size, scaler):
    model.eval()
    last_window = data[-window_size:]
    last_window_scaled = scaler.transform(last_window)
    last_window_scaled = torch.tensor(last_window_scaled, dtype=torch.float32).view(1, -1)
    
    with torch.no_grad():
        predicted_price_scaled = model(last_window_scaled)
    
    predicted_price = scaler.inverse_transform(predicted_price_scaled.numpy().reshape(-1, 1))
    return predicted_price[0, 0]

# Step 6: Convert Model to ONNX
def serialize_to_onnx(model, input_size, onnx_file_path):
    model.eval()
    dummy_input = torch.randn(1, input_size)
    torch.onnx.export(model, dummy_input, onnx_file_path,
                      input_names=['input'], output_names=['output'],
                      dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}})
    print(f"✅ Model has been converted to ONNX and saved at {onnx_file_path} ")

# Main execution
def pred():


    start = dt.datetime(2020,1,1)
    end = dt.datetime.now()

    st.write(""" ## Cryptocurrency Price Visualizer """)

    crypto_name = st.selectbox("Select Cryptcurrency",("STRK","ETH","BTC","DOGE","ADA","XRP","TRX","LINK",))
    currency_name = st.selectbox("Select Local Currency",("USD","EUR","INR","CAD","AUD","GBP"))
    custom = st.text_input("Enter crypto-currency")
    address = st.text_input("Enter wallet address")
    private_key = st.text_input("Enter private key")

    if st.button("Visualize"):
        custom_data = custom.split("-")
        if custom:
            crypto_name = custom_data[0]
            currency_name = custom_data[1]
            data = yf.download(tickers=f"{crypto_name}-{currency_name}", start=start, end=end)
        else:
            data = yf.download(tickers=f"{crypto_name}-{currency_name}", start=start, end=end)
        # data = web.DataReader(f"{crypto_name}-{currency_name}", "yahoo")
        # st.write(pd.DataFrame(data))
        st.write(f"Ploting the graph between {crypto_name} and {currency_name}.")
  
        s = data['Close'].tail(1) 
        st.write(f"The closing price for the {crypto_name} is {s} ")

        st.markdown("##")
        data = data.reset_index()
        data['Date'] = pd.to_datetime(data.Date, errors='coerce')
        st.altair_chart(
        alt.Chart(data).mark_line(color='blue').encode(
            y=alt.Y('Close:N', sort='descending'),
            x=alt.X('Date:T', sort='ascending'),
        ).properties(
        width=800,
        height=300
        ),  use_container_width=True
        )

        # Parameters
     
        ticker_pair = f"{crypto_name}-{currency_name}"
        ticker = ticker_pair
        start_date = "2020-01-01"
        window_size = 60
        batch_size = 32
        epochs = 50



        
        # Fetch and preprocess data
        print("Fetching and preprocessing data...")
        data = fetch_data(ticker, start_date)
        X, y, scaler = preprocess_data(data, window_size)
        
        # Convert to PyTorch tensors
        X_tensor = torch.tensor(X, dtype=torch.float32)
        y_tensor = torch.tensor(y, dtype=torch.float32).view(-1, 1)
        
        # Create DataLoader
        print("Creating DataLoader...")
        dataset = TensorDataset(X_tensor, y_tensor)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        # Build and train model
        print("Building and training model...")
        model = PricePredictor(X_tensor.shape[1])
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        
        train_model(model, dataloader, criterion, optimizer, epochs=epochs)
        
        # Predict the next price
        st.info("Predicting the next price...")
        next_price = predict_next_price(model, data, window_size, scaler)
        st.success(f"Predicted next price of {crypto_name}-{currency_name}: {next_price}")



        

        if private_key: 
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            model = loop.run_until_complete(create_model_(private_key, address, next_price,s[0]))
            st.write(model)

        else:
            st.info("No Private key")

    

