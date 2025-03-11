#RPE test


#Code essai 

import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

def save_profiles():
    with open("profiles.json", "w") as file:
        json.dump(st.session_state.profiles, file)

def load_profiles():
    if os.path.exists("profiles.json"):
        try:
            with open("profiles.json", "r") as file:
                st.session_state.profiles = json.load(file)
        except json.JSONDecodeError:
            st.error("Erreur de chargement des profils. Le fichier JSON est peut-être corrompu.")
            st.session_state.profiles = {}
    else:
        st.session_state.profiles = {}


if 'profiles' not in st.session_state:
    load_profiles()

if 'selected_profile' not in st.session_state:
    st.session_state.selected_profile = None

if 'selected_test_type' not in st.session_state:
    st.session_state.selected_test_type = "Borg 6-20"

if 'accumulated_data' not in st.session_state:
    st.session_state.accumulated_data = []

if 'language' not in st.session_state:
    st.session_state.language = "Français"

borg_image_url = "https://i.etsystatic.com/46581789/r/il/8eaaa2/6539867170/il_1080xN.6539867170_7mhu.jpg"
cr10_image_url = "https://fatsecretfrance.fr/wp-content/uploads/2023/01/Medium_echelle_de_borg.jpg"
Explication_url = "https://www.tripassion.fr/wp-content/uploads/2017/12/rpe.jpg"

translations = {
    "Test": {
        "Français": "Test",
        "English": "Test"
    },
    "Sélectionnez un profil": {
        "Français": "Sélectionnez un profil",
        "English": "Select a Profile"
    },
    "Profils disponibles": {
        "Français": "Profils disponibles",
        "English": "Available Profiles"
    },
    "Veuillez créer un profil avant de Test.": {
        "Français": "Veuillez créer un profil avant de Test.",
        "English": "Please create a profile before taking the test."
    },
    "Sélectionnez le type de test": {
        "Français": "Sélectionnez le type de test",
        "English": "Select the Test Type"
    },
    "Type de test RPE": {
        "Français": "Type de test RPE",
        "English": "RPE Test Type"
    },
    "Sélectionnez le type de séance": {
        "Français": "Sélectionnez le type de séance",
        "English": "Select the Session Type"
    },
    "Type de séance": {
        "Français": "Type de séance",
        "English": "Session Type"
    },
    "Questionnaire": {
        "Français": "Questionnaire",
        "English": "Questionnaire"
    },
    "À quel point cette séance/match a-t-il été physiquement exigeant ?": {
        "Français": "À quel point cette séance/match a-t-il été physiquement exigeant ?",
        "English": "How physically demanding was this session/match?"
    },
    "À quel point cette séance/match a-t-il été mentalement exigeant ?": {
        "Français": "À quel point cette séance/match a-t-il été mentalement exigeant ?",
        "English": "How mentally demanding was this session/match?"
    },
    "Comment évalues-tu globalement la difficulté de cette séance/match ?": {
        "Français": "Comment évalues-tu globalement la difficulté de cette séance/match ?",
        "English": "How do you rate the overall difficulty of this session/match?"
    },
    "Commentaires": {
        "Français": "Commentaires",
        "English": "Comments"
    },
    "Ajoutez des commentaires ou des notes supplémentaires": {
        "Français": "Ajoutez des commentaires ou des notes supplémentaires",
        "English": "Add any additional comments or notes"
    },
    "Soumettre": {
        "Français": "Soumettre",
        "English": "Submit"
    },
    "Réponses enregistrées avec succès!": {
        "Français": "Réponses enregistrées avec succès!",
        "English": "Responses successfully recorded!"
    },
    "Feedback": {
        "Français": "Feedback",
        "English": "Feedback"
    },
    "Votre score est élevé. Pensez à bien récupérer pour éviter la fatigue excessive.": {
        "Français": "Votre score est élevé. Pensez à bien récupérer pour éviter la fatigue excessive.",
        "English": "Your score is high. Make sure to recover well to avoid excessive fatigue."
    },
    "Votre score est modéré. Continuez ainsi!": {
        "Français": "Votre score est modéré. Continuez ainsi!",
        "English": "Your score is moderate. Keep it up!"
    },
    "Scores de la Session": {
        "Français": "Scores de la Session",
        "English": "Session Scores"
    },
    "Aucun profil ou donnée disponible.": {
        "Français": "Aucun profil ou donnée disponible.",
        "English": "No profile or data available."
    },
    "Langue": {
        "Français": "Langue",
        "English": "Language"
    },
    "Choisir la langue": {
        "Français": "Choisir la langue",
        "English": "Choose Language"
    }
}


