
import joblib
import streamlit as st
import pandas as pd

# --- Configuración de la Página ---
# Esto debe ser lo primero que se ejecute en el script.
st.set_page_config(
    page_title="Predictor del porcentaje de la concentración de sílice",
    page_icon="🧪",
    layout="wide"
)

# --- Carga del Modelo ---
# Usamos @st.cache_resource para que el modelo se cargue solo una vez y se mantenga en memoria,
# lo que hace que la aplicación sea mucho más rápida.
@st.cache_resource
def load_model(model_path):
    """Carga el modelo entrenado desde un archivo .joblib."""
    try:
        model = joblib.load(model_path)
        return model
    except FileNotFoundError:
        st.error(f"Error: No se encontró el archivo del modelo en {model_path}. Asegúrate de que el archivo del modelo esté en el directorio correcto.")
        return None

# Cargamos nuestro modelo campeón. Streamlit buscará en la ruta 'modelo_xgboost_final.joblib'.
model = load_model('model_flotacion.joblib')

# --- Barra Lateral para las Entradas del Usuario ---
with st.sidebar:
    st.header("⚙️ Parámetros de Entrada")
    st.markdown("""
    Ajusta los deslizadores para que coincidan con los parametros del proceso de flotación.
    """)

    # Slider para el caudal de amina (m3/s)
    flowrate = st.slider(
        label='Caudal de amina (m³/s)',
        min_value= 241.70,
        max_value= 739.30,
        value= 488.43 , # Valor inicial
        step=1
    )
    st.caption("El flujo de amina es una de las variables más críticas, porque controla la selectividad y la eficiencia de la separación entre sílica y hierro")

    # Slider para el caudal del aire en la columna 1
    temperature = st.slider(
        label='Flujo de aire que ingresa a la columna 1 (m³/s)',
        min_value= 175.85,
        max_value= 372.44,
        value= 280.13,
        step=1
    )
    st.caption("El flujo del aire es una de las variables operativas más importantes, porque controla la formación, cantidad y tamaño de burbujas, que se encarga del transporte de las partículas sílice")

    # Slider para el % de concentración de hierro
    pressure = st.slider(
        label='Concentración de Hierro (%)',
        min_value= 62.51,
        max_value= 68.01,
        value=0,
        step=1
    )
    st.caption("El % de hierro en el concentrado está inversamente relacionado con la calidad de la sílice")

# --- Contenido de la Página Principal ---
st.title("🧪 Predictor de la calidad del sílice")
st.markdown("""
¡Bienvenido! Esta aplicación utiliza un modelo de machine learning para predecir la calidad de silice en un proceso de flotación aplicado a la industria minera.

**Esta herramienta puede ayudar a los ingenieros de procesos y operadores a:**
- **Optimizar** las condiciones de operación para obtener el máximo rendimiento.
- **Predecir** el impacto de los cambios en el proceso antes de implementarlos.
- **Solucionar** problemas potenciales simulando diferentes escenarios.
""")

# --- Lógica de Predicción ---
# Solo intentamos predecir si el modelo se ha cargado correctamente.
if model is not None:
    # El botón principal que el usuario presionará para obtener un resultado.
    if st.button('🚀 Predecir % concentracion de Silice ', type="primary"):
        # Creamos un DataFrame de pandas con las entradas del usuario.
        # ¡Es crucial que los nombres de las columnas coincidan exactamente con los que el modelo espera!
        df_input = pd.DataFrame({
            'Amina Flow': [flowrateAmina],
            'Flotation Column 01 Air Flow': [flowrate],
            '% Iron Concentrate': [IronConcentrate]
        })

        # Hacemos la predicción
        try:
            prediction_value = model.predict(df_input)
            st.subheader("📈 Resultado de la Predicción")
            # Mostramos el resultado en un cuadro de éxito, formateado a dos decimales.
            st.success(f"**% Concentracion de Sílice Predicho:** `{prediction_value[0]:.2f}%`")
            st.info("Este valor representa el porcentaje estimado del % de la concentración de sílice despues del proceso de flotación.")
        except Exception as e:
            st.error(f"Ocurrió un error durante la predicción: {e}")
else:
    st.warning("El modelo no pudo ser cargado. Por favor, verifica la ruta del archivo del modelo.")

st.divider()

# --- Sección de Explicación ---
with st.expander("ℹ️ Sobre la Aplicación"):
    st.markdown("""
    **¿Cómo funciona?**

    1.  **Datos de Entrada:** Proporcionas los parámetros operativos clave usando los deslizadores en la barra lateral.
    2.  **Predicción:** El modelo de machine learning pre-entrenado recibe estas entradas y las analiza basándose en los patrones que aprendió de datos históricos.
    3.  **Resultado:** La aplicación muestra el % de la concentración de sílice estimado.
    """)

    st.markdown("""

    **Detalles del Modelo:**

    * **Tipo de Modelo:** `Regression Model` (XGBoost Optimizado)
    * **Propósito:** Predecir el valor continuo del rendimiento de la destilación.
    * **Características Usadas:** Caudal de Amina, Flujo de aire en la columna de flotación 01 y % de Hierro Concentrado.
    * **Fuente de Datos:** Utilizan
    """)
