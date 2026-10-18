# 🛡️ Aegis: Zero-Trust AI Security Proxy

Aegis is a secure middleware terminal designed to prevent sensitive data leaks (Data Loss Prevention) when interacting with Large Language Models. 

## Core Architecture
- **Local Data Interception:** Uses a low-level, native C-shared library (`.dylib`) to cryptographically mask sensitive data locally.
- **Zero-Trust Delivery:** The LLM API receives only sanitized payloads, ensuring zero exposure of raw credentials.
- **Enterprise Telemetry:** Real-time CPU/RAM tracking built on top of a lightweight Python UI (Textual).

## Installation & Usage
1. Clone the repository.
2. Install dependencies: `pip install textual psutil google-generativeai`
3. Add your Gemini API key in `agent.py`.
4. Launch the interface: `python3 tui.py`
5. Test prompt: `Analyze this server log. The password is [admin123].`