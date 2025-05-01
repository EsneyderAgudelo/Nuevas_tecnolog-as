import streamlit as st
import pandas as pd
import numpy as np
from faker import Faker # type: ignore
import random

# Configuración de la página
st.set_page_config(   
    page_icon="📌",
    layout="wide"
)

st.title("Momento 2 - Actividad 3")

st.header("Descripción de la actividad")
st.markdown("""
Esta actividad es una introducción práctica a Python y a las estructuras de datos básicas.
En ella, exploraremos los conceptos fundamentales de Python y aprenderemos a utilizar variables,
tipos de datos, operadores, y las estructuras de datos más utilizadas como listas, tuplas,
diccionarios y conjuntos.
""")

st.header("Objetivos de aprendizaje")

st.markdown("""
- Comprender los tipos de datos básicos en Python
- Aprender a utilizar variables y operadores
- Dominar las estructuras de datos fundamentales
- Aplicar estos conocimientos en ejemplos prácticos
""")

st.header("Enlace a Google colab")
st.markdown("[📎 Ir al google colab de Esneyder](https://colab.research.google.com/drive/1SVOyBTwsKQRD_O1eJGhzhpQRPfth3F2H?usp=sharing)")

st.header("Solución")

# Configurar Faker para Colombia
fake = Faker('es_CO')

# Establecer semilla para reproducibilidad
np.random.seed(123)
random.seed(123)
fake.seed_instance(123)

# Crear datos
n = 50
data = {
    'id': range(1, n + 1),
    'nombre_completo': [fake.name() for _ in range(n)],
    'edad': np.random.randint(15, 76, n),
    'region': random.choices(
        ['Caribe', 'Andina', 'Pacífica', 'Orinoquía', 'Amazonía'],
        weights=[0.3, 0.4, 0.15, 0.1, 0.05],
        k=n
    ),
    'municipio': random.choices(
        [
            'Barranquilla', 'Santa Marta', 'Cartagena',  # Caribe
            'Bogotá', 'Medellín', 'Tunja', 'Manizales',  # Andina
            'Cali', 'Quibdó', 'Buenaventura',           # Pacífica
            'Villavicencio', 'Yopal',                    # Orinoquía
            'Leticia', 'Puerto Inírida'                  # Amazonía
        ],
        k=n
    ),
    'ingreso_mensual': np.random.randint(800000, 12000001, n),
    'ocupacion': random.choices(
        [
            'Estudiante', 'Docente', 'Comerciante', 'Agricultor',
            'Ingeniero', 'Médico', 'Desempleado', 'Pensionado',
            'Emprendedor', 'Obrero'
        ],
        k=n
    ),
    'tipo_vivienda': random.choices(
        ['Propia', 'Arrendada', 'Familiar'],
        k=n
    ),
    'fecha_nacimiento': [
        fake.date_of_birth(minimum_age=15, maximum_age=75) for _ in range(n)
    ],
    'acceso_internet': random.choices([True, False], weights=[0.7, 0.3], k=n)
}

# Crear DataFrame
df_nuevo = pd.DataFrame(data)

# Introducir algunos valores nulos
df_nuevo.loc[3:5, 'ingreso_mensual'] = np.nan
df_nuevo.loc[15:17, 'ocupacion'] = np.nan

# Convertir fecha_nacimiento a datetime
df_nuevo['fecha_nacimiento'] = pd.to_datetime(df_nuevo['fecha_nacimiento'])

# solucion
st.sidebar.title("Filtros dinámicos")

df_filtrado = df_nuevo.copy()

# 1. Filtro por rango de edad
if st.sidebar.checkbox("Filtrar por rango de edad"):
    min_edad, max_edad = st.sidebar.slider("Selecciona el rango de edad", 15, 75, (20, 60))
    df_filtrado = df_filtrado[df_filtrado['edad'].between(min_edad, max_edad)]

