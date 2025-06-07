import { useState, useEffect } from 'react'

const API_URL = 'http://127.0.0.1:8000'

function App() {
  const [gameId, setGameId] = useState(null)
  const [board, setBoard] = useState(Array(9).fill(' '))
  const [winner, setWinner] = useState(null)
  const [gameOver, setGameOver] = useState(false)
  const [isTraining, setIsTraining] = useState(false)
  const [isTrained, setIsTrained] = useState(false)
  const [qTableSize, setQTableSize] = useState(0)
  const [loading, setLoading] = useState(true)

  // Check training status on load
  useEffect(() => {
    checkStatus()
  }, [])

  // Ensure we start on training screen when not trained
  useEffect(() => {
    if (!loading && !isTrained) {
      setGameId(null)
      setBoard(Array(9).fill(' '))
      setWinner(null)
      setGameOver(false)
    }
  }, [loading, isTrained])

  const checkStatus = async () => {
    try {
      const response = await fetch(`${API_URL}/status`)
      const data = await response.json()
      setIsTrained(data.is_trained)
      setQTableSize(data.q_table_size)
    } catch (error) {
      console.error('Failed to check status:', error)
    } finally {
      setLoading(false)
    }
  }

  const startNewGame = async () => {
    try {
      const response = await fetch(`${API_URL}/start`, { method: 'POST' })
      const data = await response.json()
      
      setGameId(data.game_id)
      setBoard(data.board)
      setWinner(data.winner)
      setGameOver(data.game_over)
      setIsTrained(data.is_trained)
    } catch (error) {
      console.error('Failed to start game:', error)
    }
  }

  const makeMove = async (position) => {
    if (board[position] !== ' ' || gameOver) return

    try {
      const response = await fetch(`${API_URL}/move`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ game_id: gameId, position })
      })
      
      const data = await response.json()
      setBoard(data.board)
      setWinner(data.winner)
      setGameOver(data.game_over)
    } catch (error) {
      console.error('Failed to make move:', error)
    }
  }

  const trainAgent = async () => {
    setIsTraining(true)
    try {
      const response = await fetch(`${API_URL}/train`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ episodes: 1000000 })
      })
      
      const data = await response.json()
      setIsTrained(true)
      setQTableSize(data.q_table_size)
      alert(`Training completed! Q-table has ${data.q_table_size} entries.`)
    } catch (error) {
      console.error('Failed to train agent:', error)
      alert('Training failed. Please try again.')
    } finally {
      setIsTraining(false)
    }
  }

  const resetGame = async () => {
    if (!gameId) return
    
    try {
      const response = await fetch(`${API_URL}/reset/${gameId}`, { method: 'POST' })
      const data = await response.json()
      
      setBoard(data.board)
      setWinner(data.winner)
      setGameOver(data.game_over)
    } catch (error) {
      console.error('Failed to reset game:', error)
    }
  }

  const resetAI = async () => {
    if (confirm('This will delete the trained AI and return to the training screen. Are you sure?')) {
      try {
        const response = await fetch(`${API_URL}/reset_ai`, { method: 'POST' })
        const data = await response.json()
        
        // Reset all state to initial
        setGameId(null)
        setBoard(Array(9).fill(' '))
        setWinner(null)
        setGameOver(false)
        setIsTrained(false)
        setQTableSize(0)
        
        alert('AI has been reset. You can now train a new model.')
      } catch (error) {
        console.error('Failed to reset AI:', error)
        alert('Failed to reset AI. Please try again.')
      }
    }
  }

  const getStatusText = () => {
    if (gameOver) {
      if (winner === 'X') return "🎉 You Won!"
      if (winner === 'O') return "🤖 AI Won!"
      return "🤝 It's a Draw!"
    }
    return "Your turn! Click a cell to play."
  }

  const getStatusClass = () => {
    if (gameOver) {
      if (winner === 'X') return "status winning"
      if (winner === 'O') return "status losing"
      return "status draw"
    }
    return "status"
  }

  if (loading) {
    return (
      <div className="container">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading RL Tic-Tac-Toe...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="container">
      <div className="header">
        <h1 className="title">🤖 RL Tic-Tac-Toe</h1>
        <p className="subtitle">Play against a Q-Learning AI Agent</p>
      </div>

      {!isTrained && (
        <div className="game-card training-card">
          <h3>🧠 AI Training Required</h3>
          <p>The AI agent needs to be trained before you can play. This will take a few moments.</p>
          <div className="controls" style={{ marginTop: '1rem' }}>
            <button 
              className="btn btn-success"
              onClick={trainAgent}
              disabled={isTraining}
            >
              {isTraining ? 'Training...' : 'Train AI (1M episodes)'}
            </button>
          </div>
          {isTraining && (
            <div style={{ textAlign: 'center', marginTop: '1rem' }}>
              <div className="spinner"></div>
              <p>Training in progress... Please wait.</p>
            </div>
          )}
        </div>
      )}

      {isTrained && (
        <div className="game-card">
          <div style={{ textAlign: 'center', marginBottom: '1rem' }}>
            <span>🧠 AI Trained</span>
            <span className="trained-badge">{qTableSize.toLocaleString()} Q-values</span>
          </div>

          {!gameId ? (
            <div className="controls">
              <button className="btn btn-primary" onClick={startNewGame}>
                Start New Game
              </button>
            </div>
          ) : (
            <>
              <div className={getStatusClass()}>
                {getStatusText()}
              </div>

              <div className="board">
                {board.map((cell, index) => (
                  <button
                    key={index}
                    className={`cell ${cell.toLowerCase()} ${gameOver ? 'disabled' : ''}`}
                    onClick={() => makeMove(index)}
                    disabled={gameOver || cell !== ' '}
                  >
                    {cell !== ' ' ? cell : ''}
                  </button>
                ))}
              </div>

              <div className="controls">
                <button className="btn btn-primary" onClick={startNewGame}>
                  New Game
                </button>
                <button className="btn btn-secondary" onClick={resetAI} style={{ backgroundColor: '#ef4444' }}>
                  Reset AI
                </button>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  )
}

export default App