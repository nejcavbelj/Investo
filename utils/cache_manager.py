"""
Simple caching manager for Investo
"""

import json
import time
from pathlib import Path
from typing import Any, Optional
from config.settings import PROJECT_ROOT

class CacheManager:
    """Simple JSON-based cache manager"""
    
    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or (PROJECT_ROOT / "cache")
        self.cache_dir.mkdir(exist_ok=True)
    
    def _get_cache_path(self, key: str) -> Path:
        """Get cache file path for a key"""
        return self.cache_dir / f"{key}.json"
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get value from cache"""
        cache_path = self._get_cache_path(key)
        
        if not cache_path.exists():
            return default
        
        try:
            with open(cache_path, 'r') as f:
                data = json.load(f)
                
            # Check if expired
            if 'expires_at' in data and time.time() > data['expires_at']:
                cache_path.unlink()  # Delete expired cache
                return default
                
            return data.get('value', default)
        except Exception:
            return default
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """Set value in cache with TTL in seconds"""
        cache_path = self._get_cache_path(key)
        
        data = {
            'value': value,
            'expires_at': time.time() + ttl,
            'created_at': time.time()
        }
        
        try:
            with open(cache_path, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving cache for {key}: {e}")
    
    def delete(self, key: str) -> bool:
        """Delete cache entry"""
        cache_path = self._get_cache_path(key)
        try:
            if cache_path.exists():
                cache_path.unlink()
                return True
        except Exception:
            pass
        return False
    
    def clear(self) -> None:
        """Clear all cache files"""
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
        except Exception as e:
            print(f"Error clearing cache: {e}")
    
    def get_info(self) -> dict:
        """Get cache information"""
        cache_files = list(self.cache_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in cache_files)
        
        return {
            "cache_dir": str(self.cache_dir),
            "file_count": len(cache_files),
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2)
        }

# Global cache instance
cache = CacheManager()
