import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import CategoricalNB
from sklearn.model_selection import train_test_split


# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="Sistema de Recomendación Urbana",
    page_icon="🏙️",
    layout="wide"
)

PALETA = [
    "#FF69B4",
    "#FFB6C1",
    "#87CEEB",
    "#B0E0E6",
    "#6A5ACD"
]

# ==========================================
# CARGAR DATOS
# ==========================================

@st.cache_data
def cargar_datos():
    return pd.read_excel("csvencuestayabien.xlsx")

df_original = cargar_datos()

# ==========================================
# COLUMNAS
# ==========================================

COL_COLONIA = "Colonia"

COL_INGRESO = "¿Ingreso Mensual en Casa?"

COL_SERVICIOS = "¿Crees que dispones con las necesidades necesarias (escuelas, farmacias, consultorios, tiendas de bienes, transporte, etc) cerca de ti?"

COL_OBJETIVO = "¿Qué crees que sería una buena adición a tu colonia?"

COL_SATISFACCION = "¿Estás satisfecho con tu lugar de residencia ?"

# ==========================================
# PREPARAR MODELO
# ==========================================

encoders = {}

df_modelo = df_original[
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

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import CategoricalNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="Sistema de Recomendación Urbana",
    page_icon="🏙️",
    layout="wide"
)

PALETA = [
    "#FF69B4",
    "#FFB6C1",
    "#87CEEB",
    "#B0E0E6",
    "#6A5ACD"
]

# ==========================================
# CARGAR DATOS
# ==========================================

@st.cache_data
def cargar_datos():
    return pd.read_excel("csvencuestayabien.xlsx")

df_original = cargar_datos()

# ==========================================
# COLUMNAS
# ==========================================

COL_COLONIA = "Colonia"

COL_INGRESO = "¿Ingreso Mensual en Casa?"

COL_SERVICIOS = "¿Crees que dispones con las necesidades necesarias (escuelas, farmacias, consultorios, tiendas de bienes, transporte, etc) cerca de ti?"

COL_OBJETIVO = "¿Qué crees que sería una buena adición a tu colonia?"

COL_SATISFACCION = "¿Estás satisfecho con tu lugar de residencia ?"

# ==========================================
# PREPARAR MODELO
# ==========================================

encoders = {}

