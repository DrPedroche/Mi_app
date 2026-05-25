import streamlit as st
import pandas as pd

import base64
import os


#
st.set_page_config(layout="centered", page_icon=':soccer:', page_title="Ranking F.Pedroche",initial_sidebar_state="expanded")
st.title("Clasificación alternativa a la liga de Fútbol de 1ª división masculina")
st.markdown("### F. Pedroche. IMM. <br> Universitat Politècnica de València", unsafe_allow_html=True)


with st.expander("Selecciona temporada y jornada en el menú de la izquierda. Haz click para saber más del método"):
        st.write("El método de clasificación se basa en primar los goles en los partidos, favoreciendo las goleadas. "
				 "Solo hay tres reglas muy simples que se aplican a los equipos que han vencido, empatado o perdido "
				 "en los encuentros. El método designa como 'campeón de la jornada' al equipo que ha vencido por mayor "
				 "diferencia de goles (DG). En caso de que haya dos equipos vencedores con la misma DG, se prioriza al "
				 "que más goles haya marcado. En caso de empate en DG y G, se prioriza al equipo con mejor clasificación "
				 "en la jornada anterior. A continuación, en la clasificación vienen los equipos que hayan empatado, "
				 "ordenados según el número de goles en el encuentro. Por último, vienen los  equipos que han perdido, "
				 "también ordenados según el número de goles del encuentro. En caso de empate en el orden, se mira "
				 "a la clasificación de la jornada anterior y se prioriza al equipo con mejor orden.")


st.sidebar.title('Selecciona Temporada')
temporada_elegida=st.sidebar.radio('',['2024-25','2025-26'])

st.subheader(f"Temporada {temporada_elegida}")
#st.subheader("Pongo ficheros")

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


with st.sidebar:
    parVariable=st.selectbox('Equipo a estudiar',options=opciones_ordenada)  #con esa parvariable puedo hacer algo en el futuro

st.subheader(f"{parVariable}") 
st.image(f"escudos/{parVariable}.png", caption="Escudo")



# Prefijo de las hojas (ej. 'r0', 'r1', ...)
PREFIJO_HOJAS = "r"
# Número de hojas de ranking (de r0 a r38 son 39 hojas) #toda la liga hay que poner 39
NUM_HOJAS = 39 #39 jornada completa



@st.cache_data
def cargar_rankings(archivo_excel: str, prefijo: str, num_hojas: int) -> dict:

    todos_los_rankings = {}
    
    try:
        # 
        xls = pd.ExcelFile(archivo_excel)
        nombres_hojas_disponibles = xls.sheet_names

        for i in range(num_hojas):
            nombre_hoja = f"{prefijo}{i}"
            if nombre_hoja not in nombres_hojas_disponibles:
                st.error(f"Error: La hoja '{nombre_hoja}' no se encontró en el archivo Excel.")
                return None

            #
            df_temp = pd.read_excel(xls, sheet_name=nombre_hoja, header=None)            
            columna_sin_nombre = 0

            # 
            if columna_sin_nombre not in df_temp.columns:
                st.error(f"Error: La columna sin nombre (posición 0) no se encontró en la hoja '{nombre_hoja}'.")
                return None
            
            #
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
#
rankings_cargados = cargar_rankings(NOMBRE_ARCHIVO_EXCEL, PREFIJO_HOJAS, NUM_HOJAS)

# 
opciones = rankings_cargados['r0']   #para coger el nombre de los equipos como en r0
opciones_ordenada = opciones.sort_values() #los pongo en orden alfabetico

number = st.sidebar.number_input("Selecciona una jornada",min_value=1, max_value=38, value="min", step=1,)
#st.write("The current number is ", number)

with st.sidebar:
    st.markdown(
        """
        ### 📰 Noticias sobre el método en prensa

    - 🔵 [ABC](https://www.abc.es/espana/comunidad-valenciana/tanda-penaltis-elegir-campo-copiar-formula-sistema-20230810113333-nt.html)
    - 🔴 [Antena 3](https://www.antena3.com/noticias/deportes/futbol/revolucionario-metodo-matematico-puntuar-liga-estilo-formula-1_2024081266ba2e284d41750001187df6.html)
    - 🟢 [Àpunt](https://www.apuntmedia.es/esports/futbol/video-un-professor-upv-idea-un-innovador-sistema-puntuacio-liga_8_1724446.html)
    - 🟡 [RTVE-CV via X](https://x.com/i/status/1824128618739712359)
    - 🔵 [SER](https://cadenaser.com/comunitat-valenciana/2023/08/10/un-estudio-concluye-que-el-sistema-de-clasificacion-de-laliga-no-es-atractivo-y-perjudica-la-competitividad-entre-equipos-radio-valencia/)
    - 🔴 [UPV](https://www.upv.es/noticias-upv/noticia-14776-competitividad-es.html)

        ### 📘 Publicación científica

        - 📄 [Pedroche, F. (2025). *A New Proposal for Team Ranking in First Division of Spanish Football League*](https://doi.org/10.1007/978-3-032-00567-0_3)
        """,
        unsafe_allow_html=True
    )


