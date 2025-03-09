import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import networkx as nx
from pyvis.network import Network
import tempfile
import os
from typing import List, Dict, Any, Optional

def create_funding_pool_plot(df: pd.DataFrame) -> go.Figure:
    """
    Create a line plot of the funding pool balance over time.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing simulation history with 'month' and 'pool_balance' columns
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Plotly figure object
    """
    fig = px.line(
        df, 
        x='month', 
        y='pool_balance',
        title="Funding Pool Balance Over Time",
        labels={"month": "Month", "pool_balance": "Pool Balance ($)"},
        markers=True
    )
    
    # Add markers for annual funding additions
    if 'annual_funding_added' in df.columns:
        annual_funding_months = df[df['annual_funding_added'] > 0]['month'].tolist()
        annual_funding_amounts = df[df['annual_funding_added'] > 0]['annual_funding_added'].tolist()
        annual_funding_balances = df[df['annual_funding_added'] > 0]['pool_balance'].tolist()
        
        if annual_funding_months:
            # Add annotations for annual funding additions
            for i, month in enumerate(annual_funding_months):
                fig.add_annotation(
                    x=month,
                    y=annual_funding_balances[i],
                    text=f"+${annual_funding_amounts[i]:,.0f}",
                    showarrow=True,
                    arrowhead=1,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor="#28a745",
                    ax=0,
                    ay=-40
                )
            
            # Add vertical lines for year boundaries
            for month in annual_funding_months:
                fig.add_vline(
                    x=month, 
                    line_dash="dash", 
                    line_color="#28a745",
                    opacity=0.5,
                    annotation_text="Year End",
                    annotation_position="top right"
                )
    
    fig.update_layout(
        xaxis=dict(tickmode='linear'),
        hovermode="x unified",
        plot_bgcolor='white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

def create_grantee_allocation_plot(df: pd.DataFrame, grantees: List[Any]) -> go.Figure:
    """
    Create a stacked bar chart of grantee allocations over time.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing simulation history with allocation columns
    grantees : list
        List of Grantee objects
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Plotly figure object
    """
    # Extract allocation columns
    allocation_cols = [col for col in df.columns if col.startswith('alloc_to_')]
    
    if not allocation_cols:
        # Create empty figure if no allocation data
        fig = go.Figure()
        fig.update_layout(
            title="No Allocation Data Available",
            xaxis_title="Month",
            yaxis_title="Allocation Amount"
        )
        return fig
    
    # Create figure
    fig = go.Figure()
    
    # Add trace for each grantee
    for col in allocation_cols:
        grantee_id = col.replace('alloc_to_', '')
        grantee_name = next((g.name for g in grantees if g.id == grantee_id), grantee_id)
        
        fig.add_trace(go.Bar(
            x=df['month'],
            y=df[col],
            name=grantee_name
        ))
    
    # Update layout
    fig.update_layout(
        title="Grantee Allocations Over Time",
        xaxis_title="Month",
        yaxis_title="Allocation Amount",
        barmode='stack',
        hovermode="x unified",
        plot_bgcolor='white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

def create_distribution_metrics_plot(df: pd.DataFrame, grantees: List[Any]) -> Dict[str, go.Figure]:
    """
    Create plots for distribution metrics.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing simulation history
    grantees : list
        List of Grantee objects
        
    Returns:
    --------
    dict
        Dictionary mapping metric names to Plotly figure objects
    """
    figures = {}
    
    # Extract distribution columns
    dist_cols = [col for col in df.columns if col.startswith('dist_to_')]
    
    if not dist_cols:
        # Create empty figure if no distribution data
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="No Distribution Data Available",
            xaxis_title="Month",
            yaxis_title="Amount"
        )
        figures['empty'] = empty_fig
        return figures
    
    # 1. Gini coefficient over time
    gini_values = []
    months = df['month'].tolist()
    
    for month in months:
        month_df = df[df['month'] == month]
        distributions = [month_df[col].iloc[0] for col in dist_cols]
        gini = calculate_gini(distributions)
        gini_values.append(gini)
    
    gini_fig = px.line(
        x=months,
        y=gini_values,
        title="Gini Coefficient Over Time (Higher = More Inequality)",
        labels={"x": "Month", "y": "Gini Coefficient"},
        markers=True
    )
    
    gini_fig.update_layout(
        xaxis=dict(tickmode='linear'),
        yaxis=dict(range=[0, 1]),
        hovermode="x unified",
        plot_bgcolor='white'
    )
    
    figures['gini'] = gini_fig
    
    # 2. Concentration ratio (% to top 3 grantees)
    concentration_values = []
    
    for month in months:
        month_df = df[df['month'] == month]
        distributions = {col.replace('dist_to_', ''): month_df[col].iloc[0] for col in dist_cols}
        concentration = calculate_concentration_ratio(distributions, 3)
        concentration_values.append(concentration)
    
    concentration_fig = px.line(
        x=months,
        y=concentration_values,
        title="Concentration Ratio Over Time (% to Top 3 Grantees)",
        labels={"x": "Month", "y": "Concentration Ratio (%)"},
        markers=True
    )
    
    concentration_fig.update_layout(
        xaxis=dict(tickmode='linear'),
        yaxis=dict(range=[0, 100]),
        hovermode="x unified",
        plot_bgcolor='white'
    )
    
    figures['concentration'] = concentration_fig
    
    # 3. Funding stability (coefficient of variation)
    if len(months) > 1:
        stability_data = []
        
        for col in dist_cols:
            grantee_id = col.replace('dist_to_', '')
            grantee_name = next((g.name for g in grantees if g.id == grantee_id), grantee_id)
            values = df[col].tolist()
            cv = np.std(values) / np.mean(values) if np.mean(values) > 0 else 0
            
            stability_data.append({
                'grantee': grantee_name,
                'stability': cv
            })
        
        stability_df = pd.DataFrame(stability_data)
        
        stability_fig = px.bar(
            stability_df,
            x='grantee',
            y='stability',
            title="Funding Stability by Grantee (Lower = More Stable)",
            labels={"grantee": "Grantee", "stability": "Coefficient of Variation"}
        )
        
        stability_fig.update_layout(
            xaxis=dict(tickangle=45),
            plot_bgcolor='white'
        )
        
        figures['stability'] = stability_fig
    
    return figures

def create_network_plot(council, month: Optional[int] = None) -> str:
    """
    Create a network visualization of member-grantee relationships.
    
    Parameters:
    -----------
    council : Council
        Council object containing members and grantees
    month : int, optional
        Specific month to visualize (defaults to latest)
        
    Returns:
    --------
    str
        HTML string of the network visualization
    """
    # Create network graph
    G = nx.Graph()
    
    # Add member nodes
    for member in council.members:
        G.add_node(f"m_{member.id}", label=f"Member {member.id}", group=1, size=10 + member.voting_power/100)
    
    # Add grantee nodes
    for grantee in council.grantees:
        G.add_node(f"g_{grantee.id}", label=grantee.name, group=2, size=10)
    
    # Add edges based on allocations
    for member_id, allocations in council.allocations.items():
        for grantee_id, amount in allocations.items():
            if amount > 0:
                G.add_edge(f"m_{member_id}", f"g_{grantee_id}", weight=amount, title=f"Allocation: {amount}")
    
    # Create PyVis network
    net = Network(notebook=True, height="600px", width="100%")
    net.from_nx(G)
    
    # Set node colors
    for node in net.nodes:
        if node['group'] == 1:  # Member
            node['color'] = '#4285F4'
        else:  # Grantee
            node['color'] = '#EA4335'
    
    # Generate HTML
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp:
        net.save_graph(tmp.name)
        with open(tmp.name, 'r') as f:
            html_string = f.read()
        os.unlink(tmp.name)
    
    return html_string

def calculate_gini(values: List[float]) -> float:
    """
    Calculate the Gini coefficient for a list of values.
    
    Parameters:
    -----------
    values : list
        List of numerical values
        
    Returns:
    --------
    float
        Gini coefficient (0 = perfect equality, 1 = perfect inequality)
    """
    if not values or sum(values) == 0:
        return 0
    
    # Sort values
    sorted_values = sorted(values)
    n = len(sorted_values)
    
    # Calculate Gini coefficient
    index = np.arange(1, n + 1)
    return (2 * np.sum(index * sorted_values) / (n * np.sum(sorted_values))) - (n + 1) / n

def calculate_concentration_ratio(distributions: Dict[str, float], n: int) -> float:
    """
    Calculate the concentration ratio (percentage of funds to top N grantees).
    
    Parameters:
    -----------
    distributions : dict
        Dictionary mapping grantee_id to distribution amount
    n : int
        Number of top grantees to consider
        
    Returns:
    --------
    float
        Concentration ratio as a percentage
    """
    if not distributions:
        return 0
    
    total = sum(distributions.values())
    if total == 0:
        return 0
    
    # Sort grantees by distribution amount
    sorted_grantees = sorted(distributions.items(), key=lambda x: x[1], reverse=True)
    
    # Calculate sum of top N
    top_n_sum = sum(amount for _, amount in sorted_grantees[:n])
    
    return (top_n_sum / total) * 100 