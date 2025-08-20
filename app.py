import streamlit as st

st.set_page_config(
    page_title="Página Principal",
    layout="wide"
)

st.title("Bienvenido a la Aplicación de Gestión de Datos")

st.sidebar.success("Selecciona una página arriba.")

st.markdown("""
### ¿Cómo usar esta aplicación?

- **SRA_DATA**: Navega a esta página para visualizar y filtrar los datos existentes en la base de datos de MongoDB.
- **Subir_Base**: Usa esta sección para cargar nuevos datos a la base de datos desde un archivo.

Utiliza la barra lateral para navegar entre las diferentes secciones de la aplicación.
""")