#cargo partidos
def cargar_partidos(archivo_excel: str, prefijo: str, num_hojas: int) -> dict:

    todos_los_partidos = {}
    
    try:
        # 
        xls = pd.ExcelFile(archivo_excel)
        nombres_hojas_disponibles = xls.sheet_names

        for i in range(1,num_hojas+1):
            nombre_hoja = f"{prefijo}{i}"
            if nombre_hoja not in nombres_hojas_disponibles:
                st.error(f"Error: La hoja '{nombre_hoja}' no se encontró en el archivo Excel.")
                return None
            
            df_temp = pd.read_excel(xls, sheet_name=nombre_hoja, header=None)                
            todos_los_partidos[nombre_hoja] =df_temp
        

    except FileNotFoundError:
        st.error(f"Error: El archivo '{archivo_excel}' no se encontró. Asegúrate de que está en la misma carpeta que tu script de Streamlit.")
        return None
    except Exception as e:
        st.error(f"Ocurrió un error inesperado al cargar los rankings: {e}")
        return None

    return todos_los_partidos


resultados_encuentros = cargar_partidos(NOMBRE_ARCHIVO_PARTIDOS, 'Jornada', 38)  ################# 38 temporada completa


#resultados_encuentros['Jornada1']  #resultados de la jornada 1: debo borrar columnas y renombrar



#cargo clasificacion general pedroche
rankings_gen_pedroche_carg = cargar_partidos(Nombre_archivo_General_Pedroche, 'J', 38) ################# 38 temporada completa

#cargo partidos
def cargar_laliga(archivo_excel: str, prefijo: str, num_hojas: int) -> dict:

    todos_los_partidos = {}
    
    try:
        # 
        xls = pd.ExcelFile(archivo_excel)
        nombres_hojas_disponibles = xls.sheet_names

        for i in range(1,num_hojas+1):
            nombre_hoja = f"{prefijo}{i}"
            if nombre_hoja not in nombres_hojas_disponibles:
                st.error(f"Error: La hoja '{nombre_hoja}' no se encontró en el archivo Excel.")
                return None

            # 
            df_temp = pd.read_excel(xls, sheet_name=nombre_hoja, header=None)    
            todos_los_partidos[nombre_hoja] =df_temp
        

    except FileNotFoundError:
        st.error(f"Error: El archivo '{archivo_excel}' no se encontró. Asegúrate de que está en la misma carpeta que tu script de Streamlit.")
        return None
    except Exception as e:
        st.error(f"Ocurrió un error inesperado al cargar los rankings: {e}")
        return None

    return todos_los_partidos


#cargo clasificacion general LALIGA
rankings_gen_LALIGA = cargar_laliga(Nombre_archivo_GenLALIGA,'J', 38)  #N38 jornada completa



# Si los datos no se pudieron cargar, detener la ejecución del resto de la aplicación
if rankings_cargados is None:
    st.stop()

# --- Interfaz de usuario para selección de ranking ---
# Crear una lista de opciones para el selectbox
opciones_rankings = sorted(list(rankings_cargados.keys()))

ranking_seleccionado=number
dict_dataframes = {k: v.to_frame() for k, v in rankings_cargados.items()}

#dict_dataframes['r0']  #jornada 0

#print(ranking_seleccionado)
entrada = ranking_seleccionado  #ejemplo r15
#numero = entrada[1:]  # Extrae todo después del primer carácter ('15')
numero = entrada  # 
if numero=='0':         #si se elije 'r0'
    jornada_resultado = "Jornada1"   
    jornada_cgeneral="J1"
    jornada_cLALIGA="J1"
else:
    jornada_resultado = f"Jornada{numero}"    
    jornada_cgeneral= f"J{numero}"
    #jornada_cLALIGA=f"Jornada {numero}"
    jornada_cLALIGA = f"J{numero}"

#print(jornada_resultado)  # Salida: Jornada15
print(jornada_cgeneral)  # Salida: J1
print(jornada_cLALIGA) #Salida Jornada 1

df_resultados = resultados_encuentros[jornada_resultado] 

df_gen_pedroche = rankings_gen_pedroche_carg[jornada_cgeneral] 

df_gen_pedroche.columns=['Equipo','Ptos']


df_LALIGA=rankings_gen_LALIGA[jornada_cLALIGA]

#rankings_gen_LALIGA['J10'] #
#df_LALIGA.iloc[2:,:]


df_LALIGA_select=df_LALIGA.iloc[2:,:]
df_LALIGA_select.columns=['Posición','Logo','Equipo','PJ','Win','Draw','Lost','Goals','DG','Ptos']
df_LALIGA_select['Posición']=range(1,21)
df_LALIGA_select.info()
df_LALIGA_select = df_LALIGA_select.rename(columns={'Pts': 'Ptos'})
#print(df_resultados)

#st.subheader("Linea 356")

df_resultados.columns = ['ID', 'Local', 'Goles L', 'Visitante','Goles V']


# Clasificacion jornada metodo Pedroche
df_1 = dict_dataframes['r'+str(ranking_seleccionado)] 
df_1.columns = ['Equipo']


