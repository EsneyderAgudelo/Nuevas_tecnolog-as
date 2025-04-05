import streamlit as st
import pandas as pd
from io import StringIO

# Configuración de la página
st.set_page_config(
    page_title="Estudiantes Colombia",
    page_icon="📊",
    layout="wide"
)

st.title("Análisis de Datos de Estudiantes Colombianos")

st.header("Descripción de la actividad")
st.markdown("""
Esta aplicación forma parte de un proyecto educativo que combina:
- **Ciencia de datos** con Python
- **Análisis estadístico** de información educativa
- **Visualización interactiva** con Streamlit
            
El objetivo es explorar los datos académicos de estudiantes colombianos para identificar patrones,
tendencias y relaciones significativas que puedan informar decisiones educativas.            
""")

st.header("Objetivos de aprendizaje")

st.markdown("""
Al trabajar con este proyecto, desarrollarás competencias en:

1. **Manejo de datos**:
   - Carga y limpieza de datasets educativos
   - Transformación de variables académicas
   - Filtrado y selección de información relevante

2. **Análisis estadístico**:
   - Cálculo de métricas educativas (promedios, distribuciones)
   - Identificación de correlaciones entre variables
   - Generación de resúmenes estadísticos

3. **Visualización interactiva**:
   - Creación de dashboards educativos
   - Implementación de filtros dinámicos
   - Presentación efectiva de hallazgos
""")

st.header("📋 Estructura del Análisis")
st.markdown("""
La aplicación está organizada en cuatro secciones principales:

1. **Vista general**: Primeras y últimas filas del dataset
2. **Resumen estadístico**: Información descriptiva básica
3. **Selección de variables**: Análisis por columnas específicas
4. **Filtros avanzados**: Exploración segmentada por criterios académicos
""")

st.info("💡 **Nota metodológica**: Los datos utilizados son anónimos y representativos del sistema educativo colombiano.")


st.header("Solución")

@st.cache_data
def load_data():
    try:
        data = pd.read_csv("static\datasets\estudiantes_colombia.csv")
        
        expected_columns = ['nombre', 'edad', 'promedio']
        for col in expected_columns:
            if col not in data.columns:
                st.warning(f"Advertencia: La columna '{col}' no se encontró en el dataset")
        
        return data
    
    except FileNotFoundError:
        st.error("❌ Error: No se encontró el archivo 'estudiantes_colombia.csv'")
        st.info("ℹ️ Por favor asegúrate de que el archivo esté en el mismo directorio que esta aplicación")
        return None
    except Exception as e:
        st.error(f"❌ Error inesperado al cargar los datos: {str(e)}")
        return None

df = load_data()

if df is not None:
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Vista General", 
        "📋 Resumen Estadístico", 
        "🎯 Selección Columnas", 
        "📈 Filtros Avanzados"
    ])
    
    with tab1:
        st.header("Vista General del Dataset")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Primeras 5 filas")
            st.dataframe(df.head(), use_container_width=True)
        
        with col2:
            st.subheader("Últimas 5 filas")
            st.dataframe(df.tail(), use_container_width=True)
        
        st.subheader("Dimensión del Dataset")
        st.write(f"El dataset contiene {df.shape[0]} filas y {df.shape[1]} columnas")
    
    with tab2:
        st.header("Resumen Estadístico")
        
        with st.expander("🔎 Información del Dataset (.info())", expanded=True):
            buffer = StringIO()
            df.info(buf=buffer)
            st.text(buffer.getvalue())
        
        st.subheader("Estadísticas Descriptivas (.describe())")
        st.dataframe(df.describe(), use_container_width=True)
        
        # Mostrar tipos de datos
        st.subheader("Tipos de Datos")
        st.write(df.dtypes)
    
    with tab3:
        st.header("Selección de Columnas Específicas")
        
        selected_columns = st.multiselect(
            "Selecciona las columnas que deseas visualizar:",
            options=sorted(df.columns),
            default=["nombre", "edad", "promedio"] if all(col in df.columns for col in ["nombre", "edad", "promedio"]) else []
        )
        
        if selected_columns:
            st.dataframe(df[selected_columns], use_container_width=True)
        else:
            st.warning("Por favor selecciona al menos una columna para visualizar")
    
    with tab4:
        st.header("Filtros Avanzados")
        
        if "promedio" in df.columns:
            col1, col2 = st.columns([1, 3])
            
            with col1:
                min_score = st.slider(
                    "Promedio mínimo:",
                    min_value=float(df["promedio"].min()),
                    max_value=float(df["promedio"].max()),
                    value=float(df["promedio"].mean()),
                    step=0.5
                )

                age_range = st.slider(
                    "Rango de edad:",
                    min_value=int(df["edad"].min()),
                    max_value=int(df["edad"].max()),
                    value=(int(df["edad"].min()), int(df["edad"].max()))
                )
            
            with col2:
                filtered_df = df[
                    (df["promedio"] >= min_score) &
                    (df["edad"] >= age_range[0]) & 
                    (df["edad"] <= age_range[1])
                ]
                
                st.metric("Estudiantes filtrados", len(filtered_df))
                st.dataframe(filtered_df, use_container_width=True)
                
                if len(filtered_df) > 0:
                    csv = filtered_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Descargar datos filtrados",
                        data=csv,
                        file_name="estudiantes_filtrados.csv",
                        mime="text/csv"
                    )
        else:
            st.warning("No se encontró la columna 'promedio' en el dataset")

else:
    st.info("Por favor corrige los errores mencionados arriba para continuar")