import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional

from models.council import Council
from models.member import Member
from models.grantee import Grantee
from utils.simulation_runner import run_simulation, run_batch_simulations
from utils.helpers import generate_members, generate_grantees
from visualization.plots import (
    create_funding_pool_plot,
    create_grantee_allocation_plot,
    create_distribution_metrics_plot,
    create_network_plot
)

def run_dashboard():
    """Run the Streamlit dashboard for the Council funding simulation."""
    
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
        
        if voting_power_dist == "Custom":
            power_skew = st.slider("Power Skew (Higher = More Unequal)", 0.0, 1.0, 0.5)
        else:
            power_skew = 0.5
        
        initial_pool = st.slider("Initial Funding Pool ($)", 10000, 1000000, 100000)
        distribution_rate = st.slider("Monthly Distribution Rate (%)", 1, 10, 5) / 100
        
        # Annual funding addition
        annual_funding_addition = st.slider(
            "Annual Funding Addition ($)", 
            0, 1000000, 0, 
            step=10000,
            help="Amount to add to the funding pool at the end of each year"
        )
        
        # Grantee parameters
        st.subheader("Grantee Configuration")
        num_grantees = st.slider("Number of Grantees", 1, 100, 10)
        
        quality_distribution = st.selectbox(
            "Grantee Quality Distribution",
            ["Uniform", "Normal", "Bimodal"]
        )
        
        popularity_correlation = st.slider(
            "Quality-Popularity Correlation", 
            -1.0, 1.0, 0.5,
            help="How strongly grantee quality correlates with popularity"
        )
        
        # Member behavior
        st.subheader("Member Behavior")
        allocation_strategy = st.selectbox(
            "Allocation Strategy",
            ["Random", "Merit-based", "Popularity-based", "Coalition"]
        )
        
        if allocation_strategy == "Coalition":
            coalition_size = st.slider(
                "Coalition Size (%)", 
                10, 100, 30,
                help="Percentage of members in coalitions"
            )
            coalition_focus = st.slider(
                "Coalition Focus", 
                1, min(5, num_grantees), 2,
                help="Number of grantees each coalition supports"
            )
        else:
            coalition_size = 30
            coalition_focus = 2
        
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
                ["None", "Number of Members", "Distribution Rate", "Participation Rate", "Annual Funding Addition"]
            )
    
    # Create config dictionary
    config = {
        'num_members': num_members,
        'num_grantees': num_grantees,
        'initial_pool': initial_pool,
        'distribution_rate': distribution_rate,
        'annual_funding_addition': annual_funding_addition,
        'voting_power_distribution': voting_power_dist.lower(),
        'power_skew': power_skew,
        'quality_distribution': quality_distribution.lower(),
        'popularity_correlation': popularity_correlation,
        'allocation_strategy': allocation_strategy.lower(),
        'coalition_size': coalition_size / 100,
        'coalition_focus': coalition_focus,
        'participation_rate': participation_rate,
        'duration_months': duration_months
    }
    
    # Run simulation button
    if st.sidebar.button("Run Simulation"):
        with st.spinner("Running simulation..."):
            if run_multiple and parameter_to_vary != "None":
                # Run batch simulations with parameter variations
                results = run_batch_simulations(config, parameter_to_vary, num_simulations)
                display_batch_results(results, parameter_to_vary)
            else:
                # Run single simulation
                council, df = run_simulation(config)
                display_results(council, df)

