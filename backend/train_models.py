#!/usr/bin/env python3
"""
Training script for RL Tic-Tac-Toe models.
Run this script to train all difficulty levels for both 3x3 and 4x4 games.
"""

import sys
import os
import time

# Add the backend directory to Python path
sys.path.append(os.path.dirname(__file__))

from models.training_pipeline import TrainingPipeline

def main():
    print("🎮 RL Tic-Tac-Toe Model Training Pipeline")
    print("=" * 50)
    
    # Ask user which models to train
    print("\nSelect training option:")
    print("1. Train 3x3 models only")
    print("2. Train 4x4 models only") 
    print("3. Train both 3x3 and 4x4 models")
    print("4. Quick training (reduced episodes for testing)")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    force_retrain = input("Force retrain existing models? (y/N): ").strip().lower() == 'y'
    
    start_time = time.time()
    
    if choice == "1":
        train_3x3_models(force_retrain)
    elif choice == "2":
        train_4x4_models(force_retrain)
    elif choice == "3":
        train_3x3_models(force_retrain)
        train_4x4_models(force_retrain)
    elif choice == "4":
        quick_training(force_retrain)
    else:
        print("Invalid choice. Exiting.")
        return
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n🎉 Training completed in {total_time/60:.1f} minutes!")
    print("You can now start the API server and play against the trained agents.")

def train_3x3_models(force_retrain=False):
    """Train all difficulty levels for 3x3 Tic-Tac-Toe"""
    print("\n🎯 Training 3x3 Tic-Tac-Toe models...")
    pipeline = TrainingPipeline(game_size=3)
    pipeline.train_all_difficulties(force_retrain=force_retrain)
    print("✅ 3x3 models training completed!")

def train_4x4_models(force_retrain=False):
    """Train all difficulty levels for 4x4 Tic-Tac-Toe"""
    print("\n🎯 Training 4x4 Tic-Tac-Toe models...")
    pipeline = TrainingPipeline(game_size=4)
    pipeline.train_all_difficulties(force_retrain=force_retrain)
    print("✅ 4x4 models training completed!")

def quick_training(force_retrain=False):
    """Quick training with reduced episodes for testing"""
    print("\n⚡ Quick training mode (reduced episodes)...")
    
    # Temporarily modify training episodes for quick testing
    from models.training_pipeline import DIFFICULTY_LEVELS
    
    original_episodes = {}
    for difficulty in DIFFICULTY_LEVELS:
        original_episodes[difficulty] = DIFFICULTY_LEVELS[difficulty]["episodes"]
        DIFFICULTY_LEVELS[difficulty]["episodes"] = min(1000, DIFFICULTY_LEVELS[difficulty]["episodes"])
    
    try:
        train_3x3_models(force_retrain)
        # Uncomment if you want 4x4 in quick mode too
        # train_4x4_models(force_retrain)
    finally:
        # Restore original episode counts
        for difficulty in DIFFICULTY_LEVELS:
            DIFFICULTY_LEVELS[difficulty]["episodes"] = original_episodes[difficulty]
    
    print("✅ Quick training completed!")

if __name__ == "__main__":
    main()