from models.proper_rl_training import ProperRLTraining

print("Testing proper RL training...")
trainer = ProperRLTraining()

# Quick test with fewer episodes
agent = trainer.train_proper_rl_agent(10000, 'test', target_win_rate=0.2)
print("Test completed!")