st.markdown("""
    <style>
    body {
        background-color: #f0f0f5;
        color: #333;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    </style>
""", unsafe_allow_html=True)


def show_explanation():
    st.title("RPE")
    st.write("Le test RPE est une échelle utilisée pour mesurer la perception de l'effort.")
    st.write("Il existe deux versions principales : l'échelle de Borg (6-20) et l'échelle CR10 (0-10).")
    st.image(Explication_url, use_container_width=True, caption="Échelle RPE")
    st.write("""
      **Présentation du suivi du RPE et du CR10 en football**

    L’évaluation de l’effort perçu est un outil utilisé depuis plusieurs années dans le sport de haut niveau. En football, elle permet aux joueurs de quantifier l’intensité ressentie après une séance d’entraînement ou un match. Ce suivi aide les préparateurs physiques et entraîneurs à ajuster les charges de travail pour optimiser la performance et limiter les risques de fatigue ou de blessure.

    **Origine et principe du RPE et du CR10**

    "L’échelle de perception de l’effort (RPE) a été développée par le physiologiste suédois Gunnar Borg dans les années 1970. Initialement conçue pour refléter l’intensité de l’effort en lien avec la fréquence cardiaque, elle est utilisée dans de nombreux sports pour évaluer la charge d’entraînement.

    L’échelle RPE 6-20 est graduée de 6 à 20, ces valeurs ayant été choisies pour correspondre approximativement à la fréquence cardiaque multipliée par 10 chez un adulte en bonne santé. Ainsi, un effort ressenti à 13 (effort "assez dur") correspond en moyenne à une fréquence cardiaque de 130 battements par minute.

    L’échelle CR10, une version simplifiée, va de 0 à 10. Elle est plus intuitive et plus facile à utiliser au quotidien. Dans le football, elle est souvent privilégiée, car elle permet aux joueurs de donner une estimation rapide et claire de leur ressenti après un match ou une séance d’entraînement.

    **Comment utiliser le RPE ou le CR10 en football ?**

    À la fin d’une séance d’entraînement ou d’un match, chaque joueur est invité à donner une note sur l’échelle choisie en répondant à une question simple :

    "Comment as-tu ressenti l’intensité de cette séance ?"

    Le joueur doit donner une réponse en fonction de son ressenti global, sans se baser uniquement sur sa fatigue musculaire ou son essoufflement. L’idée est d’avoir une vision subjective de la difficulté de la séance, intégrant à la fois la charge physique, la charge mentale et les exigences du jeu.

    Cette évaluation est ensuite multipliée par la durée de l’effort en minutes pour obtenir une valeur de charge d’entraînement.

    **Exemple de calcul :**

    Un joueur attribue une note de 7 sur le CR10 après un match de 90 minutes.
    La charge d’entraînement est donc :

    7 × 90 = 630

    Ce chiffre permet de comparer les charges de travail entre les joueurs et sur différentes périodes.

    **Traitement et analyse des données**

    Les valeurs de charge d’entraînement recueillies sont enregistrées et permettent d’analyser l’évolution de la charge de travail au fil des semaines. Un suivi régulier permet d’identifier des tendances et d’adapter la préparation physique en conséquence.

    L’un des indicateurs clés utilisés est le ratio charge aiguë / charge chronique (ACWR). Il compare la charge de travail récente (dernière semaine) à la charge moyenne des quatre semaines précédentes.

    - Un ratio trop élevé (> 1,5) signifie que la charge récente est bien supérieure à la charge habituelle, augmentant le risque de blessure.
    - Un ratio trop faible (< 0,8) indique une charge insuffisante, ce qui peut limiter la progression du joueur.

    Les données peuvent être utilisées individuellement ou collectivement. L’analyse des charges entre les différents postes permet également d’adapter le travail spécifique des joueurs selon leur rôle sur le terrain.

    **Pourquoi ces échelles sont-elles scientifiquement valides ?**

    L’évaluation de l’effort perçu est un outil validé scientifiquement depuis plusieurs décennies. De nombreuses études ont montré une forte corrélation entre les scores de RPE ou de CR10 et des mesures physiologiques objectives comme la consommation d’oxygène (VO2), la concentration de lactate sanguin et la fréquence cardiaque.

    Dans le football, des travaux comme ceux de Foster (1998) ou Malone et al. (2017) ont démontré que le suivi du CR10 permet de mieux prévenir les blessures en contrôlant les fluctuations de la charge d’entraînement.

    Ces échelles sont aujourd’hui utilisées par la majorité des clubs professionnels, car elles offrent une méthode simple et efficace pour suivre la charge de travail sans nécessiter de matériel coûteux.

    **Utilisation pratique et avantages**

    L’évaluation de l’effort perçu permet d’ajuster les charges d’entraînement en fonction des besoins des joueurs. Elle est particulièrement utile pour :

    - Adapter la planification des séances en fonction de l’état de forme des joueurs.
    - Prévenir la fatigue excessive et le surentraînement en identifiant les périodes de surcharge.
    - Optimiser la récupération en ajustant le volume et l’intensité du travail.
    - Comparer les charges entre joueurs et ajuster les entraînements en fonction des postes.

    Cet outil simple permet un suivi efficace de la charge d’entraînement et s’intègre facilement dans la gestion quotidienne d’un effectif.
    """)