df_modelo = df_original[
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

# ==========================================
# TABLA DE UBICACIÓN
# ==========================================

tabla = pd.crosstab(
    df_original[COL_COLONIA],
    df_original[COL_OBJETIVO]
)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🏙️ Menú")

opcion = st.sidebar.radio(
    "Seleccione una sección",
    [
        "📊 Dashboard",
        "🤖 Predicción Inteligente",
        "🏗️ Recomendación de Ubicación",
        "📋 Datos"
    ]
)

# ==========================================
# DASHBOARD
# ==========================================

if opcion == "📊 Dashboard":

    st.title("📊 Dashboard General")

    necesidad_top = (
        df_original[COL_OBJETIVO]
        .value_counts()
        .idxmax()
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Encuestas",
        len(df_original)
    )

    c2.metric(
        "Colonias",
        df_original[COL_COLONIA].nunique()
    )

    c3.metric(
        "Necesidad Principal",
        necesidad_top
    )



    st.divider()

    colA, colB = st.columns(2)

    necesidades = (
        df_original[COL_OBJETIVO]
        .value_counts()
        .reset_index()
    )

    necesidades.columns = [
        "Necesidad",
        "Cantidad"
    ]

    fig1 = px.bar(
        necesidades,
        x="Necesidad",
        y="Cantidad",
        color="Necesidad",
        color_discrete_sequence=PALETA,
        title="Necesidades más solicitadas"
    )

    colA.plotly_chart(
        fig1,
        use_container_width=True
    )

    fig2 = px.pie(
        necesidades,
        names="Necesidad",
        values="Cantidad",
        title="Distribución de necesidades",
        color_discrete_sequence=PALETA
    )

    colB.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.divider()

    colC, colD = st.columns(2)

    ingresos = (
        df_original[COL_INGRESO]
        .value_counts()
        .reset_index()
    )

    ingresos.columns = [
        "Ingreso",
        "Cantidad"
    ]

    fig3 = px.bar(
        ingresos,
        x="Ingreso",
        y="Cantidad",
        color="Ingreso",
        color_discrete_sequence=PALETA,
        title="Distribución de ingresos"
    )

    colC.plotly_chart(
        fig3,
        use_container_width=True
    )

    satisfaccion = (
        df_original[COL_SATISFACCION]
        .value_counts()
        .reset_index()
    )

    satisfaccion.columns = [
        "Respuesta",
        "Cantidad"
    ]

    fig4 = px.pie(
        satisfaccion,
        names="Respuesta",
        values="Cantidad",
        title="Satisfacción residencial",
        color_discrete_sequence=PALETA
    )

    colD.plotly_chart(
        fig4,
        use_container_width=True
    )

    st.divider()

    top_colonias = (
        df_original[COL_COLONIA]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_colonias.columns = [
        "Colonia",
        "Encuestas"
    ]

    fig5 = px.bar(
        top_colonias,
        x="Colonia",
        y="Encuestas",
        color="Encuestas",
        color_continuous_scale="Blues",
        title="Top 10 colonias con más registros"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

    st.info(
    f"""
    Conclusión automática:

    La necesidad más frecuente identificada fue:
    {necesidad_top}.

    Los resultados sugieren que esta necesidad
    debería considerarse prioritaria para futuras
    inversiones en infraestructura urbana.
    """
    )

# ==========================================
# PREDICCIÓN
# ==========================================

elif opcion == "🤖 Predicción Inteligente":

    st.title("🤖 Predicción de Necesidades")

    colonia = st.selectbox(
        "Seleccione una colonia",
        sorted(
            df_original[COL_COLONIA]
            .unique()
        )
    )

    servicios = st.selectbox(
        "¿Cuenta con servicios cercanos?",
        sorted(
            df_original[COL_SERVICIOS]
            .dropna()
            .unique()
        )
    )

    if st.button("Predecir"):

        datos = pd.DataFrame({
            COL_COLONIA:[
                encoders[COL_COLONIA]
                .transform([colonia])[0]
            ],
            COL_SERVICIOS:[
                encoders[COL_SERVICIOS]
                .transform([servicios])[0]
            ]
        })

        probabilidades = modelo.predict_proba(datos)[0]

        clases = encoders[
            COL_OBJETIVO
        ].inverse_transform(
            np.arange(len(probabilidades))
        )

        resultados = pd.DataFrame({
            "Necesidad": clases,
            "Probabilidad": probabilidades
        })

        resultados = resultados.sort_values(
            by="Probabilidad",
            ascending=False
        )

        st.success(
            f"Recomendación principal: {resultados.iloc[0]['Necesidad']}"
        )

        st.subheader(
            "Top 3 recomendaciones"
        )

        st.dataframe(
            resultados.head(3),
            use_container_width=True
        )

        fig = px.bar(
            resultados.head(3),
            x="Necesidad",
            y="Probabilidad",
            color="Necesidad",
            color_discrete_sequence=PALETA,
            title="Probabilidades"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader(
            f"Historial de necesidades en {colonia}"
        )

        filtro = df_original[
            df_original[COL_COLONIA]
            == colonia
        ]

        hist = (
            filtro[COL_OBJETIVO]
            .value_counts()
            .reset_index()
        )

        hist.columns = [
            "Necesidad",
            "Cantidad"
        ]

        fig2 = px.bar(
            hist,
            x="Necesidad",
            y="Cantidad",
            color="Necesidad",
            color_discrete_sequence=PALETA
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

# ==========================================
# UBICACIÓN
# ==========================================

elif opcion == "🏗️ Recomendación de Ubicación":

    st.title("🏗️ Recomendación de Ubicación")

    establecimiento = st.selectbox(
        "Seleccione establecimiento",
        sorted(tabla.columns)
    )

    datos = (
        tabla[establecimiento]
        .sort_values(
            ascending=False
        )
        .reset_index()
    )

    datos.columns = [
        "Colonia",
        "Solicitudes"
    ]

    mejor = datos.iloc[0]["Colonia"]

    st.success(
        f"Mejor colonia recomendada: {mejor}"
    )

    st.subheader(
        "Top 10 colonias"
    )

    st.dataframe(
        datos.head(10),
        use_container_width=True
    )

    fig = px.bar(
        datos.head(10),
        x="Solicitudes",
        y="Colonia",
        orientation="h",
        color="Solicitudes",
        color_continuous_scale="Blues",
        title=f"Demanda de {establecimiento}"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================
# DATOS
# ==========================================

elif opcion == "📋 Datos":

    st.title("📋 Datos de la Encuesta")

    st.dataframe(
        df_original,
        use_container_width=True
    )

    csv = df_original.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "Descargar CSV",
        csv,
        "encuesta.csv",
        "text/csv"
    )

# ==========================================
# TABLA DE UBICACIÓN
# ==========================================

tabla = pd.crosstab(
    df_original[COL_COLONIA],
    df_original[COL_OBJETIVO]
)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🏙️ Menú")

opcion = st.sidebar.radio(
    "Seleccione una sección",
    [
        "📊 Dashboard",
        "🤖 Predicción Inteligente",
        "🏗️ Recomendación de Ubicación",
        "📋 Datos"
    ]
)

# ==========================================
# DASHBOARD
# ==========================================

if opcion == "📊 Dashboard":

    st.title("📊 Dashboard General")

    necesidad_top = (
        df_original[COL_OBJETIVO]
        .value_counts()
        .idxmax()
    )

   c1, c2, c3 = st.columns(3)

    c1.metric(
        "Encuestas",
        len(df_original)
    )

    c2.metric(
        "Colonias",
        df_original[COL_COLONIA].nunique()
    )

    c3.metric(
        "Necesidad Principal",
        necesidad_top
    )


    st.divider()

    colA, colB = st.columns(2)

    necesidades = (
        df_original[COL_OBJETIVO]
        .value_counts()
        .reset_index()
    )

    necesidades.columns = [
        "Necesidad",
        "Cantidad"
    ]

    fig1 = px.bar(
        necesidades,
        x="Necesidad",
        y="Cantidad",
        color="Necesidad",
        color_discrete_sequence=PALETA,
        title="Necesidades más solicitadas"
    )

    colA.plotly_chart(
        fig1,
        use_container_width=True
    )

    fig2 = px.pie(
        necesidades,
        names="Necesidad",
        values="Cantidad",
        title="Distribución de necesidades",
        color_discrete_sequence=PALETA
    )

    colB.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.divider()

    colC, colD = st.columns(2)

    ingresos = (
        df_original[COL_INGRESO]
        .value_counts()
        .reset_index()
    )

    ingresos.columns = [
        "Ingreso",
        "Cantidad"
    ]

    fig3 = px.bar(
        ingresos,
        x="Ingreso",
        y="Cantidad",
        color="Ingreso",
        color_discrete_sequence=PALETA,
        title="Distribución de ingresos"
    )

    colC.plotly_chart(
        fig3,
        use_container_width=True
    )

    satisfaccion = (
        df_original[COL_SATISFACCION]
        .value_counts()
        .reset_index()
    )

    satisfaccion.columns = [
        "Respuesta",
        "Cantidad"
    ]

    fig4 = px.pie(
        satisfaccion,
        names="Respuesta",
        values="Cantidad",
        title="Satisfacción residencial",
        color_discrete_sequence=PALETA
    )

    colD.plotly_chart(
        fig4,
        use_container_width=True
    )

    st.divider()

    top_colonias = (
        df_original[COL_COLONIA]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_colonias.columns = [
        "Colonia",
        "Encuestas"
    ]

    fig5 = px.bar(
        top_colonias,
        x="Colonia",
        y="Encuestas",
        color="Encuestas",
        color_continuous_scale="Blues",
        title="Top 10 colonias con más registros"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

    st.info(
    f"""
    Conclusión automática:

    La necesidad más frecuente identificada fue:
    {necesidad_top}.

    Los resultados sugieren que esta necesidad
    debería considerarse prioritaria para futuras
    inversiones en infraestructura urbana.
    """
)
# ==========================================
# PREDICCIÓN
# ==========================================

elif opcion == "🤖 Predicción Inteligente":

    st.title("🤖 Predicción de Necesidades")

    colonia = st.selectbox(
        "Seleccione una colonia",
        sorted(
            df_original[COL_COLONIA]
            .unique()
        )
    )

    servicios = st.selectbox(
        "¿Cuenta con servicios cercanos?",
        sorted(
            df_original[COL_SERVICIOS]
            .dropna()
            .unique()
        )
    )

    if st.button("Predecir"):

        datos = pd.DataFrame({
            COL_COLONIA:[
                encoders[COL_COLONIA]
                .transform([colonia])[0]
            ],
            COL_SERVICIOS:[
                encoders[COL_SERVICIOS]
                .transform([servicios])[0]
            ]
        })

        probabilidades = modelo.predict_proba(datos)[0]

        clases = encoders[
            COL_OBJETIVO
        ].inverse_transform(
            np.arange(len(probabilidades))
        )

        resultados = pd.DataFrame({
            "Necesidad": clases,
            "Probabilidad": probabilidades
        })

        resultados = resultados.sort_values(
            by="Probabilidad",
            ascending=False
        )

        st.success(
            f"Recomendación principal: {resultados.iloc[0]['Necesidad']}"
        )

        st.subheader(
            "Top 3 recomendaciones"
        )

        st.dataframe(
            resultados.head(3),
            use_container_width=True
        )

        fig = px.bar(
            resultados.head(3),
            x="Necesidad",
            y="Probabilidad",
            color="Necesidad",
            color_discrete_sequence=PALETA,
            title="Probabilidades"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader(
            f"Historial de necesidades en {colonia}"
        )

        filtro = df_original[
            df_original[COL_COLONIA]
            == colonia
        ]

        hist = (
            filtro[COL_OBJETIVO]
            .value_counts()
            .reset_index()
        )

        hist.columns = [
            "Necesidad",
            "Cantidad"
        ]

        fig2 = px.bar(
            hist,
            x="Necesidad",
            y="Cantidad",
            color="Necesidad",
            color_discrete_sequence=PALETA
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

# ==========================================
# UBICACIÓN
# ==========================================

elif opcion == "🏗️ Recomendación de Ubicación":

    st.title("🏗️ Recomendación de Ubicación")

    establecimiento = st.selectbox(
        "Seleccione establecimiento",
        sorted(tabla.columns)
    )

    datos = (
        tabla[establecimiento]
        .sort_values(
            ascending=False
        )
        .reset_index()
    )

    datos.columns = [
        "Colonia",
        "Solicitudes"
    ]

    mejor = datos.iloc[0]["Colonia"]

    st.success(
        f"Mejor colonia recomendada: {mejor}"
    )

    st.subheader(
        "Top 10 colonias"
    )

    st.dataframe(
        datos.head(10),
        use_container_width=True
    )

    fig = px.bar(
        datos.head(10),
        x="Solicitudes",
        y="Colonia",
        orientation="h",
        color="Solicitudes",
        color_continuous_scale="Blues",
        title=f"Demanda de {establecimiento}"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================
# DATOS
# ==========================================

elif opcion == "📋 Datos":

    st.title("📋 Datos de la Encuesta")

    st.dataframe(
        df_original,
        use_container_width=True
    )

    csv = df_original.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "Descargar CSV",
        csv,
        "encuesta.csv",
        "text/csv"
    )
