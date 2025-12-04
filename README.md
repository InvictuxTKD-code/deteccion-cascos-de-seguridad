# Sentinel - Sistema de Detección de Cascos de Seguridad 👷‍♂️🛡️

**Sentinel** es una aplicación de **visión por computadora** basada en **Inteligencia Artificial** diseñada para monitorear y verificar el uso de **Equipos de Protección Personal (EPP)**, específicamente **cascos de seguridad**, en entornos industriales en **tiempo real**.

---

## 🚀 Características Principales

* **Detección en Tiempo Real:** Utiliza modelos **YOLOv8** para una inferencia rápida y precisa.
* **Soporte Multi-fuente:** Capaz de analizar **imágenes estáticas**, **videos pregrabados** y **webcam en vivo**.
* **Interfaz Moderna:** **Dashboard** intuitivo y de fácil uso construido con **Streamlit** para una experiencia de usuario fluida.
* **Alertas Visuales:** Proporciona indicadores claros de cumplimiento (**Verde**) e incumplimiento (**Rojo**) del uso del casco.

---

## 🛠️ Tecnologías Utilizadas

| Categoría | Tecnología | Propósito |
| :--- | :--- | :--- |
| **Backend** | Python 3.9+ | Lenguaje de programación principal. |
| **IA/Detección** | [YOLOv8 (Ultralytics)](https://docs.ultralytics.com/) | Motor de detección de objetos en tiempo real. |
| **Frontend/UI** | [Streamlit](https://streamlit.io/) | Construcción del dashboard interactivo. |
| **Procesamiento** | OpenCV & Pillow | Gestión y manipulación de imágenes y video. |
| **Streaming** | Streamlit-WebRTC | Gestión de streaming de video en directo para navegadores. |

---

## 📦 Instalación y Uso Local

Se recomienda enfáticamente el uso de un **entorno virtual** para aislar las dependencias del proyecto.

### Pasos

1.  **Clonar el repositorio:**

    ```bash
    git clone [https://github.com/tu-usuario/sentinel-detector.git](https://github.com/tu-usuario/sentinel-detector.git)
    cd sentinel-detector
    ```

2.  **Instalar dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Ejecutar la aplicación:**

    ```bash
    streamlit run app.py
    ```

    La aplicación se abrirá automáticamente en tu navegador web predeterminado.

---

## ☁️ Despliegue

Este proyecto está configurado para un despliegue sencillo en servicios de cloud como **AWS**, **Heroku** o **Streamlit Community Cloud**.

> **Nota Importante:** Asegúrate de incluir el archivo del modelo entrenado (`best.pt` o equivalente) en el directorio raíz antes de realizar el despliegue.

---

## 👥 Autores

Desarrollado por:

* **Andrés Jaramillo**
* **Max Delgado**

SafetyAI Solutions © 2025.
Este proyecto está listo para ser desplegado en servicios como AWS, Heroku o Streamlit Community Cloud. Asegúrate de incluir el archivo best.pt en el directorio raíz.

👥 Autores

Desarrollado por Andrés Jaramillo y Max Delgado.
SafetyAI Solutions © 2025.
