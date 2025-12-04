Sentinel - Sistema de Detección de Cascos de Seguridad 👷‍♂️🛡️

Sentinel es una aplicación de visión por computadora basada en Inteligencia Artificial diseñada para monitorear y verificar el uso de equipos de protección personal (cascos) en entornos industriales en tiempo real.

🚀 Características

Detección en Tiempo Real: Utiliza modelos YOLOv8 para inferencia rápida.

Soporte Multi-fuente: Analiza imágenes estáticas, videos pregrabados y webcam en vivo.

Interfaz Moderna: Dashboard construido con Streamlit para una experiencia de usuario fluida.

Alertas Visuales: Indicadores claros de cumplimiento (Verde) e incumplimiento (Rojo).

🛠️ Tecnologías Utilizadas

Python 3.9+

Streamlit: Frontend interactivo.

YOLOv8 (Ultralytics): Motor de detección de objetos.

OpenCV & Pillow: Procesamiento de imágenes.

Streamlit-WebRTC: Gestión de streaming de video para navegadores.

📦 Instalación y Uso Local

Clonar el repositorio:

git clone [https://github.com/tu-usuario/sentinel-detector.git](https://github.com/tu-usuario/sentinel-detector.git)
cd sentinel-detector


Instalar dependencias:
Se recomienda usar un entorno virtual.

pip install -r requirements.txt


Ejecutar la aplicación:

streamlit run app.py


☁️ Despliegue

Este proyecto está listo para ser desplegado en servicios como AWS, Heroku o Streamlit Community Cloud. Asegúrate de incluir el archivo best.pt en el directorio raíz.

👥 Autores

Desarrollado por Andrés Jaramillo y Max Delgado.
SafetyAI Solutions © 2025.
