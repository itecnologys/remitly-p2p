# SERVER_FLUXUS_AUDIT.py

import pandas as pd
from flask import Flask, render_template, jsonify, request
import os
import numpy as np

app = Flask(__name__)

# Configurações
CSV_PATH = os.path.join("..", "06_DATA", "DATA_STRESS_TEST_AUDIT_LOG_POWERBI.csv")

def load_data():
    if not os.path.exists(CSV_PATH):
        return None
    df = pd.read_csv(CSV_PATH)
    
    # --- Sintetização de Timestamps Virtuais ---
    # Para cada grupo de (Month, Day, LP_ID), vamos distribuir as transações no tempo
    # Isso permite o filtro de "Hora" solicitado pelo usuário.
    df['Base_Date'] = pd.to_datetime('2026-' + df['Month'].astype(str) + '-' + df['Day'].astype(str))
    
    # Criar um offset de segundos baseado no Cycle_Num para não sobrepor
    # Distribuindo entre 09:00 e 21:00 (12 horas = 43200 segundos)
    df['Seconds_Offset'] = (df['Cycle_Num'] * 3600) % 43200 
    df['Timestamp'] = df['Base_Date'] + pd.to_timedelta(9, unit='h') + pd.to_timedelta(df['Seconds_Offset'], unit='s')
    
    # Cálculo de Valor de Retorno (Capital + Lucro 1.5%)
    df['Return_Value'] = df['Transaction_Value'] + df['LP_Profit_1.5pct']
    
    # Sintetização de Lifecycle Hash para Auditoria
    # Combinação de LP, Mês, Dia e Ciclo para rastro único
    df['Lifecycle_Hash'] = 'FLX-' + df['Month'].astype(str).str.zfill(2) + df['Day'].astype(str).str.zfill(2) + \
                          '-' + df['Cycle_Num'].astype(str).str.zfill(3) + '-' + df['LP_ID'].str[-3:]
    
    return df

@app.route('/')
def index():
    df = load_data()
    if df is None:
        return "Arquivo de auditoria não encontrado."
    
    total_gtv = df['Transaction_Value'].sum()
    total_yield = df['LP_Profit_1.5pct'].sum()
    total_opex = df['Dock_Reload_Cost'].sum() + df['Blockchain_Gas'].sum()
    total_pool = df['Pool_Reserve_2.0pct_GTV'].sum()
    
    stats = {
        'total_gtv': f"R$ {total_gtv:,.2f}",
        'total_yield': f"R$ {total_yield:,.2f}",
        'total_opex': f"R$ {total_opex:,.2f}",
        'total_pool': f"R$ {total_pool:,.2f}",
        'yield_pct': f"{(total_yield / total_gtv * 100):.2f}%" if total_gtv > 0 else "0%"
    }
    
    lp_stats = df.groupby('LP_ID').agg({
        'LP_Profit_1.5pct': 'sum',
        'Principal_Capital': 'last'
    }).sort_values(by='LP_Profit_1.5pct', ascending=False).head(10).rename(columns={
        'LP_Profit_1.5pct': 'LP_Profit',
        'Principal_Capital': 'Principal'
    }).reset_index()
    
    return render_template('index.html', stats=stats, top_lps=lp_stats.to_dict(orient='records'))

@app.route('/my-wallet')
def my_wallet():
    df = load_data()
    # Métricas consolidadas para a carteira global/investidor
    total_principal = df.groupby('LP_ID')['Principal_Capital'].last().sum()
    total_profit = df['LP_Profit_1.5pct'].sum()
    total_reserves = df['Pool_Reserve_2.0pct_GTV'].sum()
    total_opex = df['Dock_Reload_Cost'].sum() + df['Blockchain_Gas'].sum()
    
    wallet_stats = {
        'principal': f"R$ {total_principal:,.2f}",
        'profit': f"R$ {total_profit:,.2f}",
        'reserves': f"R$ {total_reserves:,.2f}",
        'opex': f"R$ {total_opex:,.2f}"
    }
    
    return render_template('my-wallet.html', stats=wallet_stats)

@app.route('/transactions')
def transactions():
    return render_template('transaction.html')

