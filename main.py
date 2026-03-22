import itertools
from rules import proportional_rule, cea_rule, cel_rule, talmud_rule, talmud_theta_rule
from utils import (
    plot_allocations, 
    plot_gradients, 
    plot_gradients_heatmap, 
    plot_gradients_bar3d,
    plot_gradients_aggregated_heatmap
)
from cache import get_claims_sum

def simulate_bankruptcy(N, E, rule_func):
    """
    Simulates the bankruptcy problem on N agents with E estate.
    The simulation runs on all combinations of claims, where each claim is in 1..E,
    and the sum of claims is strictly greater than E.
    """
    print(f"Starting simulation with N={N}, E={E}, Rule={rule_func.__name__}")
    
    # Generate unique combinations of claims on the agents (ignoring order)
    # Each claim is in the range of 1 to E
    claims_combinations = itertools.combinations_with_replacement(range(1, E + 1), N)
    
    results = []
    
    for claims in claims_combinations:
        # Filter out cases where the total sum of claims is <= estate
        if get_claims_sum(claims) <= E:
            continue
            
        allocation = rule_func(E, list(claims))
        results.append({
            'claims': claims,
            'allocation': allocation
        })
        
    return results

if __name__ == "__main__":
    # parameters
    N = 3
    E = 20
    theta_steps = 4
    
    # We load the rules implemented
    rules_to_plot = [proportional_rule]
    
    # Add 0/theta_steps to theta_steps/theta_steps talmud theta rules dynamically
    for i in range(0, theta_steps + 1):
        theta_val = i / theta_steps
        # Capture theta locally inside lambda to avoid closure issues in the loop
        rule = lambda E, claims, t=theta_val: talmud_theta_rule(E, claims, theta=t)
        if (i == 0):
            rule.__name__ = f"CEL"
        elif (i == theta_steps):
            rule.__name__ = f"CEA"
        elif (i == theta_steps/2):
            rule.__name__ = f"Talmud"
        else:
            rule.__name__ = f"Tal-theta {i}/{theta_steps}"
        rules_to_plot.append(rule)
    
    # Run the dynamic plot logic mapping for 3D surface topology 
    # plot_allocations(N, E, rules_to_plot, simulate_bankruptcy)
    
    # Plot the gradients to analyze marginal gains for Agent 1
    # We now have 3 visualizations for gradients available:
    # plot_gradients(N, E, rules_to_plot, simulate_bankruptcy)
    
    if (N==2):
        print("Plotting discrete Heatmap for Gradients...")
        plot_gradients_heatmap(N, E, rules_to_plot, simulate_bankruptcy)
    elif (N==3):
        print("Plotting 3D Bar Plot for Gradients...")
        plot_gradients_bar3d(N, E, rules_to_plot, simulate_bankruptcy)
    else:
        print(f"Plotting Aggregated Heatmap for N={N} agents...")
        plot_gradients_aggregated_heatmap(N, E, rules_to_plot, simulate_bankruptcy)
