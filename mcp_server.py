from mcp.server.fastmcp import FastMCP
from pipeline import (
    ingest_data,
    retrieve_data,
    chunk_video,
    generate_notes
)

mcp = FastMCP("ragie")

@mcp.tool()
def ingest_data_tool(directory: str, replace: bool = False) -> None:
    """
    Loads data from a directory into the Ragie index. Wait until the data is fully ingested before continuing.

    Args:
        directory (str): The directory to load data from.
        replace (bool): If True, clears the index before ingesting. If False (default), appends.

    Returns:
        str: A message indicating that the data was loaded successfully.
    """
    try:
        if replace:
            clear_index()
        ingest_data(directory)
        return "Data loaded successfully"   
    except Exception as e:
        return f"Failed to load data: {str(e)}"

@mcp.tool()
def retrieve_data_tool(
    query: str,
    min_score: float | None = None,
    top_k: int = 15,
    document_names: list[str] | None = None,
) -> list[dict]:
    """
    Retrieves data from the Ragie index across all ingested videos (cross-video reasoning).
    Returns a list of dicts with: text, document_name, start_time, end_time, score.
    Use min_score to drop low-relevance chunks; use document_names to limit to specific videos.

    Args:
        query (str): The query to retrieve data from the Ragie index.
        min_score (float | None): Minimum relevance score (optional). Chunks below this are excluded.
        top_k (int): Maximum number of chunks to return. Default 15.
        document_names (list[str] | None): Limit to these video file names. None = all videos.

    Returns:
        list[dict]: The retrieved data with citations (document_name, start_time, end_time).
    """
    try:
        content = retrieve_data(
            query,
            top_k=top_k,
            min_score=min_score,
            document_names=document_names,
        )
        return content
    except Exception as e:
        return [{"error": str(e)}]

@mcp.tool()
def show_video_tool(document_name: str, start_time: float, end_time: float) -> str:
    """
    Creates and saves a video chunk based on the document name, start time, and end time of the chunk.
    Returns a message indicating that the video chunk was created successfully.

    Args:
        document_name (str): The name of the document the chunk belongs to
        start_time (float): The start time of the chunk
        end_time (float): The end time of the chunk

    Returns:
        str: A message indicating that the video chunk was created successfully
    """
    try:
        chunk_video(document_name, start_time, end_time)
        return "Video chunk created successfully"
    except Exception as e:
        return f"Failed to create video chunk: {str(e)}"


@mcp.tool()
def generate_notes_tool(
    query_or_topic: str,
    document_names: list[str] | None = None,
    min_score: float = 0.0,
    output_path: str | None = None,
) -> str:
    """
    Generate structured notes from video content and save to a downloadable file.
    Optionally limit to specific videos via document_names.
    Notes are grounded in retrieved chunks only (low hallucination).

    Args:
        query_or_topic (str): Topic or question to generate notes about (used for retrieval).
        document_names (list[str] | None): Limit to these video file names. None = all videos.
        min_score (float): Minimum relevance score for chunks. Default 0.0.
        output_path (str | None): File path to save notes (e.g. "notes/my_notes.md").
            If None, saves to notes/notes_<timestamp>.md in the project directory.

    Returns:
        str: Confirmation with file path and the notes content.
    """
    try:
        from datetime import datetime

        if output_path is None:
            safe_topic = "".join(c if c.isalnum() or c in " -_" else "_" for c in query_or_topic[:30])
            ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output_path = f"notes/notes_{safe_topic}_{ts}.md"
        return generate_notes(
            query_or_topic,
            document_names=document_names,
            min_score=min_score,
            top_k=20,
            output_path=output_path,
        )
    except Exception as e:
        return f"Failed to generate notes: {str(e)}"


# Run the server locally
if __name__ == "__main__":
    mcp.run(transport='stdio')