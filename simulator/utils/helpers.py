import numpy as np
from typing import List, Dict, Any, Optional
import string
import random

def generate_members(
    num_members: int,
    voting_power_distribution: str = 'equal',
    power_skew: float = 0.5,
    total_voting_power: int = 100000
) -> List[Any]:
    """
    Generate a list of council members with specified voting power distribution.
    
    Parameters:
    -----------
    num_members : int
        Number of members to generate
    voting_power_distribution : str
        Distribution type ('equal', 'normal', 'pareto', 'custom')
    power_skew : float
        Skew parameter for custom distribution (0.0 to 1.0)
    total_voting_power : int
        Total voting power to distribute among members
        
    Returns:
    --------
    list
        List of Member objects
    """
    from models.member import Member
    
    if num_members <= 0:
        return []
    
    # Generate member IDs
    member_ids = [f"m{i+1}" for i in range(num_members)]
    
    # Generate voting power based on distribution
    if voting_power_distribution == 'equal':
        # Equal distribution
        voting_power = np.ones(num_members) * (total_voting_power / num_members)
        
    elif voting_power_distribution == 'normal':
        # Normal distribution
        mean = total_voting_power / num_members
        std_dev = mean * 0.5  # Adjust standard deviation as needed
        voting_power = np.random.normal(mean, std_dev, num_members)
        voting_power = np.clip(voting_power, mean * 0.1, mean * 3)  # Clip to reasonable range
        
    elif voting_power_distribution == 'pareto':
        # Pareto distribution (power law)
        shape = 1.5  # Pareto shape parameter (lower = more unequal)
        voting_power = np.random.pareto(shape, num_members) + 1
        
    elif voting_power_distribution == 'custom':
        # Custom distribution based on power_skew
        # power_skew of 0.0 is equal, 1.0 is extremely skewed
        if power_skew <= 0.01:
            # Almost equal
            voting_power = np.ones(num_members) * (total_voting_power / num_members)
        else:
            # Generate exponential distribution with varying rate
            rate = 5 * (1 - power_skew) + 0.1  # Rate parameter (higher = more equal)
            voting_power = np.random.exponential(1/rate, num_members)
    
    else:
        # Default to equal distribution
        voting_power = np.ones(num_members) * (total_voting_power / num_members)
    
    # Normalize to ensure total voting power is correct
    voting_power = voting_power / voting_power.sum() * total_voting_power
    
    # Convert to integers
    voting_power = np.round(voting_power).astype(int)
    
    # Adjust for rounding errors
    diff = total_voting_power - voting_power.sum()
    if diff != 0:
        # Add or subtract the difference from the largest voting power
        idx = np.argmax(voting_power)
        voting_power[idx] += diff
    
    # Create Member objects
    members = []
    for i in range(num_members):
        members.append(Member(member_ids[i], int(voting_power[i])))
    
    return members

