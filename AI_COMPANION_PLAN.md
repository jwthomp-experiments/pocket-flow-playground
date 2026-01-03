# AI Companion System Plan

## Overview

This system will be a voice-based AI companion that:
1. Listens for voice input
2. Recognizes who is speaking
3. Converts speech to text with speaker identification metadata
4. Determines appropriate responses
5. Stores interaction history with metadata
6. Converts text responses to speech
7. Runs entirely locally using models with ≤24B parameters

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            AI Companion System                             │
├─────────────────┬─────────────────┬─────────────────┬─────────────────┬───────┤
│   Audio Input   │ Speaker ID      │ Speech-to-Text  │ AI Response     │ Text-  │
│  (Microphone)   │  (Voice Biometrics) │  (Whisper)      │  (Local LLM)    │ to-   │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┼ Speech │
│                 │                 │                 │                 │ (TTS) │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┴───────┘
```

## Component Breakdown

### 1. Audio Input Layer
- **Microphone Interface**: Capture audio in real-time
- **Wake Word Detection**: Trigger recording when specific phrase is detected (e.g., "Hey AI")
- **Audio Preprocessing**: Noise suppression, normalization, chunking
- **Target Models**: None (system component)

### 2. Speaker Identification
- **Voice Biometrics**: Identify speaker from voice characteristics
- **Speaker Embeddings**: Create unique voice signatures for each user
- **Target Models**:
  - SpeakerNet (2-5M parameters)
  - Resemblyzer (small footprint, good accuracy)

### 3. Speech-to-Text
- **Automatic Speech Recognition**: Convert speech to text
- **Speaker Metadata**: Attach speaker ID to transcribed text
- **Target Models**:
  - Whisper-tiny (39M parameters)
  - Whisper-base (74M parameters)
  - Local alternative: Coqui STT

### 4. AI Response Generation
- **Context Understanding**: Process conversation history
- **Response Generation**: Generate appropriate responses
- **Target Models**:
  - Llama 3 (8B or 16B parameters)
  - Mistral 7B
  - Phi-3 (3B parameters)
  - Local fine-tuned models

### 5. Interaction History Storage
- **Structured Storage**: JSON or SQLite database
- **Metadata Tracking**: Speaker ID, timestamp, confidence scores
- **Conversation Context**: Maintain context across sessions
- **Target Implementation**: SQLite database with schema for:
  - Conversations (ID, timestamp, participants)
  - Messages (ID, conversation_id, speaker_id, text, timestamp, confidence)
  - Speaker Profiles (ID, voice_embedings, name, preferences)

### 6. Text-to-Speech
- **Speech Synthesis**: Convert text to natural-sounding speech
- **Voice Customization**: Different voices for different speakers
- **Target Models**:
  - Coqui TTS (XTTS model, ~300M parameters - slightly over but essential)
  - VITS (smaller variants)
  - Local TTS alternatives

## Implementation Plan

### Phase 1: Core Infrastructure (2-3 weeks)

1. **Set up development environment**
   - Python 3.10+ with necessary libraries
   - ONNX runtime for model optimization
   - PyTorch/TensorFlow for model loading

2. **Audio pipeline**
   - Microphone capture with PyAudio/SoundDevice
   - Wake word detection using Porcupine or local keyword spotting
   - Audio preprocessing pipeline

3. **Speaker identification**
   - Implement Resemblyzer for speaker embeddings
   - Create speaker registration system
   - Build speaker verification pipeline

### Phase 2: Speech Processing (2-3 weeks)

1. **Speech-to-Text**
   - Integrate Whisper-tiny/base models
   - Implement speaker diarization (who spoke when)
   - Add speaker metadata to transcripts

2. **Text-to-Speech**
   - Integrate Coqui TTS or VITS
   - Implement voice selection and customization
   - Add prosody control for natural speech

### Phase 3: AI Core (3-4 weeks)

1. **Model selection and optimization**
   - Evaluate Llama 3, Mistral, and Phi-3 models
   - Implement quantization (4-bit/8-bit)
   - Add model caching and memory management

2. **Conversation system**
   - Implement prompt engineering for context
   - Build conversation history management
   - Add response filtering and safety checks

3. **Metadata integration**
   - Attach speaker info to LLM prompts
   - Implement personalized responses based on speaker
   - Add emotional tone detection and response

### Phase 4: Storage and Retrieval (1-2 weeks)

1. **Database design**
   - SQLite schema for conversations and messages
   - Indexing for fast retrieval
   - Backup and export functionality

2. **History management**
   - Context window management
   - Session continuity
   - Search and retrieval by speaker/timestamp

### Phase 5: Integration and Testing (2-3 weeks)

1. **End-to-end pipeline**
   - Connect all components
   - Implement error handling and retries
   - Add logging and monitoring

2. **Performance optimization**
   - Model loading/unloading
   - Memory management
   - Real-time processing optimization

3. **User testing**
   - Multi-speaker scenarios
   - Different audio environments
   - Various conversation types

## Technical Requirements

### Hardware Requirements

- **Minimum**: 8GB RAM, 256GB SSD, Intel i5 or equivalent
- **Recommended**: 16GB+ RAM, 512GB+ SSD, Intel i7/Ryzen 7 or better, NVIDIA GPU (optional for faster TTS)
- **Storage**: ~10-20GB for models and data

### Software Requirements

- Python 3.10+
- PyTorch/TensorFlow
- ONNX Runtime
- SQLite
- Audio libraries (SoundDevice, PyAudio)

### Model Selection (All ≤24B parameters)

1. **Speaker ID**: Resemblyzer (2-5M)
2. **STT**: Whisper-tiny (39M) or Whisper-base (74M)
3. **LLM**: Llama 3 8B or 16B, Mistral 7B, Phi-3 3B
4. **TTS**: Coqui TTS (XTTS, ~300M - slightly over but essential for quality)

## Data Flow

1. **Input**: Microphone captures audio
2. **Wake Word**: System wakes on trigger phrase
3. **Recording**: Audio recorded for 5-10 seconds
4. **Speaker ID**: Voice biometrics identify speaker
5. **STT**: Speech converted to text with speaker metadata
6. **Context**: Previous conversation loaded from database
7. **LLM**: Generates response based on context and speaker
8. **Storage**: Conversation saved with metadata
9. **TTS**: Response converted to speech
10. **Output**: Speech played through speakers

## Error Handling and Recovery

1. **Audio issues**: Retry recording, request clarification
2. **STT failures**: Fallback to manual input, ask for repetition
3. **LLM errors**: Generate safe default response, log error
4. **TTS failures**: Fallback to text display, log error
5. **Storage issues**: Local caching, retry on next run

## Privacy and Security

1. **Local-only processing**: No data leaves the device
2. **Encrypted storage**: SQLite with encryption
3. **Speaker privacy**: Voice embeddings stored locally only
4. **Data control**: Easy export/import and deletion

## Future Enhancements

1. **Model fine-tuning**: Customize responses for specific users
2. **Additional features**: Calendar integration, smart home control
3. **Multi-device sync**: Secure synchronization across devices
4. **Advanced TTS**: Emotional tone, voice cloning
5. **Better diarization**: Real-time speaker separation

## Project Timeline

- **Phase 1**: 2-3 weeks
- **Phase 2**: 2-3 weeks
- **Phase 3**: 3-4 weeks
- **Phase 4**: 1-2 weeks
- **Phase 5**: 2-3 weeks
- **Total**: 10-14 weeks
