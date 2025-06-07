# RL Tic-Tac-Toe Web Application

A web-based Tic-Tac-Toe game featuring a Q-Learning AI agent trained through reinforcement learning. Built with React frontend and FastAPI backend, demonstrating practical machine learning implementation.

## 🎯 Features

- **Q-Learning AI Agent**: AI trained through 1M episodes of self-play
- **Real-time Gameplay**: Play against the trained RL agent
- **Modern UI**: Clean, responsive interface built with React
- **Training Visualization**: See Q-table size and training progress
- **Model Persistence**: Trained agents are saved and can be reused
- **Clean Architecture**: Streamlined codebase focused on RL fundamentals

## 🏗️ Architecture

### Frontend (React + Vite)
- **React 18** with modern hooks
- **Vite** for fast development and building
- **Clean CSS** for responsive styling

### Backend (FastAPI + Python)
- **FastAPI** for REST API
- **Python 3.8+** with type hints
- **Q-Learning Agent** with pickle persistence
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
cd backend
pip install -r requirements.txt

# Start backend server
python main.py
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

1. **Train the AI**: First time users need to train the Q-Learning agent (takes a few moments)

2. **Start Game**: Click "Start New Game" to begin playing

3. **Make Your Move**: Click any empty cell to place your mark (X)

4. **AI Responds**: The trained RL agent will automatically make its move (O)

5. **Win Conditions**: Get 3 in a row horizontally, vertically, or diagonally

6. **Reset Options**: Start new games or reset the AI to retrain from scratch

## 🧠 Q-Learning Implementation

The AI uses Q-Learning, a reinforcement learning algorithm:

1. **State Representation**: Board positions represented as tuples
2. **Action Selection**: Epsilon-greedy policy with exploration/exploitation
3. **Q-Value Updates**: Bellman equation for temporal difference learning
4. **Training Process**: 1M episodes of self-play with strategic opponents
5. **Model Persistence**: Q-table saved as pickle file for reuse

**Learning Parameters**:
- **Alpha (Learning Rate)**: 0.1
- **Gamma (Discount Factor)**: 0.9  
- **Epsilon (Exploration)**: Starts at 0.1, decays during training

## 📁 Project Structure

```
RL/
├── backend/
│   ├── main.py              # FastAPI application & API endpoints
│   ├── rl_game.py           # Q-Learning agent & game engine
│   ├── requirements.txt     # Python dependencies
│   └── models/
│       └── trained_agent.pkl # Saved Q-learning model
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React application
│   │   ├── main.jsx         # React entry point
│   │   └── index.css        # Styling
│   ├── index.html           # HTML template
│   ├── package.json         # Node dependencies
│   └── vite.config.js       # Vite configuration
├── README.md
└── docker-compose.yml       # Container orchestration
```

## 🔧 API Endpoints

- `GET /` - API status check
- `POST /start` - Start a new game session
- `POST /move` - Make a player move and get AI response
- `POST /train` - Train the Q-Learning agent
- `POST /reset/{game_id}` - Reset current game
- `POST /reset_ai` - Delete trained model and reset AI
- `GET /status` - Get training status and Q-table size

## 🛠️ Development

### Backend Development
```bash
cd backend
python main.py
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
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🎯 Design Philosophy

This project demonstrates **practical reinforcement learning implementation**:

- **Q-Learning fundamentals** - Core RL algorithm with clear implementation
- **Interactive training** - Users can see AI learning in real-time
- **Clean architecture** - Minimal dependencies, maximum educational value
- **Modern web technologies** for accessible ML demonstrations
- **Practical persistence** - Models saved and reusable across sessions

The implementation focuses on **understanding over complexity** - showing how Q-Learning works in practice rather than using black-box libraries. Perfect for learning RL concepts hands-on.

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
- Demonstrates practical reinforcement learning concepts
- Designed for educational understanding of Q-Learning algorithms
