# Melodic AI - Music Playlist Generator

Melodic AI is a full-stack web application that leverages artificial intelligence to curate personalized music playlists based on selected genres. It features a modern, responsive frontend built with Vue 3 and Tailwind CSS, and a robust Flask backend powered by Groq's LLM engine.

## 🚀 Features

- **AI-Powered Curation**: Instantly generates 5-song playlists using the Llama 3 model via Groq.
- **Modern UI/UX**: stylized interface with glassmorphism effects, smooth animations, and responsive design.
- **Interactive Experience**: Real-time loading states, valid toast notifications, and dynamic genre selection.
- **Robust Backend**: Python Flask API with error handling and consistent JSON response formatting.

## 🛠️ Technology Stack

### Frontend
- **Framework**: [Vue 3](https://vuejs.org/) (Composition API + TypeScript)
- **Build Tool**: [Vite](https://vitejs.dev/)
- **Styling**: [Tailwind CSS 4](https://tailwindcss.com/)
- **Icons**: [Lucide Vue](https://lucide.dev/)

### Backend
- **Framework**: [Flask](https://flask.palletsprojects.com/)
- **Language**: Python 3.12
- **AI Provider**: [Groq](https://groq.com/) (Llama-3.3-70b-versatile)
- **Utilities**: `flask-cors`, `pydantic`

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- **Node.js** (v18 or higher)
- **Python** (v3.12 recommended)

---

## ⚙️ Installation & Setup

### 1. Backend Setup (Server)

Navigate to the server directory and set up the Python environment.

```bash
# Go to server directory
cd server

# Create a virtual environment (Python 3.12)
py -3.12 -m venv venv

# Activate the virtual environment
# On Windows (PowerShell):
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

> **Note:** The Groq API key is currently configured in `app.py`. For production, ensure this is moved to a `.env` file.

### 2. Frontend Setup (Client)

Navigate to the client directory and install Node dependencies.

```bash
# Go to client directory
cd client/melodic

# Install dependencies
npm install
```

---

## 🏃‍♂️ Running the Application

You will need two terminal windows running simultaneously.

### Terminal 1: Start the Backend
```bash
cd server
# Ensure venv is activated
.\venv\Scripts\python app.py
```
The server will start at `http://127.0.0.1:5000`.

### Terminal 2: Start the Frontend
```bash
cd client/melodic
npm run dev
```
The application will launch at `http://localhost:5173`.

---

## 🔌 API Documentation

### Generate Playlist
Generates a curated list of songs based on the provided genre.

- **Endpoint**: `POST /api/generate-playlist`
- **Content-Type**: `application/json`
- **Request Body**:
  ```json
  {
    "genre": "Afrobeats"
  }
  ```
- **Success Response** (200 OK):
  ```json
  {
    "genre": "Afrobeats",
    "message": "Successfully generated 5 Afrobeats songs",
    "playlist": [
      {
        "artist": "Wizkid",
        "song": "Essence"
      },
      ...
    ]
  }
  ```

### Health Check
- **Endpoint**: `GET /api/health`
- **Response**: Returns status of the API.

---

## 📂 Project Structure

```
musical/
├── client/
│   └── melodic/
│       ├── src/
│       │   ├── App.vue        # Main application component
│       │   ├── main.ts        # Entry point
│       │   └── style.css      # Tailwind & global styles
│       ├── package.json
│       └── vite.config.ts
└── server/
    ├── app.py                 # Main Flask application & AI logic
    ├── requirements.txt       # Python dependencies
    └── venv/                  # Virtual environment
```
