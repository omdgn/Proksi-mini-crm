from transformers import pipeline
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class SummarizeService:
    def __init__(self):
        try:
            # Use a lightweight model for summarization
            self.summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=-1  # Use CPU
            )
            logger.info("AI summarization model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load summarization model: {e}")
            self.summarizer = None

    def summarize_text(self, text: str) -> Optional[str]:
        """
        Summarize the given text using Hugging Face model or fallback
        """
        if not text or len(text.strip()) < 10:
            return text

        text = text.strip()

        # Try AI summarization first
        if self.summarizer:
            try:
                return self._ai_summarize(text)
            except Exception as e:
                logger.error(f"AI summarization failed: {e}")

        # Fallback to rule-based summarization
        return self._rule_based_summary(text)

    def _ai_summarize(self, text: str) -> str:
        """
        AI-based summarization using Hugging Face
        """
        # Limit input length for the model (BART max ~1024 tokens)
        max_input_length = 1024
        if len(text) > max_input_length:
            text = text[:max_input_length]

        # Generate summary
        summary = self.summarizer(
            text,
            max_length=150,
            min_length=30,
            do_sample=False
        )

        return summary[0]['summary_text']

    def _rule_based_summary(self, text: str) -> str:
        """
        Fallback rule-based summarization
        """
        sentences = text.split('.')
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) <= 2:
            return text

        # Take first 2-3 sentences as summary
        summary_sentences = sentences[:min(3, len(sentences))]
        summary = '. '.join(summary_sentences)

        if not summary.endswith('.'):
            summary += '.'

        # Limit length
        if len(summary) > 200:
            summary = summary[:197] + '...'

        return summary