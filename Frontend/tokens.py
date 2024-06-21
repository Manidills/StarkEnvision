import requests
import streamlit as st
import pandas as pd
import datetime
import altair as alt
import time
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report




def tokens():
    st.title("Voyager API Data Fetcher")

    

    # Input fields
    attribute = st.selectbox("Select Attribute", ["holders", "transfers"])
    type_ = st.selectbox("Select Type", ["erc721", "erc20", "erc1155"])
    ps = st.number_input("Page Size (ps)", min_value=1, value=10)
    p = st.number_input("Page Number (p)", min_value=1, value=1)

    if attribute == 'holders':
        if type_ == 'erc20':
            data = pd.read_csv('data_pipeline/tokens_erc20.csv')
            data['Holders'] = pd.to_numeric(data['Holders'])
        elif type_ == 'erc721':
            data = pd.read_csv('data_pipeline/tokens_erc721.csv')
            data['Holders'] = pd.to_numeric(data['Holders'])
        else:
            data = pd.read_csv('data_pipeline/tokens_erc1155.csv')
            data['Holders'] = pd.to_numeric(data['Holders'])
        


        min_holders, max_holders = st.slider(
                'Select range for holders',
                min_value=int(data['Holders'].min()),
                max_value=int(data['Holders'].max()),
                value=(int(data['Holders'].min()), int(data['Holders'].max()))
            )
        

    # Fetch data button
    if st.button("Fetch Data"):
        # API Call
        url = f"https://api.voyager.online/beta/tokens?attribute={attribute}&type={type_}&ps={ps}&p={p}"
        headers = {
            "accept": "application/json",
            "x-api-key": "Kcb7B3do0Q6Vd9FHlI2UO6q92MM8hGW37NiYk2t9"
        }
        
        response = requests.get(url, headers=headers)
       

        
        
        if response.status_code == 200:
            data_ = response.json()
            st.markdown("##")
            df = pd.DataFrame(data_['items'])

            # Display data in a dataframe
            st.dataframe(df)

            if attribute == 'holders':
                st.markdown("##")
                st.write("Filtered DATA")

                df_filtered = data[(data['Holders'] >= min_holders) & (data['Holders'] <= max_holders)]
                st.dataframe(df_filtered)
        
            # Download as CSV
            st.markdown("##")
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='voyager_data.csv',
                mime='text/csv',
            )

            st.markdown("##")
            with st.expander('Check Report'):
                pr = ProfileReport(df, explorative=True)
                st_profile_report(pr)
        else:
            st.error("Failed to fetch data. Please try again.")