import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd

def create_metric_card(title, content, key, description="No Description"):
    ui.metric_card(title=title, content=content, description=description, key=key)

def display(data):
    power_data_list = data.get('power_data', [])
    power_data = power_data_list[0] if power_data_list else {}
    date_time = power_data.get('DATECREATE' , 'N/A')
    
    st.write(f"Last updated data : {date_time}")

    PP4 = power_data.get('PP3B22KV', 'N/A')
    PP4Main = power_data.get('PP3BMain', 'N/A')

    cols = st.columns(5)
    with cols[2]:
        create_metric_card("Electricity", f"{PP4} Mw" , "PP4Gen")
    with cols[2]:
        create_metric_card("Steam", f"{PP4Main} kg/s" , "PP4Stream")