@app.route('/api/transactions')
def api_transactions():
    df = load_data()
    
    # Filtros
    lp_id = request.args.get('lp_id')
    month = request.args.get('month')
    min_val = request.args.get('min_val', type=float)
    
    if lp_id:
        df = df[df['LP_ID'] == lp_id]
    if month:
        df = df[df['Month'] == int(month)]
    if min_val:
        df = df[df['Transaction_Value'] >= min_val]
        
    # Ordenar por mais recentes e pegar as últimas 100 para performance
    df = df.sort_values(by='Timestamp', ascending=False).head(100)
    
    # Formatação para JSON
    df['Timestamp_Str'] = df['Timestamp'].dt.strftime('%d/%m/%Y %H:%M')
    
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/chart/gtv')
def api_chart_gtv():
    df = load_data()
    monthly = df.groupby('Month')['Transaction_Value'].sum().reset_index()
    return jsonify({
        'months': monthly['Month'].tolist(),
        'values': monthly['Transaction_Value'].tolist()
    })

@app.route('/api/chart/profit_trend')
def api_chart_profit():
    df = load_data()
    daily = df.groupby(['Month', 'Day'])['LP_Profit_1.5pct'].sum().tail(10).reset_index()
    return jsonify({
        'values': daily['LP_Profit_1.5pct'].tolist()
    })

@app.route('/api/lps')
def api_lps():
    df = load_data()
    lps = sorted(df['LP_ID'].unique().tolist())
    return jsonify(lps)

@app.route('/api/wallet-analytics')
def api_wallet_analytics():
    lp_id = request.args.get('lp_id', 'LP_001')
    full_audit = request.args.get('full_audit', 'false') == 'true'
    df = load_data()
    
    lp_df = df[df['LP_ID'] == lp_id]
    if lp_df.empty:
        return jsonify({"error": "LP not found"}), 404

    # Agregações de GTV, Ciclos e Lucros
    max_ts = lp_df['Timestamp'].max()
    
    # GTV
    gtv_day = lp_df[lp_df['Timestamp'] >= (max_ts - pd.Timedelta(days=1))]['Transaction_Value'].sum()
    gtv_week = lp_df[lp_df['Timestamp'] >= (max_ts - pd.Timedelta(days=7))]['Transaction_Value'].sum()
    gtv_month = lp_df['Transaction_Value'].sum()
    
    # Profits (Net Return)
    profit_day = lp_df[lp_df['Timestamp'] >= (max_ts - pd.Timedelta(days=1))]['LP_Profit_1.5pct'].sum()
    profit_week = lp_df[lp_df['Timestamp'] >= (max_ts - pd.Timedelta(days=7))]['LP_Profit_1.5pct'].sum()
    profit_month = lp_df['LP_Profit_1.5pct'].sum()
    
    # Cycles
    cycles_day = len(lp_df[lp_df['Timestamp'] >= (max_ts - pd.Timedelta(days=1))])
    cycles_week = len(lp_df[lp_df['Timestamp'] >= (max_ts - pd.Timedelta(days=7))])
    cycles_month = len(lp_df)
    
    # Lógica de Segmentos (Simulação baseada no ID do LP)
    try:
        lp_seed = int(lp_id.split('_')[1])
    except:
        lp_seed = 1
        
    segments = [
        {"name": "Maritime Insurance", "active": (lp_seed % 2 == 0)},
        {"name": "Freight Settlement", "active": (lp_seed % 3 == 0)},
        {"name": "International Gateways", "active": (lp_seed % 5 == 0)},
        {"name": "Intercompany Transfers", "active": (lp_seed % 7 == 0)},
        {"name": "Agri-Business Export", "active": (lp_seed % 11 == 0)},
        {"name": "Supply Chain Finance", "active": True}
    ]
    
    if full_audit:
        # Pega todas as transações do mês selecionado ou todas do LP
        recent = lp_df.sort_values(by='Timestamp', ascending=False).copy()
    else:
        recent = lp_df.sort_values(by='Timestamp', ascending=False).head(10).copy()
        
    recent['Timestamp_Str'] = recent['Timestamp'].dt.strftime('%d/%m/%Y %H:%M:%S')
    
    return jsonify({
        "lp_id": lp_id,
        "gtv": {
            "day": f"R$ {gtv_day:,.2f}",
            "week": f"R$ {gtv_week:,.2f}",
            "month": f"R$ {gtv_month:,.2f}"
        },
        "profit": {
            "day": f"R$ {profit_day:,.2f}",
            "week": f"R$ {profit_week:,.2f}",
            "month": f"R$ {profit_month:,.2f}"
        },
        "cycles": {
            "day": cycles_day,
            "week": cycles_week,
            "month": cycles_month
        },
        "segments": segments,
        "recent_activities": recent.to_dict(orient='records')
    })

if __name__ == '__main__':
    app.run(debug=True, port=3500)
