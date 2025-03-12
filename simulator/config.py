"""
Configuration settings for the Council funding simulation.
"""

# Default simulation parameters
DEFAULT_CONFIG = {
    # Council parameters
    'num_members': 100,
    'voting_power_distribution': 'equal',
    'power_skew': 0.5,
    'initial_pool': 100000,
    'distribution_rate': 0.05,
    'annual_funding_addition': 0,
    
    # Grantee parameters
    'num_grantees': 10,
    'quality_distribution': 'uniform',
    'popularity_correlation': 0.5,
    'min_funding_threshold': 1000,
    
    # Member behavior
    'allocation_strategy': 'random',
    'coalition_size': 0.3,
    'coalition_focus': 2,
    'participation_rate': 0.8,
    
    # Temporal parameters
    'duration_months': 12,
    
    # Simulation parameters
    'random_seed': 42,
    'num_simulations': 10
}

# Parameter ranges for UI controls
PARAMETER_RANGES = {
    'num_members': (1, 60000, 100),
    'power_skew': (0.0, 1.0, 0.5),
    'initial_pool': (10000, 1000000, 100000),
    'distribution_rate': (0.01, 0.1, 0.05),
    'annual_funding_addition': (0, 1000000, 0),
    'num_grantees': (1, 100, 10),
    'popularity_correlation': (-1.0, 1.0, 0.5),
    'coalition_size': (0.1, 1.0, 0.3),
    'coalition_focus': (1, 5, 2),
    'participation_rate': (0.1, 1.0, 0.8),
    'duration_months': (1, 36, 12)
}

# Options for dropdown menus
DROPDOWN_OPTIONS = {
    'voting_power_distribution': ['Equal', 'Normal', 'Pareto', 'Custom'],
    'quality_distribution': ['Uniform', 'Normal', 'Bimodal'],
    'allocation_strategy': ['Random', 'Merit-based', 'Popularity-based', 'Coalition'],
    'parameter_to_vary': ['None', 'Number of Members', 'Distribution Rate', 'Participation Rate', 'Annual Funding Addition']
}

# Paths for data storage
DATA_PATHS = {
    'results_dir': 'data/results',
    'figures_dir': 'data/figures',
    'config_dir': 'data/configs'
}

# Enable or disable features
FEATURES = {
    'parallel_processing': True,
    'save_results': True,
    'network_visualization': True,
    'comparative_analysis': True
} 