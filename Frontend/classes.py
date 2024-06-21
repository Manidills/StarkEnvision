import requests
import streamlit as st
import pandas as pd
import datetime
import altair as alt
import time
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report




def classes():
    st.title("Classes Data Fetcher")

    

    # Input fields
   
    Class_hash = st.text_input("Enter Class_hash")
    ps = st.number_input("Page Size (ps)", min_value=1, value=10)
    p = st.number_input("Page Number (p)", min_value=1, value=1)


        
    # Fetch data button
    if st.button("Fetch Data"):
        if Class_hash:
            url = f"https://api.voyager.online/beta/classes/{Class_hash}"
            headers = {
                "accept": "application/json",
                "x-api-key": "Kcb7B3do0Q6Vd9FHlI2UO6q92MM8hGW37NiYk2t9"
            }
            
            response = requests.get(url, headers=headers)
        else:

        # API Call
            url = f"https://api.voyager.online/beta/classes?ps={ps}0&p={p}"
            headers = {
                "accept": "application/json",
                "x-api-key": "Kcb7B3do0Q6Vd9FHlI2UO6q92MM8hGW37NiYk2t9"
            }
            
            response = requests.get(url, headers=headers)
       

        
        
        if response.status_code == 200:
            data_ = response.json()
            st.markdown("##")
            if Class_hash:
                st.write(data_)
            else:
                df = pd.DataFrame(data_['items'])

                # Display data in a dataframe
                st.dataframe(df)

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