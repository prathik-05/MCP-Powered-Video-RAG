# 🎥 MCP-Powered Video Intelligence Platform

An AI-powered multimodal video understanding system built using MCP (Model Context Protocol), Retrieval-Augmented Generation (RAG), semantic retrieval, conversational memory, and intelligent clip generation.

This platform enables users to upload videos or ingest YouTube content, semantically query video content, retrieve relevant segments, generate downloadable clips, and create AI-powered notes from video understanding workflows.

---

# 🚀 Features

## 🎥 Video Ingestion
- Upload local MP4 videos
- Import videos directly from YouTube
- Selective multi-video ingestion
- Workspace-style indexing

## 🧠 AI Retrieval System
- Semantic video search
- Cross-segment reasoning
- Context-aware conversational retrieval
- Relevance-scored responses

## 💬 Conversational Memory
- Multi-turn video conversations
- Query context preservation
- Follow-up question understanding

## 🎬 Intelligent Clip Generation
- Automatic clip extraction
- Timestamp-based video chunking
- Download generated clips

## 📝 AI Notes Generation
- Generate structured notes from video content
- Topic-focused summarization
- Downloadable notes

## 📊 Video Timeline Visualization
- Temporal retrieval visualization
- Segment-aware timeline display

## ⚡ MCP Integration
- MCP server support
- MCP Inspector compatibility
- Modular tool-based architecture

---

# 🏗️ System Architecture

```text
                ┌─────────────────────┐
                │   Streamlit UI      │
                └─────────┬───────────┘
                          │
                          ▼
                ┌─────────────────────┐
                │   Pipeline Layer    │
                └─────────┬───────────┘
                          │
          ┌───────────────┼────────────────┐
          ▼               ▼                ▼
 ┌────────────────┐ ┌──────────────┐ ┌───────────────┐
 │  Ingestion     │ │ Retrieval    │ │ Notes Engine  │
 └────────┬───────┘ └──────┬───────┘ └──────┬────────┘
          │                │                 │
          ▼                ▼                 ▼
    ┌─────────────────────────────────────────────┐
    │           Ragie Semantic Engine             │
    └─────────────────────────────────────────────┘
                          │
                          ▼
                ┌─────────────────────┐
                │ Video Clip Engine   │
                └─────────────────────┘
```

---

# 📂 Project Structure

```text
MCP-Powered-Video-RAG/
│
├── rag/
│   ├── ingest.py
│   ├── retriever.py
│   ├── notes.py
│
├── utils/
│   ├── video_utils.py
│   ├── youtube_utils.py
│
├── videos/
├── video_chunks/
├── notes/
│
├── streamlit_app.py
├── pipeline.py
├── mcp_server.py
├── config.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/prathik-05/MCP-Powered-Video-RAG.git

cd MCP-Powered-Video-RAG
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
RAGIE_API_KEY=your_ragie_api_key
```

---

# ▶️ Run Streamlit App

```bash
streamlit run streamlit_app.py
```

---

# ⚡ Run MCP Server

```bash
mcp dev mcp_server.py
```

---

# 📺 Workflow

## 1️⃣ Upload or Import Videos
- Upload local MP4 videos
- Or import videos from YouTube

## 2️⃣ Ingest Selected Videos
- Choose videos for semantic indexing
- Replace or append indexes

## 3️⃣ Ask Questions
- Query videos semantically
- Retrieve relevant segments

## 4️⃣ Generate Clips
- Automatically extract relevant clips

## 5️⃣ Generate Notes
- Produce AI-generated notes from video content

---

# 🧠 Conversational Retrieval

The platform supports conversational memory.

Example:

```text
User: What did he explain about transformers?

User: Explain that more simply.

User: Show the earlier example clip.
```

The assistant preserves conversational context across queries.

---

# 🛠️ Tech Stack

## Frontend
- Streamlit

## Backend
- Python

## AI / Retrieval
- Ragie
- Retrieval-Augmented Generation (RAG)
- Semantic Search

## Video Processing
- MoviePy
- yt-dlp

## MCP
- Model Context Protocol (MCP)

---

# 📸 Screenshots

## Home Interface
_Add screenshot here_

## Retrieval Interface
_Add screenshot here_

## Clip Generation
_Add screenshot here_

## Notes Generation
_Add screenshot here_

---

# 🔮 Future Improvements

- FAISS / Chroma Vector DB Integration
- Async Video Ingestion
- Background Processing
- Transcript Viewer
- Cloud Deployment
- Multi-user Workspaces
- Authentication System
- Advanced LLM Summarization
- Timestamp Jump Navigation

---

# 📈 Key Highlights

- Modular AI architecture
- MCP-enabled tooling
- Conversational video understanding
- Semantic video retrieval
- Multimodal AI workflows
- Production-style project structure

---

# 🤝 Contributing

Contributions are welcome.

Feel free to fork the repository and submit pull requests.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

## Prathik

GitHub:
https://github.com/prathik-05
