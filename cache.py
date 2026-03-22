class ClaimsSumCache:
    """
    A simple cache to store the sum of claims (demand) combinations.
    """
    def __init__(self):
        self._cache = {}

    def get_sum(self, claims):
        """
        Retrieves the sum from cache, or calculates it and stores it.
        """
        key = tuple(claims)
        if key not in self._cache:
            self._cache[key] = sum(claims)
        return self._cache[key]

# Global instance
claims_cache = ClaimsSumCache()

def get_claims_sum(claims):
    """Convenience function to access the cache directly."""
    return claims_cache.get_sum(claims)
