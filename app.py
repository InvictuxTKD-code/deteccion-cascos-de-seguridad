import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import cv2
import numpy as np
from ultralytics import YOLO
import tempfile
import os
import time
from PIL import Image, ImageOps  # Importamos ImageOps para corregir rotación

# ============================
# 1. CONFIGURACIÓN DE PÁGINA
# ============================
st.set_page_config(
    page_title="Sentinel - Detector de Cascos",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicializar estado de navegación
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Inicio"

def navigate_to(page):
    st.session_state.current_page = page

# Configuración por defecto del modelo (ya que se quitó el slider)
CONF_THRESHOLD = 0.5 

# ============================
# 2. ESTILOS CSS PERSONALIZADOS (MODERNO & AMIGABLE)
# ============================
st.markdown("""
<style>
    /* Importar fuente moderna 'Inter' */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    /* Variables de color para fácil mantenimiento */
    :root {
        --bg-color: #1a1c24;
        --card-bg: #252836;
        --text-primary: #ffffff;
        --text-secondary: #b0b3b8;
        --accent-color: #4F8BF9;
        --success-color: #00C851;
        --danger-color: #ff4444;
    }

    /* Aplicar fuente globalmente */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Fondo general más suave (Azul oscuro grisáceo) */
    [data-testid="stAppViewContainer"] {
        background-color: var(--bg-color);
    }
    
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }

    /* Títulos más grandes y limpios */
    h1 {
        color: var(--text-primary) !important;
        font-weight: 700;
        font-size: 3rem !important;
        padding-bottom: 1rem;
    }
    
    h2, h3 {
        color: var(--text-primary) !important;
        font-weight: 600;
    }
    
    /* Texto Justificado por defecto */
    p, label, .stMarkdown, div.stMarkdown {
        color: var(--text-secondary) !important;
        font-size: 1.1rem !important;
        line-height: 1.6;
        text-align: justify !important;
    }

    /* CLASE ESPECÍFICA PARA CENTRAR EN INICIO (SOBREESCRIBE LO ANTERIOR) */
    .home-center {
        text-align: center !important;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .home-center p, .home-center h3, .home-center li {
        text-align: center !important;
    }

    /* Tarjetas de métricas estilizadas y flotantes */
    div[data-testid="metric-container"] {
        background-color: var(--card-bg);
        border: none;
        padding: 20px;
        border-radius: 15px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
    }
    
    /* Estilo de las etiquetas de métricas */
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        font-size: 1rem !important;
    }
    [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-size: 2rem !important;
    }

    /* Botones de navegación más amigables */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: var(--card-bg);
        color: var(--text-primary);
        border: 1px solid #3a3f50;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: var(--accent-color);
        color: white;
        border-color: var(--accent-color);
        box-shadow: 0 5px 15px rgba(79, 139, 249, 0.4);
    }

    /* Imágenes con bordes suaves */
    img {
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }

    /* Footer integrado */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: var(--card-bg);
        color: var(--text-secondary);
        text-align: center;
        padding: 15px;
        font-size: 0.9rem;
        border-top: 1px solid #3a3f50;
        z-index: 100;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Ocultar el Sidebar completamente si no se usa */
    [data-testid="stSidebar"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# ============================
# 3. CARGA DEL MODELO (OPTIMIZADO)
# ============================
@st.cache_resource
def load_model(path):
    """Carga el modelo y lo guarda en caché para mejorar velocidad."""
    try:
        return YOLO(path)
    except Exception as e:
        st.error(f"Error cargando el modelo: {e}. Asegúrate de que 'best.pt' esté en la carpeta.")
        return None

# Cargar modelo (Asegúrate de tener best.pt)
model_path = "best.pt" 
# model_path = "yolov8n.pt" # Descomentar para pruebas si no tienes el modelo personalizado

model = load_model(model_path)

# ============================
# 4. PANEL DE CONTROL SUPERIOR
# ============================

# Título Principal "Sentinel"
st.markdown("""
    <div style="text-align: center; margin-top: 20px; margin-bottom: 30px;">
        <h1 style="font-size: 60px; font-weight: 800; color: #4F8BF9; margin-bottom: 0px;">Sentinel</h1>
        <h3 style="font-weight: 400; color: #b0b3b8; margin-top: 0px;">Sistema Inteligente de Detección de Cascos de Seguridad</h3>
    </div>
""", unsafe_allow_html=True)

col_nav1, col_nav2, col_nav3, col_nav4 = st.columns(4)

with col_nav1:
    if st.button("🏠 Inicio", key="nav_home"):
        navigate_to("Inicio")

with col_nav2:
    if st.button("🖼️ Analizar Imagen", key="nav_img"):
        navigate_to("Imagen")

with col_nav3:
    if st.button("🎬 Analizar Video", key="nav_vid"):
        navigate_to("Video")

with col_nav4:
    if st.button("📹 Cámara en Vivo", key="nav_cam"):
        navigate_to("Cámara")

st.markdown("---")

# ============================
# 5. PÁGINAS DE LA APP
# ============================

# --- PÁGINA DE INICIO ---
if st.session_state.current_page == "Inicio":
    
    # Aplicamos la clase .home-center para forzar el centrado del contenedor
    # Pero usamos text-align: justify !important para los párrafos de características e instrucciones
    st.markdown("""
<div class="home-center">
<h3 style="margin-bottom: 20px;">Bienvenido a Sentinel</h3>
<p style="max-width: 800px; margin: 0 auto 40px auto; text-align: center !important;">
Bienvenido al sistema de seguridad industrial asistido por <strong>Inteligencia Artificial</strong>. 
Esta plataforma ha sido diseñada para auditar y monitorear el cumplimiento de normas de seguridad, 
específicamente el uso de <strong>cascos de seguridad</strong>, en entornos laborales de manera eficiente y moderna.
</p>
<h3 style="margin-bottom: 20px;">Características Principales</h3>
<p style="max-width: 800px; margin: 0 auto 40px auto; text-align: justify !important;">
<strong>1. Detección Automática:</strong> Utiliza algoritmos de visión por computadora (YOLOv8) de última generación.<br>
<strong>2. Multi-formato:</strong> Para analizar fotografías estáticas, archivos de video y transmisiones en tiempo real.<br>
<strong>3. Reportes Inmediatos:</strong> Visualización clara de métricas de cumplimiento e incumplimiento.
</p>
<h3 style="margin-bottom: 20px;">Instrucciones</h3>
<p style="max-width: 800px; margin: 0 auto; text-align: justify !important;">
1. Utilice el <strong>Panel de Control</strong> superior para seleccionar el modo de trabajo.<br>
2. Cargue el archivo correspondiente o habilite su cámara web.<br>
3. Observe los resultados en pantalla. Las alertas rojas indican personas sin casco.
</p>
</div>
""", unsafe_allow_html=True)

    # El banner ahora se muestra debajo del texto, ocupando también el ancho completo
    st.markdown(
        """
<div style="background-color: #252836; padding: 40px; border-radius: 20px; text-align: center; margin-top: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
    <img src="https://cdn-icons-png.flaticon.com/512/1165/1165674.png" width="100" style="margin-bottom: 20px;">
    <h2 style="color: white; font-size: 28px; margin-bottom: 10px;">Sentinel Solutions</h2>
    <div style="font-size: 18px; color: #b0b3b8;">
        Tecnología al servicio de la prevención.<br><br>
        <span style="color: #00C851; font-weight: bold;">● Estado del Sistema: En Línea</span>
    </div>
</div>
""", unsafe_allow_html=True
    )

# --- PÁGINA DE IMAGEN ---
elif st.session_state.current_page == "Imagen":
    st.title("🖼️ Análisis de Imágenes")
    
    uploaded_file = st.file_uploader("Arrastre y suelte una imagen aquí", type=['jpg', 'png', 'jpeg'])
    
    if uploaded_file:
        col1, col2 = st.columns(2, gap="medium")
        
        # Leer imagen
        image = Image.open(uploaded_file)
        
        # --- CORRECCIÓN DE ORIENTACIÓN (EXIF) ---
        try:
            # Esto rota la imagen automáticamente según sus metadatos
            image = ImageOps.exif_transpose(image)
        except Exception:
            pass # Si falla o no tiene EXIF, continuamos con la original
            
        img_array = np.array(image)
        
        with col1:
            st.markdown("### Imagen Original")
            st.image(image, use_container_width=True)
            
        # Procesar
        with st.spinner('Analizando píxeles con IA...'):
            results = model.predict(img_array, conf=CONF_THRESHOLD)
            res_plotted = results[0].plot()
            
            # Contar clases
            classes = results[0].boxes.cls.cpu().numpy()
            n_helmet = np.sum(classes == 0)
            n_no_helmet = np.sum(classes == 1)
            
        with col2:
            st.markdown("### Resultado Detección")
            st.image(res_plotted, use_container_width=True)
            
        # Dashboard de resultados
        st.markdown("---")
        st.markdown("### 📊 Métricas del Análisis")
        m1, m2, m3 = st.columns(3)
        m1.metric("👥 Total Personas", int(len(classes)))
        
        m2.metric("✅ Con Casco", int(n_helmet), delta="Cumplimiento", delta_color="normal")
        m3.metric("⚠️ Sin Casco", int(n_no_helmet), delta="-Riesgo detectado", delta_color="inverse")

        if n_no_helmet > 0:
            st.error(f"🚨 **ALERTA:** Se han detectado {int(n_no_helmet)} personas sin casco de seguridad.")
        else:
            st.success("✅ **Zona Segura:** Todo el personal cuenta con casco.")

# --- PÁGINA DE VIDEO ---
elif st.session_state.current_page == "Video":
    st.title("🎬 Procesamiento de Video")
    
    video_file = st.file_uploader("Seleccione un archivo de video (MP4, AVI)", type=['mp4', 'avi'])
    
    if video_file:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(video_file.read())
        
        col1, col2 = st.columns([2, 1], gap="medium")
        with col1:
            st.markdown("### Video Original")
            st.video(tfile.name)
        with col2:
            st.markdown("### Estado del Proceso")
            st.info("ℹ️ El video se procesará cuadro por cuadro buscando cascos de seguridad.")
            if st.button("▶️ Iniciar Procesamiento"):
                
                # Configuración de video
                cap = cv2.VideoCapture(tfile.name)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                
                # Archivo temporal de salida
                output_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
                
                fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
                out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
                
                st_frame = st.empty()
                progress_bar = st.progress(0)
                
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                curr_frame = 0
                
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # Predicción
                    results = model.predict(frame, conf=CONF_THRESHOLD)
                    res_plotted = results[0].plot()
                    
                    out.write(res_plotted)
                    
                    frame_rgb = cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB)
                    st_frame.image(frame_rgb, caption=f"Procesando frame {curr_frame}/{total_frames}", use_container_width=True)
                    
                    curr_frame += 1
                    if total_frames > 0:
                        progress_bar.progress(curr_frame / total_frames)

                cap.release()
                out.release()
                
                st.success("🎉 Procesamiento finalizado con éxito.")
                
                try:
                    st.video(output_path)
                except:
                    st.warning("Formato de video no soportado por el navegador para previsualización directa.")
                
                with open(output_path, "rb") as f:
                    st.download_button("⬇️ Descargar Video Procesado", f, file_name="video_procesado.mp4")

# --- PÁGINA DE WEBCAM ---
elif st.session_state.current_page == "Cámara":
    st.title("📹 Monitoreo en Tiempo Real")
    st.write("El sistema analizará la transmisión de video en vivo buscando cascos de seguridad.")
    
    col_cam, col_stats = st.columns([3, 1], gap="large")
    
    with col_cam:
        class VideoProcessor(VideoTransformerBase):
            def __init__(self):
                self.model = model
                self.conf = CONF_THRESHOLD

            def transform(self, frame):
                img = frame.to_ndarray(format="bgr24")
                results = self.model.predict(img, conf=self.conf)
                annotated_frame = results[0].plot()
                return annotated_frame

        webrtc_streamer(
            key="safety-cam",
            video_processor_factory=VideoProcessor,
            media_stream_constraints={"video": True, "audio": False},
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
        )
    
    with col_stats:
        st.markdown("### Estado del Sistema")
        st.markdown("""
        <div style="text-align: center; padding: 20px; background-color: #252836; border-radius: 15px; border: 1px solid #3a3f50; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
            <div style="color: #00C851; font-weight: bold; font-size: 24px; margin-bottom: 5px;">● ACTIVO</div>
            <div style="font-size: 14px; color: #b0b3b8;">Monitoreo de Cascos</div>
            <hr style="border-color: #3a3f50; margin: 15px 0;">
            <div style="font-size: 12px; color: #888;">Latencia: < 100ms</div>
        </div>
        """, unsafe_allow_html=True)

# ============================
# FOOTER
# ============================
st.markdown("""
<div class="footer">
    © 2025 - Sentinel | Desarrollado por Andrés Jaramillo y Max Delgado.
</div>
""", unsafe_allow_html=True)