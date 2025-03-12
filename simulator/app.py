#!/usr/bin/env python3
"""
Streamlit app entry point for the Council funding simulation.
"""

import streamlit as st
import numpy as np
import os
import sys
from pathlib import Path

# Add the current directory to the path to ensure imports work correctly
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Set page title and favicon - MUST be the first Streamlit command
st.set_page_config(
    page_title="Council Funding Simulator",
    page_icon="💰",
    layout="wide"
)

# Import after path setup
from visualization.dashboard import run_dashboard
from config import DEFAULT_CONFIG, DATA_PATHS

def setup_directories():
    """Create necessary directories if they don't exist."""
    for path in DATA_PATHS.values():
        Path(path).mkdir(parents=True, exist_ok=True)

def main():
    """Main function to run the Streamlit app."""
    # Create necessary directories
    setup_directories()
    
    # Set random seed for reproducibility
    np.random.seed(DEFAULT_CONFIG['random_seed'])
    
    # Run the dashboard
    run_dashboard()

if __name__ == "__main__":
    main() 