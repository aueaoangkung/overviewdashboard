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
    
    PP5 = power_data.get('PP522KV', 'N/A')
    PP5Main = power_data.get('PP5Main', 'N/A')

    cols = st.columns(5)
    with cols[2]:
        create_metric_card("Electricity", f"{PP5} Mw" , "PP5Gen")
    with cols[2]:
        create_metric_card("Steam", f"{PP5Main} kg/s" , "PP5Stream")