def generate_grantees(
    num_grantees: int,
    quality_distribution: str = 'uniform',
    popularity_correlation: float = 0.5,
    min_funding_threshold: float = 1000
) -> List[Any]:
    """
    Generate a list of grantees with specified quality and popularity distributions.
    
    Parameters:
    -----------
    num_grantees : int
        Number of grantees to generate
    quality_distribution : str
        Distribution type for quality ('uniform', 'normal', 'bimodal')
    popularity_correlation : float
        Correlation between quality and popularity (-1.0 to 1.0)
    min_funding_threshold : float
        Minimum funding threshold for viability
        
    Returns:
    --------
    list
        List of Grantee objects
    """
    from models.grantee import Grantee
    
    if num_grantees <= 0:
        return []
    
    # Generate grantee IDs and names
    grantee_ids = [f"g{i+1}" for i in range(num_grantees)]
    grantee_names = [generate_project_name() for _ in range(num_grantees)]
    
    # Generate quality based on distribution
    if quality_distribution == 'uniform':
        # Uniform distribution
        quality = np.random.uniform(0.1, 1.0, num_grantees)
        
    elif quality_distribution == 'normal':
        # Normal distribution
        quality = np.random.normal(0.5, 0.15, num_grantees)
        quality = np.clip(quality, 0.1, 1.0)  # Clip to valid range
        
    elif quality_distribution == 'bimodal':
        # Bimodal distribution (mix of high and low quality)
        group1 = np.random.normal(0.25, 0.1, num_grantees // 2)
        group2 = np.random.normal(0.75, 0.1, num_grantees - num_grantees // 2)
        quality = np.concatenate([group1, group2])
        np.random.shuffle(quality)
        quality = np.clip(quality, 0.1, 1.0)  # Clip to valid range
        
    else:
        # Default to uniform distribution
        quality = np.random.uniform(0.1, 1.0, num_grantees)
    
    # Generate popularity based on quality and correlation
    if popularity_correlation >= 0:
        # Positive correlation
        # Base popularity on quality with some random noise
        noise = np.random.normal(0, 0.2, num_grantees)
        popularity = quality * popularity_correlation + (1 - popularity_correlation) * noise
    else:
        # Negative correlation
        # Inverse relationship between quality and popularity
        noise = np.random.normal(0, 0.2, num_grantees)
        popularity = (1 - quality) * abs(popularity_correlation) + (1 - abs(popularity_correlation)) * noise
    
    # Clip and normalize popularity
    popularity = np.clip(popularity, 0.1, 1.0)
    
    # Create Grantee objects
    grantees = []
    for i in range(num_grantees):
        # Vary minimum funding threshold slightly
        threshold = min_funding_threshold * (0.8 + 0.4 * quality[i])
        
        grantees.append(Grantee(
            grantee_ids[i],
            grantee_names[i],
            quality=quality[i],
            popularity=popularity[i],
            min_funding_threshold=threshold
        ))
    
    return grantees

def generate_project_name() -> str:
    """Generate a random project name."""
    adjectives = [
        "Decentralized", "Autonomous", "Open", "Distributed", "Transparent",
        "Sustainable", "Innovative", "Community", "Global", "Resilient",
        "Inclusive", "Regenerative", "Collaborative", "Ethical", "Adaptive"
    ]
    
    nouns = [
        "Protocol", "Network", "DAO", "Platform", "Ecosystem",
        "Commons", "Initiative", "Collective", "Foundation", "Project",
        "System", "Framework", "Alliance", "Guild", "Venture"
    ]
    
    return f"{random.choice(adjectives)} {random.choice(nouns)}"

def setup_coalitions(members: List[Any], grantees: List[Any], coalition_size: float, coalition_focus: int) -> List[Any]:
    """
    Set up coalitions among members.
    
    Parameters:
    -----------
    members : list
        List of Member objects
    grantees : list
        List of Grantee objects
    coalition_size : float
        Fraction of members in coalitions (0.0 to 1.0)
    coalition_focus : int
        Number of grantees each coalition supports
        
    Returns:
    --------
    list
        Updated list of Member objects
    """
    if not members or not grantees or coalition_size <= 0 or coalition_focus <= 0:
        return members
    
    # Determine number of coalitions (roughly 1 coalition per 10 members)
    num_coalitions = max(1, int(len(members) / 10))
    
    # Determine number of members in coalitions
    num_coalition_members = int(len(members) * coalition_size)
    
    # Select members for coalitions
    coalition_members = np.random.choice(members, num_coalition_members, replace=False)
    
    # Create coalitions
    coalitions = []
    for _ in range(num_coalitions):
        # Select random grantees for this coalition
        coalition_grantees = np.random.choice(
            [g.id for g in grantees],
            min(coalition_focus, len(grantees)),
            replace=False
        ).tolist()
        
        coalitions.append(coalition_grantees)
    
    # Assign members to coalitions
    members_per_coalition = num_coalition_members // num_coalitions
    remaining = num_coalition_members % num_coalitions
    
    member_index = 0
    for i, coalition in enumerate(coalitions):
        # Calculate number of members in this coalition
        count = members_per_coalition + (1 if i < remaining else 0)
        
        # Assign members to this coalition
        for j in range(count):
            if member_index < len(coalition_members):
                coalition_members[member_index].join_coalition(coalition)
                member_index += 1
    
    return members 