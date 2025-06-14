from transformers import pipeline
import logging

logger = logging.getLogger("summarizer.service")


class SummarizerService:
    def __init__(self, model_name="t5-small"):
        self.model = None
        self.model_name = model_name
        self._initialize_model()

    def _initialize_model(self):
        try:
            logger.info(f"Loading model: {self.model_name}")
            self.model = pipeline("summarization", model=self.model_name)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            self.model = None

    def is_ready(self):
        return self.model is not None

    def summarize(self, text):
        if not self.is_ready():
            logger.error("Summarization attempted but model is not loaded")
            raise RuntimeError("Model is not loaded")

        try:
            logger.info(f"Generating summary for text of length: {len(text)}")
            result = self.model(text, max_length=130, min_length=30, do_sample=False)
            summary = result[0]["summary_text"]
            logger.info(f"Summary generated successfully: length={len(summary)}")
            return summary
        except Exception as e:
            logger.error(f"Summarization error: {str(e)}")
            raise RuntimeError(f"Error generating summary: {str(e)}")


summarizer_service = SummarizerService()