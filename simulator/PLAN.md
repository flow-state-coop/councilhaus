# Comprehensive Plan for Council Funding Simulation Tool

After reviewing the provided contracts and plan, I'll help you develop a more comprehensive plan for creating a Python simulation tool to model funding rounds using the Council contracts.

## Understanding the System

The Council contract system consists of:

1. **Council**: Main contract that manages council members with voting power, budget allocations, and grantees
2. **NonTransferableToken**: Represents voting power that cannot be transferred
3. **PoolManager**: Manages the distribution pool and grantee allocations
4. **CouncilFactory**: Creates new Council instances

The key mechanics are:
- Council members have voting power (non-transferable tokens)
- Members allocate their voting power to grantees
- Funds are distributed to grantees proportionally based on allocated voting power

## Simulation Tool Plan

### 1. Core Components

```
simulation/
├── data/                  # Store simulation results
├── models/                # Core simulation models
│   ├── __init__.py
│   ├── council.py         # Council model
│   ├── member.py          # Council member model
│   ├── grantee.py         # Grantee model
│   └── allocation.py      # Allocation strategies
├── visualization/         # Visualization components
│   ├── __init__.py
│   ├── dashboard.py       # Streamlit dashboard
│   └── plots.py           # Plotting functions using Plotly
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── helpers.py         # Helper functions
│   └── simulation_runner.py # Parallel simulation runner
├── config.py              # Configuration settings
├── main.py                # Main entry point
├── app.py                 # Streamlit app entry point
└── requirements.txt       # Dependencies
```

### 2. Simulation Parameters

Expand on the initial parameters:

1. **Council Configuration**
   - Number of council members (1-60,000)
   - Distribution of voting power (equal, normal, pareto, custom)
   - Initial funding pool size ($10,000-$1,000,000)
   - Distribution rate (1%-10% per month)

2. **Grantee Configuration**
   - Number of grantees (1-100)
   - Grantee characteristics (quality, popularity, etc.)
   - Minimum funding threshold

3. **Member Behavior Models**
   - Allocation strategies (random, merit-based, popularity-based, etc.)
   - Participation rate (% of members who allocate)
   - Coordination patterns (independent, coalition-forming)

4. **Temporal Parameters**
   - Simulation duration (months)
   - Allocation frequency (monthly, quarterly, yearly)
   - Funding distribution frequency (constant rate)

### 3. Simulation Logic

```python
# Pseudocode for simulation flow
def run_simulation(config):
    # Initialize council with members and grantees
    council = Council(
        members=generate_members(config.num_members, config.voting_power_distribution),
        grantees=generate_grantees(config.num_grantees),
        initial_pool=config.initial_pool,
        distribution_rate=config.distribution_rate
    )
    
    results = []
    
    # Run simulation for specified duration
    for month in range(config.duration_months):
        # Members allocate voting power
        for member in council.active_members(config.participation_rate):
            allocations = member.allocate(council.grantees, strategy=config.allocation_strategy)
            council.record_allocations(member, allocations)
        
        # Distribute funds based on allocations
        distribution = council.distribute_funds(month)
        
        # Record results
        results.append({
            'month': month,
            'allocations': council.current_allocations(),
            'distribution': distribution,
            'pool_remaining': council.pool_balance
        })
    
    return results
```

### 4. Visualization Dashboard with Streamlit

We'll use Streamlit as the primary tool for creating an interactive dashboard, with Plotly for interactive visualizations:

1. **Input Controls**
   - Sliders for all simulation parameters
   - Dropdown for allocation strategies
   - Buttons to run/reset simulation
   - Save/load configuration options

2. **Output Visualizations with Plotly**
   - Interactive time series of funding pool balance
   - Dynamic bar charts of grantee allocations over time
   - Network graph of member-grantee relationships
   - Distribution statistics with interactive plots

3. **Comparative Analysis**
   - Side-by-side comparison of multiple simulation runs
   - Parameter sensitivity analysis with heatmaps
   - Statistical summaries of multiple runs

4. **Batch Simulation Features**
   - Run multiple simulations with parameter sweeps
   - Monte Carlo simulations with random parameter variations
   - Progress tracking for long-running simulations

