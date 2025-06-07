import { useState, useCallback } from 'react';
import { useAPI } from './useAPI';
import { GAME_STATES, PLAYERS } from '../utils/gameLogic';

export const useGameState = () => {
  const [gameState, setGameState] = useState(GAME_STATES.SETUP);
  const [gameId, setGameId] = useState(null);
  const [board, setBoard] = useState([]);
  const [gameSize, setGameSize] = useState(3);
  const [specialCells, setSpecialCells] = useState([]);
  const [availableMoves, setAvailableMoves] = useState([]);
  const [currentPlayer, setCurrentPlayer] = useState(PLAYERS.HUMAN);
  const [winner, setWinner] = useState(null);
  const [difficulty, setDifficulty] = useState('');
  const [difficultyInfo, setDifficultyInfo] = useState({});
  const [gameMessage, setGameMessage] = useState('');
  const [isAIThinking, setIsAIThinking] = useState(false);
  const [gameStats, setGameStats] = useState({
    gamesPlayed: 0,
    wins: 0,
    losses: 0,
    draws: 0,
  });

  const api = useAPI();

  // Start a new game
  const startGame = useCallback(async (selectedDifficulty, size = 3) => {
    try {
      setGameState(GAME_STATES.PLAYING);
      setGameMessage('Starting game...');
      
      const response = await api.startGame(selectedDifficulty, size);
      
      setGameId(response.game_id);
      setBoard(response.board);
      setGameSize(response.size);
      setSpecialCells(response.special_cells || []);
      setAvailableMoves(response.available_moves);
      setDifficulty(response.difficulty);
      setDifficultyInfo(response.difficulty_info);
      setCurrentPlayer(PLAYERS.HUMAN);
      setWinner(null);
      setGameMessage('Your turn! Click a cell to make your move.');
      setIsAIThinking(false);
      
      return response;
    } catch (error) {
      setGameMessage(`Failed to start game: ${error.message}`);
      setGameState(GAME_STATES.SETUP);
      throw error;
    }
  }, [api]);

  // Make a move
  const makeMove = useCallback(async (position) => {
    // Simple validation
    if (gameState !== GAME_STATES.PLAYING || isAIThinking || !availableMoves.includes(position)) {
      return;
    }

    try {
      setIsAIThinking(true);
      setGameMessage('AI is thinking...');

      const response = await api.makeMove(gameId, position);

      if (!response.success) {
        setGameMessage(response.message);
        return;
      }

      // Update game state
      setBoard(response.board);
      setAvailableMoves(response.available_moves);

      if (response.game_over) {
        setGameState(GAME_STATES.FINISHED);
        setWinner(response.winner);
        setGameMessage(response.message);
        
        // Update stats
        setGameStats(prev => ({
          gamesPlayed: prev.gamesPlayed + 1,
          wins: prev.wins + (response.winner === PLAYERS.HUMAN ? 1 : 0),
          losses: prev.losses + (response.winner === PLAYERS.AI ? 1 : 0),
          draws: prev.draws + (!response.winner ? 1 : 0),
        }));
      } else {
        setGameMessage(response.message);
      }
    } catch (error) {
      setGameMessage(`Move failed: ${error.message}`);
    } finally {
      setIsAIThinking(false);
    }
  }, [gameState, isAIThinking, availableMoves, gameId, api]);

  // Reset to setup
  const resetGame = useCallback(() => {
    setGameState(GAME_STATES.SETUP);
    setGameId(null);
    setBoard([]);
    setGameSize(3);
    setSpecialCells([]);
    setAvailableMoves([]);
    setCurrentPlayer(PLAYERS.HUMAN);
    setWinner(null);
    setDifficulty('');
    setDifficultyInfo({});
    setGameMessage('');
    setIsAIThinking(false);
  }, []);

  // Play again
  const playAgain = useCallback(async () => {
    if (difficulty && gameSize) {
      await startGame(difficulty, gameSize);
    } else {
      resetGame();
    }
  }, [difficulty, gameSize, startGame, resetGame]);

  return {
    // Game state
    gameState,
    gameId,
    board,
    gameSize,
    specialCells,
    availableMoves,
    currentPlayer,
    winner,
    difficulty,
    difficultyInfo,
    gameMessage,
    isAIThinking,
    gameStats,
    
    // API state
    loading: api.loading,
    error: api.error,
    setError: api.setError,
    
    // Actions
    startGame,
    makeMove,
    resetGame,
    playAgain,
    
    // API methods
    getDifficulties: api.getDifficulties,
    checkHealth: api.checkHealth,
  };
};