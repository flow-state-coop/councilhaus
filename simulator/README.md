# Council Funding Simulator

A Python-based simulation tool for modeling funding rounds using the Council contracts. This tool allows you to explore different parameters and strategies for allocating funds to grantees.

## Features

- Simulate council members with different voting power distributions
- Model various allocation strategies (random, merit-based, popularity-based, coalition)
- Visualize funding distribution and metrics over time
- Run batch simulations to compare different parameters
- Interactive Streamlit dashboard for easy parameter adjustment
- Simulate annual funding additions to the pool

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd councilhaus/simulator
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Streamlit Dashboard

The easiest way to use the simulator is through the Streamlit dashboard:

```
streamlit run app.py
```

This will open a web browser with an interactive dashboard where you can:
- Adjust simulation parameters using sliders and dropdowns
- Run single or batch simulations
- View visualizations of the results
- Compare different parameter configurations

### Command Line Interface

You can also run simulations from the command line:

```
python main.py --num_members 100 --num_grantees 10 --initial_pool 100000 --distribution_rate 0.05 --duration_months 12
```

For batch simulations, use the `--batch` flag:

```
python main.py --batch --parameter_to_vary "Number of Members" --num_simulations 10 --output results.csv
```

Run `python main.py --help` to see all available options.

## Simulation Parameters

### Council Configuration
- **Number of Members**: Number of council members (1-60,000)
- **Voting Power Distribution**: How voting power is distributed among members (Equal, Normal, Pareto, Custom)
- **Initial Funding Pool**: Starting amount in the funding pool ($10,000-$1,000,000)
- **Distribution Rate**: Monthly percentage of the pool distributed (1%-10%)
- **Annual Funding Addition**: Amount added to the funding pool at the end of each year ($0-$1,000,000)

### Grantee Configuration
- **Number of Grantees**: Number of projects receiving funding (1-100)
- **Quality Distribution**: How project quality is distributed (Uniform, Normal, Bimodal)
- **Quality-Popularity Correlation**: Relationship between quality and popularity (-1.0 to 1.0)

### Member Behavior
- **Allocation Strategy**: How members allocate their voting power (Random, Merit-based, Popularity-based, Coalition)
- **Participation Rate**: Percentage of members who participate in allocation (10%-100%)
- **Coalition Size**: Percentage of members in coalitions (for Coalition strategy)

### Temporal Parameters
- **Simulation Duration**: Number of months to simulate (1-36)

## Analysis Metrics

The simulator provides several metrics to evaluate funding outcomes:

- **Gini Coefficient**: Measures inequality in funding distribution (0 = perfect equality, 1 = perfect inequality)
- **Concentration Ratio**: Percentage of funds allocated to top N grantees
- **Funding Stability**: Coefficient of variation in monthly funding for each grantee
- **Viability**: Whether grantees received enough funding to meet their minimum threshold

## Project Structure

```
simulator/
├── data/                  # Store simulation results
├── models/                # Core simulation models
│   ├── council.py         # Council model
│   ├── member.py          # Council member model
│   ├── grantee.py         # Grantee model
│   └── allocation.py      # Allocation strategies
├── visualization/         # Visualization components
│   ├── dashboard.py       # Streamlit dashboard
│   └── plots.py           # Plotting functions
├── utils/                 # Utility functions
│   ├── helpers.py         # Helper functions
│   └── simulation_runner.py # Simulation runner
├── config.py              # Configuration settings
├── main.py                # Command-line entry point
├── app.py                 # Streamlit app entry point
└── requirements.txt       # Dependencies
```

## License

This project is licensed under the AGPL License - see the LICENSE file for details. 