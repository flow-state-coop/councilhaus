import numpy as np
from typing import List, Dict, Any, Optional

class Member:
    """
    Member model representing a council member with voting power and allocation strategies.
    """
    
    def __init__(self, id: str, voting_power: int, strategy: str = 'random'):
        """
        Initialize a Member instance.
        
        Parameters:
        -----------
        id : str
            Unique identifier for the member
        voting_power : int
            Amount of voting power (non-transferable tokens)
        strategy : str
            Allocation strategy ('random', 'merit', 'popularity', 'coalition')
        """
        self.id = id
        self.voting_power = voting_power
        self.strategy = strategy
        self.coalition = None  # For coalition-based strategies
        
    def allocate(self, grantees: List[Any], strategy: Optional[str] = None) -> Dict[str, int]:
        """
        Allocate voting power to grantees based on strategy.
        
        Parameters:
        -----------
        grantees : list
            List of Grantee objects
        strategy : str, optional
            Override the member's default strategy
            
        Returns:
        --------
        dict
            Dictionary mapping grantee_id to allocation amount
        """
        strategy = strategy or self.strategy
        allocations = {}
        
        if not grantees:
            return allocations
        
        if strategy == 'random':
            # Random allocation
            weights = np.random.random(len(grantees))
            weights = weights / weights.sum() * self.voting_power
            
            for i, grantee in enumerate(grantees):
                allocations[grantee.id] = int(weights[i])
                
        elif strategy == 'merit':
            # Allocate based on grantee quality
            total_quality = sum(g.quality for g in grantees)
            if total_quality > 0:
                for grantee in grantees:
                    allocations[grantee.id] = int((grantee.quality / total_quality) * self.voting_power)
            else:
                # Equal allocation if no quality information
                equal_amount = self.voting_power // len(grantees)
                for grantee in grantees:
                    allocations[grantee.id] = equal_amount
                
        elif strategy == 'popularity':
            # Allocate based on grantee popularity
            total_popularity = sum(g.popularity for g in grantees)
            if total_popularity > 0:
                for grantee in grantees:
                    allocations[grantee.id] = int((grantee.popularity / total_popularity) * self.voting_power)
            else:
                # Equal allocation if no popularity information
                equal_amount = self.voting_power // len(grantees)
                for grantee in grantees:
                    allocations[grantee.id] = equal_amount
        
        elif strategy == 'coalition':
            # Allocate based on coalition preferences
            if self.coalition:
                coalition_grantees = [g for g in grantees if g.id in self.coalition]
                if coalition_grantees:
                    equal_amount = self.voting_power // len(coalition_grantees)
                    for grantee in coalition_grantees:
                        allocations[grantee.id] = equal_amount
                else:
                    # Fallback to random if no coalition grantees present
                    return self.allocate(grantees, 'random')
            else:
                # Fallback to random if no coalition defined
                return self.allocate(grantees, 'random')
        
        else:
            # Default to equal allocation for unknown strategies
            equal_amount = self.voting_power // len(grantees)
            for grantee in grantees:
                allocations[grantee.id] = equal_amount
        
        # Ensure we don't allocate more than voting power due to rounding
        total_allocated = sum(allocations.values())
        if total_allocated > self.voting_power:
            # Adjust the largest allocation down
            max_grantee = max(allocations, key=allocations.get)
            allocations[max_grantee] -= (total_allocated - self.voting_power)
        
        # Ensure we allocate all voting power
        remaining = self.voting_power - sum(allocations.values())
        if remaining > 0 and allocations:
            # Add remaining to the smallest allocation
            min_grantee = min(allocations, key=allocations.get)
            allocations[min_grantee] += remaining
                
        return allocations
    
    def join_coalition(self, coalition_grantees):
        """
        Join a coalition supporting specific grantees.
        
        Parameters:
        -----------
        coalition_grantees : list
            List of grantee IDs in the coalition
        """
        self.coalition = coalition_grantees
        self.strategy = 'coalition'
    
    def leave_coalition(self):
        """Leave any coalition and revert to random strategy."""
        self.coalition = None
        self.strategy = 'random' 