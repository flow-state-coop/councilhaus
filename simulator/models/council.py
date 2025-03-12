import numpy as np
import pandas as pd

class Council:
    """
    Council model representing the main contract that manages council members,
    voting power, budget allocations, and grantees.
    """
    
    def __init__(self, initial_pool, distribution_rate, members=None, grantees=None, annual_funding_addition=0):
        """
        Initialize a Council instance.
        
        Parameters:
        -----------
        initial_pool : float
            Initial funding pool size in currency units
        distribution_rate : float
            Monthly distribution rate as a fraction (0.01 to 0.1)
        members : list
            List of Member objects
        grantees : list
            List of Grantee objects
        annual_funding_addition : float
            Amount to add to the funding pool at the end of each year
        """
        self.pool_balance = initial_pool
        self.distribution_rate = distribution_rate
        self.members = members or []
        self.grantees = grantees or []
        self.allocations = {}  # member_id -> {grantee_id: amount}
        self.history = []  # Track historical state
        self.annual_funding_addition = annual_funding_addition
        
    def active_members(self, participation_rate=1.0):
        """
        Return active members based on participation rate.
        
        Parameters:
        -----------
        participation_rate : float
            Fraction of members who participate (0.0 to 1.0)
            
        Returns:
        --------
        list
            List of active Member objects
        """
        num_active = int(len(self.members) * participation_rate)
        if num_active == 0 and len(self.members) > 0:
            num_active = 1  # Ensure at least one member if any exist
        return np.random.choice(self.members, num_active, replace=False).tolist()
    
    def record_allocations(self, member, allocations):
        """
        Record a member's allocations.
        
        Parameters:
        -----------
        member : Member
            The member making allocations
        allocations : dict
            Dictionary mapping grantee_id to allocation amount
        """
        self.allocations[member.id] = allocations
        
    def current_allocations(self):
        """
        Calculate current total allocations per grantee.
        
        Returns:
        --------
        dict
            Dictionary mapping grantee_id to total allocation amount
        """
        total_allocations = {grantee.id: 0 for grantee in self.grantees}
        for member_allocations in self.allocations.values():
            for grantee_id, amount in member_allocations.items():
                if grantee_id in total_allocations:
                    total_allocations[grantee_id] += amount
        return total_allocations
    
    def distribute_funds(self, month):
        """
        Distribute funds based on current allocations.
        
        Parameters:
        -----------
        month : int
            Current month in the simulation
            
        Returns:
        --------
        dict
            Dictionary mapping grantee_id to distributed amount
        """
        total_allocations = self.current_allocations()
        total_votes = sum(total_allocations.values())
        
        # Calculate amount to distribute this month
        distribution_amount = self.pool_balance * self.distribution_rate
        self.pool_balance -= distribution_amount
        
        # Distribute proportionally
        distribution = {}
        for grantee_id, votes in total_allocations.items():
            if total_votes > 0:
                distribution[grantee_id] = (votes / total_votes) * distribution_amount
            else:
                distribution[grantee_id] = 0
        
        # Update grantees with received funds
        for grantee in self.grantees:
            if grantee.id in distribution:
                grantee.receive_funds(distribution[grantee.id])
        
        # Check if it's the end of a year (month % 12 == 11 for 0-indexed months)
        annual_funding_added = 0
        if (month + 1) % 12 == 0 and self.annual_funding_addition > 0:
            self.pool_balance += self.annual_funding_addition
            annual_funding_added = self.annual_funding_addition
        
        # Record state for history
        self.history.append({
            'month': month,
            'pool_balance': self.pool_balance,
            'distribution': distribution.copy(),
            'allocations': total_allocations.copy(),
            'annual_funding_added': annual_funding_added
        })
                
        return distribution
    
    def get_history_dataframe(self):
        """
        Convert history to a pandas DataFrame.
        
        Returns:
        --------
        pandas.DataFrame
            DataFrame containing simulation history
        """
        if not self.history:
            return pd.DataFrame()
        
        # Basic history data
        df = pd.DataFrame(self.history)
        
        # Expand distribution and allocations into separate columns
        for record in self.history:
            for grantee_id, amount in record['distribution'].items():
                df.loc[df['month'] == record['month'], f'dist_to_{grantee_id}'] = amount
                
            for grantee_id, amount in record['allocations'].items():
                df.loc[df['month'] == record['month'], f'alloc_to_{grantee_id}'] = amount
        
        return df 