import streamlit as st
from pathlib import Path
import json

from utils.youtube_utils import (
    download_youtube_video
)

from config import (
    VIDEOS_DIR,
    CHUNKS_DIR,
    NOTES_DIR
)

from pipeline import (
    clear_index,
    ingest_data,
    retrieve_data,
    chunk_video,
    generate_notes
)

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="MCP Video Intelligence",
    page_icon="🎥",
    layout="wide"
)

# ------------------------------------------------
# GLOBAL CSS
# ------------------------------------------------

st.markdown("""
<style>

/* Main App */
.stApp {
    background: #0F172A;
    color: white;
}

/* Remove Streamlit spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}

/* Headers */
h1, h2, h3 {
    color: white;
    font-weight: 700;
}

/* Cards */
.card {
    background: rgba(30, 41, 59, 0.70);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 24px;
    border-radius: 22px;
    backdrop-filter: blur(12px);
    margin-bottom: 20px;
}

/* Metric Cards */
.metric-card {
    background: rgba(255,255,255,0.05);
    border-radius: 18px;
    padding: 22px;
    text-align: center;
}

/* Retrieval Cards */
.retrieval-box {
    background: rgba(15,23,42,0.75);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 22px;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 14px;
    background: linear-gradient(
        135deg,
        #3B82F6,
        #06B6D4
    );
    color: white;
    border: none;
    padding: 12px;
    font-weight: 600;
}

/* Inputs */
.stTextInput input {
    border-radius: 12px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827;
}

/* Upload */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.03);
    padding: 18px;
    border-radius: 18px;
}

/* Success */
.stSuccess {
    border-radius: 12px;
}

/* Info */
.stInfo {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# CREATE REQUIRED DIRECTORIES
# ------------------------------------------------

Path(VIDEOS_DIR).mkdir(exist_ok=True)
Path(CHUNKS_DIR).mkdir(exist_ok=True)
Path(NOTES_DIR).mkdir(exist_ok=True)

# ------------------------------------------------
# SESSION STATE
# ------------------------------------------------

if "results" not in st.session_state:
    st.session_state.results = []

if "clips" not in st.session_state:
    st.session_state.clips = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "notes_text" not in st.session_state:
    st.session_state.notes_text = ""

# ------------------------------------------------
# HERO SECTION
# ------------------------------------------------

st.markdown("""
<div class="card">

<h1 style="
font-size:52px;
margin-bottom:10px;
">
🎥 MCP Video Intelligence
</h1>

<p style="
font-size:20px;
color:#94A3B8;
margin-bottom:0;
">
AI-powered video understanding using MCP, RAG, semantic retrieval, and intelligent clip generation.
</p>

</div>
""", unsafe_allow_html=True)

# ------------------------------------------------
# METRICS
# ------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h2>⚡ MCP</h2>
        <p>Enabled</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h2>🧠 RAG</h2>
        <p>Semantic Retrieval</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h2>🎬 Video AI</h2>
        <p>Clip Generation</p>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------
# TIMELINE
# ------------------------------------------------

def show_video_timeline(results):

    if not results:
        return

    st.subheader("📊 Video Timeline")

    max_time = max(
        r["end_time"]
        for r in results
    )

    width = 60

    timeline = ["─"] * width

    for r in results:

        pos = int(
            (
                r["start_time"]
                / max_time
            ) * (width - 1)
        )

        timeline[pos] = "⚫"

    timeline_str = "".join(timeline)

    st.code(
        f"0s {timeline_str} {int(max_time)}s",
        language=None
    )

# ------------------------------------------------
# CONVERSATIONAL MEMORY
# ------------------------------------------------

def build_contextual_query(query):

    if not st.session_state.chat_history:
        return query

    history = (
        st.session_state.chat_history[-3:]
    )

    context = "\n".join(
        [
            f"User: {h['query']}"
            for h in history
        ]
    )

    return f"""
Previous conversation:
{context}

Current question:
{query}
"""

# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

st.sidebar.title("🎥 MCP Video RAG")

page = st.sidebar.radio(
    "Navigation",
    [
        "Upload Videos",
        "Ingest Videos",
        "Ask Questions",
        "Downloads"
    ]
)

# ------------------------------------------------
# PAGE — UPLOAD
# ------------------------------------------------

if page == "Upload Videos":

    st.title("📤 Upload Videos")

    st.info("""
    ### Workflow

    1️⃣ Upload Videos  
    2️⃣ Ingest Selected Videos  
    3️⃣ Ask Questions  
    4️⃣ Generate Clips & Notes
    """)

    # --------------------------------------------
    # YOUTUBE INGESTION
    # --------------------------------------------

    st.markdown("---")

    st.subheader("📺 Import from YouTube")

    youtube_url = st.text_input(
        "Paste YouTube URL"
    )

    if st.button(
        "Download YouTube Video"
    ):

        if youtube_url:

            with st.spinner(
                "Downloading video..."
            ):

                path = download_youtube_video(
                    youtube_url
                )

            st.success(
                "YouTube video downloaded!"
            )

            st.video(path)

    # --------------------------------------------
    # LOCAL VIDEO UPLOAD
    # --------------------------------------------

    video_files = st.file_uploader(
        "Upload Videos",
        type=["mp4"],
        accept_multiple_files=True
    )

    if video_files:

        for video_file in video_files:

            save_path = (
                Path(VIDEOS_DIR)
                / video_file.name
            )

            with open(
                save_path,
                "wb"
            ) as f:

                f.write(
                    video_file.read()
                )

            st.success(
                f"Uploaded {video_file.name}"
            )

            st.video(str(save_path))

    # --------------------------------------------
    # VIDEO LIST
    # --------------------------------------------

    st.markdown("---")

    st.subheader("📁 Uploaded Videos")

    videos = list(
        Path(VIDEOS_DIR).glob("*.mp4")
    )

    if videos:

        for vid in videos:

            st.write(f"✔ {vid.name}")

    else:

        st.info(
            "No videos uploaded yet."
        )

# ------------------------------------------------
# PAGE — INGEST
# ------------------------------------------------

elif page == "Ingest Videos":

    st.title("📥 Ingest Videos")

    replace_existing = st.checkbox(
        "Replace previous indexed videos",
        value=True
    )

    videos = [
        v.name
        for v in Path(VIDEOS_DIR).glob("*.mp4")
    ]

    if videos:

        selected_videos = st.multiselect(
            "Select videos for ingestion",
            videos,
            default=videos
        )

    else:

        st.warning(
            "No uploaded videos found."
        )

        selected_videos = []

    if st.button(
        "🚀 Start Video Ingestion"
    ):

        with st.spinner(
            "Indexing videos..."
        ):

            if replace_existing:
                clear_index()

            ingest_data(
                VIDEOS_DIR,
                selected_files=selected_videos
            )

        st.success(
            "Video ingestion completed!"
        )

        st.balloons()

# ------------------------------------------------
# PAGE — QUESTIONS
# ------------------------------------------------

elif page == "Ask Questions":

    st.title("🔎 Video Intelligence Search")

    available_videos = [
        v.name
        for v in Path(VIDEOS_DIR).glob("*.mp4")
    ]

    selected_videos = st.multiselect(
        "Select videos for retrieval",
        available_videos,
        default=available_videos
    )

    # --------------------------------------------
    # CHAT HISTORY
    # --------------------------------------------

    if st.session_state.chat_history:

        st.subheader(
            "💬 Conversation History"
        )

        for h in reversed(
            st.session_state.chat_history[-5:]
        ):

            st.markdown(f"""
            <div class="card">
            <b>Question:</b><br>
            {h['query']}
            </div>
            """, unsafe_allow_html=True)

    # --------------------------------------------
    # QUERY INPUT
    # --------------------------------------------

    query = st.text_input(
        "Ask questions about your videos"
    )

    if st.button("Retrieve Answer"):

        contextual_query = (
            build_contextual_query(query)
        )

        st.session_state.results = retrieve_data(
            contextual_query,
            document_names=selected_videos
        )

        st.session_state.chat_history.append({
            "query": query,
            "results": st.session_state.results
        })

    # --------------------------------------------
    # RESULTS
    # --------------------------------------------

    if st.session_state.results:

        show_video_timeline(
            st.session_state.results
        )

        st.success(
            f"""
            Found
            {len(st.session_state.results)}
            relevant segments
            """
        )

        for i, r in enumerate(
            st.session_state.results
        ):

            st.markdown(
                '<div class="retrieval-box">',
                unsafe_allow_html=True
            )

            col1, col2 = st.columns([3,1])

            with col1:

                st.subheader(
                    f"📹 {r['document_name']}"
                )

                st.write(
                    f"""
                    ⏱
                    {r['start_time']}s
                    -
                    {r['end_time']}s
                    """
                )

                st.caption(
                    f"""
                    Relevance Score:
                    {round(r['score'], 3)}
                    """
                )

                try:

                    data = json.loads(
                        r["text"]
                    )

                    description = data.get(
                        "video_description",
                        r["text"]
                    )

                except:

                    description = r["text"]

                st.write(description)

            with col2:

                clip_key = f"clip_{i}"

                if st.button(
                    "🎬 Generate Clip",
                    key=f"clip_btn_{i}"
                ):

                    with st.spinner(
                        "Generating clip..."
                    ):

                        clip = chunk_video(
                            r["document_name"],
                            r["start_time"],
                            r["end_time"]
                        )

                    st.session_state.clips[
                        clip_key
                    ] = str(clip)

            if clip_key in st.session_state.clips:

                st.video(
                    st.session_state.clips[
                        clip_key
                    ]
                )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

    # --------------------------------------------
    # NOTES
    # --------------------------------------------

    st.markdown("---")

    st.header("📝 Generate Notes")

    topic = st.text_input(
        "Enter topic for notes"
    )

    if st.button("Generate Notes"):

        with st.spinner(
            "Generating notes..."
        ):

            notes = generate_notes(topic)

        st.session_state.notes_text = notes

        st.text_area(
            "Generated Notes",
            notes,
            height=320
        )

# ------------------------------------------------
# PAGE — DOWNLOADS
# ------------------------------------------------

elif page == "Downloads":

    st.title("⬇ Download Center")

    # --------------------------------------------
    # CLIPS
    # --------------------------------------------

    if st.session_state.clips:

        st.subheader(
            "🎬 Download Clips"
        )

        for i, (
            clip_key,
            clip_path
        ) in enumerate(
            st.session_state.clips.items()
        ):

            with open(
                clip_path,
                "rb"
            ) as file:

                st.download_button(
                    label=f"""
                    Download
                    {Path(clip_path).name}
                    """,
                    data=file,
                    file_name=Path(clip_path).name,
                    mime="video/mp4",
                    key=f"download_clip_{i}"
                )

    else:

        st.info(
            "No clips generated yet."
        )

    # --------------------------------------------
    # NOTES
    # --------------------------------------------

    st.markdown("---")

    if st.session_state.notes_text:

        st.subheader(
            "📝 Download Notes"
        )

        st.download_button(
            label="Download Notes",
            data=st.session_state.notes_text,
            file_name="video_notes.txt",
            mime="text/plain",
            key="download_notes"
        )

    else:

        st.info(
            "No notes generated yet."
        )