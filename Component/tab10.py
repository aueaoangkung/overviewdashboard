import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd

def create_metric_card(title, content, key, description="No Description"):
    ui.metric_card(title=title, content=content, description=description, key=key)

def display(data):
    product_503 = data.get('product_503', []).get('transformedData', [])
    product_503_df = pd.DataFrame(product_503)
    power_data_list = data.get('power_data', [])
    power_data = power_data_list[0] if power_data_list else {}
    date_time = power_data.get('DATECREATE' , 'N/A')
    dcs_data = data.get('dcs_data', {})

    st.write(f"Last updated data : {date_time}")
    
    PP9 = power_data.get('PP9KV', 'N/A')
    PP9Main = power_data.get('PP9Main', 'N/A')
    PP9_fuel = dcs_data.get('NPP9_FUEL', 'N/A')

    cols = st.columns(7)
    with cols[2]:
        create_metric_card("Electricity", f"{PP9} Mw" , "PP9Gen")
    with cols[3]:
        create_metric_card("Steam", f"{PP9Main} kg/s" , "PP9Stream")
    with cols[4]:
        create_metric_card("FUEL", f"{PP9_fuel} t/h" , "PP9fuel")

    col1, col2, col3 = st.columns([0.3, 1, 0.3])
    with col2:
        product_503_df.index += 1
        st.dataframe(product_503_df, use_container_width=True)