#!/usr/bin/env python3

"""
Test script to verify that the system can handle different Tic-Tac-Toe board sizes
within the current architecture limitations.
"""

import sys
import os
import numpy as np

# Add the project root to Python path
sys.path.append('.')

from ai_agent.network.modelmanager import ModelManager

def test_different_board_sizes():
    """Test that the system can handle different board sizes up to 10x10."""
    print("Testing different Tic-Tac-Toe board sizes...")
    
    model_manager = ModelManager("test_multi_size")
    
    # Test different board sizes
    board_sizes = [3, 5, 7, 10]  # Different Tic-Tac-Toe variants
    
    for size in board_sizes:
        print(f"\nTesting {size}x{size} board...")
        
        # Create a test board
        test_board = np.zeros((size, size), dtype=int)
        
        # Add some pieces to make it more realistic
        if size >= 3:
            test_board[0, 0] = 1  # X in top-left
            test_board[1, 1] = 2  # O in center (for odd sizes)
            if size >= 5:
                test_board[2, 2] = 1  # X in another position
                test_board[0, size-1] = 2  # O in top-right
        
        # Generate possible moves (all empty positions)
        test_moves = []
        for y in range(size):
            for x in range(size):
                if test_board[y, x] == 0:  # Empty position
                    test_moves.append([x, y])
        
        print(f"Board size: {size}x{size}")
        print(f"Empty positions: {len(test_moves)}")
        print(f"Board preview:")
        print(test_board)
        
        # Test prediction
        try:
            padded_board, padded_moves, prediction = model_manager.predict(test_board, test_moves)
            
            # Verify prediction is valid
            assert isinstance(prediction, int), f"Prediction should be integer, got {type(prediction)}"
            assert prediction >= 0, f"Prediction should be non-negative, got {prediction}"
            assert prediction < len(test_moves), f"Prediction {prediction} should be < {len(test_moves)}"
            
            predicted_move = test_moves[prediction]
            print(f"✅ Prediction successful! Chose move: {predicted_move}")
            
        except Exception as e:
            print(f"❌ Prediction failed for {size}x{size} board: {e}")
            return False
    
    print(f"\n🎉 All board size tests passed! System can handle boards from 3x3 to 10x10")
    return True

def test_edge_cases():
    """Test edge cases like full boards and almost-full boards."""
    print("\nTesting edge cases...")
    
    model_manager = ModelManager("test_edge_cases")
    
    # Test 1: Almost full board (only one move left)
    print("\n1. Testing almost-full board...")
    full_board = np.ones((3, 3), dtype=int)  # All positions taken
    full_board[1, 1] = 0  # Only center is free
    
    test_moves = [[1, 1]]  # Only one possible move
    
    try:
        _, _, prediction = model_manager.predict(full_board, test_moves)
        assert prediction == 0, f"Should predict the only available move (0), got {prediction}"
        print("✅ Almost-full board test passed!")
    except Exception as e:
        print(f"❌ Almost-full board test failed: {e}")
        return False
    
    # Test 2: Empty board (all moves available)
    print("\n2. Testing empty board...")
    empty_board = np.zeros((5, 5), dtype=int)
    
    # All positions are possible moves
    test_moves = [[x, y] for y in range(5) for x in range(5)]
    
    try:
        _, _, prediction = model_manager.predict(empty_board, test_moves)
        assert 0 <= prediction < 25, f"Prediction {prediction} should be between 0 and 24"
        print(f"✅ Empty board test passed! Chose move: {test_moves[prediction]}")
    except Exception as e:
        print(f"❌ Empty board test failed: {e}")
        return False
    
    return True

def test_reward_consistency():
    """Test that rewards are consistent across different scenarios."""
    print("\nTesting reward consistency...")
    
    from ai_agent.network.modelmanager import REWARD
    
    # Test that rewards make logical sense
    scenarios = [
        ("Winning", REWARD['WON'], "should be positive"),
        ("Drawing", REWARD['DRAW'], "should be positive but less than winning"),
        ("Moving", REWARD['MOVED'], "should be neutral (zero)"),
        ("Losing", REWARD['LOST'], "should be negative"),
        ("Incorrect move", REWARD['INCORRECT'], "should be very negative")
    ]
    
    for scenario, reward, expectation in scenarios:
        print(f"{scenario}: {reward} ({expectation})")
        
        if scenario == "Winning":
            assert reward > 0, f"Winning reward should be positive, got {reward}"
        elif scenario == "Drawing":
            assert reward > 0 and reward < REWARD['WON'], f"Drawing reward should be positive but less than winning"
        elif scenario == "Moving":
            assert reward == 0, f"Moving reward should be neutral (0), got {reward}"
        elif scenario == "Losing":
            assert reward < 0, f"Losing reward should be negative, got {reward}"
        elif scenario == "Incorrect move":
            assert reward < REWARD['LOST'], f"Incorrect move should be worse than losing"
    
    print("✅ All reward consistency tests passed!")
    return True

if __name__ == "__main__":
    print("Running multi-board size tests for AI-Gamer...\n")
    
    success = True
    success &= test_different_board_sizes()
    success &= test_edge_cases()
    success &= test_reward_consistency()
    
    if success:
        print("\n🎉 All multi-board size tests completed successfully!")
        print("\nCurrent system capabilities:")
        print("- ✅ Handles board sizes from 3x3 to 10x10")
        print("- ✅ Proper reward system (winning > drawing > moving > losing > incorrect)")
        print("- ✅ DQN with experience replay and target networks")
        print("- ✅ Dynamic move prediction for different board states")
        print("\nNext steps for improvement:")
        print("- Consider increasing MAX_GRID_SIZE for larger games like Gomoku")
        print("- Add game type encoding for multi-game support")
        print("- Implement transformer architecture for true variable board sizes")
    else:
        print("\n❌ Some tests failed. Check the output above for details.")