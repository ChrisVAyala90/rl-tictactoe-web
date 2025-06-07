import React, { useState, useEffect } from 'react';
import { AlertCircle, Wifi, WifiOff } from 'lucide-react';
import DifficultySelector from './components/DifficultySelector';
import GameBoard from './components/GameBoard';
import GameStats from './components/GameStats';
import { useGameState } from './hooks/useGameState';
import { GAME_STATES } from './utils/gameLogic';

const ConnectionStatus = ({ isConnected, onRetry }) => (
  <div className={`fixed top-4 right-4 z-50 flex items-center space-x-2 px-4 py-2 rounded-lg shadow-lg ${
    isConnected ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
  }`}>
    {isConnected ? (
      <>
        <Wifi className="w-4 h-4" />
        <span className="text-sm font-medium">Connected</span>
      </>
    ) : (
      <>
        <WifiOff className="w-4 h-4" />
        <span className="text-sm font-medium">Disconnected</span>
        <button
          onClick={onRetry}
          className="text-xs bg-red-200 hover:bg-red-300 px-2 py-1 rounded"
        >
          Retry
        </button>
      </>
    )}
  </div>
);

const ErrorBanner = ({ error, onDismiss }) => (
  <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
    <div className="flex items-start">
      <AlertCircle className="w-5 h-5 text-red-500 mr-3 mt-0.5" />
      <div className="flex-1">
        <h3 className="text-sm font-semibold text-red-800">Error</h3>
        <p className="text-sm text-red-700 mt-1">{error}</p>
      </div>
      <button
        onClick={onDismiss}
        className="text-red-500 hover:text-red-700 ml-3"
      >
        ×
      </button>
    </div>
  </div>
);

function App() {
  const [difficulties, setDifficulties] = useState(null);
  const [isConnected, setIsConnected] = useState(true);
  const [gameSize, setGameSize] = useState(3);
  
  const {
    gameState,
    board,
    gameSize: currentGameSize,
    specialCells,
    winner,
    difficulty,
    difficultyInfo,
    gameMessage,
    isAIThinking,
    gameStats,
    loading,
    error,
    setError,
    startGame,
    makeMove,
    resetGame,
    playAgain,
    getDifficulties,
    checkHealth,
  } = useGameState();

  // Check backend connection and load difficulties
  useEffect(() => {
    const initializeApp = async () => {
      try {
        // Check backend health
        await checkHealth();
        setIsConnected(true);
        
        // Load difficulties
        const difficultiesData = await getDifficulties();
        setDifficulties(difficultiesData);
      } catch (err) {
        console.error('Failed to initialize app:', err);
        setIsConnected(false);
      }
    };

    initializeApp();
  }, [checkHealth, getDifficulties]);

  // Handle connection retry
  const handleRetryConnection = async () => {
    try {
      await checkHealth();
      setIsConnected(true);
      const difficultiesData = await getDifficulties();
      setDifficulties(difficultiesData);
      setError(null);
    } catch (err) {
      setIsConnected(false);
    }
  };

  // Handle difficulty selection and game start
  const handleDifficultySelect = async (selectedDifficulty, selectedGameSize) => {
    try {
      await startGame(selectedDifficulty, selectedGameSize);
    } catch (err) {
      console.error('Failed to start game:', err);
    }
  };

  // Handle cell click in game
  const handleCellClick = async (position) => {
    try {
      await makeMove(position);
    } catch (err) {
      console.error('Failed to make move:', err);
    }
  };

  // Handle game size change
  const handleGameSizeChange = (size) => {
    setGameSize(size);
  };

  // Handle new game
  const handleNewGame = () => {
    resetGame();
  };

  // Handle play again
  const handlePlayAgain = () => {
    playAgain();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Connection Status */}
      <ConnectionStatus 
        isConnected={isConnected} 
        onRetry={handleRetryConnection} 
      />

      <div className="container mx-auto px-4 py-8">
        {/* Error Banner */}
        {error && (
          <ErrorBanner 
            error={error} 
            onDismiss={() => setError(null)} 
          />
        )}

        {/* Main Content */}
        {gameState === GAME_STATES.SETUP ? (
          <DifficultySelector
            onSelect={handleDifficultySelect}
            onSizeChange={handleGameSizeChange}
            difficulties={difficulties}
            loading={loading}
            error={!isConnected ? 'Cannot connect to backend server' : null}
          />
        ) : (
          <div className="space-y-8">
            {/* Game Board */}
            <GameBoard
              board={board}
              size={currentGameSize}
              onCellClick={handleCellClick}
              disabled={loading || !isConnected}
              specialCells={specialCells}
              winner={winner}
              difficulty={difficulty}
              difficultyInfo={difficultyInfo}
              gameMessage={gameMessage}
              isAIThinking={isAIThinking}
              onPlayAgain={handlePlayAgain}
              onNewGame={handleNewGame}
              gameState={gameState}
            />

            {/* Game Statistics */}
            <GameStats 
              stats={gameStats}
              className="max-w-2xl mx-auto"
            />
          </div>
        )}

        {/* Footer */}
        <footer className="text-center mt-12 text-gray-500 text-sm">
          <p>
            RL Tic-Tac-Toe - AI agents trained with Reinforcement Learning
          </p>
          <p className="mt-1">
            Choose different difficulty levels to play against AI with varying training experience
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;