import streamlit as st
import pandas as pd

import base64
import os


# --- Configuración de la aplicación Streamlit ---
st.set_page_config(layout="centered", page_icon=':soccer:', page_title="Ranking F.Pedroche",initial_sidebar_state="expanded")
# st.set_page_config(layout="wide", page_title="Ranking de Equipos",initial_sidebar_state="expanded",
#                    menu_items={
#         'Get Help': 'https://www.extremelycoolapp.com/help',
#         'Report a bug': "https://www.extremelycoolapp.com/bug",
#         'About': "# This is a header. This is an *extremely* cool app!"
#                               }
#                    )




st.title("Clasificación alternativa a la liga de Fútbol de 1ª división masculina")
#st.subheader("Método de F. Pedroche. IMM.  Universitat Politècnica de València")
st.markdown("### Método de F. Pedroche. IMM. <br> Universitat Politècnica de València", unsafe_allow_html=True)
#st.write("Selecciona una jornada.")

with st.expander("Selecciona temporada y jornada en el menú de la izquierda. Haz click para saber más del método"):
        st.write("El método se basa en promocionar los goles en los partidos"
                 "Por eso se favorecen las goleadas. Las reglas son muy simples"
                 " El método permite asignar un 'campeón de la copa de la jornada' "
                 "al equipo que ha vencido con mayor diferencia de goles. ")

st.sidebar.title('Selecciona Temporada')
temporada_elegida=st.sidebar.radio('',['2024-25','2025-26'])

st.subheader(f"Temporada {temporada_elegida}")

if temporada_elegida=='2024-25':
#     st.subheader("Has elegido la Temporada pasada")    
# Nombre del archivo Excel
    NOMBRE_ARCHIVO_EXCEL = "ranking-old-24-25.xlsx"
    NOMBRE_ARCHIVO_PARTIDOS = "LFP-24-25.xlsx"
    Nombre_archivo_General_Pedroche="CGeneral24-25.xlsx"
    Nombre_archivo_GenLALIGA="Laliga24-25-transfmkt.xlsx"

else:
#     st.subheader("Has elegido la Temporada actual")      
    NOMBRE_ARCHIVO_EXCEL = "ranking-old-25-26.xlsx"
    NOMBRE_ARCHIVO_PARTIDOS = "LFP-25-26.xlsx"
    Nombre_archivo_General_Pedroche="CGeneral25-26.xlsx"
    Nombre_archivo_GenLALIGA="Laliga25-26-transfmkt.xlsx"
