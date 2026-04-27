import sys
import unittest
from unittest.mock import MagicMock
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.direct_answer_routing import try_resolve_direct_answer


class TestDirectAnswerRouting(unittest.TestCase):
    def setUp(self):
        self.das = MagicMock()
        self.storage = MagicMock()
        self.openai = MagicMock()
        self.embedding = [0.1] * 10

    def _loaded_answer(self):
        return {
            "answer": "Body",
            "emotion": "happy",
            "suggestions": [{"text": f"Q{i}"} for i in range(6)],
            "projectLinks": None,
        }

    def test_tier1_high_score_no_llm(self):
        self.storage.query_similar.return_value = [
            {
                "score": 0.92,
                "metadata": {
                    "file_path": "notes/tier-1-direct-answers/tell-me-about-yourself.md",
                },
            }
        ]
        self.das.load_direct_answer.return_value = self._loaded_answer()
        r = try_resolve_direct_answer(
            self.openai,
            self.storage,
            self.das,
            self.embedding,
            "Tell me about yourself",
        )
        self.assertIsNotNone(r)
        self.assertEqual(r["confidence"], "direct_answer")
        self.assertEqual(r["top_score"], 0.92)
        self.openai.match_direct_answer_title.assert_not_called()

    def test_tier15_llm_match(self):
        self.storage.query_similar.return_value = [
            {
                "score": 0.55,
                "metadata": {
                    "file_path": "notes/tier-1-direct-answers/where-do-you-see-yourself-in-five-years.md",
                    "question": "Where do you see yourself in five years?",
                },
            }
        ]
        self.das.get_index.return_value = [
            {
                "filename": "where-do-you-see-yourself-in-five-years.md",
                "fullTitle": "Where do you see yourself in five years?",
                "shortTitle": "5-year goals",
            }
        ]
        self.openai.match_direct_answer_title.return_value = {
            "title": "Where do you see yourself in five years?",
            "confidence": 0.9,
        }
        self.das.load_direct_answer.return_value = self._loaded_answer()
        r = try_resolve_direct_answer(
            self.openai,
            self.storage,
            self.das,
            self.embedding,
            "If I hire you where do you want to be in five years?",
        )
        self.assertIsNotNone(r)
        self.assertEqual(r["confidence"], "direct_answer_llm_match")
        self.assertEqual(r["top_score"], 0.55)
        self.openai.match_direct_answer_title.assert_called_once()

    def test_tier15_low_confidence_falls_back(self):
        self.storage.query_similar.return_value = [
            {
                "score": 0.5,
                "metadata": {
                    "file_path": "notes/tier-1-direct-answers/where-do-you-see-yourself-in-five-years.md",
                    "question": "Where do you see yourself in five years?",
                },
            }
        ]
        self.das.get_index.return_value = [
            {
                "filename": "where-do-you-see-yourself-in-five-years.md",
                "fullTitle": "Where do you see yourself in five years?",
                "shortTitle": "x",
            }
        ]
        self.openai.match_direct_answer_title.return_value = {
            "title": "Where do you see yourself in five years?",
            "confidence": 0.4,
        }
        r = try_resolve_direct_answer(
            self.openai,
            self.storage,
            self.das,
            self.embedding,
            "vague",
        )
        self.assertIsNone(r)
        self.das.load_direct_answer.assert_not_called()

    def test_empty_results_returns_none(self):
        self.storage.query_similar.return_value = []
        r = try_resolve_direct_answer(
            self.openai,
            self.storage,
            self.das,
            self.embedding,
            "Q",
        )
        self.assertIsNone(r)

    def test_tier1_load_failure_returns_none(self):
        self.storage.query_similar.return_value = [
            {
                "score": 0.9,
                "metadata": {
                    "file_path": "notes/tier-1-direct-answers/missing.md",
                },
            }
        ]
        self.das.load_direct_answer.side_effect = ValueError("no suggestions")
        r = try_resolve_direct_answer(
            self.openai,
            self.storage,
            self.das,
            self.embedding,
            "Q",
        )
        self.assertIsNone(r)


if __name__ == "__main__":
    unittest.main()
