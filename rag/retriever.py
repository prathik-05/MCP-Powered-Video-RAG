import os
import time
import json
import logging

from dotenv import load_dotenv
from ragie import Ragie

load_dotenv()

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

ragie = Ragie(
    auth=os.getenv("RAGIE_API_KEY")
)


def expand_query(query):

    return [query]


def retrieve_data(
        query,
        top_k=10,
        min_score=0.16,
        document_names=None
):

    logger.info(f"Retrieving query: {query}")

    all_chunks = []

    for q in expand_query(query):

        try:

            retrieval = ragie.retrievals.retrieve(
                request={
                    "query": q,
                    "top_k": top_k,
                    "rerank": True
                }
            )

            all_chunks.extend(
                retrieval.scored_chunks
            )

            time.sleep(1)

        except Exception as e:

            logger.error(
                f"Retrieval failed: {e}"
            )

            return []

    results = []

    for chunk in all_chunks:

        score = getattr(chunk, "score", 0)

        doc = getattr(
            chunk,
            "document_name",
            None
        )

        if document_names and doc not in document_names:
            continue

        start = (
            chunk.metadata or {}
        ).get("start_time")

        end = (
            chunk.metadata or {}
        ).get("end_time")

        if start is None or end is None:
            continue

        text = chunk.text

        try:

            data = json.loads(text)

            text = data.get(
                "video_description",
                text
            )

        except:
            pass

        results.append({
            "document_name": doc,
            "text": text,
            "start_time": float(start),
            "end_time": float(end),
            "score": score
        })

    results.sort(
        key=lambda x: (
            x["document_name"],
            x["start_time"]
        )
    )

    filtered = [
        r for r in results
        if r["score"] >= min_score
    ]

    if not filtered:

        logger.warning(
            "No strong matches, using fallback results"
        )

        filtered = results[:6]

    seen = set()

    cleaned = []

    for r in filtered:

        key = (
            r["document_name"],
            int(r["start_time"])
        )

        if key in seen:
            continue

        seen.add(key)

        cleaned.append(r)

    merged = []

    for r in cleaned:

        if not merged:

            merged.append(r)

            continue

        last = merged[-1]

        if (
            r["document_name"] == last["document_name"]
            and r["start_time"] <= last["end_time"]
        ):

            last["end_time"] = max(
                last["end_time"],
                r["end_time"]
            )

            if len(r["text"]) > len(last["text"]):

                last["text"] = r["text"]

        else:

            merged.append(r)

    logger.info(
        f"Returning {len(merged)} segments"
    )

    return merged[:8]

def expand_query(query):

    # Returning only one query prevents hitting
    # Ragie rate limit (10 requests per minute)
    return [query]
