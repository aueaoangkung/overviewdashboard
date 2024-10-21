import streamlit_shadcn_ui as ui
import streamlit as st
from streamlit_echarts import st_echarts

def create_metric_card(title, content, key, description="No Description"):
    ui.metric_card(title=title, content=content, description=description, key=key)

streamlit_style = """
    <style>
    iframe[title="streamlit_echarts.st_echarts"]{ height: 150px;} 
</style>
"""

def display(data):
    codes = [
        "NPS Solar PWH1",
        "NPS Solar PWH2",
        "NPS Solar PWH3.1",
        "NPS Solar PWH4",
        "AC5.13 Solar",
        "AC5.15 Solar"
    ]

    st.markdown(streamlit_style, unsafe_allow_html=True)

    solar_data = data.get('solar_data', [])
    meter_data = {
        "NPS Solar PWH1": data.get('meter_data1', ([], [])),
        "NPS Solar PWH2": data.get('meter_data2', ([], [])),
        "NPS Solar PWH3.1": data.get('meter_data3', ([], [])),
        "NPS Solar PWH4": data.get('meter_data4', ([], [])),
        "AC5.13 Solar": data.get('meter_data5', ([], [])),
        "AC5.15 Solar": data.get('meter_data6', ([], []))
    }

    daily_yield = data.get('solar_daily_yield', [])
    solar_total_qty = data.get('solar_total_qty', 'N/A')
    daily_yield_value = daily_yield[0][6] if daily_yield else 'N/A'

    cols = st.columns(6)
    with cols[2]:
        create_metric_card("Total RealTime", f"{solar_total_qty} Mw", "Solar Total", description="Install cap 144.50 Mwp")
    with cols[3]:
        create_metric_card("Yield", f"{daily_yield_value} Mwh", "Solar Yield")

    installation_caps = [
        "Install cap 14.93 Mwp",
        "Install cap 15.07 Mwp",
        "Install cap 14.60 Mwp",
        "Install cap 15.40 Mwp",
        "Install cap 29.95 Mwp",
        "Install cap 54.56 Mwp"
    ]

    for index in range(0, len(solar_data), 2):
        cols = st.columns([0.3, 1, 0.3, 1])
        for i in range(2):
            if index + i >= len(solar_data):
                break
            row = solar_data[index + i]
            # ใช้อินเด็กซ์ในการเข้าถึงข้อมูลแทนการใช้คีย์
            name = row[0]  # 'code' ที่อยู่ในตำแหน่งที่ 0
            value = row[2]  # 'qty' ที่อยู่ในตำแหน่งที่ 2
            try:
                value = float(value)
            except (ValueError, TypeError) as e:
                st.error(f"Error converting value for {name}: {e}")
                value = 0.0
            description = installation_caps[(index + i) % len(installation_caps)]
            with cols[i * 2]:
                ui.metric_card(title=name, content=f"{value:.2f} Mw", description=description, key=f"Solar {index + i + 1}")
                code = codes[(index + i) % len(codes)]
                meter_qty_value, meter_time = meter_data.get(code, ([], []))
                if not meter_qty_value or not meter_time:
                    st.warning(f"No data available for solar chart {code}.")
                else:
                    options_solar = {
                        "xAxis": {
                            "type": "category",
                            "boundaryGap": False,
                            "data": meter_time,
                        },
                        "yAxis": {"type": "value"},
                        "series": [
                            {
                                "data": meter_qty_value,
                                "type": "line",
                                "areaStyle": {},
                            }
                        ],
                        "grid": {
                            "top": '20px',
                            "bottom": '30px',
                            "left": '10px',
                            "right": '15px',
                            "containLabel": True
                        }
                    }
                    default_height = 400
                    reduced_height = int(default_height * 0.44)
                    with cols[i * 2 + 1]:
                        st_echarts(options=options_solar, height=f'{reduced_height}px', key=f"echarts_{code}_solar")