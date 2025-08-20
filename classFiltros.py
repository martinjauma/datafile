import streamlit as st
import pandas as pd

class Filtros:
    """
    Una clase para generar filtros en cascada donde cada filtro depende del anterior.
    """
    def __init__(self, df: pd.DataFrame):
        """
        Inicializa la clase con un DataFrame original.

        Args:
            df: El DataFrame de pandas que se va a filtrar.
        """
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Se esperaba un DataFrame de pandas.")
        self.df_original = df

    def crear_filtros_dependientes(self, columnas: list) -> pd.DataFrame:
        """
        Genera filtros en la barra lateral y aplica la selección progresivamente.
        El orden de las columnas en la lista determina la dependencia.

        Args:
            columnas: La lista ordenada de columnas por las que se debe filtrar.

        Returns:
            El DataFrame de pandas final después de aplicar todos los filtros.
        """
        st.sidebar.header("Filtros")
        
        df_filtrado = self.df_original.copy()
        
        for col in columnas:
            if col not in df_filtrado.columns:
                st.sidebar.warning(f"La columna '{col}' no se encontró y será ignorada.")
                continue

            opciones = ["Todos"] + sorted(df_filtrado[col].dropna().unique().tolist())
            
            # El widget selectbox devuelve directamente la opción que el usuario elige.
            seleccion = st.sidebar.selectbox(f"Filtrar por {col}", options=opciones)
            
            # Si el usuario elige una opción, filtramos el dataframe que se usará
            # para generar las opciones del *siguiente* filtro en el bucle.
            if seleccion != "Todos":
                df_filtrado = df_filtrado[df_filtrado[col] == seleccion]
        
        return df_filtrado