def display_results(council: Council, df: pd.DataFrame):
    """
    Display results for a single simulation run.
    
    Parameters:
    -----------
    council : Council
        Council object with simulation results
    df : pandas.DataFrame
        DataFrame containing simulation history
    """
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["Funding Pool", "Grantee Allocations", "Distribution Metrics", "Network"])
    
    with tab1:
        st.subheader("Funding Pool Balance Over Time")
        fig = create_funding_pool_plot(df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary statistics
        initial_pool = df['pool_balance'].iloc[0] if not df.empty else 0
        final_pool = df['pool_balance'].iloc[-1] if not df.empty else 0
        total_distributed = initial_pool - final_pool
        
        # Check if annual funding was added
        annual_funding = 0
        if 'annual_funding_added' in df.columns:
            annual_funding = df['annual_funding_added'].sum()
            total_distributed += annual_funding
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Initial Pool", f"${initial_pool:,.2f}")
        col2.metric("Annual Funding Added", f"${annual_funding:,.2f}")
        col3.metric("Final Pool", f"${final_pool:,.2f}")
        col4.metric("Total Distributed", f"${total_distributed:,.2f}")
    
    with tab2:
        st.subheader("Funding Distribution to Grantees")
        
        # Allocation plot
        alloc_fig = create_grantee_allocation_plot(df, council.grantees)
        st.plotly_chart(alloc_fig, use_container_width=True)
        
        # Grantee funding table
        st.subheader("Grantee Funding Summary")
        
        grantee_data = []
        for grantee in council.grantees:
            grantee_data.append({
                "ID": grantee.id,
                "Name": grantee.name,
                "Quality": f"{grantee.quality:.2f}",
                "Popularity": f"{grantee.popularity:.2f}",
                "Total Funding": f"${grantee.received_funds:,.2f}",
                "Viable": "Yes" if grantee.is_viable() else "No"
            })
        
        grantee_df = pd.DataFrame(grantee_data)
        st.dataframe(grantee_df, use_container_width=True)
    
    with tab3:
        st.subheader("Distribution Metrics")
        
        # Get metric plots
        metric_figs = create_distribution_metrics_plot(df, council.grantees)
        
        # Display each metric in its own section
        if 'gini' in metric_figs:
            st.plotly_chart(metric_figs['gini'], use_container_width=True)
            
        if 'concentration' in metric_figs:
            st.plotly_chart(metric_figs['concentration'], use_container_width=True)
            
        if 'stability' in metric_figs:
            st.plotly_chart(metric_figs['stability'], use_container_width=True)
    
    with tab4:
        st.subheader("Member-Grantee Network")
        
        # Create network visualization
        html_string = create_network_plot(council)
        st.components.v1.html(html_string, height=600)
        
        # Member statistics
        st.subheader("Member Statistics")
        
        member_data = []
        for member in council.members:
            allocations = council.allocations.get(member.id, {})
            num_grantees_supported = sum(1 for amount in allocations.values() if amount > 0)
            
            member_data.append({
                "ID": member.id,
                "Voting Power": member.voting_power,
                "Strategy": member.strategy.capitalize(),
                "Grantees Supported": num_grantees_supported
            })
        
        member_df = pd.DataFrame(member_data)
        st.dataframe(member_df, use_container_width=True)

def display_batch_results(results: Dict[str, Any], parameter_varied: str):
    """
    Display comparative results for multiple simulation runs.
    
    Parameters:
    -----------
    results : dict
        Dictionary containing batch simulation results
    parameter_varied : str
        Name of the parameter that was varied
    """
    st.subheader(f"Comparative Analysis - Varying {parameter_varied}")
    
    # Extract data
    configs = results['configs']
    simulation_results = results['results']
    
    # Create parameter values for x-axis
    param_values = []
    for config in configs:
        if parameter_varied == "Number of Members":
            param_values.append(config['num_members'])
        elif parameter_varied == "Distribution Rate":
            param_values.append(config['distribution_rate'] * 100)  # Convert to percentage
        elif parameter_varied == "Participation Rate":
            param_values.append(config['participation_rate'] * 100)  # Convert to percentage
        elif parameter_varied == "Annual Funding Addition":
            param_values.append(config['annual_funding_addition'])
        else:
            param_values.append(0)  # Placeholder for unknown parameter
    
    # Extract metrics for each simulation
    final_pool_values = []
    gini_values = []
    concentration_values = []
    
    for council, df in simulation_results:
        # Final pool balance
        final_pool = df['pool_balance'].iloc[-1] if not df.empty else 0
        final_pool_values.append(final_pool)
        
        # Gini coefficient (last month)
        dist_cols = [col for col in df.columns if col.startswith('dist_to_')]
        if dist_cols and not df.empty:
            last_month_df = df.iloc[-1]
            distributions = [last_month_df[col] for col in dist_cols]
            from visualization.plots import calculate_gini
            gini = calculate_gini(distributions)
            gini_values.append(gini)
        else:
            gini_values.append(0)
        
        # Concentration ratio (last month)
        if dist_cols and not df.empty:
            last_month_df = df.iloc[-1]
            distributions = {col.replace('dist_to_', ''): last_month_df[col] for col in dist_cols}
            from visualization.plots import calculate_concentration_ratio
            concentration = calculate_concentration_ratio(distributions, 3)
            concentration_values.append(concentration)
        else:
            concentration_values.append(0)
    
    # Create comparative plots
    tab1, tab2, tab3 = st.tabs(["Final Pool", "Gini Coefficient", "Concentration Ratio"])
    
    with tab1:
        fig1 = px.line(
            x=param_values, 
            y=final_pool_values,
            title=f"Final Pool Balance vs {parameter_varied}",
            labels={"x": parameter_varied, "y": "Final Pool Balance ($)"},
            markers=True
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with tab2:
        fig2 = px.line(
            x=param_values, 
            y=gini_values,
            title=f"Gini Coefficient vs {parameter_varied}",
            labels={"x": parameter_varied, "y": "Gini Coefficient"},
            markers=True
        )
        fig2.update_layout(yaxis=dict(range=[0, 1]))
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab3:
        fig3 = px.line(
            x=param_values, 
            y=concentration_values,
            title=f"Concentration Ratio vs {parameter_varied}",
            labels={"x": parameter_varied, "y": "Concentration Ratio (%)"},
            markers=True
        )
        fig3.update_layout(yaxis=dict(range=[0, 100]))
        st.plotly_chart(fig3, use_container_width=True)
    
    # Display raw data
    st.subheader("Raw Data")
    
    data = []
    for i, (config, (council, _)) in enumerate(zip(configs, simulation_results)):
        row = {
            parameter_varied: param_values[i],
            "Final Pool": final_pool_values[i],
            "Gini Coefficient": gini_values[i],
            "Concentration Ratio": concentration_values[i],
            "Viable Grantees": sum(1 for g in council.grantees if g.is_viable())
        }
        data.append(row)
    
    data_df = pd.DataFrame(data)
    st.dataframe(data_df, use_container_width=True) 