def manage_profiles():
    st.title("Profils")

    
    new_profile = st.text_input("Nom du nouveau profil")
    if st.button("Créer un profil"):
        if new_profile and new_profile not in st.session_state.profiles:
            st.session_state.profiles[new_profile] = []
            st.success(f"Profil '{new_profile}' créé avec succès!")
            save_profiles()  

    
    st.write("Profils existants")
    profile_options = list(st.session_state.profiles.keys())
    if profile_options:
        for profile in profile_options:
            st.write(f"- {profile}")
            if st.button(f"Supprimer {profile}", key=f"delete_{profile}"):
                del st.session_state.profiles[profile]
                st.success(f"Profil '{profile}' supprimé avec succès!")
                save_profiles()  
    else:
        st.write("Aucun profil créé pour le moment.")


def take_test():
    st.title(translations["Test"][st.session_state.language])

    
    st.write(translations["Sélectionnez un profil"][st.session_state.language])
    profile_options = list(st.session_state.profiles.keys())
    selected_profile = st.selectbox(translations["Profils disponibles"][st.session_state.language], profile_options)
    if selected_profile:
        st.session_state.selected_profile = selected_profile
        st.write(f"Profil sélectionné : {selected_profile}")
    else:
        st.warning(translations["Veuillez créer un profil avant de Test."][st.session_state.language])
        return

    
    st.write(translations["Sélectionnez le type de test"][st.session_state.language])
    test_type = st.radio(translations["Type de test RPE"][st.session_state.language], ["Borg 6-20", "CR10"])
    st.session_state.selected_test_type = test_type

    
    st.write(translations["Sélectionnez le type de séance"][st.session_state.language])
    session_type = st.selectbox(translations["Type de séance"][st.session_state.language], ["Match", "Entraînement", "Exercice spécifique"])

   
    if test_type == "Borg 6-20":
        rpe_scale = list(range(6, 21))
        max_score = 20
    else:
        rpe_scale = list(range(11))
        max_score = 10

    if st.session_state.selected_test_type == "Borg 6-20":
        st.image(borg_image_url, caption="Tableau RPE de Borg", use_container_width=True)
    else:
        st.image(cr10_image_url, caption="Tableau RPE CR10", use_container_width=True)

    
    st.write(translations["Questionnaire"][st.session_state.language])
    responses = {}

    
    st.write("#### Physique")
    responses["Physique"] = st.select_slider(
        translations["À quel point cette séance/match a-t-il été physiquement exigeant ?"][st.session_state.language],
        options=rpe_scale,
        key="physique"
    )

    st.write("#### Mental")
    responses["Mental"] = st.select_slider(
        translations["À quel point cette séance/match a-t-il été mentalement exigeant ?"][st.session_state.language],
        options=rpe_scale,
        key="mental"
    )

    st.write("#### Global")
    responses["Global"] = st.select_slider(
        translations["Comment évalues-tu globalement la difficulté de cette séance/match ?"][st.session_state.language],
        options=rpe_scale,
        key="global"
    )

    
    st.write(translations["Commentaires"][st.session_state.language])
    responses["Commentaires"] = st.text_area(translations["Ajoutez des commentaires ou des notes supplémentaires"][st.session_state.language])

    
    if st.button(translations["Soumettre"][st.session_state.language]):
        date = datetime.now().strftime("%Y-%m-%d")
        responses['date'] = date
        responses['profile'] = st.session_state.selected_profile
        responses['test_type'] = st.session_state.selected_test_type
        responses['session_type'] = session_type
        st.session_state.accumulated_data.append(responses)
        st.success(translations["Réponses enregistrées avec succès!"][st.session_state.language])

        
        st.write(translations["Feedback"][st.session_state.language])
        if responses["Physique"] == max_score or responses["Mental"] == max_score or responses["Global"] == max_score:
            st.warning(translations["Votre score est élevé. Pensez à bien récupérer pour éviter la fatigue excessive."][st.session_state.language])
        else:
            st.success(translations["Votre score est modéré. Continuez ainsi!"][st.session_state.language])


