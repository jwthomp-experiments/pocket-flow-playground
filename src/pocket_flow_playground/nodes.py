"""
Audio Input Node - Captures audio from microphone
"""

import re
import sounddevice as sd
import numpy as np
import queue
import time
from pocketflow import Node, Flow
from .logging_config import logger
from pocket_flow_playground.client_openai import call_llm


class AudioInputNode(Node):
    """
    Node that captures audio from microphone.

    This node:
    1. Initializes microphone stream
    2. Captures audio in chunks
    3. Stores audio data in shared state
    """

    def __init__(self, sample_rate=16000, channels=1, dtype="float32"):
        super().__init__()
        self.sample_rate = sample_rate
        self.channels = channels
        self.dtype = dtype
        self.stream = None  # type: sounddevice.InputStream | None
        self.audio_queue = queue.Queue()
        self.recording = False
        self.recording_thread = None
        self.blocksize = 1024  # Number of samples per block

    def prep(self, shared):
        """
        Prepare the audio stream.

        Args:
            shared: Shared state dictionary

        Returns:
            None
        """
        # Initialize audio data structure in shared state
        if "audio_data" not in shared:
            shared["audio_data"] = {
                "sample_rate": self.sample_rate,
                "channels": self.channels,
                "dtype": self.dtype,
                "chunks": [],
                "timestamp": None,
            }

        # Initialize microphone stream
        try:
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype=self.dtype,
                blocksize=self.blocksize,
                callback=self._audio_callback,
            )
            logger.info(
                f"Audio stream initialized: {self.sample_rate}Hz, {self.channels} channels"
            )
        except Exception as e:
            logger.error(f"Failed to initialize audio stream: {e}")
            raise

        return None

    def _audio_callback(self, indata, frames, time_info, status):
        """
        Callback function for audio stream.

        Args:
            indata: Audio data from microphone
            frames: Number of frames
            time_info: Time information
            status: Stream status
        """
        if self.recording:
            self.audio_queue.put(indata.copy())

    def exec(self, prep_res):
        """
        Execute audio capture.

        Args:
            prep_res: Result from prep()

        Returns:
            Audio data as numpy array
        """
        # Start recording
        self.recording = True
        logger.info("Starting audio capture...")

        # Clear previous audio data
        shared["audio_data"]["chunks"].clear()
        shared["audio_data"]["timestamp"] = time.time()

        # Start audio stream
        self.stream.start()  # type: ignore[attr-defined]

        # Record for a fixed duration (e.g., 5 seconds)
        record_duration = 5.0  # seconds
        start_time = time.time()

        while time.time() - start_time < record_duration and self.recording:
            # Check if we have audio data
            if not self.audio_queue.empty():
                audio_chunk = self.audio_queue.get()
                shared["audio_data"]["chunks"].append(audio_chunk)

            # Small sleep to prevent high CPU usage
            time.sleep(0.01)

        # Stop recording
        self.recording = False
        logger.info(
            f"Finished audio capture. Collected {len(shared['audio_data']['chunks'])} chunks."
        )

        # Stop audio stream
        self.stream.stop()  # type: ignore[attr-defined]

        # Combine all chunks into single array
        if shared["audio_data"]["chunks"]:
            audio_data = np.concatenate(shared["audio_data"]["chunks"], axis=0)
            return audio_data

        return None

    def post(self, shared, prep_res, exec_res):
        """
        Process the captured audio.

        Args:
            shared: Shared state dictionary
            prep_res: Result from prep()
            exec_res: Result from exec()

        Returns:
            Action string ("continue" or "error")
        """
        if exec_res is not None:
            # Audio captured successfully
            logger.info(f"Audio captured: {exec_res.shape[0]} samples")
            shared["audio_data"]["raw_audio"] = exec_res
            return "continue"
        else:
            # No audio captured
            logger.warning("No audio data captured")
            return "error"

    def cleanup(self):
        """Clean up resources."""
        if self.stream is not None:
            self.stream.close()
            logger.info("Audio stream closed")
        self.recording = False


