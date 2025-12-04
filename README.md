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

## 🧠 Entrenamiento del Modelo

El núcleo de Sentinel es un modelo de visión por computadora personalizado. El proceso de creación del dataset y entrenamiento siguió una metodología rigurosa para asegurar la precisión en la detección:

1.  **Recolección y Balanceo de Datos:**
    * Se recopiló un conjunto de imágenes centrado en entornos industriales.
    * Para evitar sesgos en el modelo, se realizó un **balanceo de clases exacto (50/50)**.
    * El dataset inicial consta de **130 imágenes** distribuidas equitativamente:
        * 👷 **65 imágenes** etiquetadas como `helmet` (con casco).
        * ⚠️ **65 imágenes** etiquetadas como `no-helmet` (sin casco).

2.  **Etiquetado y Preprocesamiento:**
    * Cada imagen fue inspeccionada y etiquetada manualmente utilizando la plataforma **[Roboflow](https://roboflow.com/)**, asegurando *bounding boxes* precisos para cada objeto.
    * Se generó un dataset estructurado y normalizado listo para ser ingerido por el algoritmo.

3.  **Entrenamiento:**
    * Se utilizó este dataset curado para realizar un *fine-tuning* sobre el modelo base YOLOv8.
    * **Resultados:** El modelo final demostró métricas de rendimiento muy favorables, logrando una alta confianza tanto en la detección de cumplimiento como de incumplimiento de la norma de seguridad.

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

## 👥 Autores

Desarrollado por Andrés Jaramillo y Max Delgado.
Sentinel © 2025.
