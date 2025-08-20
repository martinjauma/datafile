import pandas as pd
import streamlit as st
from io import BytesIO
import json
import xml.etree.ElementTree as ET

class UploadProcessor:
    """Clase base para procesadores de archivos. Define la interfaz común."""
    def __init__(self, contenido_bytes):
        self.contenido_bytes = contenido_bytes

    def process(self):
        """Método abstracto que debe ser implementado por las subclases."""
        raise NotImplementedError("El método process debe ser implementado por la subclase.")

class AnglesCsvProcessor(UploadProcessor):
    """Procesa archivos de tipo CSV."""
    def process(self):
        st.info("Usando el procesador de CSV...")
        return pd.read_csv(BytesIO(self.contenido_bytes))

class AnglesJsonProcessor(UploadProcessor):
    """Procesa archivos JSON con la estructura anidada de Fulcrum."""
    def process(self):
        st.info("Usando el procesador de JSON...")
        data = json.loads(self.contenido_bytes)
        filas_procesadas = []
        for grupo_fila in data.get('rows', []):
            nombre_fila = grupo_fila.get('row_name')
            for clip in grupo_fila.get('clips', []):
                fila_plana = {
                    'Row Name': nombre_fila,
                    'Clip Start': clip.get('time_start'),
                    'Clip End': clip.get('time_end')
                }
                qualifiers = clip.get('qualifiers', {}).get('qualifiers_array', [])
                for qualifier in qualifiers:
                    if 'category' in qualifier and 'name' in qualifier:
                        fila_plana[qualifier['category']] = qualifier['name']
                filas_procesadas.append(fila_plana)
        return pd.DataFrame(filas_procesadas)

class AnglesXmlProcessor(UploadProcessor):
    """Procesa archivos XML con la estructura específica de Fulcrum."""
    def process(self):
        st.info("Usando el procesador de XML...")
        try:
            xml_content = self.contenido_bytes.decode('utf-16')
        except UnicodeDecodeError:
            xml_content = self.contenido_bytes.decode('utf-8')
        
        root = ET.fromstring(xml_content)
        filas_procesadas = []
        for instance in root.findall('.//instance'):
            flat_row = {}
            code_element = instance.find('code')
            if code_element is not None:
                flat_row['Row Name'] = code_element.text
            
            for label in instance.findall('label'):
                group_element = label.find('group')
                text_element = label.find('text')
                if group_element is not None and text_element is not None and group_element.text is not None:
                    flat_row[group_element.text] = text_element.text
            
            filas_procesadas.append(flat_row)
        return pd.DataFrame(filas_procesadas)

def get_processor(tipo_seleccionado, contenido_bytes):
    """Función Fábrica: Devuelve una instancia del procesador adecuado."""
    procesadores = {
        "Fulcrum Angles.csv": AnglesCsvProcessor,
        "Fulcrum Angles.json": AnglesJsonProcessor,
        "Fulcrum Angles.xml": AnglesXmlProcessor
    }
    procesador_class = procesadores.get(tipo_seleccionado)
    if procesador_class:
        return procesador_class(contenido_bytes)
    return None
