import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Analyse SDR - Profilage", page_icon="🔴", layout="wide")

SDR_RED = "#D71920"  # Rouge Reims
SDR_GREY = "#888888" # Gris pour la médiane/comparaison
SDR_DARK = "#0E1117" # Noir Profond

# --- 2. CSS CUSTOM (STYLE PRO) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {SDR_DARK}; color: white; }}
    [data-testid="stSidebar"] {{ background-color: {SDR_RED}; }}
    [data-testid="stSidebar"] *, [data-testid="stSidebar"] span {{ color: white !important; }}
    h1, h2, h3 {{ color: {SDR_RED} !important; }}
    p, li, span, label, div {{ color: white !important; }}
    div[data-testid="stMetric"] {{
        background-color: #262730;
        border-radius: 8px;
        padding: 10px;
        border: 1px solid #444;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. CHARGEMENT & PRÉPARATION ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Datagps.csv", sep=";")
        
        # Nettoyage numérique
        cols_num = ['distanceTotal', 'distanceZ5Abs', 'distanceZ6Abs', 'entriesZ6Abs', 'maxSpeed']
        for col in cols_num:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace(',', '.').apply(pd.to_numeric, errors='coerce')

        # --- CALCUL DU HSR (Z5 + Z6) ---
        df['distanceHSR'] = df['distanceZ5Abs'].fillna(0) + df['distanceZ6Abs'].fillna(0)

        # Filtres Matchs Officiels (CORRECTION DU WARNING REGEX ICI avec r'')
        df = df[df['sessionType'].str.contains('Match', case=False, na=False)]
        df = df[~df['sessionType'].str.contains(r'Day -|Day \+', regex=True, na=False)]
        
        return df
    except Exception as e:
        st.error(f"Erreur de chargement : {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# --- 4. SIDEBAR ---
st.sidebar.header("Profil Joueur")

groupe_pro = "Pro2"
df_jeunes = df[~df['team'].str.contains(groupe_pro, case=False, na=False)]
liste_jeunes = sorted(df_jeunes['DisplayName'].unique())

if not liste_jeunes:
    st.error("Aucun jeune trouvé (vérifiez le nom de l'équipe Pro dans le CSV).")
    st.stop()

joueur_cible = st.sidebar.selectbox("Sélectionner un joueur", liste_jeunes)
df_joueur = df[df['DisplayName'] == joueur_cible]
poste_joueur = df_joueur['position'].iloc[0] if not df_joueur.empty else "Inconnu"

st.sidebar.info(f"**{joueur_cible}**\n\nPoste : {poste_joueur}")
st.sidebar.markdown("---")

# --- 5. FONCTION GRAPHIQUE FLEXIBLE ---
def create_comparison_chart(df_data, metric_col, title, group_col='Groupe', unit="m"):
    """
    Crée un graphique à barres groupées (Moyenne vs Médiane).
    Accepte une colonne de groupe variable ('Groupe' ou 'position').
    """
    # Calcul des stats
    stats = df_data.groupby(group_col)[metric_col].agg(['mean', 'median']).reset_index()
    stats = stats.melt(id_vars=group_col, var_name='Statistique', value_name='Valeur')
    
    # Renommage pour l'affichage
    stats['Statistique'] = stats['Statistique'].replace({'mean': 'Moyenne', 'median': 'Médiane'})
    
    fig = px.bar(
        stats, 
        x=group_col, 
        y='Valeur', 
        color='Statistique',
        barmode='group',
        title=title,
        text_auto='.0f',
        color_discrete_map={'Moyenne': SDR_RED, 'Médiane': SDR_GREY},
        template="plotly_dark"
    )
    fig.update_layout(
        yaxis_title=unit,
        xaxis_title="",
        legend_title="",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig

# --- 6. CONTENU PRINCIPAL ---
st.title(f"Rapport Profilage : {joueur_cible}")

# Données de référence (Pro)
df_pro_all = df[df['team'].str.contains(groupe_pro, case=False)]
df_pro_ref = df_pro_all[df_pro_all['position'] == poste_joueur]

# --- PARTIE 0 : CONTEXTE PAR POSTE (LA DEMANDE "REMETTRE LA COMPARAISON") ---
st.header("1. Référence par Poste (Pro2)")
st.write("Vue d'ensemble des moyennes et médianes de courses à haute intensité (HSR) et Sprint (Z6) pour chaque poste.")

if not df_pro_all.empty:
    # On utilise 'position' comme colonne de groupe ici
    fig_context = create_comparison_chart(df_pro_all, 'distanceZ6Abs', "Distance Z6 par Poste (Moyenne vs Médiane)", group_col='position')
    st.plotly_chart(fig_context, use_container_width=True)
else:
    st.warning("Pas assez de données Pro pour le graphique par poste.")

st.markdown("---")

# --- PARTIE SUIVANTE : LE JOUEUR VS SON POSTE ---
st.header(f"2. Focus Joueur : {joueur_cible} vs Standard {poste_joueur}")

if df_pro_ref.empty:
    st.warning(f"Attention : Pas de données '{groupe_pro}' trouvées pour le poste {poste_joueur}.")
else:
    # Préparation des données pour comparaison directe
    df_compare = pd.concat([
        df_joueur[['distanceZ6Abs', 'distanceHSR']].assign(Groupe=f"Joueur ({joueur_cible})"),
        df_pro_ref[['distanceZ6Abs', 'distanceHSR']].assign(Groupe="Standard Pro")
    ])

    # --- PARTIE A : HAUTE INTENSITÉ (HSR : Z5 + Z6) ---
    st.subheader("Volume Haute Intensité (HSR > 20 km/h)")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Ici on utilise 'Groupe' (créé juste au-dessus)
        fig_hsr = create_comparison_chart(df_compare, 'distanceHSR', "Comparaison HSR", group_col='Groupe')
        st.plotly_chart(fig_hsr, use_container_width=True)
        
    with col2:
        st.caption("Analyse des écarts")
        hsr_j = df_joueur['distanceHSR'].mean()
        hsr_p = df_pro_ref['distanceHSR'].mean()
        delta_hsr = hsr_j - hsr_p
        
        st.metric("Moyenne Joueur", f"{hsr_j:.0f} m")
        st.metric("Standard Pro", f"{hsr_p:.0f} m", delta_color="normal" if delta_hsr >= 0 else "inverse", delta=f"{delta_hsr:.0f} m")

    # --- PARTIE B : SPRINT PUR (Z6 > 25.2 km/h) ---
    st.subheader("Sprint (Z6)")
    col3, col4 = st.columns([2, 1])
    
    with col3:
        fig_z6 = create_comparison_chart(df_compare, 'distanceZ6Abs', "Comparaison Sprint Z6", group_col='Groupe')
        st.plotly_chart(fig_z6, use_container_width=True)
        
    with col4:
        st.caption("Analyse des écarts")
        z6_j = df_joueur['distanceZ6Abs'].mean()
        z6_p = df_pro_ref['distanceZ6Abs'].mean()
        delta_z6 = z6_j - z6_p
        
        st.metric("Moyenne Joueur", f"{z6_j:.0f} m")
        st.metric("Standard Pro", f"{z6_p:.0f} m", delta_color="normal" if delta_z6 >= 0 else "inverse", delta=f"{delta_z6:.0f} m")
 # #   streamlit run app_oral.py