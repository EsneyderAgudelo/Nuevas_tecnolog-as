import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import json
import os

# Configuración de la página
st.set_page_config(
    page_title="Momento 2 - Actividad 1",
    page_icon="📌",
    layout="wide"
)

st.title("Momento 2 - Actividad 1")

# Descripción de la actividad
st.header("Descripción de la actividad")
st.markdown("""
Esta actividad es una introducción práctica a la creación y manipulación de DataFrames en Pandas.
Aprenderemos a construir estructuras de datos tabulares desde diferentes fuentes y visualizarlos
en una interfaz interactiva usando Streamlit. Trabajaremos con:
- Diccionarios y listas de Python
- Archivos locales (CSV, Excel, JSON)
- Bases de datos (SQLite)
- Datos desde internet (URLs públicas)
""")

# Objetivos de aprendizaje
st.header("Objetivos de aprendizaje")
st.markdown("""
- Comprender la estructura de DataFrames en Pandas
- Aprender a crear DataFrames desde múltiples fuentes
- Dominar las funciones básicas de visualización en Streamlit
- Aplicar estos conocimientos en ejemplos prácticos con datos colombianos
""")

# Solución
st.header("Solución")
st.markdown("A continuación se presentan diferentes métodos para crear DataFrames:")

# --------------------------------------------------
# 1. DataFrame desde diccionario (Libros colombianos)
# --------------------------------------------------
st.subheader("1. Desde diccionario - Libros colombianos")
st.markdown("Creamos un diccionario con datos de libros y lo convertimos a DataFrame.")

libros_dict = {
    "Título": ["Cien años de soledad", "Delirio", "La vorágine"],
    "Autor": ["Gabriel García Márquez", "Laura Restrepo", "José Eustasio Rivera"],
    "Año": [1967, 2004, 1924],
    "Género": ["Realismo mágico", "Novela psicológica", "Novela de la selva"]
}

df_libros = pd.DataFrame(libros_dict)
st.dataframe(df_libros)

# --------------------------------------------------
# 2. DataFrame desde lista de diccionarios (Ciudades)
# --------------------------------------------------
st.subheader("2. Desde lista de diccionarios - Ciudades colombianas")
st.markdown("Cada diccionario representa una fila con datos de ciudades.")

ciudades = [
    {"Ciudad": "Bogotá", "Altitud (m)": 2640, "Fundación": 1538},
    {"Ciudad": "Medellín", "Altitud (m)": 1475, "Fundación": 1616},
    {"Ciudad": "Cali", "Altitud (m)": 995, "Fundación": 1536}
]

df_ciudades = pd.DataFrame(ciudades)
st.dataframe(df_ciudades)

# --------------------------------------------------
# 3. DataFrame desde lista de listas (Productos)
# --------------------------------------------------
st.subheader("3. Desde lista de listas - Productos típicos")
st.markdown("Cada lista interna representa una fila de datos.")

productos = [
    ["Café", 15000, "Alimento"],
    ["Sombrero vueltiao", 80000, "Artesanía"],
    ["Mochila wayuu", 120000, "Artesanía"]
]

df_productos = pd.DataFrame(productos, columns=["Producto", "Precio (COP)", "Categoría"])
st.dataframe(df_productos)

# --------------------------------------------------
# 4. DataFrame desde Series (Datos demográficos)
# --------------------------------------------------
st.subheader("4. Desde Series - Datos demográficos")
st.markdown("Combinamos varias Series para formar un DataFrame.")

departamentos = pd.Series(["Antioquia", "Cundinamarca", "Valle del Cauca"])
poblacion = pd.Series([6.7, 3.2, 4.5])  # En millones
capital = pd.Series(["Medellín", "Bogotá", "Cali"])

df_demografia = pd.DataFrame({
    "Departamento": departamentos,
    "Población (millones)": poblacion,
    "Capital": capital
})
st.dataframe(df_demografia)

# --------------------------------------------------
# 5. DataFrame desde CSV (Datos de exportaciones)
# --------------------------------------------------
st.subheader("5. Desde CSV - Exportaciones colombianas")
st.markdown("Leemos datos desde un archivo CSV.")

# Crear archivo CSV de ejemplo si no existe
if not os.path.exists("exportaciones.csv"):
    datos_export = {
        "Producto": ["Café", "Petróleo", "Flores", "Banano"],
        "Valor (USD millones)": [2850, 12500, 1500, 850],
        "Destino principal": ["EE.UU.", "EE.UU.", "EE.UU.", "Europa"]
    }
    pd.DataFrame(datos_export).to_csv("exportaciones.csv", index=False)