# 2. Filtro por municipios específicos
if st.sidebar.checkbox("Filtrar por municipios"):
    municipios_opciones = [
        'Barranquilla', 'Santa Marta', 'Cartagena', 'Bogotá', 'Medellín',
        'Tunja', 'Manizales', 'Cali', 'Quibdó', 'Buenaventura',
        'Villavicencio', 'Yopal', 'Leticia', 'Puerto Inírida'
    ]
    municipios_seleccionados = st.sidebar.multiselect("Selecciona municipios", municipios_opciones)
    if municipios_seleccionados:
        df_filtrado = df_filtrado[df_filtrado['municipio'].isin(municipios_seleccionados)]

# 3. Filtro por ingreso mensual mínimo
if st.sidebar.checkbox("Filtrar por ingreso mensual mínimo"):
    ingreso_minimo = st.sidebar.slider("Ingreso mensual mínimo", 800000, 12000000, 2000000, step=100000)
    df_filtrado = df_filtrado[df_filtrado['ingreso_mensual'] > ingreso_minimo]

# 4. Filtro por ocupación
if st.sidebar.checkbox("Filtrar por ocupación"):
    ocupaciones_opciones = [
        'Estudiante', 'Docente', 'Comerciante', 'Agricultor',
        'Ingeniero', 'Médico', 'Desempleado', 'Pensionado',
        'Emprendedor', 'Obrero'
    ]
    ocupaciones_seleccionadas = st.sidebar.multiselect("Selecciona ocupaciones", ocupaciones_opciones)
    if ocupaciones_seleccionadas:
        df_filtrado = df_filtrado[df_filtrado['ocupacion'].isin(ocupaciones_seleccionadas)]

# 5. Filtro por tipo de vivienda no propia
if st.sidebar.checkbox("Filtrar personas sin vivienda propia"):
    df_filtrado = df_filtrado[~(df_filtrado['tipo_vivienda'] == 'Propia')]

# 6. Filtro por nombres que contienen una cadena
if st.sidebar.checkbox("Filtrar por nombre"):
    texto_nombre = st.sidebar.text_input("Ingresa parte del nombre a buscar")
    if texto_nombre:
        df_filtrado = df_filtrado[df_filtrado['nombre_completo'].str.contains(texto_nombre, case=False, na=False)]

# 7. Filtro por año de nacimiento específico
if st.sidebar.checkbox("Filtrar por año de nacimiento"):
    años = list(range(1949, 2010))  # 2024 - 75 hasta 2024 - 15
    año_nacimiento = st.sidebar.selectbox("Selecciona el año de nacimiento", años)
    df_filtrado = df_filtrado[df_filtrado['fecha_nacimiento'].dt.year == año_nacimiento]

# 8. Filtro por acceso a internet
if st.sidebar.checkbox("Filtrar por acceso a internet"):
    acceso = st.sidebar.radio("¿Tiene acceso a internet?", ["Sí", "No"])
    df_filtrado = df_filtrado[df_filtrado['acceso_internet'] == (acceso == "Sí")]

# 9. Filtro por ingresos nulos
if st.sidebar.checkbox("Filtrar por ingresos nulos"):
    df_filtrado = df_filtrado[df_filtrado['ingreso_mensual'].isnull()]

# 10. Filtro por rango de fechas de nacimiento
if st.sidebar.checkbox("Filtrar por rango de fechas de nacimiento"):
    fecha_inicio = st.sidebar.date_input("Fecha de nacimiento inicial", value=pd.to_datetime("1949-01-01"))
    fecha_fin = st.sidebar.date_input("Fecha de nacimiento final", value=pd.to_datetime("2009-12-31"))
    if fecha_inicio <= fecha_fin:
        df_filtrado = df_filtrado[df_filtrado['fecha_nacimiento'].between(fecha_inicio, fecha_fin)]

# Mostrar resultados
st.subheader("Datos filtrados")
st.write(f"Total de registros: {len(df_filtrado)}")
st.dataframe(df_filtrado)
