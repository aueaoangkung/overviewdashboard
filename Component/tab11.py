import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd

def create_metric_card(title, content, key, description="No Description"):
    ui.metric_card(title=title, content=content, description=description, key=key)

def display(data):
    product_501 = data.get('product_501', []).get('transformedData', [])
    product_501_df = pd.DataFrame(product_501)
    power_data_list = data.get('power_data', [])
    power_data = power_data_list[0] if power_data_list else {}
    date_time = power_data.get('DATECREATE' , 'N/A')

    st.write(f"Last updated data : {date_time}")
    
    PP10 = power_data.get('PP5AGen', 'N/A')
    PP10Main = power_data.get('PP5AMain', 'N/A')

    cols = st.columns(6)
    with cols[2]:
        create_metric_card("Electricity", f"{PP10} Mw" , "PP10Gen")
    with cols[3]:
        create_metric_card("Steam", f"{PP10Main} kg/s" , "PP10Stream")

    col1, col2, col3 = st.columns([0.3, 1, 0.3])
    with col2:
        product_501_df.index += 1
        st.dataframe(product_501_df, use_container_width=True)