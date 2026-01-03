"""
Simple test for audio input node
"""

import sys
sys.path.insert(0, '/Users/jwthomp/repos/github.com/jwthomp-experiments/pf/src')

from pocket_flow_playground.nodes import AudioInputNode

def test_audio_input_node():
    """Test the audio input node"""
    print("Testing audio input node...")
    
    shared = {}
    node = AudioInputNode(sample_rate=16000, channels=1)
    
    try:
        # Run the node
        result = node.run(shared)
        
        # Check results
        if "audio_data" in shared and "raw_audio" in shared["audio_data"]:
            audio_data = shared["audio_data"]["raw_audio"]
            print(f"✓ Audio captured successfully: {audio_data.shape[0]} samples")
            print(f"✓ Sample rate: {shared['audio_data']['sample_rate']} Hz")
            print(f"✓ Channels: {shared['audio_data']['channels']}")
            return True
        else:
            print("✗ No audio data captured")
            return False
            
    except Exception as e:
        print(f"✗ Error during audio capture: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_audio_input_node()
    sys.exit(0 if success else 1)
