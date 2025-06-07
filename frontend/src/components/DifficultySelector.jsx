import React, { useState, useEffect } from 'react';
import { Brain, Zap, Target, Trophy, Crown } from 'lucide-react';
import { DIFFICULTY_LEVELS, formatNumber } from '../utils/gameLogic';

const DifficultySelector = ({ onSelect, onSizeChange, difficulties, loading, error }) => {
  const [selectedDifficulty, setSelectedDifficulty] = useState('medium');
  const [selectedSize, setSelectedSize] = useState(3);
  const [availableDifficulties, setAvailableDifficulties] = useState({});

  useEffect(() => {
    if (difficulties && difficulties.difficulties) {
      setAvailableDifficulties(difficulties.difficulties);
    }
  }, [difficulties]);

  const getDifficultyIcon = (difficulty) => {
    const iconProps = { size: 24, className: "mx-auto mb-2" };
    switch (difficulty) {
      case 'easy': return <Zap {...iconProps} className="mx-auto mb-2 text-blue-600" />;
      case 'medium': return <Target {...iconProps} className="mx-auto mb-2 text-yellow-600" />;
      case 'hard': return <Crown {...iconProps} className="mx-auto mb-2 text-red-600" />;
      default: return <Brain {...iconProps} />;
    }
  };

  const getDifficultyColor = (difficulty) => {
    const colors = {
      easy: 'border-blue-300 hover:border-blue-500',
      medium: 'border-yellow-300 hover:border-yellow-500',
      hard: 'border-red-300 hover:border-red-500',
    };
    return colors[difficulty] || 'border-gray-300 hover:border-gray-500';
  };

  const getSelectedColor = (difficulty) => {
    const colors = {
      easy: 'border-blue-500 bg-blue-50',
      medium: 'border-yellow-500 bg-yellow-50',
      hard: 'border-red-500 bg-red-50',
    };
    return colors[difficulty] || 'border-gray-500 bg-gray-50';
  };

  const handleDifficultySelect = (difficulty) => {
    setSelectedDifficulty(difficulty);
  };

  const handleSizeChange = (size) => {
    setSelectedSize(size);
    onSizeChange(size);
  };

  const handleStartGame = () => {
    if (selectedDifficulty) {
      onSelect(selectedDifficulty, selectedSize);
    }
  };

  const getFilteredDifficulties = () => {
    const filtered = {};
    
    Object.keys(DIFFICULTY_LEVELS).forEach(key => {
      if (availableDifficulties[key]) {
        filtered[key] = {
          ...DIFFICULTY_LEVELS[key],
          trained: availableDifficulties[key].trained,
          episodes: availableDifficulties[key].episodes,
          description: availableDifficulties[key].description // Use backend description
        };
      }
    });
    
    return filtered;
  };

  if (loading) {
    return (
      <div className="text-center py-8">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Loading difficulty levels...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-600 font-semibold">Error loading difficulties</p>
          <p className="text-red-500 text-sm mt-1">{error}</p>
          <p className="text-gray-600 text-sm mt-2">
            Make sure the backend server is running and models are trained.
          </p>
        </div>
      </div>
    );
  }

  const filteredDifficulties = getFilteredDifficulties();

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-800 mb-2">
          RL Tic-Tac-Toe Challenge
        </h1>
        <p className="text-gray-600 text-lg">
          Choose your difficulty and test your skills against AI agents trained with different levels of experience
        </p>
      </div>

      {/* Game Size Selection */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-gray-700 mb-4 text-center">
          Select Game Mode
        </h2>
        <div className="flex justify-center space-x-4">
          <button
            onClick={() => handleSizeChange(3)}
            className={`px-6 py-3 rounded-lg border-2 transition-all duration-200 ${
              selectedSize === 3
                ? 'border-blue-500 bg-blue-50 text-blue-700'
                : 'border-gray-300 hover:border-blue-300 text-gray-700'
            }`}
          >
            <div className="text-center">
              <div className="font-semibold">Classic 3×3</div>
              <div className="text-sm opacity-75">Traditional Tic-Tac-Toe</div>
            </div>
          </button>
          <button
            onClick={() => handleSizeChange(4)}
            className={`px-6 py-3 rounded-lg border-2 transition-all duration-200 ${
              selectedSize === 4
                ? 'border-purple-500 bg-purple-50 text-purple-700'
                : 'border-gray-300 hover:border-purple-300 text-gray-700'
            }`}
          >
            <div className="text-center">
              <div className="font-semibold">Enhanced 4×4</div>
              <div className="text-sm opacity-75">With special cells</div>
            </div>
          </button>
        </div>
      </div>

      {/* Difficulty Selection */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-gray-700 mb-4 text-center">
          Choose AI Difficulty Level
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-3xl mx-auto">
          {Object.entries(filteredDifficulties).map(([key, info]) => (
            <div
              key={key}
              onClick={() => handleDifficultySelect(key)}
              className={`p-6 rounded-lg border-2 cursor-pointer transition-all duration-200 ${
                selectedDifficulty === key ? getSelectedColor(key) : getDifficultyColor(key)
              } ${!info.trained ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              <div className="text-center">
                {getDifficultyIcon(key)}
                <h3 className="font-bold text-lg mb-1">{info.name}</h3>
                <div className="text-sm text-gray-600 mb-2">
                  Rule-based AI
                </div>
                <p className="text-xs text-gray-500 mb-3 leading-tight">
                  {info.description}
                </p>
                <div className="text-xs font-semibold text-gray-700">
                  Strategy: {info.winRate || 'Strategic play'}
                </div>
                {!info.trained && (
                  <div className="mt-2 text-xs text-red-500 font-semibold">
                    Not Trained
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* AI Strategy Information */}
      {selectedDifficulty && filteredDifficulties[selectedDifficulty] && (
        <div className="mb-8 bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-4 text-center">
            Selected AI: {filteredDifficulties[selectedDifficulty].name}
          </h3>
          <div className="text-center">
            <p className="text-gray-600 mb-2">
              {filteredDifficulties[selectedDifficulty].description}
            </p>
            <p className="text-sm text-blue-600 font-semibold">
              Strategy: {filteredDifficulties[selectedDifficulty].winRate}
            </p>
          </div>
        </div>
      )}

      {/* Start Game Button */}
      <div className="text-center">
        <button
          onClick={handleStartGame}
          disabled={!selectedDifficulty || !filteredDifficulties[selectedDifficulty]?.trained}
          className={`px-8 py-4 rounded-lg font-semibold text-lg transition-all duration-200 ${
            selectedDifficulty && filteredDifficulties[selectedDifficulty]?.trained
              ? 'bg-blue-600 hover:bg-blue-700 text-white shadow-lg hover:shadow-xl transform hover:scale-105'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }`}
        >
          {selectedDifficulty 
            ? `Start Game vs ${filteredDifficulties[selectedDifficulty]?.name} AI`
            : 'Select Difficulty to Start'
          }
        </button>
        
        {selectedDifficulty && !filteredDifficulties[selectedDifficulty]?.trained && (
          <p className="text-red-500 text-sm mt-2">
            This difficulty level hasn't been trained yet. Please train the models first.
          </p>
        )}
      </div>
    </div>
  );
};

export default DifficultySelector;