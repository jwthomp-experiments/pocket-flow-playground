"""
Test script for audio input flow
"""

import sys
sys.path.insert(0, '/Users/jwthomp/repos/github.com/jwthomp-experiments/pf/src')

from pocket_flow_playground.audio_flow import audio_flow

def test_audio_flow_structure():
    """Test the audio input flow structure"""
    print("Testing audio input flow structure...")
    
    # Check that the flow was created successfully
    assert audio_flow is not None, "Audio flow not created"
    print("✓ Audio flow created successfully")
    
    # Check that nodes exist
    assert hasattr(audio_flow, 'wake_word_node'), "Wake word node not found"
    assert hasattr(audio_flow, 'audio_input_node'), "Audio input node not found"
    print("✓ All nodes exist")
    
    # Check node types
    from pocket_flow_playground.nodes import WakeWordDetectionNode, AudioInputNode
    assert isinstance(audio_flow.wake_word_node, WakeWordDetectionNode), "Wake word node is not correct type"
    assert isinstance(audio_flow.audio_input_node, AudioInputNode), "Audio input node is not correct type"
    print("✓ All nodes are correct types")
    
    # Check start node
    assert hasattr(audio_flow, 'start_node'), "Start node not set"
    assert audio_flow.start_node == audio_flow.wake_word_node, "Start node is not wake word node"
    print("✓ Start node is correctly set")
    
    print("\n✓ All structure tests passed!")

def test_audio_flow_nodes():
    """Test the audio input flow nodes without running the actual flow"""
    print("\nTesting audio input flow nodes...")
    
    # Check wake word node configuration
    wake_node = audio_flow.wake_word_node
    assert wake_node.wake_word == "hey ai", "Wake word not set correctly"
    assert wake_node.sample_rate == 16000, "Sample rate not set correctly"
    assert wake_node.channels == 1, "Channels not set correctly"
    print("✓ Wake word node configuration correct")
    
    # Check audio input node configuration
    audio_node = audio_flow.audio_input_node
    assert audio_node.sample_rate == 16000, "Sample rate not set correctly"
    assert audio_node.channels == 1, "Channels not set correctly"
    print("✓ Audio input node configuration correct")
    
    print("\n✓ All node tests passed!")

if __name__ == "__main__":
    test_audio_flow_structure()
    test_audio_flow_nodes()
    print("\n✓ All tests passed!")
