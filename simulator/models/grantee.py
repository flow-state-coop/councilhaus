class Grantee:
    """
    Grantee model representing a project or entity receiving funding.
    """
    
    def __init__(self, id, name, quality=0.5, popularity=0.5, min_funding_threshold=0):
        """
        Initialize a Grantee instance.
        
        Parameters:
        -----------
        id : str
            Unique identifier for the grantee
        name : str
            Name of the grantee project
        quality : float
            Intrinsic quality of the project (0.0 to 1.0)
        popularity : float
            Popularity of the project (0.0 to 1.0)
        min_funding_threshold : float
            Minimum funding needed for the project to be viable
        """
        self.id = id
        self.name = name
        self.quality = quality
        self.popularity = popularity
        self.min_funding_threshold = min_funding_threshold
        self.received_funds = 0
        self.monthly_funding = []  # Track funding by month
        
    def receive_funds(self, amount):
        """
        Record funds received.
        
        Parameters:
        -----------
        amount : float
            Amount of funds received
        """
        self.received_funds += amount
        self.monthly_funding.append(amount)
        
    def is_viable(self):
        """
        Check if the grantee has received enough funding to be viable.
        
        Returns:
        --------
        bool
            True if funding exceeds minimum threshold, False otherwise
        """
        return self.received_funds >= self.min_funding_threshold
    
    def funding_stability(self):
        """
        Calculate the stability of funding (lower variance is more stable).
        
        Returns:
        --------
        float
            Coefficient of variation of monthly funding (or 0 if no funding)
        """
        import numpy as np
        
        if not self.monthly_funding or sum(self.monthly_funding) == 0:
            return 0
            
        return np.std(self.monthly_funding) / np.mean(self.monthly_funding)
    
    def __str__(self):
        return f"{self.name} (ID: {self.id}, Quality: {self.quality:.2f}, Popularity: {self.popularity:.2f})" 