def view_scores():
    st.title("Scores de la Session")

    if not st.session_state.accumulated_data:
        st.write("Aucun profil ou donnée disponible.")
        return

    
    scores_df = pd.DataFrame(st.session_state.accumulated_data)
    scores_df = scores_df[["profile", "test_type", "session_type", "date", "Physique", "Mental", "Global", "Commentaires"]]
    st.write(scores_df)

    
    st.write("Exportation des Données")
    if st.button("Télécharger les données en CSV"):
        csv = scores_df.to_csv(index=False)
        st.download_button(
            label="Télécharger les données en CSV",
            data=csv,
            file_name='scores.csv',
            mime='text/csv',
        )


def show_help():
    st.title("Guide Utilisateur")
    st.write("""
    Bienvenue dans l'application de gestion des tests RPE. Voici comment utiliser l'application :

    1. **Créer un Profil :** Allez dans la section "Profils" pour créer un nouveau profil.
    2. **Test :** Sélectionnez un profil et passez le test RPE dans la section "Test".
    3. **Données et Export :** Consultez vos scores dans la section "Données et Export".
    4. **Exporter les Données :** Téléchargez vos données en CSV.
    """)


st.sidebar.title("Menu")
page = st.sidebar.radio("Aller à", ["Introduction au RPE", "Profils", "Test", "Données et Export", "Aide"])


st.sidebar.title("Langue")
language = st.sidebar.radio("Choisir la langue", ["Français", "English"])
st.session_state.language = language


if page == "Introduction au RPE":
    show_explanation()
elif page == "Profils":
    manage_profiles()
elif page == "Test":
    take_test()
elif page == "Données et Export":
    view_scores()
elif page == "Aide":
    show_help()










# streamlit run "C:\Users\Utilisateur\OneDrive - URCA\Bureau\RPE test\RPE test.py"