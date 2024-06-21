from io import StringIO
import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import altair as alt
import time
import os


def new_user():
    df = pd.read_csv("/data_pipeline/DailyNewUsers.csv")
    df['starknet_user_count'] = pd.to_numeric(df.starknet_user_count, errors='coerce')
    return df

def distribution():
    df = pd.read_csv("data_pipeline/ETHAmountDistributionStarkNet.csv")
    df['frequency'] = pd.to_numeric(df.frequency, errors='coerce')
    return df

def clamis():
    df = pd.read_csv("data_pipeline/QmNSh6cP52MEmA4hPZZ5WdKsr8uwY4JGdeP6qi3RmCZpqA.csv")
    df['cumulative_claims'] = pd.to_numeric(df.cumulative_claims, errors='coerce')
    df['claims'] = pd.to_numeric(df.claims, errors='coerce')
    return df

def rolling_sum_eth():
    df = pd.read_csv("data_pipeline/RollingsumofETHdepositedintoStarknetfromEthereumbyday.csv")
    df['rolling_sum'] = pd.to_numeric(df.rolling_sum, errors='coerce')
    return df

def rolling_sum():
    df = pd.read_csv("data_pipeline/RollingSumOfNewAddressesInteractiveWithStarknetFromEthernumbyday.csv")
    df['rolling_sum'] = pd.to_numeric(df.rolling_sum, errors='coerce')
    return df

def montly_new_user():
    df = pd.read_csv("data_pipeline/MonthlyNewUsers.csv")
    df['starknet_user_count'] = pd.to_numeric(df.starknet_user_count, errors='coerce')
    return df

def zk_vs_stack():
    df = pd.read_csv("data_pipeline/StarknetzkSyncTransactionCount.csv")
    df['deposit_amount_usd'] = pd.to_numeric(df.deposit_amount_usd, errors='coerce')
    df['balance_amount_usd'] = pd.to_numeric(df.balance_amount_usd, errors='coerce')
    return df

def active_users():
    df = pd.read_csv("/data_pipeline/DailyActiveUsers.csv")
    df['starknet_tx_count'] = pd.to_numeric(df.starknet_tx_count, errors='coerce')
    df['starknet_bridged_amount_usd'] = pd.to_numeric(df.starknet_bridged_amount_usd, errors='coerce')
    df['starknet_balance_amount_usd'] = pd.to_numeric(df.starknet_balance_amount_usd, errors='coerce')
    return df

def monthly_active_users():
    df = pd.read_csv("data_pipeline/MonthlyActiveUsers.csv")
    df['starknet_tx_count'] = pd.to_numeric(df.starknet_tx_count, errors='coerce')
    df['starknet_bridged_amount_usd'] = pd.to_numeric(df.starknet_bridged_amount_usd, errors='coerce')
    df['starknet_balance_amount_usd'] = pd.to_numeric(df.starknet_balance_amount_usd, errors='coerce')
    return df

