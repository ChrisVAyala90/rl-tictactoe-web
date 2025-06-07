import { useState, useCallback } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const useAPI = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const request = useCallback(async (method, url, data = null) => {
    setLoading(true);
    setError(null);

    try {
      const response = await api.request({
        method,
        url,
        data,
      });
      return response.data;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'An error occurred';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  // Game API methods
  const getDifficulties = useCallback(() => {
    return request('GET', '/game/difficulties');
  }, [request]);

  const startGame = useCallback((difficulty, gameSize = 3) => {
    return request('POST', '/game/start', {
      difficulty,
      game_size: gameSize,
    });
  }, [request]);

  const makeMove = useCallback((gameId, position) => {
    return request('POST', '/game/move', {
      game_id: gameId,
      position,
      player: 'O', // Human is always O
    });
  }, [request]);

  const endGame = useCallback((gameId) => {
    return request('DELETE', `/game/end/${gameId}`);
  }, [request]);

  const getGameStats = useCallback(() => {
    return request('GET', '/game/stats');
  }, [request]);

  const checkHealth = useCallback(() => {
    return request('GET', '/health');
  }, [request]);

  return {
    loading,
    error,
    setError,
    getDifficulties,
    startGame,
    makeMove,
    endGame,
    getGameStats,
    checkHealth,
  };
};