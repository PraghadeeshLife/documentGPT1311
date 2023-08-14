from typing import *
import reflex as rx
from .searchgpt import retrieve_vector_store, generate_answer, ingest_document
import asyncio


vector_store = retrieve_vector_store()

class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str


class State(rx.State):
    """The app state."""

    # A dict from the chat name to the list of questions and answers.
    chats: Dict[str, List[QA]] = {
        "Intros": [QA(question="Hey 👋 Document GPT! What can you do for me?", answer="Hello, you can upload any text document and ask me any questions regarding the text, I make your life simpler by leveraging GPT models to quickly answer your questions in a concise way! 🤗 You can try uploading a text document, by clicking the avatar on top right and click Upload Files to get started with the text ingestion process.")],
    }
    
    # The current chat name.
    current_chat = "Intros"

    # The currrent question.
    question: str

    # Whether we are processing the question.
    processing: bool = False

    # Whether we are processing the upload.
    upload_processing: bool = False


    async def handle_upload(
        self, files: List[rx.UploadFile]
    ):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        self.upload_processing = True
        yield

        for i in range(5):
            await asyncio.sleep(0.001)

        for file in files:
            upload_data = await file.read()
            outfile = rx.get_asset_path(file.filename)
            # Save the file.
            with open(outfile, "wb") as file_object:
                file_object.write(upload_data)
            ingest_document(outfile)
            yield

        self.upload_processing = False
        


    async def process_question(self, form_data: Dict[str, str]):
        """Get the response from the API.

        Args:
            form_data: A dict with the current question.
        """
        # Check if we have already asked the last question or if the question is empty
        self.question = form_data["question"]
        if (
            self.chats[self.current_chat][-1].question == self.question
            or self.question == ""
        ):
            return

        # Set the processing flag to true and yield.
        self.processing = True
        yield

        # Start a new session to answer the question.
        qa = QA(question=self.question, answer="")
        for i in range(2):
            await asyncio.sleep(0.001)

        # Getting the answer for the question.
        answer = generate_answer(qa.question, vector_store)
        self.chats[self.current_chat].append(qa)

        # Making it look like answer is delivered as a stream.
        for i in range(len(answer)):
            # Pause to show the streaming effect.
            await asyncio.sleep(0.025)
            # Add one letter at a time to the output.
            self.chats[self.current_chat][-1].answer =  answer[:i]
            self.chats = self.chats
            yield
        # Toggle the processing flag.
        self.processing = False