def dash():

    st.markdown("##")
    st.write("""
        ### Starknet_Bridged_Amount_Usd ###
        """)
    current_file_path = os.path.abspath(__file__)

    # Display the current file path in the Streamlit app
    st.write(f"The current file path is: {current_file_path}")
    st.markdown("##")
    st.altair_chart(
        alt.Chart(active_users()).mark_line(color='blue').encode(
            y=alt.Y('starknet_bridged_amount_usd:N', sort='descending'),
            x=alt.X('block_date:T', sort='ascending'),
        ).properties(
        width=800,
        height=300
    ),  use_container_width=True
    )
    
    st.markdown("##")
    a,b = st.columns([2,2])
    with a:
        st.markdown("##")
        st.write("""
        ### Daily New Users ###
        """)
        st.markdown("##")
        st.altair_chart(
        alt.Chart(new_user()).mark_line(color='red').encode(
            y=alt.Y('starknet_user_count:N', sort='descending'),
            x=alt.X('block_date:T', sort='ascending'),
        ).properties(
        width=800,
        height=300
    ),  use_container_width=True
    )

    with b:
        st.markdown("##")
        st.write("""
            ### Active Users ###
            """)
        st.markdown("##")
        st.altair_chart(
            alt.Chart(active_users()).mark_line(color='yellow').encode(
                y=alt.Y('starknet_tx_count:N', sort='descending'),
                x=alt.X('block_date:T', sort='ascending'),
            ).properties(
            width=800,
            height=300
        ),  use_container_width=True
        )


    st.markdown("##")
    st.write("""
        ### starknet_balance_amount_usd ###
        """)
    st.markdown("##")
    st.altair_chart(
        alt.Chart(active_users()).mark_circle(color='blue').encode(
            y=alt.Y('starknet_balance_amount_usd:N', sort='descending'),
            x=alt.X('block_date:T', sort='ascending'),
        ).properties(
        width=800,
        height=300
    ),  use_container_width=True
    )

    st.markdown("##")
    a,b = st.columns([2,2])
    with a:
        st.markdown("##")
        st.write("""
        ### Montly Txs ###
        """)
        st.markdown("##")
        st.altair_chart(
        alt.Chart(monthly_active_users()).mark_line(color='green').encode(
            y=alt.Y('starknet_tx_count:N', sort='descending'),
            x=alt.X('block_date:T', sort='ascending'),
        ).properties(
        width=800,
        height=300
    ),  use_container_width=True
    )

    with b:
        st.markdown("##")
        st.write("""
            ### Montly Users ###
            """)
        st.markdown("##")
        st.altair_chart(
            alt.Chart(monthly_active_users()).mark_line(color='pink').encode(
                y=alt.Y('starknet_user_count:N', sort='descending'),
                x=alt.X('block_date:T', sort='ascending'),
            ).properties(
            width=800,
            height=300
        ),  use_container_width=True
        )
    

    st.markdown("##")
    st.write("""
    ### Montly New Users ###
    """)
    st.markdown("##")
    st.altair_chart(
    alt.Chart(montly_new_user()).mark_line(color='red').encode(
        y=alt.Y('starknet_user_count:N', sort='descending'),
        x=alt.X('block_date:T', sort='ascending'),
    ).properties(
    width=800,
    height=300
    ),  use_container_width=True
    )


    st.markdown("##")
    a,b = st.columns([2,2])
    with a:
    
        st.markdown("##")
        st.write("""
            ### Starknet_Vs_ZkSync  ###
            """)
        st.markdown("##")
        st.altair_chart(
            alt.Chart(zk_vs_stack()).mark_arc().encode(
                theta='type',
                color="deposit_amount_usd",    
            ).properties(
            width=800,
            height=300
        ),  use_container_width=True
        )
    
    with b:
        st.markdown("##")
        st.write("""
            ### Balance Amount USD  ###
            """)
        st.markdown("##")
        st.altair_chart(
            alt.Chart(zk_vs_stack()).mark_arc().encode(
                theta='type',
                color="balance_amount_usd", 
            ).properties(
            width=800,
            height=300
        ),  use_container_width=True
    
        )

    st.markdown("##")
    a,b = st.columns([2,2])
    with b:
        st.markdown("##")
        st.write("""
        ### RollingSum_Addresses ###
        """)
        st.markdown("##")
        st.altair_chart(
        alt.Chart(rolling_sum()).mark_line(color='orange').encode(
            y=alt.Y('rolling_sum:N', sort='descending'),
            x=alt.X('day:T', sort='ascending'),
        ).properties(
        width=800,
        height=300
        ),  use_container_width=True
        )
    with a:
        st.markdown("##")
        st.write("""
        ### RollingSum_ETH_deposits ###
        """)
        st.markdown("##")
        st.altair_chart(
        alt.Chart(rolling_sum_eth()).mark_line(color='brown').encode(
            y=alt.Y('rolling_sum:N', sort='descending'),
            x=alt.X('day:T', sort='ascending'),
        ).properties(
        width=800,
        height=300
        ),  use_container_width=True
        )
    
    st.markdown("##")
    st.write("""
    ### Claims ###
    """)
    st.markdown("##")
    st.altair_chart(
    alt.Chart(clamis()).mark_line(color='blue').encode(
        y=alt.Y('claims:N', sort='descending'),
        x=alt.X('date:T', sort='ascending'),
    ).properties(
    width=800,
    height=300
    ),  use_container_width=True
    )

    st.markdown("##")
    st.write("""
    ### Cumulative_Claims ###
    """)
    st.markdown("##")
    st.altair_chart(
    alt.Chart(clamis()).mark_bar(color='blue').encode(
        y=alt.Y('cumulative_claims:N', sort='descending'),
        x=alt.X('date:T', sort='ascending'),
    ).properties(
    width=800,
    height=300
    ),  use_container_width=True
    )


    st.markdown("##")
    st.write("""
        ### Distribution  ###
        """)
    st.markdown("##")
    st.altair_chart(
        alt.Chart(distribution()).mark_arc().encode(
            theta='range',
            color="frequency", 
        ).properties(
        width=800,
        height=300
    ),  use_container_width=True

    )
            
