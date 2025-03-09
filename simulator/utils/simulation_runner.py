import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from typing import Dict, Any, List, Tuple, Optional

def run_simulation(config: Dict[str, Any]) -> Tuple[Any, pd.DataFrame]:
    """
    Run a single simulation with the given configuration.
    
    Parameters:
    -----------
    config : dict
        Dictionary containing simulation parameters
        
    Returns:
    --------
    tuple
        (Council object, DataFrame with simulation history)
    """
    from models.council import Council
    from utils.helpers import generate_members, generate_grantees, setup_coalitions
    
    # Extract parameters
    num_members = config.get('num_members', 100)
    num_grantees = config.get('num_grantees', 10)
    initial_pool = config.get('initial_pool', 100000)
    distribution_rate = config.get('distribution_rate', 0.05)
    annual_funding_addition = config.get('annual_funding_addition', 0)
    voting_power_distribution = config.get('voting_power_distribution', 'equal')
    power_skew = config.get('power_skew', 0.5)
    quality_distribution = config.get('quality_distribution', 'uniform')
    popularity_correlation = config.get('popularity_correlation', 0.5)
    allocation_strategy = config.get('allocation_strategy', 'random')
    coalition_size = config.get('coalition_size', 0.3)
    coalition_focus = config.get('coalition_focus', 2)
    participation_rate = config.get('participation_rate', 0.8)
    duration_months = config.get('duration_months', 12)
    
    # Generate members and grantees
    members = generate_members(
        num_members,
        voting_power_distribution,
        power_skew
    )
    
    grantees = generate_grantees(
        num_grantees,
        quality_distribution,
        popularity_correlation
    )
    
    # Set up coalitions if using coalition strategy
    if allocation_strategy == 'coalition':
        members = setup_coalitions(members, grantees, coalition_size, coalition_focus)
    
    # Set member strategies
    for member in members:
        if member.strategy != 'coalition':  # Don't override coalition strategy
            member.strategy = allocation_strategy
    
    # Initialize council
    council = Council(
        initial_pool, 
        distribution_rate, 
        members, 
        grantees,
        annual_funding_addition
    )
    
    # Run simulation for specified duration
    for month in range(duration_months):
        # Members allocate voting power
        for member in council.active_members(participation_rate):
            allocations = member.allocate(council.grantees)
            council.record_allocations(member, allocations)
        
        # Distribute funds based on allocations
        council.distribute_funds(month)
    
    # Get history as DataFrame
    df = council.get_history_dataframe()
    
    return council, df

def create_parameter_variations(
    base_config: Dict[str, Any],
    parameter: str,
    num_variations: int
) -> List[Dict[str, Any]]:
    """
    Create variations of a parameter for batch simulations.
    
    Parameters:
    -----------
    base_config : dict
        Base configuration dictionary
    parameter : str
        Name of the parameter to vary
    num_variations : int
        Number of variations to create
        
    Returns:
    --------
    list
        List of configuration dictionaries
    """
    configs = []
    
    if parameter == "Number of Members":
        min_members = 10
        max_members = min(60000, base_config.get('num_members', 100) * 10)
        member_values = np.linspace(min_members, max_members, num_variations, dtype=int)
        
        for members in member_values:
            new_config = base_config.copy()
            new_config['num_members'] = int(members)
            configs.append(new_config)
            
    elif parameter == "Distribution Rate":
        min_rate = 0.01
        max_rate = 0.1
        rate_values = np.linspace(min_rate, max_rate, num_variations)
        
        for rate in rate_values:
            new_config = base_config.copy()
            new_config['distribution_rate'] = rate
            configs.append(new_config)
            
    elif parameter == "Participation Rate":
        min_rate = 0.1
        max_rate = 1.0
        rate_values = np.linspace(min_rate, max_rate, num_variations)
        
        for rate in rate_values:
            new_config = base_config.copy()
            new_config['participation_rate'] = rate
            configs.append(new_config)
            
    elif parameter == "Annual Funding Addition":
        min_addition = 10000
        max_addition = 1000000
        addition_values = np.linspace(min_addition, max_addition, num_variations)
        
        for addition in addition_values:
            new_config = base_config.copy()
            new_config['annual_funding_addition'] = int(addition)
            configs.append(new_config)
    
    else:
        # Default to running the same config multiple times
        configs = [base_config.copy() for _ in range(num_variations)]
    
    return configs

def run_batch_simulations(
    base_config: Dict[str, Any],
    parameter_to_vary: str,
    num_simulations: int
) -> Dict[str, Any]:
    """
    Run multiple simulations with variations of a parameter.
    
    Parameters:
    -----------
    base_config : dict
        Base configuration dictionary
    parameter_to_vary : str
        Name of the parameter to vary
    num_simulations : int
        Number of simulations to run
        
    Returns:
    --------
    dict
        Dictionary containing batch simulation results
    """
    if parameter_to_vary == "None":
        # Run the same simulation multiple times (Monte Carlo)
        configs = [base_config.copy() for _ in range(num_simulations)]
    else:
        # Create variations of the specified parameter
        configs = create_parameter_variations(base_config, parameter_to_vary, num_simulations)
    
    # Run simulations (sequentially for now)
    # TODO: Implement parallel processing for large simulations
    results = []
    for config in configs:
        results.append(run_simulation(config))
    
    # For small numbers of simulations, sequential is fine
    # For larger batches, we could use parallel processing:
    # with ProcessPoolExecutor() as executor:
    #     results = list(executor.map(run_simulation, configs))
    
    return {
        'configs': configs,
        'results': results,
        'parameter_varied': parameter_to_vary
    } 