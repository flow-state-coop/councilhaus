import numpy as np
from typing import List, Dict, Any

def generate_random_allocation(member, grantees: List[Any]) -> Dict[str, int]:
    """
    Generate a random allocation of voting power to grantees.
    
    Parameters:
    -----------
    member : Member
        The member making the allocation
    grantees : list
        List of Grantee objects
        
    Returns:
    --------
    dict
        Dictionary mapping grantee_id to allocation amount
    """
    if not grantees:
        return {}
        
    # Generate random weights
    weights = np.random.random(len(grantees))
    weights = weights / weights.sum() * member.voting_power
    
    # Create allocation dictionary
    allocations = {}
    for i, grantee in enumerate(grantees):
        allocations[grantee.id] = int(weights[i])
    
    # Adjust for rounding errors
    total_allocated = sum(allocations.values())
    if total_allocated != member.voting_power:
        # Add or subtract the difference from the largest allocation
        diff = member.voting_power - total_allocated
        max_grantee = max(allocations, key=allocations.get)
        allocations[max_grantee] += diff
    
    return allocations

def generate_merit_based_allocation(member, grantees: List[Any]) -> Dict[str, int]:
    """
    Generate an allocation based on grantee quality.
    
    Parameters:
    -----------
    member : Member
        The member making the allocation
    grantees : list
        List of Grantee objects
        
    Returns:
    --------
    dict
        Dictionary mapping grantee_id to allocation amount
    """
    if not grantees:
        return {}
        
    # Calculate total quality
    total_quality = sum(g.quality for g in grantees)
    
    # Create allocation dictionary
    allocations = {}
    if total_quality > 0:
        for grantee in grantees:
            allocations[grantee.id] = int((grantee.quality / total_quality) * member.voting_power)
    else:
        # Equal allocation if no quality information
        equal_amount = member.voting_power // len(grantees)
        for grantee in grantees:
            allocations[grantee.id] = equal_amount
    
    # Adjust for rounding errors
    total_allocated = sum(allocations.values())
    if total_allocated != member.voting_power and allocations:
        # Add or subtract the difference from the largest allocation
        diff = member.voting_power - total_allocated
        max_grantee = max(allocations, key=allocations.get)
        allocations[max_grantee] += diff
    
    return allocations

def generate_popularity_based_allocation(member, grantees: List[Any]) -> Dict[str, int]:
    """
    Generate an allocation based on grantee popularity.
    
    Parameters:
    -----------
    member : Member
        The member making the allocation
    grantees : list
        List of Grantee objects
        
    Returns:
    --------
    dict
        Dictionary mapping grantee_id to allocation amount
    """
    if not grantees:
        return {}
        
    # Calculate total popularity
    total_popularity = sum(g.popularity for g in grantees)
    
    # Create allocation dictionary
    allocations = {}
    if total_popularity > 0:
        for grantee in grantees:
            allocations[grantee.id] = int((grantee.popularity / total_popularity) * member.voting_power)
    else:
        # Equal allocation if no popularity information
        equal_amount = member.voting_power // len(grantees)
        for grantee in grantees:
            allocations[grantee.id] = equal_amount
    
    # Adjust for rounding errors
    total_allocated = sum(allocations.values())
    if total_allocated != member.voting_power and allocations:
        # Add or subtract the difference from the largest allocation
        diff = member.voting_power - total_allocated
        max_grantee = max(allocations, key=allocations.get)
        allocations[max_grantee] += diff
    
    return allocations

def generate_coalition_allocation(member, grantees: List[Any], coalition_grantees: List[str]) -> Dict[str, int]:
    """
    Generate an allocation based on coalition preferences.
    
    Parameters:
    -----------
    member : Member
        The member making the allocation
    grantees : list
        List of Grantee objects
    coalition_grantees : list
        List of grantee IDs in the coalition
        
    Returns:
    --------
    dict
        Dictionary mapping grantee_id to allocation amount
    """
    if not grantees:
        return {}
        
    # Filter grantees in the coalition
    coalition_grantees_objs = [g for g in grantees if g.id in coalition_grantees]
    
    # If no coalition grantees present, fall back to random allocation
    if not coalition_grantees_objs:
        return generate_random_allocation(member, grantees)
    
    # Create allocation dictionary
    allocations = {}
    equal_amount = member.voting_power // len(coalition_grantees_objs)
    
    for grantee in grantees:
        if grantee.id in coalition_grantees:
            allocations[grantee.id] = equal_amount
        else:
            allocations[grantee.id] = 0
    
    # Adjust for rounding errors
    total_allocated = sum(allocations.values())
    if total_allocated != member.voting_power and allocations:
        # Add or subtract the difference from the first coalition grantee
        diff = member.voting_power - total_allocated
        for grantee_id in coalition_grantees:
            if grantee_id in allocations:
                allocations[grantee_id] += diff
                break
    
    return allocations

def get_allocation_strategy(strategy_name: str):
    """
    Get the allocation strategy function by name.
    
    Parameters:
    -----------
    strategy_name : str
        Name of the allocation strategy
        
    Returns:
    --------
    function
        The allocation strategy function
    """
    strategies = {
        'random': generate_random_allocation,
        'merit': generate_merit_based_allocation,
        'popularity': generate_popularity_based_allocation,
        'coalition': generate_coalition_allocation
    }
    
    return strategies.get(strategy_name, generate_random_allocation) 