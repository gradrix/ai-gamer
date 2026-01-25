#!/usr/bin/env python3

"""
Test script to validate the DQN fixes
"""

import sys
import os
import numpy as np

# Add the project root to Python path
sys.path.append('.')

from ai_agent.network.modelmanager import ModelManager, REWARD
from ai_agent.network.controller import Controller

def test_reward_system():
    """Test that the reward system is correctly fixed"""
    print("Testing reward system...")
    
    expected_rewards = {
        'INCORRECT': -10.0,
        'LOST': -1.0,
        'MOVED': 0.0,
        'DRAW': 0.5,
        'WON': 1.0
    }
    
    for key, expected_value in expected_rewards.items():
        actual_value = REWARD[key]
        assert actual_value == expected_value, f"Reward for {key} is {actual_value}, expected {expected_value}"
        print(f"✓ {key}: {actual_value} (correct)")
    
    print("✓ Reward system test passed!\n")

def test_model_manager_initialization():
    """Test that ModelManager initializes correctly with DQN"""
    print("Testing ModelManager initialization...")
    
    try:
        # Test with a new agent
        mm = ModelManager("test_agent")
        
        # Check that model exists
        assert mm.model is not None, "Model should be initialized"
        print("✓ Main model initialized")
        
        # Check that target model exists
        assert mm.target_model is not None, "Target model should be initialized"
        print("✓ Target model initialized")
        
        # Check that replay buffer exists
        assert mm.replay_buffer is not None, "Replay buffer should be initialized"
        print("✓ Replay buffer initialized")
        
        # Check epsilon initialization
        assert mm.epsilon == 1.0, f"Epsilon should be 1.0, got {mm.epsilon}"
        print("✓ Epsilon initialized correctly")
        
        print("✓ ModelManager initialization test passed!\n")
        
        # Clean up
        if os.path.exists(mm.model_file):
            os.remove(mm.model_file)
            
    except Exception as e:
        print(f"✗ ModelManager initialization test failed: {e}")
        raise

def test_controller_integration():
    """Test that Controller integrates properly with new ModelManager"""
    print("Testing Controller integration...")
    
    try:
        controller = Controller("test_controller")
        
        # Check that model manager is initialized
        assert controller.modelManager is not None, "ModelManager should be initialized"
        print("✓ ModelManager initialized in Controller")
        
        # Check that state tracking variables exist
        assert hasattr(controller, 'last_state'), "Controller should have last_state"
        assert hasattr(controller, 'current_state'), "Controller should have current_state"
        print("✓ State tracking variables exist")
        
        print("✓ Controller integration test passed!\n")
        
        # Clean up
        if os.path.exists(controller.modelManager.model_file):
            os.remove(controller.modelManager.model_file)
            
    except Exception as e:
        print(f"✗ Controller integration test failed: {e}")
        raise

def test_dqn_prediction():
    """Test that DQN prediction works"""
    print("Testing DQN prediction...")
    
    try:
        mm = ModelManager("test_prediction")
        
        # Create a simple test board (3x3)
        test_board = np.array([
            [0, 1, 0],
            [1, 0, 2],
            [2, 1, 0]
        ])
        
        # Create test moves
        test_moves = [[0, 0], [0, 2], [1, 1], [2, 2]]
        
        # Test prediction
        padded_board, padded_moves, prediction = mm.predict(test_board, test_moves)
        
        # Check that prediction is within valid range
        assert isinstance(prediction, int), f"Prediction should be int, got {type(prediction)}"
        assert prediction >= 0, f"Prediction should be >= 0, got {prediction}"
        print(f"✓ Prediction returned valid value: {prediction}")
        
        # Check that padded board has correct shape
        assert padded_board.shape == (1, 10, 10), f"Padded board should be (1, 10, 10), got {padded_board.shape}"
        print("✓ Board padding works correctly")
        
        print("✓ DQN prediction test passed!\n")
        
        # Clean up
        if os.path.exists(mm.model_file):
            os.remove(mm.model_file)
            
    except Exception as e:
        print(f"✗ DQN prediction test failed: {e}")
        raise

def test_replay_buffer():
    """Test that replay buffer works correctly"""
    print("Testing replay buffer...")
    
    try:
        mm = ModelManager("test_replay")
        
        # Test adding experiences
        test_state = [np.random.rand(1, 10, 10), np.random.rand(1, 1000)]
        test_next_state = [np.random.rand(1, 10, 10), np.random.rand(1, 1000)]
        
        mm.remember(test_state, 5, REWARD['MOVED'], test_next_state, False)
        
        assert len(mm.replay_buffer) == 1, f"Replay buffer should have 1 item, got {len(mm.replay_buffer)}"
        print("✓ Experience added to replay buffer")
        
        # Test sampling (should return all available if batch_size > buffer size)
        samples = mm.replay_buffer.sample(min(64, len(mm.replay_buffer)))
        assert len(samples) == 1, f"Should return all available samples, got {len(samples)}"
        print("✓ Replay buffer sampling works")
        
        print("✓ Replay buffer test passed!\n")
        
        # Clean up
        if os.path.exists(mm.model_file):
            os.remove(mm.model_file)
            
    except Exception as e:
        print(f"✗ Replay buffer test failed: {e}")
        raise

def main():
    """Run all tests"""
    print("=" * 50)
    print("AI-Gamer DQN Fixes Validation Tests")
    print("=" * 50)
    print()
    
    try:
        test_reward_system()
        test_model_manager_initialization()
        test_controller_integration()
        test_dqn_prediction()
        test_replay_buffer()
        
        print("=" * 50)
        print("🎉 ALL TESTS PASSED! 🎉")
        print("The DQN fixes are working correctly.")
        print("=" * 50)
        
    except Exception as e:
        print("=" * 50)
        print("❌ TESTS FAILED ❌")
        print(f"Error: {e}")
        print("=" * 50)
        sys.exit(1)

if __name__ == "__main__":
    main()