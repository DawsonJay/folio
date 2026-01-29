from typing import Dict, List, Optional

PROJECT_LINKS = {
    "WhatNow": {
        "demo": "https://whatnow-frontend.onrender.com",
        "github": "https://github.com/DawsonJay/whatnow-frontend"
    },
    "moh-ami": {
        "demo": "https://moh-ami-production.up.railway.app/",
        "github": "https://github.com/DawsonJay/moh-ami"
    },
    "Cirrus": {
        "demo": None,
        "github": "https://github.com/DawsonJay/cirrus-project"
    },
    "Atlantis": {
        "demo": None,
        "github": "https://github.com/DawsonJay/atlantis-project"
    },
    "Portfolio Website": {
        "demo": "https://jamesdawson.dev",
        "github": "https://github.com/DawsonJay/portfolio-website"
    },
    "Folio": {
        "demo": None,
        "github": None
    }
}

def extract_project_links(note_ids: List[str]) -> Optional[Dict[str, Dict[str, Optional[str]]]]:
    """
    Extract project links for projects mentioned in retrieved notes.
    
    Args:
        note_ids: List of note IDs from retrieval (e.g., ['whatnow-overview', 'moh-ami-llm-integration'])
    
    Returns:
        Dictionary of project links for mentioned projects, or None if no projects mentioned
    """
    mentioned_projects = {}
    
    for note_id in note_ids:
        note_id_lower = note_id.lower()
        
        for project_name, links in PROJECT_LINKS.items():
            project_key = project_name.lower().replace(" ", "-")
            
            if project_key in note_id_lower or project_name.lower() in note_id_lower:
                link_dict = {}
                if links["demo"]:
                    link_dict["demo"] = links["demo"]
                if links["github"]:
                    link_dict["github"] = links["github"]
                
                if link_dict:
                    mentioned_projects[project_name] = link_dict
    
    return mentioned_projects if mentioned_projects else None

