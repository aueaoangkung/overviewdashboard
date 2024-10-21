import streamlit as st
from Component import tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12
from server import fetch_data_from_apis

st.set_page_config(layout="wide")
st.title("Dashboard")

def update_dashboard():
    data = fetch_data_from_apis()

    if data:
        with tab1_ref:
            tab1.display(data)
        with tab2_ref:
            tab2.display(data)
        with tab3_ref:
            tab3.display(data)
        with tab4_ref:
            tab4.display(data)
        with tab5_ref:
            tab5.display(data)
        with tab6_ref:
            tab6.display(data)
        with tab7_ref:
            tab7.display(data)
        with tab8_ref:
            tab8.display(data)
        with tab9_ref:
            tab9.display(data)
        with tab10_ref:
            tab10.display(data)
        with tab11_ref:
            tab11.display(data)
        with tab12_ref:
            tab12.display(data)

tab1_ref, tab2_ref, tab3_ref, tab4_ref, tab5_ref, tab6_ref, tab7_ref, tab8_ref, tab9_ref, tab10_ref, tab11_ref, tab12_ref = st.tabs([
    "Overview", "Truck", "Solar", "NPP3", "NPP4", "NPP5", "NPP6", "NPP7", "NPP8", "NPP9", "NPP10", "NPP11"
])

update_dashboard()