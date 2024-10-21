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
    
    PP6 = power_data.get('PP622KV', 'N/A')
    PP6Main = power_data.get('PP6Main', 'N/A')
    PP6Fir = power_data.get('PP6FiringRate', 'N/A')

    cols = st.columns(5)
    with cols[2]:
        create_metric_card("Electricity", f"{PP6} Mw" , "PP6Gen")
    with cols[2]:
        create_metric_card("Steam", f"{PP6Main} kg/s" , "PP6Stream")
    with cols[2]:
        create_metric_card("FiringRate", f"{PP6Fir} tds/d" , "PP6Fir")