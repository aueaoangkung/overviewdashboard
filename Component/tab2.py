import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd

def create_metric_card(title, content, key, description="No Description"):
    ui.metric_card(title=title, content=content, description=description, key=key)

def display(data):
    wait = data.get('kpi_data', {}).get('wait', 'N/A')
    heavy = data.get('kpi_data', {}).get('heavy', 'N/A')
    light = data.get('kpi_data', {}).get('light', 'N/A')

    kpi_frame = data.get('kpi_data', []).get('kpi_frame', [])
    truck_table = pd.DataFrame(kpi_frame)
    
    col1, col2, col3, col4, col5 = st.columns([2, 0.7, 0.7, 0.7, 2])
    with col2:
        create_metric_card("หางหนัก", heavy, "Heavy")
    with col3:
        create_metric_card("หางเบา", light, "light")
    with col4:
        create_metric_card("รอชั่ง", wait, "Wait")
    col1, col2, col3 = st.columns([0.3, 1, 0.3])
    with col2:
        truck_table.index += 1
        st.dataframe(truck_table, use_container_width=True)