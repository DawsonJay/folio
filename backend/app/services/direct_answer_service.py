import re
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class DirectAnswerService:
    def __init__(self, notes_base_path: Optional[Path] = None):
        if notes_base_path is None:
            notes_base_path = Path(__file__).parent.parent.parent / "notes" / "tier-1-direct-answers"
        self.notes_base_path = notes_base_path

    def get_index(self) -> List[Dict[str, str]]:
        """
        Build an index of all direct answer files.

        Returns a list of dicts with keys:
          - shortTitle: display text (shortTitle field if present, else full title)
          - fullTitle: the raw # Title (always the full question, used as the submitted query)
          - filename: the .md filename

        Excludes the metadata/ subdirectory.
        """
        index = []
        for md_file in sorted(self.notes_base_path.glob("*.md")):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                full_title = ""
                short_title = ""
                for i, line in enumerate(lines):
                    stripped = line.strip()
                    if i == 0 and stripped.startswith('# '):
                        full_title = stripped[2:].strip()
                    if stripped.startswith('**shortTitle:**'):
                        match = re.search(r'\*\*shortTitle:\*\*\s*(.+)', stripped)
                        if match:
                            short_title = match.group(1).strip()

                if full_title:
                    index.append({
                        "shortTitle": short_title if short_title else full_title,
                        "fullTitle": full_title,
                        "filename": md_file.name,
                    })
            except Exception as e:
                logger.warning(f"Could not index {md_file.name}: {e}")

        return index

    def get_suggestion_list_string(self) -> str:
        """Return all shortTitles as a formatted list for inclusion in LLM prompts."""
        return "\n".join(f"- {e['shortTitle']}" for e in self.get_index())

    def load_direct_answer(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a direct answer markdown file and extract structured data.

        Expected format:
        # Question Title

        Answer content here...

        ---

        **shortTitle:** Shorter question? (optional, only when title > 45 chars)
        **emotion:** happy
        **suggestions:**
        - Question 1?
        - Question 2?
        ...

        **projectLinks:** (optional)
        - ProjectName:
          - demo: https://...
          - github: https://...

        Returns:
            dict with keys: question, shortTitle, answer, emotion, suggestions, projectLinks
        """
        full_path = Path(file_path)
        if not full_path.is_absolute():
            full_path = self.notes_base_path.parent.parent / file_path

        if not full_path.exists():
            raise FileNotFoundError(f"Direct answer file not found: {full_path}")

        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')

        question = ""
        short_title = ""
        answer_parts = []
        emotion = "happy"
        suggestions = []
        project_links = {}

        in_answer = False
        in_suggestions = False
        in_project_links = False
        current_project = None

        for i, line in enumerate(lines):
            stripped = line.strip()

            if i == 0 and stripped.startswith('# '):
                question = stripped[2:].strip()
                in_answer = True
                continue

            if stripped == '---':
                in_answer = False
                continue

            if in_answer and stripped:
                answer_parts.append(stripped)
                continue

            if stripped.startswith('**shortTitle:**'):
                match = re.search(r'\*\*shortTitle:\*\*\s*(.+)', line)
                if match:
                    short_title = match.group(1).strip()
                continue

            if stripped.startswith('**emotion:**'):
                emotion_match = re.search(r'\*\*emotion:\*\*\s*(\w+)', line)
                if emotion_match:
                    emotion = emotion_match.group(1)
                continue

            if stripped.startswith('**suggestions:**'):
                in_suggestions = True
                continue

            if in_suggestions:
                if stripped.startswith('- '):
                    suggestion_text = stripped[2:].strip()
                    if suggestion_text:
                        suggestions.append(suggestion_text)
                elif stripped and not stripped.startswith('**'):
                    continue
                elif stripped.startswith('**') or (not stripped and suggestions):
                    in_suggestions = False

            if stripped.startswith('**projectLinks:**'):
                in_project_links = True
                continue

            if in_project_links:
                if stripped.startswith('- '):
                    project_match = re.match(r'-\s*([\w-]+):', stripped)
                    if project_match:
                        current_project = project_match.group(1)
                        project_links[current_project] = {}
                elif current_project and stripped.startswith('  - '):
                    link_match = re.match(r'\s*-\s*(demo|github):\s*(.+)', stripped)
                    if link_match:
                        link_type = link_match.group(1)
                        link_url = link_match.group(2).strip()
                        project_links[current_project][link_type] = link_url

        answer = '\n\n'.join(answer_parts).strip()

        if not question:
            raise ValueError(f"No question title found in {file_path}")

        if not answer:
            raise ValueError(f"No answer content found in {file_path}")

        if not suggestions:
            raise ValueError(f"No suggestions found in {file_path}")

        if len(suggestions) != 6:
            raise ValueError(f"Expected 6 suggestions, found {len(suggestions)} in {file_path}")

        valid_emotions = ['happy', 'thinking', 'surprised', 'derp', 'tired', 'annoyed']
        if emotion not in valid_emotions:
            emotion = 'happy'

        index = self.get_index()
        structured_suggestions = self._resolve_suggestions(suggestions, index, file_path)

        return {
            "question": question,
            "shortTitle": short_title if short_title else question,
            "answer": answer,
            "emotion": emotion,
            "suggestions": structured_suggestions,
            "projectLinks": project_links if project_links else None
        }

    def _resolve_suggestions(
        self, suggestions: List[str], index: List[Dict[str, str]], file_path: str
    ) -> List[Dict[str, str]]:
        """
        Convert suggestion strings (shortTitles) into {text, query} dicts.

        - text: the shortTitle (displayed on the chip)
        - query: the fullTitle (submitted as the query when clicked)

        When shortTitle == fullTitle (no shortTitle field on the target file),
        only 'text' is included so the Suggestion model sends no redundant query field.
        Logs a warning for any suggestion not found in the index.
        """
        short_to_full: Dict[str, str] = {
            entry["shortTitle"]: entry["fullTitle"] for entry in index
        }
        result = []
        for suggestion in suggestions:
            if suggestion not in short_to_full:
                logger.warning(
                    f"Suggestion '{suggestion}' in {file_path} does not match any known direct answer shortTitle"
                )
                result.append({"text": suggestion})
            else:
                full = short_to_full[suggestion]
                if full != suggestion:
                    result.append({"text": suggestion, "query": full})
                else:
                    result.append({"text": suggestion})
        return result

