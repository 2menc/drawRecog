# 🎨 DrawRecog – Drawing Recognition App like Quick, Draw! 

![Java](https://img.shields.io/badge/Java-21+-orange.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Gradle](https://img.shields.io/badge/Gradle-9.2-02303A.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**DrawRecog** is a client-server desktop application for real-time sketch and drawing recognition trained on Google's famous *Quick, Draw!* dataset.

The graphical user interface (built with **Java Swing**) allows users to sketch on a digital canvas and send the image over TCP sockets to a **Python** backend server. The backend preprocesses the sketch, performs Deep Learning inference using **ONNX** models, and returns the predicted class along with its confidence percentage.

***the server uses .onnx models: also works on older machines***

---

## 📸 Key Features

- 🎨 **Interactive Canvas:** Draw, clear, and interact on a digital board in real time.
- ⚡ **TCP Socket Client-Server Architecture:** Low-level, optimized binary stream communication between Java and Python.
- 🧠 **Dynamic Multi-Model Switching:** Swap ONNX models on the fly (e.g., 20 or 99 classes) directly from the Swing GUI dropdown menu.
- 🌐 **Network-Ready (Tailscale / LAN):** Easily configurable for local execution or remote servers via environment variables (`.env`).
- 🛠️ **Built-In Dataset Scraper:** Integrated Python utility task to automatically download and process categories from the Quick, Draw! dataset.

---

## 🏗️ System Architecture

```
┌─────────────────────────┐                 ┌─────────────────────────┐
│     Java Swing Client   │                 │   Python Server (ML)    │
│                         │                 │                         │
│  - Launcher / GUI       │  TCP Sockets    │  - listener.py          │
│  - Controller           ├────────────────►│  - OpenCV Preprocessing │
│  - NetworkClient        │      (Port)     │  - ONNXRuntime Inference│
└─────────────────────────┘                 └─────────────────────────┘
```

1. **Client (Java):** Converts the drawn vector points into a binary `BufferedImage` and transmits the byte stream to the server.
2. **Server (Python):** Receives the byte stream, decodes the image via **OpenCV**, applies preprocessing (cropping, padding, resizing to 28x28, and color inversion), and executes inference via **ONNX Runtime**.
3. **Response:** The server sends back the predicted class name and confidence score, updating the Swing UI.

---

## 🛠️ Prerequisites

- **Java JDK** 21 or higher
- **Python** 3.10 or higher
- **Gradle** (included via Gradle Wrapper)

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/drawRecog.git
cd drawRecog
```

### 2. Set up the Python Virtual Environment
Create a virtual environment in the `v_env` folder and install the required dependencies:

```bash
# Create the virtual environment
python -m venv v_env

# Activate the virtual environment
# On Linux/macOS:
source v_env/bin/activate
# On Windows:
.\v_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables (`.env`)
Create a **`.env`** file in the root directory of the project to specify the ML server's IP or hostname.

## 🚀 Running the Application

You can manage the entire application lifecycle using **Gradle** commands:

### 1. Start the Python ML Server
In your terminal, start the Python socket listener:
```bash
./gradlew server
```
*(On Windows: `gradlew.bat server`)*

### 2. Start the Java Swing Client
In a second terminal window, launch the desktop client:
```bash
./gradlew client
```

### 3. Run the Dataset Scraper (Optional)
To download local PNG images for the categories configured in `datasetScrapeOptions.yaml`:
```bash
./gradlew scraper
```
*this project does not provide any cnn model creation utilities: only takes the dataset for nn training*

---


## 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.
