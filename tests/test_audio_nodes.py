"""Test audio nodes functionality"""
import pytest
import numpy as np
from pocket_flow_playground.nodes import AudioInputNode, WakeWordDetectionNode


def test_audio_input_node_prep():
    """Test that AudioInputNode prep initializes shared state correctly"""
    node = AudioInputNode()
    shared = {}
    
    result = node.prep(shared)
    
    assert result is None
    assert "audio_data" in shared
    assert shared["audio_data"]["sample_rate"] == 16000
    assert shared["audio_data"]["channels"] == 1
    assert shared["audio_data"]["chunks"] == []


def test_audio_input_node_post_success():
    """Test that AudioInputNode post handles successful audio capture"""
    node = AudioInputNode()
    shared = {
        "audio_data": {
            "chunks": [],
            "raw_audio": None
        }
    }
    prep_res = None
    exec_res = np.array([1.0, 2.0, 3.0])
    
    result = node.post(shared, prep_res, exec_res)
    
    assert result == "continue"
    assert shared["audio_data"]["raw_audio"] is exec_res


def test_audio_input_node_post_failure():
    """Test that AudioInputNode post handles failed audio capture"""
    node = AudioInputNode()
    shared = {"audio_data": {"chunks": []}}
    prep_res = None
    exec_res = None
    
    result = node.post(shared, prep_res, exec_res)
    
    assert result == "error"


def test_wake_word_detection_node_prep():
    """Test that WakeWordDetectionNode prep initializes shared state correctly"""
    node = WakeWordDetectionNode(wake_word="hey ai")
    shared = {}
    
    result = node.prep(shared)
    
    assert result is None
    assert "wake_word" in shared
    assert shared["wake_word"]["wake_word"] == "hey ai"
    assert not shared["wake_word"]["detected"]


def test_wake_word_detection_node_post_continue():
    """Test that WakeWordDetectionNode post returns continue when wake word detected"""
    node = WakeWordDetectionNode()
    shared = {}
    prep_res = None
    exec_res = True
    
    result = node.post(shared, prep_res, exec_res)
    
    assert result == "continue"


def test_wake_word_detection_node_post_listen():
    """Test that WakeWordDetectionNode post returns listen when no wake word"""
    node = WakeWordDetectionNode()
    shared = {}
    prep_res = None
    exec_res = False
    
    result = node.post(shared, prep_res, exec_res)
    
    assert result == "listen"


def test_wake_word_detection_energy_calculation():
    """Test energy calculation in WakeWordDetectionNode"""
    node = WakeWordDetectionNode()
    
    # Create test audio data
    audio_data = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
    
    energy = node._calculate_energy(audio_data)
    
    # Expected energy: (0.1^2 + 0.2^2 + 0.3^2 + 0.4^2 + 0.5^2) / 5
    expected_energy = (0.01 + 0.04 + 0.09 + 0.16 + 0.25) / 5
    assert abs(energy - expected_energy) < 1e-10


def test_wake_word_detection_threshold():
    """Test wake word detection threshold"""
    node = WakeWordDetectionNode()
    
    # Low energy audio (should not detect)
    low_energy_audio = np.array([0.01, 0.02, 0.01])
    assert not node._detect_wake_word(low_energy_audio)
    
    # High energy audio (should detect)
    high_energy_audio = np.array([0.1, 0.2, 0.3])
    assert node._detect_wake_word(high_energy_audio)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
