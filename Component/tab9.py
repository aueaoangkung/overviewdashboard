import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd

def create_metric_card(title, content, key, description="No Description"):
    ui.metric_card(title=title, content=content, description=description, key=key)

def display(data):

    product_502_1 = data.get('product_502_1', {}).get('transformedData', [])
    product_502_df = pd.DataFrame(product_502_1)
    power_data_list = data.get('power_data', [])
    power_data = power_data_list[0] if power_data_list else {}
    date_time = power_data.get('DATECREATE' , 'N/A')
    dcs_data = data.get('dcs_data', {})
    
    st.write(f"Last updated data : {date_time}")

    PP8 = power_data.get('PP8ActL', 'N/A')
    PP8_mwh = round(float(dcs_data.get('8MKA10FE1TD', 'N/A')), 1)
    PP8Main = power_data.get('PP8Main', 'N/A')
    PP8Fur = power_data.get('PP8Furnace', 'N/A')

    cols = st.columns(8)
    with cols[2]:
        create_metric_card("Electricity", f"{PP8} Mw" , "PP8Gen")
    with cols[3]:
        create_metric_card("Generated", f"{PP8_mwh} Mwh" , "U8 Gen Output" , "PP8GenMwh")
    with cols[4]:
        create_metric_card("Steam", f"{PP8Main} kg/s" , "PP8Stream")
    with cols[5]:
        create_metric_card("Furance", f"{PP8Fur} m/s" , "PP8Fur")

    col1, col2, col3 = st.columns([0.3, 1, 0.3])
    with col2:
        product_502_df.index += 1
        st.dataframe(product_502_df, use_container_width=True)