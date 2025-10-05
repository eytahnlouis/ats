from typing import Dict, Tuple
import time
from .db_manager import db_manager

class KeywordCache:
    """Cache en mémoire pour les mots-clés avec TTL"""
    
    def __init__(self, ttl_seconds: int = 86400):  # Cache de 24 heures
        self._cache: Dict[str, Tuple[Dict[str, float], float]] = {}
        self._ttl = ttl_seconds
    
    def get_keywords(self, job_id: str) -> Dict[str, float]:
        """Récupère les mots-clés depuis le cache ou la DB"""
        current_time = time.time()
        
        # Vérifier si on a une entrée en cache valide
        if job_id in self._cache:
            keywords, timestamp = self._cache[job_id]
            if current_time - timestamp < self._ttl:
                return keywords
        
        # Récupérer depuis la DB et mettre en cache
        keywords = self._fetch_keywords_from_db(job_id)
        self._cache[job_id] = (keywords, current_time)
        return keywords
    
    def _fetch_keywords_from_db(self, job_id: str) -> Dict[str, float]:
        """Récupère les mots-clés depuis la base de données"""
        connection = db_manager.get_connection()
        cursor = connection.cursor()
        
        cursor.execute(
            '''SELECT k.word, jk.weight
            FROM cvs_jobs_keywords jk 
            JOIN cvs_keyword k ON jk.keyword_id = k.id 
            WHERE jk.job_id = ?;''',
            (job_id,)
        )
        
        keywords_tuples = cursor.fetchall()
        return dict(keywords_tuples)
    
    def invalidate(self, job_id: str = None):
        """Invalide le cache pour un job spécifique ou tout le cache"""
        if job_id:
            self._cache.pop(job_id, None)
        else:
            self._cache.clear()
    
    def cleanup_expired(self):
        """Nettoie les entrées expirées du cache"""
        current_time = time.time()
        expired_keys = [
            job_id for job_id, (_, timestamp) in self._cache.items()
            if current_time - timestamp >= self._ttl
        ]
        for key in expired_keys:
            del self._cache[key]

# Instance globale
keyword_cache = KeywordCache()