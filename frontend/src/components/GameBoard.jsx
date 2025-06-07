import React from 'react';
import { Bot, User, Sparkles } from 'lucide-react';
import { PLAYERS, getWinningLine, getGameResultMessage, getGameResultColor } from '../utils/gameLogic';

const GameCell = ({ 
  value, 
  onClick, 
  disabled, 
  isSpecial, 
  isWinning, 
  position,
  size 
}) => {
  const getCellContent = () => {
    if (value === 'X/O') {
      return (
        <div className="relative">
          <Sparkles className="w-8 h-8 text-purple-500" />
          <span className="absolute -top-1 -right-1 text-xs font-bold text-purple-600">
            X/O
          </span>
        </div>
      );
    }
    return value === ' ' ? '' : value;
  };

  const getCellClasses = () => {
    let classes = `game-cell ${size === 3 ? 'h-20 md:h-24' : 'h-16 md:h-20'} text-2xl md:text-3xl`;
    
    if (disabled) {
      classes += ' cursor-not-allowed bg-gray-100';
    } else if (value === ' ') {
      classes += ' hover:bg-blue-50 hover:shadow-md';
    }
    
    if (isSpecial && value === 'X/O') {
      classes += ' bg-purple-50 border-purple-300';
    }
    
    if (isWinning) {
      classes += ' bg-green-100 border-green-400 shadow-lg';
    }
    
    if (value === PLAYERS.HUMAN) {
      classes += ' text-blue-600';
    } else if (value === PLAYERS.AI) {
      classes += ' text-red-600';
    }
    
    return classes;
  };

  return (
    <button
      className={getCellClasses()}
      onClick={() => onClick(position)}
      disabled={disabled || value !== ' '}
      aria-label={`Cell ${position + 1}`}
    >
      <div className="animate-bounce-in">
        {getCellContent()}
      </div>
    </button>
  );
};

const GameBoard = ({ 
  board, 
  size, 
  onCellClick, 
  disabled, 
  specialCells = [],
  winner,
  difficulty,
  difficultyInfo,
  gameMessage,
  isAIThinking,
  onPlayAgain,
  onNewGame,
  gameState
}) => {
  const winningLine = getWinningLine(board, size, winner);
  
  const getBoardClasses = () => {
    const baseClasses = "mx-auto gap-2 p-4 bg-gray-50 rounded-xl shadow-inner";
    if (size === 3) {
      return `${baseClasses} grid-cols-3 max-w-sm`;
    } else {
      return `${baseClasses} grid-cols-4 max-w-md`;
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      {/* Game Header */}
      <div className="text-center mb-6">
        <div className="flex items-center justify-center mb-4">
          <User className="w-6 h-6 text-blue-600 mr-2" />
          <span className="text-lg font-semibold text-gray-700">You (O)</span>
          <span className="mx-4 text-gray-400">vs</span>
          <Bot className="w-6 h-6 text-red-600 mr-2" />
          <span className="text-lg font-semibold text-gray-700">
            AI ({difficulty}) (X)
          </span>
        </div>
        
        {difficultyInfo && (
          <div className="bg-white rounded-lg p-3 shadow-sm">
            <p className="text-sm text-gray-600">{difficultyInfo.description}</p>
            <p className="text-xs text-gray-500 mt-1">
              Trained on {difficultyInfo.episodes?.toLocaleString()} episodes
            </p>
          </div>
        )}
      </div>

      {/* Game Status */}
      <div className="text-center mb-6">
        <div className={`text-lg font-semibold ${getGameResultColor(winner)}`}>
          {gameMessage}
        </div>
        
        {isAIThinking && (
          <div className="flex items-center justify-center mt-2">
            <Bot className="w-5 h-5 text-red-500 animate-pulse mr-2" />
            <span className="text-sm text-gray-600">AI is thinking...</span>
            <div className="ml-2 flex space-x-1">
              <div className="w-2 h-2 bg-red-500 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-red-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
              <div className="w-2 h-2 bg-red-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
            </div>
          </div>
        )}
      </div>

      {/* Special Cells Info for 4x4 */}
      {size === 4 && specialCells.length > 0 && (
        <div className="bg-purple-50 border border-purple-200 rounded-lg p-3 mb-6">
          <div className="flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-purple-600 mr-2" />
            <span className="text-sm text-purple-700 font-medium">
              Special cells (X/O) count for both players
            </span>
          </div>
        </div>
      )}

      {/* Game Board */}
      <div className={`grid ${getBoardClasses()}`}>
        {board.map((cell, index) => (
          <GameCell
            key={index}
            value={cell}
            position={index}
            size={size}
            onClick={onCellClick}
            disabled={disabled || isAIThinking}
            isSpecial={specialCells.includes(index)}
            isWinning={winningLine.includes(index)}
          />
        ))}
      </div>

      {/* Game Controls */}
      <div className="text-center mt-6 space-y-3">
        {gameState === 'finished' && (
          <div className="space-x-4">
            <button
              onClick={onPlayAgain}
              className="btn-primary px-6 py-3"
            >
              Play Again
            </button>
            <button
              onClick={onNewGame}
              className="btn-secondary px-6 py-3"
            >
              Change Difficulty
            </button>
          </div>
        )}
        
        {gameState === 'playing' && (
          <button
            onClick={onNewGame}
            className="btn-secondary px-4 py-2"
          >
            New Game
          </button>
        )}
      </div>

      {/* Game Legend */}
      <div className="mt-8 bg-white rounded-lg p-4 shadow-sm">
        <h3 className="text-sm font-semibold text-gray-700 mb-3">Game Legend:</h3>
        <div className="grid grid-cols-2 gap-4 text-xs">
          <div className="flex items-center">
            <div className="w-8 h-8 border-2 border-gray-300 rounded-lg flex items-center justify-center text-blue-600 font-bold mr-2">
              O
            </div>
            <span className="text-gray-600">Your moves</span>
          </div>
          <div className="flex items-center">
            <div className="w-8 h-8 border-2 border-gray-300 rounded-lg flex items-center justify-center text-red-600 font-bold mr-2">
              X
            </div>
            <span className="text-gray-600">AI moves</span>
          </div>
          {size === 4 && (
            <>
              <div className="flex items-center">
                <div className="w-8 h-8 border-2 border-purple-300 rounded-lg bg-purple-50 flex items-center justify-center mr-2">
                  <Sparkles className="w-4 h-4 text-purple-500" />
                </div>
                <span className="text-gray-600">Special cells</span>
              </div>
              <div className="flex items-center">
                <div className="w-8 h-8 border-2 border-green-400 rounded-lg bg-green-100 flex items-center justify-center text-green-600 font-bold mr-2">
                  ✓
                </div>
                <span className="text-gray-600">Winning line</span>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default GameBoard;