import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from app.services.direct_answer_service import DirectAnswerService
from app.services.embedding_storage import LocalEmbeddingStorage
from app.services.openai_service import OpenAIService

logger = logging.getLogger(__name__)

DIRECT_ANSWER_THRESHOLD = 0.75
DIRECT_ANSWER_SHORTLIST_K = 30
LLM_MATCH_THRESHOLD = 0.85
TIER1_5_ENABLED = True


def _fulltitle_for_file_path(
    file_path: str,
    index: List[Dict[str, str]],
    da_results: List[Dict[str, Any]],
) -> Optional[str]:
    name = Path(file_path).name
    for e in index:
        if e["filename"] == name:
            return e["fullTitle"]
    for r in da_results:
        if r.get("metadata", {}).get("file_path") == file_path:
            q = r["metadata"].get("question")
            if q:
                return str(q)
    return None


def _load_direct_response(
    file_path: str,
    top_score: float,
    direct_answer_service: DirectAnswerService,
    confidence: str,
) -> Optional[Dict[str, Any]]:
    try:
        direct = direct_answer_service.load_direct_answer(file_path)
    except Exception as e:
        logger.warning("Failed to load direct answer %s: %s", file_path, e)
        return None
    return {
        "answer": direct["answer"],
        "emotion": direct["emotion"],
        "suggestions": direct["suggestions"],
        "projectLinks": direct.get("projectLinks"),
        "confidence": confidence,
        "top_score": top_score,
    }


def try_resolve_direct_answer(
    openai_service: OpenAIService,
    direct_answer_storage: LocalEmbeddingStorage,
    direct_answer_service: DirectAnswerService,
    query_embedding: List[float],
    question: str,
) -> Optional[Dict[str, Any]]:
    try:
        da_results = direct_answer_storage.query_similar(
            query_embedding, top_k=DIRECT_ANSWER_SHORTLIST_K
        )
    except Exception as e:
        logger.warning("Direct answer query failed: %s", e)
        return None

    if not da_results:
        return None

    top = da_results[0]
    if top["score"] >= DIRECT_ANSWER_THRESHOLD:
        file_path = top["metadata"].get("file_path")
        if not file_path:
            return None
        return _load_direct_response(
            file_path,
            top["score"],
            direct_answer_service,
            "direct_answer",
        )

    if not TIER1_5_ENABLED:
        return None

    best_by_path: Dict[str, float] = {}
    for r in da_results:
        fp = r.get("metadata", {}).get("file_path")
        if not fp:
            continue
        sc = float(r["score"])
        if fp not in best_by_path or sc > best_by_path[fp]:
            best_by_path[fp] = sc

    if not best_by_path:
        return None

    index = direct_answer_service.get_index()
    sorted_paths = sorted(
        best_by_path.keys(), key=lambda p: -best_by_path[p]
    )

    seen: Set[str] = set()
    candidate_titles: List[str] = []
    title_to_path_score: Dict[str, tuple] = {}
    for fp in sorted_paths:
        full = _fulltitle_for_file_path(fp, index, da_results)
        if not full or full in seen:
            continue
        seen.add(full)
        candidate_titles.append(full)
        title_to_path_score[full] = (fp, best_by_path[fp])

    if not candidate_titles:
        return None

    try:
        match = openai_service.match_direct_answer_title(question, candidate_titles)
    except Exception as e:
        logger.warning("Tier 1.5 title matcher failed: %s", e)
        return None

    title = match.get("title")
    confidence = match.get("confidence", 0.0)
    try:
        conf_f = float(confidence)
    except (TypeError, ValueError):
        return None

    if title is None or conf_f < LLM_MATCH_THRESHOLD:
        return None
    if not isinstance(title, str) or not title.strip():
        return None
    if title not in title_to_path_score:
        return None

    file_path, emb_score = title_to_path_score[title]
    return _load_direct_response(
        file_path,
        emb_score,
        direct_answer_service,
        "direct_answer_llm_match",
    )