class WakeWordDetectionNode(Node):
    """
    Node that listens for a wake word to trigger audio recording.

    This node:
    1. Continuously listens for audio
    2. Detects wake word using energy-based thresholding
    3. Triggers recording when wake word is detected
    """

    def __init__(
        self, wake_word="hey ai", sample_rate=16000, channels=1, dtype="float32"
    ):
        super().__init__()
        self.wake_word = wake_word.lower()
        self.sample_rate = sample_rate
        self.channels = channels
        self.dtype = dtype
        self.stream = None  # type: sounddevice.InputStream | None
        self.audio_queue = queue.Queue()
        self.listening = False
        self.blocksize = 1024
        self.wake_word_detected = False
        # Energy thresholds - these will need tuning based on environment
        self.energy_threshold = 0.01  # Adjust based on noise level
        self.silence_threshold = 0.001
        self.min_silence_duration = 0.5  # seconds

    def prep(self, shared):
        """
        Prepare the wake word detection stream.

        Args:
            shared: Shared state dictionary

        Returns:
            None
        """
        # Initialize wake word detection state
        if "wake_word" not in shared:
            shared["wake_word"] = {
                "detected": False,
                "timestamp": None,
                "wake_word": self.wake_word,
            }

        # Initialize microphone stream
        try:
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype=self.dtype,
                blocksize=self.blocksize,
                callback=self._audio_callback,
            )
            logger.info(
                f"Wake word detection stream initialized: {self.sample_rate}Hz, {self.channels} channels"
            )
            logger.info(f"Listening for wake word: '{self.wake_word}'")
        except Exception as e:
            logger.error(f"Failed to initialize wake word detection stream: {e}")
            raise

        return None

    def _audio_callback(self, indata, frames, time_info, status):
        """
        Callback function for audio stream.

        Args:
            indata: Audio data from microphone
            frames: Number of frames
            time_info: Time information
            status: Stream status
        """
        if self.listening:
            self.audio_queue.put(indata.copy())

    def _calculate_energy(self, audio_data):
        """
        Calculate energy of audio data.

        Args:
            audio_data: Audio data as numpy array

        Returns:
            Energy value
        """
        return np.sum(audio_data**2) / len(audio_data)

    def _detect_wake_word(self, audio_data):
        """
        Simple wake word detection based on audio energy.

        Args:
            audio_data: Audio data as numpy array

        Returns:
            True if wake word detected, False otherwise
        """
        energy = self._calculate_energy(audio_data)

        # Simple energy-based detection
        # Wake word detected if energy exceeds threshold
        if energy > self.energy_threshold:
            logger.info(f"High energy detected: {energy:.6f}")
            return True

        return False

    def exec(self, prep_res):
        """
        Execute wake word detection.

        Args:
            prep_res: Result from prep()

        Returns:
            True if wake word detected, False otherwise
        """
        # Start listening
        self.listening = True
        self.wake_word_detected = False
        logger.info(f"Listening for wake word: '{self.wake_word}'...")

        # Start audio stream
        self.stream.start()  # type: ignore[attr-defined]

        # Listen for wake word
        listen_duration = 30.0  # seconds (30 seconds timeout)
        start_time = time.time()
        silence_start_time = None

        while (
            time.time() - start_time < listen_duration and not self.wake_word_detected
        ):
            # Check if we have audio data
            if not self.audio_queue.empty():
                audio_chunk = self.audio_queue.get()

                # Detect wake word
                if self._detect_wake_word(audio_chunk):
                    # Wake word detected!
                    self.wake_word_detected = True
                    shared["wake_word"]["detected"] = True
                    shared["wake_word"]["timestamp"] = time.time()
                    logger.info(f"Wake word '{self.wake_word}' detected!")
                    break
                else:
                    # No wake word, check for silence
                    energy = self._calculate_energy(audio_chunk)
                    if energy < self.silence_threshold:
                        if silence_start_time is None:
                            silence_start_time = time.time()
                    else:
                        silence_start_time = None

                    # Check if we've been silent for too long
                    if (
                        silence_start_time is not None
                        and time.time() - silence_start_time > self.min_silence_duration
                    ):
                        logger.info(
                            "No speech detected for a while, continuing to listen..."
                        )
                        silence_start_time = None

            # Small sleep to prevent high CPU usage
            time.sleep(0.01)

        # Stop listening
        self.listening = False

        # Stop audio stream
        self.stream.stop()  # type: ignore[attr-defined]

        return self.wake_word_detected

    def post(self, shared, prep_res, exec_res):
        """
        Process wake word detection result.

        Args:
            shared: Shared state dictionary
            prep_res: Result from prep()
            exec_res: Result from exec()

        Returns:
            Action string ("continue" if wake word detected, "listen" otherwise)
        """
        if exec_res:
            # Wake word detected, continue to recording
            logger.info("Wake word detected, proceeding to audio capture")
            return "continue"
        else:
            # No wake word detected, keep listening
            logger.info("No wake word detected, continuing to listen")
            return "listen"

    def cleanup(self):
        """Clean up resources."""
        if self.stream is not None:
            self.stream.close()
            logger.info("Wake word detection stream closed")
        self.listening = False


