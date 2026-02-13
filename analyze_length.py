"""Count words in all direct-answer files and find long ones."""
import os
from pathlib import Path

def word_count(text: str) -> int:
    """Count words in text."""
    return len(text.split())

def analyze_direct_answers():
    """Find all direct-answer files and their word counts."""
    da_dir = Path("backend/notes/tier-1-direct-answers")
    results = []
    
    for md_file in da_dir.glob("*.md"):
        # Skip metadata folder
        if md_file.parent.name == "metadata":
            continue
            
        content = md_file.read_text(encoding="utf-8")
        
        # Extract body (between title and ---)
        lines = content.split("\n")
        body_lines = []
        in_body = False
        
        for line in lines:
            if line.startswith("# "):
                in_body = True
                continue
            if line.strip() == "---":
                break
            if in_body:
                body_lines.append(line)
        
        body = "\n".join(body_lines).strip()
        wc = word_count(body)
        
        results.append({
            "file": md_file.name,
            "words": wc,
            "path": str(md_file)
        })
    
    # Sort by word count (descending)
    results.sort(key=lambda x: x["words"], reverse=True)
    
    # Show files over 300 words (buffer below 350 limit)
    print(f"Direct answer files over 300 words (test fails at 350):\n")
    print(f"{'Words':<7} {'File':<60}")
    print("=" * 70)
    
    long_count = 0
    for r in results:
        if r["words"] > 300:
            status = "FAIL" if r["words"] > 350 else "WARN"
            print(f"{r['words']:<7} {r['file']:<60} [{status}]")
            long_count += 1
    
    print(f"\n{long_count} files over 300 words")
    print(f"\nFiles failing test (>350):")
    fails = [r for r in results if r["words"] > 350]
    for r in fails:
        print(f"  - {r['words']} words: {r['file']}")

if __name__ == "__main__":
    analyze_direct_answers()
