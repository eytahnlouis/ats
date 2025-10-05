import sqlite3
import threading
from typing import Optional

class DatabaseManager:
    """Singleton pour gérer les connexions SQLite de manière efficace"""
    _instance: Optional['DatabaseManager'] = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._connection = None
        return cls._instance
    
    def get_connection(self) -> sqlite3.Connection:
        """Retourne une connexion SQLite réutilisable"""
        if self._connection is None:
            self._connection = sqlite3.connect("db.sqlite3", check_same_thread=False)
            # Optimisations SQLite
            self._connection.execute("PRAGMA journal_mode=WAL")
            self._connection.execute("PRAGMA synchronous=NORMAL")
            self._connection.execute("PRAGMA cache_size=10000")
        return self._connection
    
    def close(self):
        """Ferme la connexion (à appeler à la fin de l'application)"""
        if self._connection:
            self._connection.close()
            self._connection = None

# Instance globale
db_manager = DatabaseManager()