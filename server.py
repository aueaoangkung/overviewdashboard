import requests
import pyodbc
import datetime
import os
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

load_dotenv()

dbConfig12 = {
    'server': os.getenv('DB_SERVER12'),
    'database': os.getenv('DB_DATABASE12'),
    'username': os.getenv('DB_USER12'),
    'password': os.getenv('DB_PASSWORD12'),
    'driver': '{ODBC Driver 17 for SQL Server}'
}

dbConfig42 = {
    'server': os.getenv('DB_SERVER42'),
    'database': os.getenv('DB_DATABASE42'),
    'username': os.getenv('DB_USER42'),
    'password': os.getenv('DB_PASSWORD42'),
    'driver': '{ODBC Driver 17 for SQL Server}'
}

def determine_status(data, power_key, opc_quality_key, dif_key, plan_shutdown_key):
    if not isinstance(data, dict):
        return "NoSignal"
    if not data or data.get(power_key) is None or data.get(opc_quality_key) != 192:
        return "NoSignal"
    if data[power_key] <= 0:
        return "Shutdown" if data.get(plan_shutdown_key) else "Breakdown"
    if data[dif_key] > 0:
        return "Higher"
    if data[dif_key] < 0:
        return "Lower"
    return "Normal"

def fetch_data(url):
    try:
        response = requests.get(url)
        return response.json() if response.status_code == 200 else {}
    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
        return {}

def fetch_dcs_data():
    data = fetch_data(os.getenv('API_URL_DCS'))
    target_ids = {'NPP9_FUEL', '7HHH10DF001FQ', '7ENA15DF001FQ', '7MKA10FE1TD', '8MKA10FE1TD'}
    filtered_values = {
        item['dcS_TAG']: item['value'] for item in data if item['dcS_TAG'] in target_ids
    }
    return filtered_values

def fetch_power_data():
    return fetch_data(os.getenv('API_URL_POWER'))

def fetch_kpi_data():
    data = fetch_data(os.getenv('API_URL_KPI')).get('data', [])
    wait, heavy, light = None, None, None
    kpi_frame = []

    for kpi in data:
        kpi_id = kpi.get('kpiId', '').upper()
        if kpi_id == '1':
            wait = kpi.get('kpiValue', 0)
        elif kpi_id == '2':
            heavy = kpi.get('kpiValue', 0)
        elif kpi_id == '3':
            light = kpi.get('kpiValue', 0)

        for item in kpi.get('kpiData', []):
            kpi_frame.append({
                'Tail': kpi.get('kpiName', 'N/A'),
                'Tail_Id': item.get('tail_id') or item.get('TAIL_ID', 'N/A'),
                'Pro_name': item.get('pro_name') or item.get('PRO_NAME', 'N/A'),
                'Dest_name': item.get('dest_name') or item.get('DEST_NAME', 'N/A'),
                'DataTime': item.get('activity_start') or item.get('ACTIVITY_START', 'N/A')
            })
    return {'wait': wait, 'heavy': heavy, 'light': light, 'kpi_frame': kpi_frame}

def fetch_data_from_db(query, db_config):
    try:
        with pyodbc.connect(
            f"DRIVER={db_config['driver']};"
            f"SERVER={db_config['server']};"
            f"DATABASE={db_config['database']};"
            f"UID={db_config['username']};"
            f"PWD={db_config['password']}"
        ) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as e:
        print(f"Error executing query: {e}")
        return []

def fetch_solar_data():
    queries = [
        "EXEC usp_SOLAR_METER_RTMW",
        "EXEC usp_SOLAR_METER_DTDMW",
        "EXEC usp_SOLAR_METER_DYIELDTMWh"
    ]
    results = [fetch_data_from_db(query, dbConfig12) for query in queries]
    solar_total_qty_value = results[1][0][1] if results[1] else 'N/A'
    return [results[0], solar_total_qty_value, results[2]]

def fetch_bea_value():
    query = """
        SELECT TOP (1) [Value]
        FROM [NPS_SOLAR].[dbo].[Kpi_BEA]
        WHERE Designation = 'TURBINE POWER'
        ORDER BY CreateDate DESC
    """
    result = fetch_data_from_db(query, dbConfig42)
    return round(float(result[0][0]), 2) if result else 0

