import html

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# =========================================================
# CONFIGURAÇÃO
# =========================================================
st.set_page_config(
    page_title="VULC Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# IDENTIDADE VISUAL
# =========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #0B100D;
        --surface: #121A15;
        --surface-2: #18231C;
        --border: #26362C;
        --green: #65E6A3;
        --text: #F0F5F1;
        --muted: #87998D;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: var(--bg);
        color: var(--text);
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1600px;
    }

    [data-testid="stSidebar"] {
        background: #101812;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] * {
        color: var(--text);
    }

    h1, h2, h3 {
        color: var(--text) !important;
        letter-spacing: -1px;
    }

    p, label {
        color: var(--muted);
    }

    /* Cards KPI personalizados: sem corte e sem reticências */
    .kpi-card {
        box-sizing: border-box;
        width: 100%;
        min-width: 0;
        min-height: 142px;
        padding: 21px 20px 18px 20px;
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 15px;
        transition: border-color .2s ease, transform .2s ease;
        overflow: visible;
    }

    .kpi-card:hover {
        border-color: var(--green);
        transform: translateY(-2px);
    }

    .kpi-label {
        color: var(--muted);
        font-size: 13px;
        font-weight: 500;
        line-height: 1.4;
        margin-bottom: 13px;
    }

    .kpi-value {
        display: block;
        width: 100%;
        color: var(--text);
        font-weight: 800;
        line-height: 1.18;
        letter-spacing: -1.1px;
        white-space: nowrap;
        overflow: visible;
        text-overflow: clip;
        font-variant-numeric: tabular-nums;
    }

    .kpi-note {
        margin-top: 10px;
        color: #718477;
        font-size: 11px;
        line-height: 1.3;
    }

    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: var(--surface);
        border-color: var(--border);
        border-radius: 10px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
    }

    .stButton button, .stDownloadButton button {
        background: var(--green);
        color: #0B100D;
        border: none;
        border-radius: 9px;
        font-weight: 700;
        transition: .2s;
    }

    .stButton button:hover, .stDownloadButton button:hover {
        background: #8AF0B9;
        color: #0B100D;
        border: none;
    }

    hr {
        border-color: var(--border);
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

