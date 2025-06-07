from models.proper_rl_training import ProperRLTraining

print("Training Expert with Proper RL...")
trainer = ProperRLTraining()

# Train expert with proper curriculum
agent = trainer.train_proper_rl_agent(200000, 'expert', target_win_rate=0.3)

# Save the model  
agent.save_model('/Users/chrisvayala/RL/backend/models/model_checkpoints/expert_proper_rl.pkl')
print("Expert proper RL model saved!")