### 5. Analysis Metrics

Define metrics to evaluate simulation outcomes:

1. **Funding Distribution**
   - Gini coefficient (inequality measure)
   - Concentration ratio (% of funds to top N grantees)
   - Funding stability (variance over time)

2. **System Efficiency**
   - Allocation participation rate
   - Time to distribute funds
   - Administrative overhead (if modeled)

3. **Outcome Metrics**
   - Correlation between grantee quality and funding
   - Funding adequacy (% of grantees receiving sufficient funds)
   - Member satisfaction (if modeled)

### 6. Implementation Plan

1. **Phase 1: Core Simulation**
   - Implement basic models (Council, Member, Grantee)
   - Create simple allocation strategies
   - Build command-line simulation runner

2. **Phase 2: Streamlit Dashboard**
   - Develop Plotly visualizations for key metrics
   - Create interactive Streamlit dashboard
   - Implement parameter controls and simulation runner

3. **Phase 3: Multi-Simulation Capabilities**
   - Implement parallel simulation runner for efficiency
   - Add parameter sweep functionality
   - Create comparative visualization tools
   - Implement simulation result caching and export

4. **Phase 4: Advanced Features**
   - Add complex allocation strategies
   - Implement member behavior models
   - Create advanced analysis tools

### 7. Sample Implementation (Core Models)

```python
# models/council.py
import numpy as np
import pandas as pd

class Council:
    def __init__(self, initial_pool, distribution_rate, members=None, grantees=None):
        self.pool_balance = initial_pool
        self.distribution_rate = distribution_rate
        self.members = members or []
        self.grantees = grantees or []
        self.allocations = {}  # member_id -> {grantee_id: amount}
        
    def active_members(self, participation_rate=1.0):
        """Return active members based on participation rate"""
        num_active = int(len(self.members) * participation_rate)
        return np.random.choice(self.members, num_active, replace=False)
    
    def record_allocations(self, member, allocations):
        """Record a member's allocations"""
        self.allocations[member.id] = allocations
        
    def current_allocations(self):
        """Calculate current total allocations per grantee"""
        total_allocations = {grantee.id: 0 for grantee in self.grantees}
        for member_allocations in self.allocations.values():
            for grantee_id, amount in member_allocations.items():
                total_allocations[grantee_id] += amount
        return total_allocations
    
    def distribute_funds(self, month):
        """Distribute funds based on current allocations"""
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
                
        return distribution
```

### 8. Streamlit Dashboard Implementation

