import streamlit as st
from classUpload import get_processor
from classFiltros import Filtros

st.set_page_config(layout="wide")
st.title("Subir Base de Datos")

# 1. Selector de tipo de archivo
tipos_de_archivo = [
    "Selecciona un tipo...",
    "Fulcrum Angles.csv",
    "Fulcrum Angles.json",
    "Fulcrum Angles.xml"
]
tipo_seleccionado = st.selectbox("Paso 1: Selecciona el tipo de archivo que vas a subir", tipos_de_archivo)

# 2. Widget de carga de archivo (dependiente de la selección)
if tipo_seleccionado != "Selecciona un tipo...":
    
    # Extraer la extensión para el file_uploader
    # Esto es para la conveniencia del usuario, la lógica real usa el string completo.
    extension = tipo_seleccionado.split('.')[-1]

    archivo_subido = st.file_uploader(
        f"Paso 2: Sube tu archivo (solo se aceptan .{extension})",
        type=[extension]
    )

    if archivo_subido is not None:
        st.success(f"Archivo '{archivo_subido.name}' cargado.")
        contenido_bytes = archivo_subido.read()
        
        procesador = get_processor(tipo_seleccionado, contenido_bytes)

        if procesador:
            df = procesador.process()

            if df is not None:
                st.subheader("Previsualización de los Datos")
                st.dataframe(df)
                st.session_state['df_subido'] = df
                st.success("El archivo ha sido procesado y está listo.")

                # Allow user to select columns for filtering
                st.subheader("Selecciona Columnas para Filtrar")
                columnas_disponibles = df.columns.tolist()
                columnas_seleccionadas = st.multiselect(
                    "Elige las columnas que deseas usar como filtros en la barra lateral:",
                    columnas_disponibles,
                    key="columnas_para_filtrar"
                )
                st.session_state['columnas_filtrables'] = columnas_seleccionadas

# Sidebar filtering logic
if 'df_subido' in st.session_state and not st.session_state['df_subido'].empty:
    st.sidebar.title("Filtros")
    df_para_filtrar = st.session_state['df_subido'].copy()

    if 'columnas_filtrables' in st.session_state and st.session_state['columnas_filtrables']:
        filtro_manager = Filtros(df_para_filtrar)
        df_filtrado = filtro_manager.crear_filtros_dependientes(st.session_state['columnas_filtrables'])
        
        st.subheader("Datos Filtrados")
        st.write(f"Mostrando {len(df_filtrado)} de {len(st.session_state['df_subido'])} registros.")
        st.dataframe(df_filtrado)
    else:
        st.subheader("Datos Originales")
        st.dataframe(df_para_filtrar)



