#!/usr/bin/env python3

"""
Test script to verify that the reward system fixes are working correctly.
"""

import sys
import os
import numpy as np

# Add the project root to Python path
sys.path.append('.')

from ai_agent.network.modelmanager import REWARD

def test_reward_system():
    """Test that the reward system has been fixed correctly."""
    print("Testing reward system...")
    
    # Test that rewards are now correctly oriented
    assert REWARD['INCORRECT'] < REWARD['LOST'] < REWARD['MOVED'] < REWARD['DRAW'] < REWARD['WON'], \
        "Rewards should be in order: INCORRECT < LOST < MOVED < DRAW < WON"
    
    # Test specific values
    assert REWARD['INCORRECT'] == -10.0, f"INCORRECT reward should be -10.0, got {REWARD['INCORRECT']}"
    assert REWARD['LOST'] == -1.0, f"LOST reward should be -1.0, got {REWARD['LOST']}"
    assert REWARD['MOVED'] == 0.0, f"MOVED reward should be 0.0, got {REWARD['MOVED']}"
    assert REWARD['DRAW'] == 0.5, f"DRAW reward should be 0.5, got {REWARD['DRAW']}"
    assert REWARD['WON'] == 1.0, f"WON reward should be 1.0, got {REWARD['WON']}"
    
    print("✅ Reward system test passed!")
    print(f"Current rewards: {REWARD}")

def test_model_manager_initialization():
    """Test that ModelManager can be initialized correctly."""
    print("\nTesting ModelManager initialization...")
    
    try:
        from ai_agent.network.modelmanager import ModelManager
        
        # Test initialization
        model_manager = ModelManager("test_agent")
        
        # Check that both models exist
        assert hasattr(model_manager, 'model'), "ModelManager should have a main model"
        assert hasattr(model_manager, 'target_model'), "ModelManager should have a target model"
        
        # Check that replay buffer exists
        assert hasattr(model_manager, 'replay_buffer'), "ModelManager should have a replay buffer"
        
        print("✅ ModelManager initialization test passed!")
        
    except Exception as e:
        print(f"❌ ModelManager initialization test failed: {e}")
        return False
    
    return True

def test_basic_prediction():
    """Test that the model can make basic predictions."""
    print("\nTesting basic prediction...")
    
    try:
        from ai_agent.network.modelmanager import ModelManager
        
        model_manager = ModelManager("test_agent")
        
        # Create a simple test board (3x3)
        test_board = [[0, 0, 0], [0, 1, 0], [0, 0, 2]]  # 0=empty, 1=X, 2=O
        test_moves = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]]
        
        # Test prediction
        padded_board, padded_moves, prediction = model_manager.predict(test_board, test_moves)
        
        # Check that prediction is valid
        assert isinstance(prediction, int), f"Prediction should be an integer, got {type(prediction)}"
        assert prediction >= 0, f"Prediction should be non-negative, got {prediction}"
        
        print(f"✅ Basic prediction test passed! Prediction: {prediction}")
        
    except Exception as e:
        print(f"❌ Basic prediction test failed: {e}")
        return False
    
    return True

def test_replay_buffer():
    """Test that the replay buffer works correctly."""
    print("\nTesting replay buffer...")
    
    try:
        from ai_agent.network.modelmanager import ReplayBuffer
        
        buffer = ReplayBuffer(max_size=10)
        
        # Test adding experiences
        for i in range(5):
            buffer.add((f"state_{i}", i, i * 0.1, f"next_state_{i}", i % 2 == 0))
        
        assert len(buffer) == 5, f"Buffer should have 5 items, got {len(buffer)}"
        
        # Test sampling
        sample = buffer.sample(3)
        assert len(sample) == 3, f"Sample should have 3 items, got {len(sample)}"
        
        # Test overflow
        for i in range(10):
            buffer.add((f"state_{i}", i, i * 0.1, f"next_state_{i}", i % 2 == 0))
        
        assert len(buffer) == 10, f"Buffer should be limited to max_size, got {len(buffer)}"
        
        print("✅ Replay buffer test passed!")
        
    except Exception as e:
        print(f"❌ Replay buffer test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Running AI-Gamer fixes verification tests...\n")
    
    # Run all tests
    test_reward_system()
    test_model_manager_initialization()
    test_basic_prediction()
    test_replay_buffer()
    
    print("\n🎉 All tests completed!")