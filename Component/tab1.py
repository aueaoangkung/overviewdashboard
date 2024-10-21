import streamlit as st

def display(data):
    wait = data.get('kpi_data', {}).get('wait', 'N/A')
    heavy = data.get('kpi_data', {}).get('heavy', 'N/A')
    light = data.get('kpi_data', {}).get('light', 'N/A')
    product_502_1 = float(data.get('total_weight_502_1', 0))
    product_502_2 = float(data.get('total_weight_502_2', 0))
    product_502 = product_502_1 + product_502_2 
    product_502 = round(product_502, 2)
    bea_value = data.get('bea_value', 'N/A')

    NPP3_Status = data.get('NPP3_Status', 'Normal')
    NPP4_Status = data.get('NPP4_Status', 'Normal')
    NPP5_Status = data.get('NPP5_Status', 'Normal')
    NPP6_Status = data.get('NPP6_Status', 'Normal')
    NPP7_Status = data.get('NPP7_Status', 'Normal')
    NPP8_Status = data.get('NPP8_Status', 'Normal')
    NPP9_Status = data.get('NPP9_Status', 'Normal')
    NPP10_Status = data.get('NPP10_Status', 'Normal')
    NPP11_Status = data.get('NPP11_Status', 'Normal')

    dcs_data = data.get('dcs_data', {})

    IP1_MWH = round(float(dcs_data.get('7MKA10FE1TD', 0) or 0) + (dcs_data.get('8MKA10FE1TD', 0) or 0), 2)
    coalflow_u7 = round(float(dcs_data.get('7HHH10DF001FQ', 'N/A')), 2)
    bf_u7 = round(float(dcs_data.get('7ENA15DF001FQ', 'N/A')), 2)

    status_colors = {
        "NoSignal": "#a0dbe8", 
        "Shutdown": "#fe522a", 
        "Breakdown": "#FFA556", 
        "Higher": "#90EE90",    
        "Lower": "#edf760",     
        "Normal": "#FFFFFF"  
    }

    pp3_color = status_colors.get(NPP3_Status, "#FFFFFF")
    pp4_color = status_colors.get(NPP4_Status, "#FFFFFF")
    pp5_color = status_colors.get(NPP5_Status, "#FFFFFF")
    pp6_color = status_colors.get(NPP6_Status, "#FFFFFF")
    pp7_color = status_colors.get(NPP7_Status, "#FFFFFF")
    pp8_color = status_colors.get(NPP8_Status, "#FFFFFF")
    pp9_color = status_colors.get(NPP9_Status, "#FFFFFF")
    pp10_color = status_colors.get(NPP10_Status, "#FFFFFF")
    pp11_color = status_colors.get(NPP11_Status, "#FFFFFF")

    solar_total_qty = data.get('solar_total_qty', 0)
    power_data = data.get('power_data', [])

    IP1 = [
        ('PP5', next((item.get('PP522KV', 'N/A') for item in power_data if 'PP522KV' in item), 'N/A')),
        ('PP6', next((item.get('PP622KV', 'N/A') for item in power_data if 'PP622KV' in item), 'N/A')),
        ('PP7', next((item.get('PP7ActL', 'N/A') for item in power_data if 'PP7ActL' in item), 'N/A')),
        ('PP8', next((item.get('PP8ActL', 'N/A') for item in power_data if 'PP8ActL' in item), 'N/A')),
        ('PP9', next((item.get('PP9KV', 'N/A') for item in power_data if 'PP9KV' in item), 'N/A')),
        ('PP10', next((item.get('PP5AGen', 'N/A') for item in power_data if 'PP5AGen' in item), 'N/A')),
        ('PP11', next((item.get('PP11Gen', 'N/A') for item in power_data if 'PP11Gen' in item), 'N/A')),
        ('Solar', solar_total_qty)
    ]

    IP2 = [
        ('PP3', next((item.get('PP322KV', 'N/A') for item in power_data if 'PP322KV' in item), 'N/A')),
        ('PP4', next((item.get('PP3B22KV', 'N/A') for item in power_data if 'PP3B22KV' in item), 'N/A')),
    ]

    power_data_list = data.get('power_data', [])
    power_data = power_data_list[0] if power_data_list else {}

    tmp_egat1 = power_data.get('TmpEgat1', 'N/A')
    date_time = power_data.get('DATECREATE' , 'N/A')
    tmp_egat2 = power_data.get('TmpEgat2', 'N/A')
    ip7 = power_data.get('IP7115KV', 'N/A')
    pulp2 = power_data.get('PULP2', 'N/A')
    topm1 = power_data.get('ToPM1', 'N/A')
    ip2_egat = round(power_data.get('PP3BEGAT', 0), 2)
    ip2main_egat = round(sum([power_data.get('PP3Main', 0), power_data.get('PP3BMain', 0)]), 2)
    ip1main = round(sum([power_data.get('PP7Main', 0), power_data.get('PP8Main', 0)]), 2)
    ip1gen = round(sum([power_data.get('PP7ActL', 0), power_data.get('PP8ActL', 0)]), 2)

    col1, col2, col3 = st.columns([0.83, 1, 1])

    with col1:
        st.write(f"Last updated data : {date_time}")

    with col2:
        st.markdown(
            '''
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

            .custom-font {
                font-family: 'Roboto', sans-serif;
            }
            </style>
            <div class="custom-font" style="text-align: center;">
                <span style="background-color:#fe522a;color:black;padding:4px;border-radius:4px;">ShutDown</span>
                <span style="background-color:#FFA556;color:black;padding:4px;border-radius:4px;margin-left:10px;">BreakDown</span>
                <span style="background-color:#a0dbe8;color:black;padding:4px;border-radius:4px;margin-left:10px;">No Signal</span>
                <span style="background-color:#90EE90;color:black;padding:4px;border-radius:4px;margin-left:10px;">Higher</span>
                <span style="background-color:#edf760;color:black;padding:4px;border-radius:4px;margin-left:10px;">Lower</span>
                <span style="background-color:#d4d4d4;color:black;padding:4px;border-radius:4px;margin-left:10px;">Normal</span>
            </div>
            ''', 
            unsafe_allow_html=True
        )

    st.components.v1.html(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
            body {{
                transform: scale(1);
                transform-origin: 0 0;
                overflow-x: hidden;
            }}
            .container {{
                display: grid;
                grid-template-columns: 1fr 1fr 0.5fr 1fr 1fr 1fr 0.5fr 1fr 1fr;
                gap: 20px;
                width: 100%;
                font-family: 'Roboto', sans-serif;
                position: relative;
            }}
            .box {{
                background-color: #f0f2f6;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                text-align: center;
                font-size: 18px;
                position: relative;
                height: auto;
                line-height: 1.5;
            }}
            .box.large {{
                grid-column: span 2;
            }}
            .box.middle {{
                grid-column: span 1.5;
            }}
            .box.wide {{
                grid-column: 4 / span 3;
                grid-row: 2 / span 3;
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 5px;
            }}
            .box.wide-bottom {{
                grid-column: 4 / span 3;
                grid-row: 5 / span 1;
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 5px;
            }}
            .sub-box {{
                background-color: #ffffff;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 1px 2px rgba(0,0,0,0.1);
                text-align: center;
                margin: 3px;
                flex: 1;
                min-height: 60px;
            }}
            .first-sub-box {{
                margin-top: 30px;
            }}
            h4 {{
                margin: 0;
                font-weight: 700;
            }}
            .header-large {{
                font-size: 30px;
                text-align: center;
                font-weight: 900;
                margin-bottom: 10px;
            }}
            .line {{
                fill: none;
                stroke-width: 2;
                stroke-dasharray: 5, 5;
                animation: draw-line 5s linear infinite;
                stroke-linecap: round;
            }}
            .line-grey {{
                stroke: #888;
            }}
            .line-yellow {{
                stroke: #ff0;
            }}
            .line-blue {{
                stroke: #00f;
            }}
            @keyframes draw-line {{
                from {{
                    stroke-dashoffset: 100;
                }}
                to {{
                    stroke-dashoffset: 0;
                }}
            }}
                            
            .sub-box.ip1-sub-box h4,
            .sub-box.ip2-sub-box h4,
            .sub-box.car-sub-box h4 {{
                font-size: 20px;
            }}
                            
        </style>
        <div class="container">
            <div class="box" style="grid-column: 1; grid-row: 1;"><h4>BEA :<span style="color: blue;"> {bea_value}</span> Mw</h4></div>
            <div class="box" id="pea" style="grid-column: 2; grid-row: 1;"><h4>PEA : Mw</h4></div>
            <div class="box large" style="grid-column: 1 / span 2; grid-row: 2 / span 3; margin-right: 45px; margin-left: 45px;">
                <h4>Truck</h4>
                <div class="sub-box car-sub-box first-sub-box" style="margin-top: 40px; display: flex; align-items: center; justify-content: center;">
                    <h4>หางหนัก : {heavy} </h4>
                </div>
                <div class="sub-box car-sub-box first-sub-box" style = "display: flex; align-items: center; justify-content: center;"><h4>หางเบา : {light} </h4></div>
                <div class="sub-box car-sub-box first-sub-box" style = "display: flex; align-items: center; justify-content: center;"><h4>รอชั่ง : {wait} </h4></div>
            </div>
            <div class="box" id="coal-bf-pp7" style="grid-column: 1 / span 2; grid-row: 5;">
                <div style="display: flex;">
                    <div class="sub-box"><h4>Coal Flow<br><span style="color: blue;">{coalflow_u7}</span> Ton</h4></div>
                    <div class="sub-box" id="BF Flow"><h4>BF Flow<br><span style="color: blue;">{bf_u7}</span> Ton</h4></div>
                </div>
            </div>

            <div class="box wide" style="margin-left: -65px; margin-right: 65px;" id="ip1">
                <h4 class="header-large">IP 1</h4>
                {''.join([f'<div class="sub-box ip1-sub-box" style="display: flex; align-items: center; justify-content: center; background-color: {pp5_color if label == "PP5" else (pp6_color if label == "PP6" else (pp7_color if label == "PP7" else (pp8_color if label == "PP8" else (pp9_color if label == "PP9" else (pp10_color if label == "PP10" else (pp11_color if label == "PP11" else "#FFFFFF"))))))};"><h4>{label}<br><span style="color: blue;">{value}</span> Mw</h4></div>' for label, value in IP1])}
            </div>
            <div class="box wide-bottom" style="margin-left: -65px; margin-right: 65px;" id="ip2">
                <h4 class="header-large">IP 2</h4>
                {''.join([f'<div class="sub-box ip2-sub-box" style="display: flex; align-items: center; justify-content: center; background-color: {pp3_color if label == "PP3" else (pp4_color if label == "PP4" else "#FFFFFF")};"><h4>{label}<br><span style="color: blue;">{value}</span> Mw</h4></div>' for label, value in IP2])}
            </div>

            <!-- Box AA -->
            <div class="box" style="grid-column: 8 / span 2; grid-row: 2; margin-left: 25px; " id="egat">
                <h4>AA</h4>
                <div style="display: flex;">
                    <div class="sub-box" id="egat1pulp2"><h4>PULP2<br><span style="color: blue;">{pulp2}</span> Mw</h4></div>
                    <div class="sub-box" id="pm1"><h4>PM1<br><span style="color: blue;">{topm1}</span> Mw</h4></div>
                </div>
            </div>

            <!-- Box IP304 -->
            <div class="box" style="grid-column: 9; grid-row: 3;" id="ip304"><h4>IP304<br><span style="color: blue;">{ip7}</span> Mw</h4></div>

            <!-- Box E-GAT -->
            <div class="box" style="grid-column: 8 / span 2; grid-row: 4; margin-left: 25px;" id="aa">
                <h4>E-GAT</h4>
                <div style="display: flex;">
                    <div class="sub-box" id="egat1" style="background-color: white">
                        <h4>E-GAT1<br><span style="color: blue;">{tmp_egat1}</span> Mw</h4>
                    </div>
                    <div class="sub-box" id="egat2" style="background-color: white">
                        <h4>E-GAT2<br><span style="color: blue;">{tmp_egat2}</span> Mw</h4>
                    </div>
                </div>
            </div>

            <!-- Box ไม่มีชื่อ -->
            <div class="box" style="grid-column: 8 / span 2; grid-row: 5 ; margin-left: 25px;" id="noname">
                <div style="display: flex;">
                    <div class="sub-box" id="lz"><h4>LZ<br><span style="color: blue;"> </span> Mw</h4></div>
                    <div class="sub-box" id="aap2"><h4>AAP2<br><span style="color: blue;"> </span> Mw</h4></div>
                </div>
            </div>

        <svg style="position:absolute; width:100%; height:100%; pointer-events:none;">
            <path id="line1" class="line line-grey"></path>
            <path id="line2" class="line line-grey"></path>
            <path id="line3" class="line line-grey"></path>
            <path id="line4" class="line line-grey"></path>
            <path id="line5" class="line line-grey"></path>
            <path id="line6" class="line line-grey"></path>
            <path id="line7" class="line line-grey"></path>
            <path id="line8" class="line line-grey"></path>
            <path id="line9" class="line line-grey"></path> <!-- Line from IP1 to E-GAT -->
            <path id="line10" class="line line-grey"></path> <!-- Line from IP1 to AA -->
            <path id="line11" class="line line-grey"></path> <!-- Line from IP2 to No Name -->
            <path id="line12" class="line line-grey"></path> <!-- Line from IP2 to E-GAT -->

            <!-- Add text to lines -->
            <text>
                <textPath href="#line4" startOffset="13%" text-anchor="start" fill="#000" font-size="18px">
                    <tspan dy="-3.5em">Generate</tspan>
                    <tspan x="-7" dy="1.2em"> {ip1gen} Mw</tspan>
                    <tspan x="-17" dy="1.2em"> {IP1_MWH} Mwh</tspan>
                </textPath>
            </text>
            <text>
                <textPath href="#line8" startOffset="10%" text-anchor="start" fill="#000" font-size="18px">
                    <tspan dy="1.5em">Steam</tspan>
                    <tspan x="-17" dy="1.2em"> {ip1main} kg/s</tspan>
                </textPath>
            </text>
            <text>
                <textPath href="#line11" startOffset="10%" text-anchor="start" fill="#000" font-size="18px">
                    <tspan dy="1.4em">Steam {ip2main_egat} kg/s</tspan>
                </textPath>
            </text>
            <text>
                <textPath href="#line12" startOffset="10%" text-anchor="start" fill="#000" font-size="18px">
                    <tspan dy="-2em">Generate</tspan>
                    <tspan x="5" dy="1.2em">{ip2_egat} Mw</tspan>
                </textPath>
            </text>
        </svg>

        </div>
        <script>
            function updateLinePosition() {{
                const peaBox = document.getElementById('pea');
                const coalBfPp7Box = document.getElementById('coal-bf-pp7');
                const ip1Box = document.getElementById('ip1');
                const ip2Box = document.getElementById('ip2');
                const egatBox = document.getElementById('egat');
                const ip304Box = document.getElementById('ip304');
                const aaBox = document.getElementById('aa');
                const nonameBox = document.getElementById('noname');
                const pulp2Box = document.getElementById('egat1pulp2');
                const path1 = document.getElementById('line1');
                const path2 = document.getElementById('line2');
                const path3 = document.getElementById('line3');
                const path4 = document.getElementById('line4');
                const path5 = document.getElementById('line5');
                const path6 = document.getElementById('line6');
                const path7 = document.getElementById('line7');
                const path8 = document.getElementById('line8');
                const path9 = document.getElementById('line9');
                const path10 = document.getElementById('line10');
                const path11 = document.getElementById('line11');
                const path12 = document.getElementById('line12');
                
                const peaBoxRect = peaBox.getBoundingClientRect();
                const coalBfPp7BoxRect = coalBfPp7Box.getBoundingClientRect();
                const ip1BoxRect = ip1Box.getBoundingClientRect();
                const ip2BoxRect = ip2Box.getBoundingClientRect();
                const egatBoxRect = egatBox.getBoundingClientRect();
                const ip304BoxRect = ip304Box.getBoundingClientRect();
                const aaBoxRect = aaBox.getBoundingClientRect();
                const nonameBoxRect = nonameBox.getBoundingClientRect();
                const pulp2BoxRect = pulp2Box.getBoundingClientRect();

                function createRightAnglePath(startX, startY, endX, endY) {{
                    const midX = startX + (endX - startX) / 2 +75;
                    return 'M' + startX + ',' + startY + ' H' + midX + ' V' + endY + ' H' + endX;
                }}

                function createRightAnglePathLine1(startX, startY, endX, endY) {{
                const midX = startX + ((endX+35) - startX) / 2 -20; 
                return 'M' + startX + ',' + startY + ' H' + midX + ' V' + endY + ' H' + endX;
                }}

                // Line 1: PEA to IP 1 with reduced length
                const d1 = createRightAnglePathLine1(peaBoxRect.right - 5, peaBoxRect.top + peaBoxRect.height / 2 - 4, ip1BoxRect.left - 10, ip1BoxRect.top + ip1BoxRect.height / 2 - 10, -50);
                path1.setAttribute('d', d1);

                // Line 2: Coal PP7/BF PP7 to IP 1 with reduced length
                const d2 = createRightAnglePathLine1(coalBfPp7BoxRect.right - 5, coalBfPp7BoxRect.top + coalBfPp7BoxRect.height / 2 + 20, ip1BoxRect.left - 10, ip1BoxRect.top + ip1BoxRect.height / 2 + 10, -50);
                path2.setAttribute('d', d2);

                // Line 4: IP 1 to IP304
                const d4 = createRightAnglePath(ip1BoxRect.right, ip1BoxRect.top + ip1BoxRect.height / 2 , ip304BoxRect.left -12, ip304BoxRect.top + ip304BoxRect.height / 2 );
                path4.setAttribute('d', d4);

                const extendedRight = ip1BoxRect.right + 160; // Extend the right position
                const d8 = 'M' + ip1BoxRect.right + ',' + (ip1BoxRect.bottom - ip1BoxRect.height / 2 + 13) + 
                            ' H' + extendedRight + 
                            ' V' + (nonameBoxRect.top + nonameBoxRect.height / 2 -15) + 
                            ' H' + (nonameBoxRect.left-10);
                path8.setAttribute('d', d8);

                // Line 9: IP1 to E-GAT
                const d9 = createRightAnglePath(ip1BoxRect.right, ip1BoxRect.top + ip1BoxRect.height / 2, egatBoxRect.left -10, egatBoxRect.top + egatBoxRect.height / 2);
                path9.setAttribute('d', d9);

                // Line 10: IP1 to AA
                const d10 = createRightAnglePath(ip1BoxRect.right, ip1BoxRect.bottom - ip1BoxRect.height / 2, aaBoxRect.left -10, aaBoxRect.top + aaBoxRect.height / 2);
                path10.setAttribute('d', d10);

                // Line 11: IP2 to No Name (straight line)
                const d11 = 'M' + ip2BoxRect.right + ',' + (ip2BoxRect.top + ip2BoxRect.height / 2 + 20) + 
                            ' H' + (nonameBoxRect.left -10) + 
                            ' V' + (nonameBoxRect.top + nonameBoxRect.height / 2 + 20);
                path11.setAttribute('d', d11);

                // Line 12: IP2 to E-GAT (straight line)
                const d12 = createRightAnglePath(ip2BoxRect.right, ip2BoxRect.top + ip2BoxRect.height / 2, egatBoxRect.left -10, egatBoxRect.top + egatBoxRect.height / 2 + 320)
                path12.setAttribute('d', d12);
            }}

            document.addEventListener("DOMContentLoaded", function() {{
                updateLinePosition();
                window.addEventListener('resize', updateLinePosition);
                window.addEventListener('scroll', updateLinePosition);
            }});
        </script>
    """, height=800)