# Llama 3.1 Intent Engine

A local, single-user AI web application built with **Flask** and **Ollama**. This system uses a custom multi-step prompting architecture to categorize user intent and respond through specific personality profiles.

## 🚀 Features

- **Local Inference:** Runs entirely on your hardware via Ollama.
- **Intent Classification:** Automatically categorizes queries into *Academic, Technical, Entertainment, Personal,* or *General*.
- **Persona Profiles:** Switch between distinct personalities:
  - **Calm Professor:** Detailed and pedagogical.
  - **Overconfident Genius:** Arrogant and highly technical.
  - **Nervous Intern:** Apologetic and stuttering.
  - **Sarcastic Reviewer:** Cynical and witty.
- **Automatic Mode:** The AI analyzes your query and chooses the best persona for the job.
- **Streaming UI:** Real-time token generation for a snappy, chat-like experience.


## 📦 Installation

1. **Install Ollama:**
   Download and install from [ollama.com](https://ollama.com).

2. **Pull the Model:**
   Open your terminal and run:
   ```bash
   ollama pull llama3.1
