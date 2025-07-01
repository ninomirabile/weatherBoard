# 🌤️ WeatherBoard

**WeatherBoard** is a fullstack project designed to display real-time weather data through a modern React frontend and a FastAPI backend.  
It is structured to evolve from mock data to real-time communication via MQTT (Phase 2).

---

## 🧱 Architecture Overview

```
weatherboard/
├── frontend/        # React + Vite + Zustand + Tailwind
├── backend/         # FastAPI with typed endpoints and MQTT-ready
├── .github/         # GitHub Actions CI pipelines
├── community/       # CONTRIBUTING, LICENSE, etc.
└── cursor.prompt.md # Cursor AI project context
```

---

## 🔹 Phase 1 – Simulated Weather Data

- The backend provides weather data for predefined cities via REST API.
- The frontend fetches and displays this data in a responsive dashboard.
- Data is simulated (randomized) at each request.

---

## 🔸 Phase 2 – MQTT Integration

- External simulators will publish weather data via MQTT.
- The backend will subscribe to MQTT topics and serve real-time data.
- The frontend will consume the same REST interface (no change).

---

## 🚀 Tech Stack

| Layer     | Technology              |
|-----------|--------------------------|
| Frontend  | React 18, Vite, Zustand, Tailwind CSS |
| Backend   | FastAPI, Pydantic, MQTT (future) |
| CI/CD     | GitHub Actions           |
| Testing   | Vitest, Pytest           |
| DevOps    | Docker, docker-compose   |

---

## 📦 Features

- Modular frontend (Feature-Sliced Design)
- Typed REST endpoints
- CI pipelines for both frontend and backend
- Ready-to-integrate MQTT architecture
- Open Source–ready (community standards included)

---

## 📜 Usage

### 🖥️ Frontend
```
cd frontend
npm install
npm run dev
```

### 🐍 Backend
```
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## ✅ Community Standards

This project follows GitHub community standards:
- [x] LICENSE (MIT)
- [x] CONTRIBUTING.md
- [x] CODE_OF_CONDUCT.md
- [x] SECURITY.md

---

## 🤖 AI Development

The codebase is AI-friendly (Cursor, Copilot) with clear structure and typed interfaces.  
See `cursor.prompt.md` for project-wide architecture rules.

---

## 🧪 Tests

- Frontend: `npm run test`
- Backend: `pytest`

---

## 📡 MQTT Integration (Planned)

The backend will subscribe to:
```
/weather/milano
/weather/roma
/weather/london
```

And expose updated REST endpoints without breaking the frontend interface.

---

## 🛡️ License

MIT — see `LICENSE` file for details.
