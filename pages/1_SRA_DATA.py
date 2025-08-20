import streamlit as st
from classDatabase import Database
from classFiltros import Filtros

# --- Funciones cacheadas ---
@st.cache_resource
def get_db_manager():
    """Crea y cachea la instancia del manejador de la base de datos."""
    return Database()

# --- Interfaz de Streamlit ---
st.set_page_config(layout="wide")
st.title("Visualizador de Base de Datos SRA")

# Obtener la instancia del manejador de BD (desde caché si existe)
db_manager = get_db_manager()

st.sidebar.title("Controles")
if st.sidebar.button("Refrescar Datos de MongoDB"):
    # Limpiar explícitamente AMBAS cachés
    get_db_manager.clear()
    db_manager.get_collection_data.clear()
    st.sidebar.success("Caché limpiada. Forzando recarga de datos.")
    st.rerun()


if db_manager.client is not None and db_manager.db is not None:
    # Obtener el DataFrame original
    df_original = db_manager.get_collection_data("DATA")

    if not df_original.empty:
        # --- Lógica de Filtros ---
        # El orden de las columnas aquí define el orden y la dependencia de los filtros.
        columnas_para_filtrar = ['Row Name','RESULTADO', 'YEAR','FECHA','EQUIPO'] # <-- CAMBIA ESTAS COLUMNAS
        
        filtro_manager = Filtros(df_original)
        # Este método ahora crea los filtros Y devuelve el dataframe ya filtrado.
        df_filtrado = filtro_manager.crear_filtros_dependientes(columnas_para_filtrar)

        # --- Mostrar Datos ---
        st.write(f"Mostrando {len(df_filtrado)} de {len(df_original)} registros.")
        st.dataframe(df_filtrado)

        with st.expander("Ver Datos Originales Completos"):
            st.dataframe(df_original)
    else:
        st.warning("No se encontraron datos en la colección 'DATA'.")
else:
    st.info("Esperando conexión a la base de datos...")
