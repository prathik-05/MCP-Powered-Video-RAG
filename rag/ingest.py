import os
import time
import logging

from pathlib import Path

from dotenv import load_dotenv
from ragie import Ragie

load_dotenv()

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

ragie = Ragie(
    auth=os.getenv("RAGIE_API_KEY")
)


def clear_index():

    while True:

        try:

            response = ragie.documents.list()

            documents = response.result.documents

            for doc in documents:

                ragie.documents.delete(
                    document_id=doc.id
                )

                logger.info(
                    f"Deleted {doc.id}"
                )

            if not response.result.pagination.next_cursor:
                break

        except Exception as e:

            logger.error(
                f"Clear index failed: {e}"
            )

            break


def ingest_data(directory,selected_files=None):

    directory = Path(directory)

    files = [
        f for f in os.listdir(directory)
        if f.endswith(".mp4")
    ]
    
    if selected_files:

        files = [
            f for f in files
            if f in selected_files
        ]

    if not files:

        logger.warning(
            "No MP4 files found."
        )

        return

    for file in files:

        path = directory / file

        try:

            with open(path, "rb") as f:

                content = f.read()

            response = ragie.documents.create(
                request={
                    "file": {
                        "file_name": file,
                        "content": content
                    },
                    "mode": {
                        "video": "audio_video",
                        "audio": True
                    }
                }
            )

            while True:

                status = ragie.documents.get(
                    document_id=response.id
                )

                if status.status == "ready":
                    break

                time.sleep(1)

            logger.info(
                f"Ingested {file}"
            )

        except Exception as e:

            logger.error(
                f"Failed {file}: {e}"
            )