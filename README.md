# RL Tic-Tac-Toe Web Application

A modern web-based Tic-Tac-Toe game with AI opponents of varying difficulty levels. Built with React frontend and FastAPI backend, featuring rule-based AI that provides genuine strategic challenge.

## 🎯 Features

- **3 Difficulty Levels**: Easy, Medium, and Hard AI opponents
- **Rule-Based AI**: Simple but effective strategic play (no training required!)
- **Multiple Game Modes**: Classic 3×3 and Enhanced 4×4 with special cells
- **Modern UI**: Clean, responsive interface built with React and Tailwind CSS
- **Real-time Gameplay**: Instant AI responses with strategic positioning
- **Game Statistics**: Track wins, losses, and draws
- **Clean Codebase**: Simplified architecture focused on what works

## 🏗️ Architecture

### Frontend (React + Vite + Tailwind)
- **React 18** with modern hooks
- **Vite** for fast development and building
- **Tailwind CSS** for responsive styling
- **Lucide React** for icons

### Backend (FastAPI + Python)
- **FastAPI** for REST API
- **Python 3.8+** with type hints
- **Rule-based AI** with strategic logic
- **CORS enabled** for frontend integration

## 🚀 Quick Start

### Prerequisites
- **Node.js** 16+ and npm
- **Python** 3.8+
- **pip** for Python package management

### 1. Clone Repository
```bash
git clone <repository-url>
cd RL
```

### 2. Backend Setup
```bash
# Install Python dependencies
pip install fastapi uvicorn

# Start backend server
cd backend
python -m api.main
```
Backend will run on `http://localhost:8000`

### 3. Frontend Setup
```bash
# Install Node dependencies
cd frontend
npm install

# Start development server
npm run dev
```
Frontend will run on `http://localhost:3000`

### 4. Play!
Open your browser to `http://localhost:3000` and start playing!

## 🎮 How to Play

1. **Select Difficulty**:
   - **Easy**: 40% random moves (casual play)
   - **Medium**: 10% random moves (good challenge) 
   - **Hard**: 0% random moves (perfect strategic play)

2. **Choose Game Mode**:
   - **Classic 3×3**: Traditional tic-tac-toe
   - **Enhanced 4×4**: Larger board with special cells

3. **Make Your Move**: Click any empty cell to place your mark (X)

4. **AI Responds**: The AI will automatically make its move (O)

5. **Win Conditions**: Get 3 (or 4) in a row horizontally, vertically, or diagonally

## 🧠 AI Strategy

The AI uses a simple but effective rule-based approach:

1. **Win if possible** - Take any winning move immediately
2. **Block opponent wins** - Prevent human from winning
3. **Strategic positioning**:
   - Prefer center control (3×3)
   - Take corners when available
   - Fall back to edges only when necessary

Difficulty is controlled by introducing controlled randomness:
- **Easy**: Makes random moves 40% of the time
- **Medium**: Makes random moves 10% of the time  
- **Hard**: Always plays optimally (never loses, only wins or draws)

## 📁 Project Structure

```
RL/
├── backend/
│   ├── api/
│   │   ├── main.py              # FastAPI application
│   │   ├── simple_game_routes.py # Game API endpoints
│   │   └── models.py            # Pydantic models
│   └── models/
│       ├── simple_ai.py         # Rule-based AI implementation
│       └── game_engine.py       # Core game logic
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── DifficultySelector.jsx # Difficulty selection UI
│   │   │   ├── GameBoard.jsx          # Game board component
│   │   │   └── GameStats.jsx          # Statistics display
│   │   ├── hooks/
│   │   │   ├── useAPI.js             # API communication
│   │   │   └── useGameState.js       # Game state management
│   │   ├── utils/
│   │   │   └── gameLogic.js          # Game utilities
│   │   └── App.jsx               # Main application
│   ├── package.json
│   └── vite.config.js
├── README.md
└── .gitignore
```

## 🔧 API Endpoints

- `GET /game/difficulties` - Get available difficulty levels
- `POST /game/start` - Start a new game
- `POST /game/move` - Make a player move
- `GET /game/stats/{game_id}` - Get game statistics
- `POST /game/reset/{game_id}` - Reset game
- `DELETE /game/end/{game_id}` - End game

## 🛠️ Development

### Backend Development
```bash
cd backend
python -m api.main
# Server runs with auto-reload enabled
```

### Frontend Development  
```bash
cd frontend
npm run dev
# Vite provides hot module replacement
```

### Building for Production
```bash
# Frontend build
cd frontend
npm run build

# Backend can be deployed with uvicorn
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

## 🎯 Design Philosophy

This project demonstrates that **simple approaches often work best**:

- **Rule-based AI** over complex machine learning for deterministic games
- **Strategic positioning** with controlled randomness for difficulty levels
- **Clean, focused UI** that prioritizes user experience
- **Modern web technologies** for responsiveness and maintainability
- **Lean codebase** with minimal dependencies and maximum clarity

The AI is immediately ready (no training required) and provides genuine strategic challenge, especially on Hard difficulty where it plays perfectly. This project was cleaned of complex RL infrastructure to focus on what actually works.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🎉 Acknowledgments

- Built with modern web technologies for optimal performance
- Inspired by classic game theory and strategic play
- Designed for both casual players and competitive challenge