#hay que añadir escudo
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{data}"
    return None

df_1['Escudo'] = df_1['Equipo'].apply(lambda x: get_image_base64(f"escudos/{x}.png"))
df_1['Club']=range(1,21)  #sale de 1 a 20


df_gen_pedroche['Escudo']=df_gen_pedroche['Equipo'].apply(lambda x: get_image_base64(f"escudos/{x}.png"))
df_gen_pedroche['Club']=range(1,21)  #sale de 1 a 20

dict_cambios = {
    'FC Barcelona': 'Barcelona',
    'Atlético de Madrid': 'Atlético',
    'Athletic Club':'Athletic',
    'Villarreal CF':'Villarreal',    
    'Real Betis':'Betis',    
    'RC Celta':'Celta',
	 'Celta de Vigo':'Celta',
	 'Real Valladolid':'Real Valladolid',
    'Real Valladolid\xa0':'Real Valladolid',
    'Rayo Vallecano':'Rayo',
    'CA Osasuna':'Osasuna',
    'RCD Mallorca':'Mallorca',
    'Real Sociedad':'R. Sociedad',
    'Valencia CF':'Valencia',
    'Getafe CF':'Getafe',
    'RCD Espanyol':'Espanyol',
    'Espanyol\xa0':'Espanyol',
    'Deportivo Alavés':'Alavés',
    'Girona FC':'Girona',
    'Sevilla FC':'Sevilla',
    'CD Leganés':'Leganés',
    'CD Leganés\xa0':'Leganés',
    'UD Las Palmas': 'Las Palmas',
    'Elche CF':'Elche CF',
    'Elche CF\xa0':'Elche CF',
    'Real Oviedo\xa0':'R. Oviedo',
    'Levante\xa0':'Levante'
}

df_LALIGA_select['Equipo'] = df_LALIGA_select['Equipo'].replace(dict_cambios)
df_LALIGA_select['Escudo']=df_LALIGA_select['Equipo'].apply(lambda x: get_image_base64(f"escudos/{x}.png"))

#Reordeno
df_1=df_1[['Club','Escudo','Equipo']]
df_1 = df_1.assign(Ptos=[25, 18, 15, 12, 10, 8, 6, 4, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
df_gen_pedroche=df_gen_pedroche[['Club','Escudo','Equipo','Ptos']]
df_LALIGA_select=df_LALIGA_select[['Posición','Escudo','Equipo','PJ','Ptos']]

# Creamos dos columnas de igual tamaño
#col1, col2 = st.columns(2)
col1, col2 = st.columns([0.55, 0.45])

# Columna de la izquierda
with col1:
    with st.container(border=True):
        #st.write(f"Jornada {number}")
        st.subheader(f"Encuentros jornada {number}")
        #st.markdown("### Encuentros")
        #st.dataframe(df_1)  # st.table es estática, st.dataframe tiene scroll
        st.dataframe(
            # df_resultados,
            df_resultados.iloc[1:11, 1:5],
            hide_index=True,
            )

# Columna de la derecha
with col2:
    with st.container(border=True):
        st.markdown("### Clasificación jornada según el método")
        st.dataframe(
            df_1,
            column_config={
                "Escudo": st.column_config.ImageColumn("Escudo"),
                "Club": ' '
            },
            hide_index=True
        )



#[25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
# left, right = st.columns(2, border=True)

# left.markdown("El campeón de la jornada se lleva 25 puntos, los siguientes: 18, 15, 12, 10, 8, 6, 4, 2 y el décimo 1 punto. El resto de equipos no gana nada. ")
# #middle.markdown("Lorem ipsum " * 5)
# right.markdown("Acumulando los puntos podemos construir una clasificación general y compararla con la clasificación oficial")

md = st.text_area('',"El campeón de la jornada se lleva 25 puntos, los siguientes: 18, 15, 12, 10, 8, 6, 4, 2 y el décimo 1 punto. "
                  "El resto de equipos no anotan puntos."
                  " Acumulando los puntos en cada jornada se puede construir una clasificación general" 
                  "  que puede compararse con la clasificación oficial")

# print(df_1)

# Creamos dos columnas de igual tamaño
#col1, col2 = st.columns(2)
col1, col2 = st.columns([0.45, 0.55])

# Columna de la izquierda
with col1:
    with st.container(border=True):
        st.markdown("## Clasificación según el método")
       
        #st.dataframe(df_1)  # st.table es estática, st.dataframe tiene scroll
        st.dataframe(
            df_gen_pedroche,
            column_config={
                "Escudo": st.column_config.ImageColumn("Escudo"),
                "Club": " " 
            },
            hide_index=True
        )
        

# Columna de la derecha
with col2:
    with st.container(border=True):
        #st.markdown("## Clasificación  <br> oficial")
        st.markdown("## Clasificación <br> oficial", unsafe_allow_html=True)
        st.dataframe(
            df_LALIGA_select,
            column_config={
                "Escudo": st.column_config.ImageColumn("Escudo"),
                "Posición": " "  # Cambia el nombre de la columna por un espacio
            },
            hide_index=True
        )
        
        
#**********************
