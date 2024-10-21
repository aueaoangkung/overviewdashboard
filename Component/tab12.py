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
    
    PP11 = power_data.get('PP11Gen', 'N/A')
    PP11Main = power_data.get('PP11Main', 'N/A')
    PP11Fir = power_data.get('PP11FiringRate', 'N/A')

    cols = st.columns(5)
    with cols[2]:
        create_metric_card("Electricity", f"{PP11} Mw" , "PP11Gen")
    with cols[2]:
        create_metric_card("Steam", f"{PP11Main} kg/s" , "PP11Stream")
    with cols[2]:
        create_metric_card("FiringRate", f"{PP11Fir} tds/d" , "PP11Fir")