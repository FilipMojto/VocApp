


class SeederInterface:
    """Interface for seeders."""
    
    def load_data(self, path: str) -> SeedData:
        """Load data from a specified path."""
        raise NotImplementedError("This method should be overridden by subclasses.")
    
