from pathlib import Path

from rag.retriever import retrieve_data


def generate_notes(
        topic,
        top_k=10,
        document_names=None,
        min_score=0.0,
        output_path=None
):

    chunks = retrieve_data(
        query=topic,
        top_k=top_k,
        min_score=min_score,
        document_names=document_names
    )

    if not chunks:
        return "No relevant segments found."

    notes = f"# Notes for: {topic}\n\n"

    for c in chunks:

        notes += (
            f"## {c['document_name']}\n"
            f"Timestamp: {c['start_time']}s "
            f"- {c['end_time']}s\n\n"
            f"{c['text']}\n\n"
        )

    if output_path:

        output_file = Path(output_path)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(notes)

    return notes