df_csv = pd.read_csv("exportaciones.csv")
st.dataframe(df_csv)

# --------------------------------------------------
# 6. DataFrame desde Excel (Indicadores económicos)
# --------------------------------------------------
st.subheader("6. Desde Excel - Indicadores económicos")
st.markdown("Leemos datos desde un archivo Excel.")

# Crear archivo Excel de ejemplo si no existe
if not os.path.exists("economia.xlsx"):
    datos_econ = {
        "Año": [2019, 2020, 2021],
        "PIB (billones COP)": [1100, 990, 1150],
        "Inflación (%)": [3.5, 2.5, 5.0]
    }
    pd.DataFrame(datos_econ).to_excel("economia.xlsx", index=False)

df_excel = pd.read_excel("economia.xlsx")
st.dataframe(df_excel)

# --------------------------------------------------
# 7. DataFrame desde JSON (Datos culturales)
# --------------------------------------------------
st.subheader("7. Desde JSON - Patrimonio cultural")
st.markdown("Leemos datos desde un archivo JSON.")

# Crear archivo JSON de ejemplo si no existe
if not os.path.exists("patrimonio.json"):
    patrimonio = [
        {"Nombre": "Carnaval de Barranquilla", "Tipo": "Inmaterial", "Año declaración": 2003},
        {"Nombre": "Parque Arqueológico de San Agustín", "Tipo": "Material", "Año declaración": 1995}
    ]
    with open("patrimonio.json", "w") as f:
        json.dump(patrimonio, f)

df_json = pd.read_json("patrimonio.json")
st.dataframe(df_json)

# --------------------------------------------------
# 8. DataFrame desde URL (Datos públicos)
# --------------------------------------------------
st.subheader("8. Desde URL - Datos públicos")
st.markdown("Leemos datos directamente desde una URL.")

url_csv = "https://raw.githubusercontent.com/plotly/datasets/master/iris.csv"
try:
    df_url = pd.read_csv(url_csv)
    st.dataframe(df_url.head()) # Mostramos solo las primeras filas
except Exception as e:
    st.error(f"Error al leer el CSV desde la URL: {e}")

# --------------------------------------------------
# 9. DataFrame desde SQLite (Datos educativos)
# --------------------------------------------------
st.subheader("9. Desde SQLite - Datos educativos")
st.markdown("Conectamos a una base de datos SQLite y consultamos datos.")

# Configurar base de datos SQLite
conn = sqlite3.connect("educacion.db")
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS colegios (
    id INTEGER PRIMARY KEY,
    nombre TEXT,
    estudiantes INTEGER,
    municipio TEXT
)
""")

# Insertar datos de ejemplo si la tabla está vacía
if cursor.execute("SELECT COUNT(*) FROM colegios").fetchone()[0] == 0:
    datos_colegios = [
        (1, "Liceo Nacional", 1200, "Bogotá"),
        (2, "INEM", 950, "Cali"),
        (3, "Normal Superior", 800, "Medellín")
    ]
    cursor.executemany("INSERT INTO colegios VALUES (?, ?, ?, ?)", datos_colegios)
    conn.commit()

# Consultar y mostrar datos
df_sql = pd.read_sql("SELECT nombre, estudiantes, municipio FROM colegios", conn)
st.dataframe(df_sql)
conn.close()

# --------------------------------------------------
# 10. DataFrame desde NumPy (Datos aleatorios)
# --------------------------------------------------
st.subheader("10. Desde NumPy - Datos simulados")
st.markdown("Generamos datos numéricos aleatorios con NumPy.")

np.random.seed(42)
datos_np = np.random.randn(5, 3)  # 5 filas, 3 columnas de datos normales
df_numpy = pd.DataFrame(datos_np, columns=["Indicador A", "Indicador B", "Indicador C"])
st.dataframe(df_numpy)

# --------------------------------------------------
# Conclusión
# --------------------------------------------------
st.markdown("---")
st.success("¡Actividad completada exitosamente!")
st.markdown("""
**Resumen:**
- Hemos creado DataFrames desde 10 fuentes diferentes
- Todos los ejemplos utilizan datos relacionados con Colombia
- Los archivos necesarios se generan automáticamente
- La visualización es interactiva gracias a Streamlit
""")