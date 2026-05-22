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
st.subheader("Pongo ficheros")

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

# Prefijo de las hojas (ej. 'r0', 'r1', ...)
PREFIJO_HOJAS = "r"
# Número de hojas de ranking (de r0 a r38 son 39 hojas) #toda la liga hay que poner 39
NUM_HOJAS = 38 #38 si es solo hasta jornada 37


# --- Función para cargar los datos (con caché para optimizar el rendimiento) ---
@st.cache_data
def cargar_rankings(archivo_excel: str, prefijo: str, num_hojas: int) -> dict:
    """
    Carga todas las hojas del archivo Excel como DataFrames y verifica la columna.

    Args:
        archivo_excel (str): Ruta al archivo Excel.
        prefijo (str): Prefijo de los nombres de las hojas (ej. 'r').
        num_hojas (int): Número total de hojas a cargar (ej. 39 para r0-r38).

    Returns:
        dict: Un diccionario donde las claves son los nombres de las hojas y los valores
              son los DataFrames cargados, o None si hay un error.
    """
    todos_los_rankings = {}
    
    try:
        # Usamos pd.ExcelFile para leer todas las hojas de manera eficiente
        xls = pd.ExcelFile(archivo_excel)
        nombres_hojas_disponibles = xls.sheet_names

        for i in range(num_hojas):
            nombre_hoja = f"{prefijo}{i}"
            if nombre_hoja not in nombres_hojas_disponibles:
                st.error(f"Error: La hoja '{nombre_hoja}' no se encontró en el archivo Excel.")
                return None

            # Cargar la hoja específica
            df_temp = pd.read_excel(xls, sheet_name=nombre_hoja, header=None)
            
            # Asumimos que la columna de equipos es la primera y no tiene nombre
            # Por lo tanto, pandas la nombra '0' si header=None
            columna_sin_nombre = 0

            # Si la columna 0 no existe, mostramos un error
            if columna_sin_nombre not in df_temp.columns:
                st.error(f"Error: La columna sin nombre (posición 0) no se encontró en la hoja '{nombre_hoja}'.")
                return None
            
            # Extraer solo la columna de equipos y asegurarse de que sean 20 filas
            equipos_serie = df_temp[columna_sin_nombre].dropna().astype(str).reset_index(drop=True)

            if len(equipos_serie) != 20:
                 st.warning(f"Advertencia: La hoja '{nombre_hoja}' no contiene exactamente 20 equipos. Contiene {len(equipos_serie)}.")
            
            todos_los_rankings[nombre_hoja] = equipos_serie

    except FileNotFoundError:
        st.error(f"Error: El archivo '{archivo_excel}' no se encontró. Asegúrate de que está en la misma carpeta que tu script de Streamlit.")
        return None
    except Exception as e:
        st.error(f"Ocurrió un error inesperado al cargar los rankings: {e}")
        return None

    return todos_los_rankings
# --- Cargar los datos al inicio de la aplicación ---
rankings_cargados = cargar_rankings(NOMBRE_ARCHIVO_EXCEL, PREFIJO_HOJAS, NUM_HOJAS)

print('Hola')
Print('rankings meus carregats')

# Cargamos las variables que usaremos como opcion seleccionable
opciones = rankings_cargados['r0']   #para coger el nombre de los equipos como en r0
opciones_ordenada = opciones.sort_values() #los pongo en orden alfabetico


       


number = st.sidebar.number_input("Selecciona una jornada",min_value=1, max_value=38, value="min", step=1,)
#st.write("The current number is ", number)

with st.sidebar:
    parVariable=st.selectbox('Equipo a estudiar',options=opciones_ordenada)  #con esa parvariable puedo hacer algo en el futuro




# Using object notation
# add_selectbox = st.sidebar.selectbox(
#     "How would you like to be contacted?",
#     ("Email", "Home phone", "Mobile phone")
# )
#print(add_selectbox)

#cargo partidos
def cargar_partidos(archivo_excel: str, prefijo: str, num_hojas: int) -> dict:
    """
    Carga todas las hojas del archivo Excel como DataFrames y verifica la columna.

    Args:
        archivo_excel (str): Ruta al archivo Excel.
        prefijo (str): Prefijo de los nombres de las hojas (ej. 'r').
        num_hojas (int): Número total de hojas a cargar (ej. 39 para r0-r38).

    Returns:
        dict: Un diccionario donde las claves son los nombres de las hojas y los valores
              son los DataFrames cargados, o None si hay un error.
    """
    todos_los_partidos = {}
    
    try:
        # Usamos pd.ExcelFile para leer todas las hojas de manera eficiente
        xls = pd.ExcelFile(archivo_excel)
        nombres_hojas_disponibles = xls.sheet_names

        for i in range(1,num_hojas+1):
            nombre_hoja = f"{prefijo}{i}"
            if nombre_hoja not in nombres_hojas_disponibles:
                st.error(f"Error: La hoja '{nombre_hoja}' no se encontró en el archivo Excel.")
                return None

            # Cargar la hoja específica
            df_temp = pd.read_excel(xls, sheet_name=nombre_hoja, header=None)
            
            # # Asumimos que la columna de equipos es la primera y no tiene nombre
            # # Por lo tanto, pandas la nombra '0' si header=None
            # columna_sin_nombre = 0

            # # Si la columna 0 no existe, mostramos un error
            # if columna_sin_nombre not in df_temp.columns:
            #     st.error(f"Error: La columna sin nombre (posición 0) no se encontró en la hoja '{nombre_hoja}'.")
            #     return None
            
            # # Extraer solo la columna de equipos y asegurarse de que sean 20 filas
            # equipos_serie = df_temp[columna_sin_nombre].dropna().astype(str).reset_index(drop=True)

            # if len(equipos_serie) != 20:
            #      st.warning(f"Advertencia: La hoja '{nombre_hoja}' no contiene exactamente 20 equipos. Contiene {len(equipos_serie)}.")
            
            #df_partidos=df_temp
            todos_los_partidos[nombre_hoja] =df_temp
            # todos_los_partidos[nombre_hoja] = equipos_serie

    except FileNotFoundError:
        st.error(f"Error: El archivo '{archivo_excel}' no se encontró. Asegúrate de que está en la misma carpeta que tu script de Streamlit.")
        return None
    except Exception as e:
        st.error(f"Ocurrió un error inesperado al cargar los rankings: {e}")
        return None

    return todos_los_partidos


resultados_encuentros = cargar_partidos(NOMBRE_ARCHIVO_PARTIDOS, 'Jornada', 37)  ################# 38 temporada completa


#resultados_encuentros['Jornada1']  #resultados de la jornada 1: debo borrar columnas y renombrar



#cargo clasificacion general pedroche
rankings_gen_pedroche_carg = cargar_partidos(Nombre_archivo_General_Pedroche, 'J', 37) ################# 38 temporada completa



