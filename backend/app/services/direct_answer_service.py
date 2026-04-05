import re
from pathlib import Path
from typing import Dict, Any, Optional, List

class DirectAnswerService:
    def __init__(self, notes_base_path: Optional[Path] = None):
        if notes_base_path is None:
            notes_base_path = Path(__file__).parent.parent.parent / "notes" / "tier-1-direct-answers"
        self.notes_base_path = notes_base_path
    
    def load_direct_answer(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a direct answer markdown file and extract structured data.
        
        Expected format:
        # Question Title
        
        Answer content here...
        
        ---
        
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
            dict with keys: question, answer, emotion, suggestions, projectLinks
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
        
        return {
            "question": question,
            "answer": answer,
            "emotion": emotion,
            "suggestions": suggestions,
            "projectLinks": project_links if project_links else None
        }

