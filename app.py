import streamlit as st
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import CategoricalNB

# ==================================
# CONFIGURACIÓN
# ==================================

st.set_page_config(
    page_title="Sistema de Recomendación Urbana",
    page_icon="🏙️",
    layout="wide"
)

st.title("🏙️ Sistema de Recomendación Urbana")
st.write("Predicción de necesidades y recomendación de ubicaciones.")

# ==================================
# CARGA DE DATOS
# ==================================

df_original = pd.read_excel("csvencuestayabien.xlsx")

df = df_original.copy()

if "Marca temporal" in df.columns:
    df = df.drop(columns=["Marca temporal"])

# ==================================
# COLUMNAS
# ==================================

COL_COLONIA = "Colonia"

COL_SERVICIOS = "¿Crees que dispones con las necesidades necesarias (escuelas, farmacias, consultorios, tiendas de bienes, transporte, etc) cerca de ti?"

COL_OBJETIVO = "¿Qué crees que sería una buena adición a tu colonia?"

# ==================================
# PREPARAR MODELO
# ==================================

encoders = {}

df_modelo = df[
    [
        COL_COLONIA,
        COL_SERVICIOS,
        COL_OBJETIVO
    ]
].copy()

for col in df_modelo.columns:
    le = LabelEncoder()
    df_modelo[col] = le.fit_transform(
        df_modelo[col].astype(str)
    )
    encoders[col] = le

X = df_modelo[
    [
        COL_COLONIA,
        COL_SERVICIOS
    ]
]

y = df_modelo[COL_OBJETIVO]

modelo = CategoricalNB()
modelo.fit(X, y)

# ==================================
# TABLA DE RECOMENDACIÓN
# ==================================

tabla = pd.crosstab(
    df_original[COL_COLONIA],
    df_original[COL_OBJETIVO]
)

# ==================================
# SIDEBAR
# ==================================

opcion = st.sidebar.radio(
    "Seleccione una opción",
    [
        "¿Qué necesita una colonia?",
        "¿Dónde construir un establecimiento?"
    ]
)

# ==================================
# OPCIÓN 1
# ==================================

if opcion == "¿Qué necesita una colonia?":

    st.header("Predicción de necesidades")

    colonias = sorted(
        list(
            encoders[COL_COLONIA].classes_
        )
    )

    colonia = st.selectbox(
        "Seleccione una colonia",
        colonias
    )

    servicios = st.selectbox(
        "¿Cuenta con servicios cercanos?",
        ["Sí", "No"]
    )

    if st.button("Predecir necesidad"):

        datos = pd.DataFrame({
            COL_COLONIA: [
                encoders[COL_COLONIA]
                .transform([colonia])[0]
            ],
            COL_SERVICIOS: [
                encoders[COL_SERVICIOS]
                .transform([servicios])[0]
            ]
        })

        pred = modelo.predict(datos)

        resultado = encoders[
            COL_OBJETIVO
        ].inverse_transform(pred)

        st.success(
            f"Se recomienda construir: {resultado[0]}"
        )

# ==================================
# OPCIÓN 2
# ==================================

elif opcion == "¿Dónde construir un establecimiento?":

    st.header("Recomendación de ubicación")

    servicios_disponibles = list(
        tabla.columns
    )

    servicio = st.selectbox(
        "Seleccione el establecimiento",
        servicios_disponibles
    )

    if st.button("Buscar colonias"):

        resultado = tabla[
            servicio
        ].sort_values(
            ascending=False
        )

        st.subheader(
            "Colonias recomendadas"
        )

        st.dataframe(
            resultado.head(10)
        )

        mejor_colonia = resultado.idxmax()

        st.success(
            f"La colonia más recomendada es: {mejor_colonia}"
        )