```python
# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from models.council import Council
from models.member import Member
from models.grantee import Grantee
from utils.simulation_runner import run_batch_simulations
from utils.helpers import calculate_gini, calculate_concentration_ratio

def main():
    st.set_page_config(layout="wide", page_title="Council Funding Simulator")
    
    st.title("Council Funding Simulation")
    st.write("Adjust parameters and run simulations to analyze funding distribution patterns")
    
    # Create sidebar for parameters
    with st.sidebar:
        st.header("Simulation Parameters")
        
        # Council parameters
        st.subheader("Council Configuration")
        num_members = st.slider("Number of Council Members", 1, 60000, 100)
        
        voting_power_dist = st.selectbox(
            "Voting Power Distribution", 
            ["Equal", "Normal", "Pareto", "Custom"]
        )
        
        initial_pool = st.slider("Initial Funding Pool ($)", 10000, 1000000, 100000)
        distribution_rate = st.slider("Monthly Distribution Rate (%)", 1, 10, 5) / 100
        
        # Grantee parameters
        st.subheader("Grantee Configuration")
        num_grantees = st.slider("Number of Grantees", 1, 100, 10)
        
        # Member behavior
        st.subheader("Member Behavior")
        allocation_strategy = st.selectbox(
            "Allocation Strategy",
            ["Random", "Merit-based", "Popularity-based", "Coalition"]
        )
        participation_rate = st.slider("Member Participation Rate (%)", 10, 100, 80) / 100
        
        # Temporal parameters
        st.subheader("Temporal Parameters")
        duration_months = st.slider("Simulation Duration (months)", 1, 36, 12)
        
        # Multi-simulation options
        st.subheader("Batch Simulation")
        run_multiple = st.checkbox("Run Multiple Simulations", False)
        
        if run_multiple:
            num_simulations = st.slider("Number of Simulations", 2, 100, 10)
            parameter_to_vary = st.selectbox(
                "Parameter to Vary",
                ["None", "Number of Members", "Distribution Rate", "Participation Rate"]
            )
        
    # Run simulation button
    if st.sidebar.button("Run Simulation"):
        with st.spinner("Running simulation..."):
            config = {
                'num_members': num_members,
                'num_grantees': num_grantees,
                'initial_pool': initial_pool,
                'distribution_rate': distribution_rate,
                'voting_power_distribution': voting_power_dist.lower(),
                'participation_rate': participation_rate,
                'allocation_strategy': allocation_strategy.lower(),
                'duration_months': duration_months
            }
            
            if run_multiple and parameter_to_vary != "None":
                # Run batch simulations with parameter variations
                results = run_batch_simulations(config, parameter_to_vary, num_simulations)
                display_batch_results(results, parameter_to_vary)
            else:
                # Run single simulation
                results = run_simulation(config)
                display_results(results)

def display_results(results):
    """Display results for a single simulation run"""
    # Convert results to DataFrame
    df = pd.DataFrame(results)
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["Funding Pool", "Grantee Allocations", "Distribution Metrics", "Network"])
    
    with tab1:
        st.subheader("Funding Pool Balance Over Time")
        fig = px.line(df, x='month', y='pool_remaining', 
                     title="Pool Balance Over Time",
                     labels={"month": "Month", "pool_remaining": "Pool Balance ($)"})
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Funding Distribution to Grantees")
        # Create visualization for grantee allocations
        # ...
    
    with tab3:
        st.subheader("Distribution Metrics")
        # Calculate and display metrics
        # ...
    
    with tab4:
        st.subheader("Member-Grantee Network")
        # Create network visualization
        # ...

def display_batch_results(results, parameter_varied):
    """Display comparative results for multiple simulation runs"""
    st.subheader(f"Comparative Analysis - Varying {parameter_varied}")
    
    # Create visualizations comparing results across simulations
    # ...

if __name__ == "__main__":
    main()
```

### 9. Multi-Simulation Implementation

```python
# utils/simulation_runner.py
import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from models.council import Council
from models.member import Member
from models.grantee import Grantee

def run_simulation(config):
    """Run a single simulation with the given configuration"""
    # Implementation as shown earlier
    # ...

def create_parameter_variations(base_config, parameter, num_variations):
    """Create variations of a parameter for batch simulations"""
    configs = []
    
    if parameter == "Number of Members":
        min_members = 10
        max_members = min(60000, base_config['num_members'] * 10)
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
    
    # Add more parameter variations as needed
    
    return configs

def run_batch_simulations(base_config, parameter_to_vary, num_simulations):
    """Run multiple simulations with variations of a parameter"""
    if parameter_to_vary == "None":
        # Run the same simulation multiple times (Monte Carlo)
        configs = [base_config] * num_simulations
    else:
        # Create variations of the specified parameter
        configs = create_parameter_variations(base_config, parameter_to_vary, num_simulations)
    
    # Run simulations in parallel
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(run_simulation, configs))
    
    return {
        'configs': configs,
        'results': results,
        'parameter_varied': parameter_to_vary
    }
```

## Next Steps

1. **Implement Core Models**: Start with the basic simulation models
2. **Create Streamlit Dashboard**: Build the interactive Streamlit interface with Plotly visualizations
3. **Implement Multi-Simulation Capabilities**: Add functionality to run and compare multiple simulations
4. **Add Advanced Features**: Implement more complex allocation strategies and metrics
5. **Optimize Performance**: Ensure efficient execution for large-scale simulations
6. **Test and Refine**: Run simulations with different parameters and refine the model

This plan provides a comprehensive framework for developing a Python simulation tool using Streamlit and Plotly that can model the Council funding system with various parameters, run multiple simulations efficiently, and visualize the results effectively.
