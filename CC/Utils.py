import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURATION STADE DE REIMS ---
SDR_RED = "#D71920"
SDR_GREY = "#F0F2F6"

def local_css():
    st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{ background-color: {SDR_RED}; }}
    [data-testid="stSidebar"] *, [data-testid="stSidebar"] span {{ color: white !important; }}
    h1, h2, h3 {{ color: {SDR_RED} !important; }}
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data(file_path):
    try:
        # Lecture flexible (virgules ou point-virgules)
        df = pd.read_csv(file_path, sep=None, engine='python')
        
        # Nettoyage basique
        if 'sessionDate' in df.columns:
            df['sessionDate'] = pd.to_datetime(df['sessionDate'], errors='coerce')
        
        # Forcer les colonnes numériques
        cols_to_numeric = ['allMaxSpeed', 'distanceTotal', 'maxSpeed', 'totalTime', 'distanceZ5Abs']
        for col in cols_to_numeric:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
        # Création d'une colonne ID unique pour l'affichage
        if 'DisplayName' in df.columns and 'team' in df.columns:
            df['FullLabel'] = df['DisplayName'] + " (" + df['team'] + ")"
            
        return df
    except Exception as e:
        st.error(f"Erreur de chargement : {e}")
        return pd.DataFrame()