def fetch_meter_data(code):
    query = f"""
        SELECT [Code], [Date_M], [QtyValue], [Subj]
        FROM [dbo].[v_Wh]
        WHERE (Subj = 'Exp Wh' OR Subj = 'Import W Demand Total')
        AND CONVERT(date, [Date_M]) = CONVERT(date, GETDATE())
        AND [Code] = '{code}'
    """
    result = fetch_data_from_db(query, dbConfig12)
    meter_qty_value, meter_time = [], []

    for row in result:
        date_m = row[1]
        time = date_m.strftime("%H:%M:%S") if isinstance(date_m, datetime.datetime) else datetime.datetime.strptime(date_m, "%Y-%m-%d %H:%M:%S").strftime("%H:%M:%S")
        if "05:00:00" <= time <= "19:00:00":
            value = (row[2] * 60 / 15 / 1000000) if code in ['NPS Solar PWH1', 'NPS Solar PWH2'] else row[2] / 1000000
            meter_qty_value.append(value)
            meter_time.append(time)

    return meter_qty_value, meter_time

def fetch_power_data2():
    data = fetch_data(os.getenv('API_URL_POWER2'))
    return data[0] if isinstance(data, list) and data else {}

def fetch_data_product(branch_id, dest_name):
    url = f"{os.getenv('API_URL_PRODUCT')}?DateStart={datetime.datetime.now().strftime('%Y-%m-%d')}&BranchId={branch_id}"
    data = fetch_data(url).get('data', [])
    filtered_data = [item for item in data if item.get('dest_name') == dest_name]
    total_weight = sum(item.get('receive_weightnet', 0) for item in filtered_data)

    transformed_data = [
        {
            'Id': item.get('id', 'N/A'),
            'Truck_Id': item.get('truck_id', 'N/A'),
            'Product': item.get('pro_name', 'N/A'),
            'DateTime': item.get('wms_dateout', 'N/A'),
            'Weight': item.get('receive_weightnet', 0)
        } for item in filtered_data
    ]

    return {'totalWeight': total_weight, 'transformedData': transformed_data}

def fetch_data_from_apis():
    with ThreadPoolExecutor() as executor:
        futures = {
            'power_data': executor.submit(fetch_power_data),
            'kpi_data': executor.submit(fetch_kpi_data),
            'bea_value': executor.submit(fetch_bea_value),
            'solar_data': executor.submit(fetch_solar_data),
            'meter_data1': executor.submit(fetch_meter_data, 'NPS Solar PWH1'),
            'meter_data2': executor.submit(fetch_meter_data, 'NPS Solar PWH2'),
            'meter_data3': executor.submit(fetch_meter_data, 'NPS Solar PWH3.1'),
            'meter_data4': executor.submit(fetch_meter_data, 'NPS Solar PWH4'),
            'meter_data5': executor.submit(fetch_meter_data, 'AC5.13 Solar'),
            'meter_data6': executor.submit(fetch_meter_data, 'AC5.15 Solar'),
            'product_501': executor.submit(fetch_data_product, 501, "โรงไฟฟ้าNPP10(5A)"),
            'product_502_1': executor.submit(fetch_data_product, 502, "โรงไฟฟ้าNPS(ท่าตูม)"),
            'product_502_2': executor.submit(fetch_data_product, 502, "โรงไฟฟ้าPP7(NPS)"),
            'product_503': executor.submit(fetch_data_product, 503, "โรงไฟฟ้าPP9(NPS)"),
            'dcs_data': executor.submit(fetch_dcs_data)
        }
        results = {key: future.result() for key, future in futures.items()}

    power2_data = fetch_power_data2()

    status_keys = [
        ('NPP3_Status', 'PP3'), ('NPP4_Status', 'PP3B'), ('NPP5_Status', 'PP5'), 
        ('NPP6_Status', 'PP6'), ('NPP7_Status', 'PP7'), ('NPP8_Status', 'PP8'), 
        ('NPP9_Status', 'PP9'), ('NPP10_Status', 'PP5A'), ('NPP11_Status', 'PP11')
    ]

    for key, prefix in status_keys:
        results[key] = determine_status(power2_data, f'{prefix}', f'{prefix}OPCQuality', f'{prefix}Dif', f'{prefix}PlanShutdown')

    return {
        **results,
        'solar_data': results['solar_data'][0],
        'solar_total_qty': results['solar_data'][1],
        'solar_daily_yield': results['solar_data'][2],
        'total_weight_501': round(results['product_501']['totalWeight'], 2),
        'total_weight_502_1': round(results['product_502_1']['totalWeight'], 2),
        'total_weight_502_2': round(results['product_502_2']['totalWeight'], 2),
        'total_weight_503': round(results['product_503']['totalWeight'], 2),
        'dcs_values': results['dcs_data']
    }

if __name__ == "__main__":
    data = fetch_data_from_apis()
    print(data)