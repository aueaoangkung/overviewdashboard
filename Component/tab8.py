import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd

def create_metric_card(title, content, key, description="No Description"):
    ui.metric_card(title=title, content=content, description=description, key=key)

def display(data):
    product_502_2 = data.get('product_502_2', {}).get('transformedData', [])
    product_502_df = pd.DataFrame(product_502_2)
    power_data_list = data.get('power_data', [])
    power_data = power_data_list[0] if power_data_list else {}
    date_time = power_data.get('DATECREATE' , 'N/A')
    dcs_data = data.get('dcs_data', {})

    st.write(f"Last updated data : {date_time}")

    PP7 = power_data.get('PP7ActL', 'N/A')
    PP7_mwh = round(float(dcs_data.get('7MKA10FE1TD', 'N/A')), 1)
    PP7Main = power_data.get('PP7Main', 'N/A')
    PP7Fur = power_data.get('PP7Furnace', 'N/A')

    cols = st.columns(8)
    with cols[2]:
        create_metric_card("Electricity", f"{PP7} Mw" , "PP7Gen")
    with cols[3]:
        create_metric_card("Generated", f"{PP7_mwh} Mwh" , "U7 Gen Output" , "PP7GenMwh")
    with cols[4]:
        create_metric_card("Steam", f"{PP7Main} kg/s" , "PP7Stream")
    with cols[5]:
        create_metric_card("Furance", f"{PP7Fur} m/s" , "PP7Fur")

    col1, col2, col3 = st.columns([0.3, 1, 0.3])
    with col2:
        product_502_df.index += 1
        st.dataframe(product_502_df, use_container_width=True)