import re
from typing import Tuple

class ProfanityFilter:
    PROFANITY_PATTERNS = [
        # Common profanity
        r'\bf+u+c+k+',
        r'\bs+h+i+t+',
        r'\bd+a+m+n+',
        r'\bh+e+l+l+',
        r'\ba+s+s+h*o+l+e+',
        r'\bb+i+t+c+h+',
        r'\bb+a+s+t+a+r+d+',
        r'\bc+r+a+p+',
        r'\bp+i+s+s+',
        r'\bb+u+l+l+s+h+i+t+',
        r'\bm+o+t+h+e+r+f+u+c+k+e+r+',
        r'\bd+i+c+k+',
        r'\bp+u+s+s+y+',
        r'\bc+o+c+k+',
        r'\bc+u+n+t+',
        r'\bg+o+d+d+a+m+n+',
        
        # Common insults
        r'\bs+t+u+p+i+d+',
        r'\bi+d+i+o+t+',
        r'\bd+u+m+b+a+s+s+',
        r'\bm+o+r+o+n+',
        r'\bf+o+o+l+',
        r'\bu+s+e+l+e+s+s+',
        r'\bw+o+r+t+h+l+e+s+s+',
        r'\bg+a+r+b+a+g+e+',
        r'\bt+r+a+s+h+',
        r'\bp+a+t+h+e+t+i+c+',
        r'\bl+o+s+e+r+',
        r'\bt+e+r+r+i+b+l+e+\s+(developer|coder|programmer)',
        r'\bs+h+i+t+t+y+\s+(code|work|developer|projects?)',
        
        # Aggressive phrases
        r'\byou+\'*r+e+\s+(stupid|terrible|useless|incompetent|garbage)',
        r'\byou+r+\s+(code|work|projects?)\s+(is|are)\s+(shit|garbage|trash|terrible|useless)',
        r'\bwhat\s+the\s+fuck',
        r'\bthis\s+(is|chatbot)\s+(fucking|shit|garbage|useless)',
    ]
    
    def __init__(self):
        self.compiled_patterns = [
            re.compile(pattern, re.IGNORECASE) 
            for pattern in self.PROFANITY_PATTERNS
        ]
    
    def contains_profanity(self, text: str) -> Tuple[bool, str]:
        text_lower = text.lower()
        text_normalized = re.sub(r'[^a-z0-9\s]', '', text_lower)
        
        for pattern in self.compiled_patterns:
            if pattern.search(text_lower) or pattern.search(text_normalized):
                matched_pattern = pattern.pattern
                return True, matched_pattern
        
        return False, ""
    
    def check_question(self, question: str) -> dict:
        has_profanity, matched_pattern = self.contains_profanity(question)
        
        return {
            "has_profanity": has_profanity,
            "matched_pattern": matched_pattern if has_profanity else None,
            "should_block": has_profanity
        }