class InputNode(Node):
    def prep(self, shared):
        # Initialize messages if this is the first run
        if "messages" not in shared:
            shared["messages"] = []
            logger.info("Welcome to the chat! Type 'exit' to end the conversation.")

        return None

    def exec(self, prep_res):
        # Get user input
        user_input = input("\nYou: ")

        # Check if user wants to exit
        if user_input.lower() == "exit":
            return None

        return user_input

    def post(self, shared, prep_res, exec_res):
        if exec_res is None:
            logger.info("Goodbye!")
            return "end"  # End the conversation

        # Add user message to history
        shared["messages"].append({"role": "user", "content": exec_res})

        # Loop back to continue the conversation
        return "continue"


class AnswerNode(Node):
    def prep(self, shared):
        """Prepare context for the LLM"""
        if not shared.get("messages"):
            return None

        # 1. Get the last 3 conversation pairs (or fewer if not available)
        recent_messages = (
            shared["messages"][-6:]
            if len(shared["messages"]) > 6
            else shared["messages"]
        )

        # 2. Add the retrieved relevant conversation if available
        context = []
        if shared.get("retrieved_conversation"):
            # Add a system message to indicate this is a relevant past conversation
            context.append(
                {
                    "role": "system",
                    "content": "The following is a relevant past conversation that may help with the current query:",
                }
            )
            context.extend(shared["retrieved_conversation"])
            context.append(
                {"role": "system", "content": "Now continue the current conversation:"}
            )

        # 3. Add the recent messages
        context.extend(recent_messages)

        return context

    def exec(self, prep_res):
        """Generate a response using the LLM"""
        if prep_res is None:
            return None

        # Call LLM with the context
        response = call_llm(prep_res)
        return response

    def post(self, shared, prep_res, exec_res):
        """Process the LLM response"""
        if prep_res is None or exec_res is None:
            return "end"  # End the conversation

        # Clean the response by removing <think> tags and their content
        cleaned_content = re.sub(
            r"<think>.*?</think>\n?", "", exec_res, flags=re.DOTALL
        )

        queue_name = self.params["queue_name"]
        # Log the assistant's response
        logger.info(f"{queue_name}: {cleaned_content}")

        # Add assistant message to history
        shared["messages"].append({"role": "assistant", "content": cleaned_content})
        shared["message"] = {"role": "assistant", "content": cleaned_content}

        # We only end if the user explicitly typed 'exit'
        # Even if last_question is set, we continue in interactive mode
        return "continue"


class EndNode(Node):
    """Node that handles flow termination.

    This node is used to mark the end of a flow execution.
    """

    pass


# Create the flow with self-loop
# input_node = InputNode()
answer_node = AnswerNode()

# input_node - "continue" >> answer_node  # Pass input to llm node
answer_node - "continue" >> EndNode()  # Call the LLM
# input_node - "end" >> EndNode()  # End the flow if user types 'exit'
answer_node - "end" >> EndNode()  # End the flow if LLM response is None

flow = Flow(start=answer_node)

flow.set_params({"queue_name": "Agent_1"})

# Start the chat
if __name__ == "__main__":
    shared = {}
    flow.run(shared)
