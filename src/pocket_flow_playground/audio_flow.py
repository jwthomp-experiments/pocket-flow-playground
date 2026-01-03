"""
Audio Input Flow - Phase 1 Implementation

This module implements the audio input pipeline for the AI companion system.
It includes:
1. Wake word detection
2. Audio recording
3. Audio preprocessing

All components are implemented as PocketFlow nodes and connected in a flow.
"""

from pocketflow import Flow
from .nodes import AudioInputNode, WakeWordDetectionNode, EndNode
from .logging_config import logger


class AudioInputFlow(Flow):
    """
    Flow for capturing audio input with wake word detection.
    
    This flow:
    1. Listens for wake word
    2. Captures audio when wake word is detected
    3. Stores audio data in shared state
    """
    
    def __init__(self):
        super().__init__()
        
        # Create nodes
        self.wake_word_node = WakeWordDetectionNode(
            wake_word="hey ai",
            sample_rate=16000,
            channels=1
        )
        self.audio_input_node = AudioInputNode(
            sample_rate=16000,
            channels=1
        )
        
        # Connect nodes
        # Wake word detection -> Audio recording -> End
        self.wake_word_node - "continue" >> self.audio_input_node
        self.wake_word_node - "listen" >> self.wake_word_node  # Self-loop for continuous listening
        self.audio_input_node - "continue" >> EndNode()
        self.audio_input_node - "error" >> self.wake_word_node  # Retry if error
        
        # Set start node
        self.start = self.wake_word_node
        
        logger.info("Audio input flow created")
    
    def run(self, shared):
        """
        Run the audio input flow.
        
        Args:
            shared: Shared state dictionary
            
        Returns:
            None
        """
        logger.info("Starting audio input flow...")
        super().run(shared)
        logger.info("Audio input flow completed")


# Create the audio input flow
audio_flow = AudioInputFlow()


if __name__ == "__main__":
    # Example usage
    shared = {}
    audio_flow.run(shared)
    
    # Print results
    if "audio_data" in shared and "raw_audio" in shared["audio_data"]:
        audio_data = shared["audio_data"]["raw_audio"]
        print(f"Audio captured: {audio_data.shape[0]} samples")
        print(f"Sample rate: {shared['audio_data']['sample_rate']} Hz")
        print(f"Channels: {shared['audio_data']['channels']}")
    else:
        print("No audio data captured")
