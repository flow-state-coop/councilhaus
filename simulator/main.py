#!/usr/bin/env python3
"""
Main entry point for the Council funding simulation.
"""

import os
import argparse
import numpy as np
import pandas as pd
from pathlib import Path

from models.council import Council
from utils.helpers import generate_members, generate_grantees, setup_coalitions
from utils.simulation_runner import run_simulation, run_batch_simulations
from config import DEFAULT_CONFIG, DATA_PATHS

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Council Funding Simulator')
    
    parser.add_argument('--num_members', type=int, default=DEFAULT_CONFIG['num_members'],
                        help='Number of council members')
    
    parser.add_argument('--voting_power_distribution', type=str, 
                        default=DEFAULT_CONFIG['voting_power_distribution'],
                        choices=['equal', 'normal', 'pareto', 'custom'],
                        help='Distribution of voting power')
    
    parser.add_argument('--power_skew', type=float, default=DEFAULT_CONFIG['power_skew'],
                        help='Skew parameter for custom distribution (0.0 to 1.0)')
    
    parser.add_argument('--initial_pool', type=float, default=DEFAULT_CONFIG['initial_pool'],
                        help='Initial funding pool size')
    
    parser.add_argument('--distribution_rate', type=float, 
                        default=DEFAULT_CONFIG['distribution_rate'],
                        help='Monthly distribution rate (0.01 to 0.1)')
    
    parser.add_argument('--annual_funding_addition', type=float, 
                        default=DEFAULT_CONFIG['annual_funding_addition'],
                        help='Amount to add to the funding pool at the end of each year ($10,000-$1,000,000)')
    
    parser.add_argument('--num_grantees', type=int, default=DEFAULT_CONFIG['num_grantees'],
                        help='Number of grantees')
    
    parser.add_argument('--allocation_strategy', type=str, 
                        default=DEFAULT_CONFIG['allocation_strategy'],
                        choices=['random', 'merit', 'popularity', 'coalition'],
                        help='Allocation strategy')
    
    parser.add_argument('--participation_rate', type=float, 
                        default=DEFAULT_CONFIG['participation_rate'],
                        help='Member participation rate (0.0 to 1.0)')
    
    parser.add_argument('--duration_months', type=int, 
                        default=DEFAULT_CONFIG['duration_months'],
                        help='Simulation duration in months')
    
    parser.add_argument('--batch', action='store_true',
                        help='Run batch simulations')
    
    parser.add_argument('--parameter_to_vary', type=str, default='None',
                        choices=['None', 'Number of Members', 'Distribution Rate', 'Participation Rate'],
                        help='Parameter to vary in batch simulations')
    
    parser.add_argument('--num_simulations', type=int, 
                        default=DEFAULT_CONFIG['num_simulations'],
                        help='Number of simulations to run in batch mode')
    
    parser.add_argument('--random_seed', type=int, default=DEFAULT_CONFIG['random_seed'],
                        help='Random seed for reproducibility')
    
    parser.add_argument('--output', type=str, default=None,
                        help='Output file for simulation results (CSV)')
    
    return parser.parse_args()

def setup_directories():
    """Create necessary directories if they don't exist."""
    for path in DATA_PATHS.values():
        Path(path).mkdir(parents=True, exist_ok=True)

def main():
    """Main function to run the simulation."""
    args = parse_args()
    setup_directories()
    
    # Set random seed for reproducibility
    np.random.seed(args.random_seed)
    
    # Create config from arguments
    config = {
        'num_members': args.num_members,
        'voting_power_distribution': args.voting_power_distribution,
        'power_skew': args.power_skew,
        'initial_pool': args.initial_pool,
        'distribution_rate': args.distribution_rate,
        'annual_funding_addition': args.annual_funding_addition,
        'num_grantees': args.num_grantees,
        'allocation_strategy': args.allocation_strategy,
        'participation_rate': args.participation_rate,
        'duration_months': args.duration_months
    }
    
    if args.batch:
        # Run batch simulations
        print(f"Running {args.num_simulations} simulations varying {args.parameter_to_vary}...")
        results = run_batch_simulations(config, args.parameter_to_vary, args.num_simulations)
        
        # Save results if output specified
        if args.output:
            output_path = args.output
            if not output_path.endswith('.csv'):
                output_path += '.csv'
                
            # Extract and save data from each simulation
            all_data = []
            for i, (sim_config, (council, df)) in enumerate(zip(results['configs'], results['results'])):
                # Add simulation index and parameter value
                if args.parameter_to_vary == "Number of Members":
                    param_value = sim_config['num_members']
                elif args.parameter_to_vary == "Distribution Rate":
                    param_value = sim_config['distribution_rate']
                elif args.parameter_to_vary == "Participation Rate":
                    param_value = sim_config['participation_rate']
                else:
                    param_value = 0
                
                # Add simulation metadata to each row
                df['simulation'] = i
                df['parameter_value'] = param_value
                all_data.append(df)
            
            # Combine all simulation data
            combined_df = pd.concat(all_data, ignore_index=True)
            combined_df.to_csv(output_path, index=False)
            print(f"Batch simulation results saved to {output_path}")
    else:
        # Run single simulation
        print("Running single simulation...")
        council, df = run_simulation(config)
        
        # Print summary
        print("\nSimulation Summary:")
        print(f"Initial Pool: ${df['pool_balance'].iloc[0]:,.2f}")
        print(f"Final Pool: ${df['pool_balance'].iloc[-1]:,.2f}")
        print(f"Total Distributed: ${df['pool_balance'].iloc[0] - df['pool_balance'].iloc[-1]:,.2f}")
        print(f"Number of Members: {len(council.members)}")
        print(f"Number of Grantees: {len(council.grantees)}")
        
        # Save results if output specified
        if args.output:
            output_path = args.output
            if not output_path.endswith('.csv'):
                output_path += '.csv'
            df.to_csv(output_path, index=False)
            print(f"Simulation results saved to {output_path}")
    
    print("Simulation complete.")

if __name__ == "__main__":
    main() 