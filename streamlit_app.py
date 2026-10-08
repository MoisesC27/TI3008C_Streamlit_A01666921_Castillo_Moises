
import pandas as pd
import plotly.express as px
import streamlit as st

# Configuracion de la pagina
st.set_page_config(
    page_title="Tablero ejecutivo de operaciones",
    page_icon="📊",
    layout="wide"
)

# Cargar los datos
@st.cache_data
def cargar_datos():
    datos = pd.read_csv("datos_ejemplo.csv")
    datos["Fecha"] = pd.to_datetime(datos["Fecha"])
    return datos

df = cargar_datos()

# Encabezado principal
st.title("Tablero ejecutivo de operaciones")
st.write("Analisis interactivo de casos, tiempos y satisfaccion.")
st.write("**Desarrollado por:** Moisés Castillo Chávez")

# Filtros laterales
st.sidebar.header("Filtros")

areas_disponibles = sorted(df["Área"].dropna().unique())
areas_seleccionadas = st.sidebar.multiselect(
    "Selecciona las areas",
    options=areas_disponibles,
    default=areas_disponibles
)

# Filtro adicional de la opcion A
regiones_disponibles = sorted(df["Región"].dropna().unique())
regiones_seleccionadas = st.sidebar.multiselect(
    "Selecciona las regiones",
    options=regiones_disponibles,
    default=regiones_disponibles
)

# Aplicar ambos filtros
df_filtrado = df[
    (df["Área"].isin(areas_seleccionadas)) &
    (df["Región"].isin(regiones_seleccionadas))
].copy()

# Validar que existan resultados
if df_filtrado.empty:
    st.warning("No hay datos para los filtros seleccionados.")
    st.stop()

# Calcular indicadores
total_casos = df_filtrado["Casos"].sum()
tiempo_promedio = df_filtrado["Tiempo_min"].mean()
satisfaccion_promedio = df_filtrado["Satisfacción"].mean()

# Indicadores principales
st.subheader("Indicadores de operacion")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total de casos", f"{total_casos:,.0f}")

with col2:
    st.metric("Tiempo promedio", f"{tiempo_promedio:.2f} min")

with col3:
    st.metric("Satisfaccion promedio", f"{satisfaccion_promedio:.2f}")

# Dos pestañas
tab1, tab2 = st.tabs(["Resumen ejecutivo", "Datos detallados"])

with tab1:
    st.subheader("Comportamiento de casos")

    casos_por_fecha = (
        df_filtrado.groupby("Fecha", as_index=False)["Casos"]
        .sum()
        .sort_values("Fecha")
    )

    fig1 = px.line(
        casos_por_fecha,
        x="Fecha",
        y="Casos",
        markers=True,
        title="Casos por fecha"
    )
    st.plotly_chart(fig1, width="stretch")

    # Comparacion de casos por area
    casos_por_area = (
        df_filtrado.groupby("Área", as_index=False)["Casos"]
        .sum()
    )

    fig2 = px.bar(
        casos_por_area,
        x="Área",
        y="Casos",
        title="Total de casos por area"
    )
    st.plotly_chart(fig2, width="stretch")

with tab2:
    st.subheader("Registros filtrados")
    st.dataframe(df_filtrado, width="stretch", hide_index=True)

    st.write("Numero de registros:", len(df_filtrado))
    st.write("Areas seleccionadas:", len(areas_seleccionadas))
    st.write("Regiones seleccionadas:", len(regiones_seleccionadas))

st.success("Tablero actualizado con los filtros seleccionados.")
