import re
from typing import Dict
from .parsing import extract_text_from_file
from .keyword_cache import keyword_cache

def score_resume(file_path, job_id: str) -> float:
    """
    Scores a resume based on the presence of keywords.
    Version optimisée avec cache et connexion réutilisable.
    """
    try:
        # Extraction du texte (mise en cache possible ici aussi)
        resume_text = extract_text_from_file(file_path)
        if not resume_text:
            return 0.0
        
        # Récupération des mots-clés depuis le cache
        keywords = keyword_cache.get_keywords(job_id)
        if not keywords:
            return 0.0
        
        # Préparation du texte pour une recherche plus efficace
        resume_text_lower = resume_text.lower()
        
        # Scoring optimisé
        score = 0
        total_score = sum(keywords.values())
        
        for keyword, points in keywords.items():
            if _keyword_matches(keyword.lower(), resume_text_lower):
                score += points
        
        return (score / total_score) * 100 if total_score > 0 else 0.0
        
    except Exception as e:
        print(f"Erreur lors du scoring: {e}")
        return 0.0

def _keyword_matches(keyword: str, text: str) -> bool:
    """
    Vérifie si un mot-clé est présent dans le texte avec une recherche plus précise.
    Utilise des limites de mots pour éviter les faux positifs.
    """
    # Utilise des limites de mots pour une recherche plus précise
    pattern = r'\b' + re.escape(keyword) + r'\b'
    return bool(re.search(pattern, text, re.IGNORECASE))

def score_multiple_resumes(file_paths: list, job_id: str) -> Dict[str, float]:
    """
    Score plusieurs CVs en une seule fois pour optimiser les appels DB.
    """
    # Récupération unique des mots-clés
    keywords = keyword_cache.get_keywords(job_id)
    if not keywords:
        return {path: 0.0 for path in file_paths}
    
    results = {}
    total_score = sum(keywords.values())
    
    for file_path in file_paths:
        try:
            resume_text = extract_text_from_file(file_path)
            if not resume_text:
                results[file_path] = 0.0
                continue
            
            resume_text_lower = resume_text.lower()
            score = 0
            
            for keyword, points in keywords.items():
                if _keyword_matches(keyword.lower(), resume_text_lower):
                    score += points
            
            results[file_path] = (score / total_score) * 100 if total_score > 0 else 0.0
            
        except Exception as e:
            print(f"Erreur pour {file_path}: {e}")
            results[file_path] = 0.0
    
    return results

def preload_keywords_cache(job_ids: list):
    """
    Précharge le cache pour plusieurs jobs.
    Utile avant un batch processing.
    """
    for job_id in job_ids:
        keyword_cache.get_keywords(job_id)