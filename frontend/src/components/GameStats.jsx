import React from 'react';
import { Trophy, Target, Users, TrendingUp } from 'lucide-react';

const StatCard = ({ icon: Icon, label, value, color = "text-blue-600" }) => (
  <div className="bg-white rounded-lg p-4 shadow-sm">
    <div className="flex items-center">
      <Icon className={`w-8 h-8 ${color} mr-3`} />
      <div>
        <p className="text-2xl font-bold text-gray-800">{value}</p>
        <p className="text-sm text-gray-600">{label}</p>
      </div>
    </div>
  </div>
);

const GameStats = ({ stats, className = "" }) => {
  const { gamesPlayed, wins, losses, draws } = stats;
  
  const winRate = gamesPlayed > 0 ? ((wins / gamesPlayed) * 100).toFixed(1) : 0;
  
  return (
    <div className={`space-y-4 ${className}`}>
      <h3 className="text-lg font-semibold text-gray-700 text-center">
        Your Performance
      </h3>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard
          icon={Users}
          label="Games Played"
          value={gamesPlayed}
          color="text-gray-600"
        />
        <StatCard
          icon={Trophy}
          label="Wins"
          value={wins}
          color="text-green-600"
        />
        <StatCard
          icon={Target}
          label="Losses"
          value={losses}
          color="text-red-600"
        />
        <StatCard
          icon={TrendingUp}
          label="Win Rate"
          value={`${winRate}%`}
          color="text-blue-600"
        />
      </div>
      
      {gamesPlayed > 0 && (
        <div className="bg-white rounded-lg p-4 shadow-sm">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>Wins</span>
            <span>Draws</span>
            <span>Losses</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3 flex overflow-hidden">
            <div
              className="bg-green-500 h-full"
              style={{ width: `${(wins / gamesPlayed) * 100}%` }}
            ></div>
            <div
              className="bg-yellow-500 h-full"
              style={{ width: `${(draws / gamesPlayed) * 100}%` }}
            ></div>
            <div
              className="bg-red-500 h-full"
              style={{ width: `${(losses / gamesPlayed) * 100}%` }}
            ></div>
          </div>
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>{wins}</span>
            <span>{draws}</span>
            <span>{losses}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default GameStats;