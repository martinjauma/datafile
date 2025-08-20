import streamlit as st
import pandas as pd
from pymongo import MongoClient

class Database:
    """
    Una clase para manejar la conexión a la base de datos MongoDB.
    """
    def __init__(self):
        """
        Inicializa la conexión a la base de datos usando las credenciales de Streamlit.
        """
        try:
            # Carga las credenciales desde el archivo secrets.toml
            mongo_uri = st.secrets["mongo"]["uri"]
            self.client = MongoClient(mongo_uri)
            self.db = self.client["SRA"] # Conéctate a tu base de datos específica
            st.success("Conexión a MongoDB exitosa.")
        except Exception as e:
            st.error(f"Error al conectar a MongoDB: {e}")
            self.client = None
            self.db = None

    @st.cache_data
    def get_collection_data(_self, collection_name: str) -> pd.DataFrame:
        """
        Obtiene los datos de una colección y los devuelve como un DataFrame de pandas.

        Args:
            collection_name: El nombre de la colección de la que se van a obtener los datos.

        Returns:
            Un DataFrame de pandas con los datos de la colección.
        """
        if _self.db is not None:
            try:
                collection = _self.db[collection_name]
                data = list(collection.find())
                if data:
                    return pd.DataFrame(data)
                else:
                    st.warning(f"La colección '{collection_name}' está vacía o no existe.")
                    return pd.DataFrame()
            except Exception as e:
                st.error(f"Error al obtener datos de la colección '{collection_name}': {e}")
                return pd.DataFrame()
        return pd.DataFrame()
