// Game logic utilities

export const GAME_STATES = {
  SETUP: 'setup',
  PLAYING: 'playing',
  FINISHED: 'finished'
};

export const PLAYERS = {
  HUMAN: 'O',
  AI: 'X'
};

export const DIFFICULTY_LEVELS = {
  easy: {
    name: 'Easy',
    color: 'bg-blue-500',
    episodes: 0,
    description: 'Casual play - makes some mistakes',
    winRate: '60% random'
  },
  medium: {
    name: 'Medium',
    color: 'bg-yellow-500',
    episodes: 0,
    description: 'Good challenge - plays strategically',
    winRate: '10% random'
  },
  hard: {
    name: 'Hard',
    color: 'bg-red-500',
    episodes: 0,
    description: 'Expert level - perfect play',
    winRate: 'Perfect play'
  }
};

export const formatNumber = (num) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M';
  } else if (num >= 1000) {
    return (num / 1000).toFixed(0) + 'K';
  }
  return num.toString();
};

export const getCellValue = (board, index, size) => {
  return board[index] || ' ';
};

export const isValidMove = (board, index) => {
  return board[index] === ' ';
};

export const getBoardDisplay = (board, size) => {
  const rows = [];
  for (let i = 0; i < size; i++) {
    const row = [];
    for (let j = 0; j < size; j++) {
      const index = i * size + j;
      row.push(board[index] || ' ');
    }
    rows.push(row);
  }
  return rows;
};

export const getWinningLine = (board, size, winner) => {
  if (!winner || winner === 'draw') return [];
  
  const lines = [];
  
  // Rows
  for (let i = 0; i < size; i++) {
    const row = [];
    for (let j = 0; j < size; j++) {
      row.push(i * size + j);
    }
    lines.push(row);
  }
  
  // Columns
  for (let i = 0; i < size; i++) {
    const col = [];
    for (let j = 0; j < size; j++) {
      col.push(j * size + i);
    }
    lines.push(col);
  }
  
  // Diagonals
  const diag1 = [];
  const diag2 = [];
  for (let i = 0; i < size; i++) {
    diag1.push(i * size + i);
    diag2.push(i * size + (size - 1 - i));
  }
  lines.push(diag1);
  lines.push(diag2);
  
  // Check which line is winning
  for (const line of lines) {
    const isWinning = line.every(index => {
      const cell = board[index];
      return cell === winner || cell === 'X/O';
    });
    
    if (isWinning) {
      return line;
    }
  }
  
  return [];
};

export const getGameResultMessage = (winner, isHuman) => {
  if (!winner) {
    return "It's a draw! 🤝";
  } else if (winner === PLAYERS.HUMAN) {
    return "Congratulations! You won! 🎉";
  } else {
    return "AI wins! Better luck next time! 🤖";
  }
};

export const getGameResultColor = (winner) => {
  if (!winner) {
    return "text-yellow-600";
  } else if (winner === PLAYERS.HUMAN) {
    return "text-green-600";
  } else {
    return "text-red-600";
  }
};