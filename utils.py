import itertools
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import argparse
import math
import typing
from collections import defaultdict
from cache import get_claims_sum


def setup_plotting_grid(num_rules: int):
    """
    Calculates the optimal subplot grid layout for the number of rules and initializes the matplotlib figure.
    Returns: fig, rows, cols
    """
    if num_rules <= 3:
        cols, rows = num_rules, 1
    elif num_rules == 4:
        cols, rows = 2, 2
    elif num_rules <= 6:
        cols, rows = 3, 2
    elif num_rules <= 8:
        cols, rows = 4, 2
    else:
        cols = int(math.ceil(math.sqrt(num_rules)))
        rows = int(math.ceil(num_rules / cols))
    
    fig = plt.figure(figsize=(6 * cols, 5 * rows))
    return fig, rows, cols


def get_marginal_gradient(E, claims, rule_func, alloc_base):
    """
    Calculates the marginal gradient for Agent 1.
    If Agent 1's claim is already at the estate limit (E), the gradient is 0.
    """
    c1 = claims[0]
    if c1 >= E:
        return 0.0
    
    claims_plus = list(claims).copy()
    claims_plus[0] += 1
    alloc_plus = rule_func(E, claims_plus)[0]
    return alloc_plus - alloc_base


def parse_arguments():
    """
    Parses command-line arguments to configure the simulation.
    Returns:
        N: Number of agents
        E: Total estate to distribute
        theta_steps: Granularity parameter for theta-Talmud rules
    """
    parser = argparse.ArgumentParser(description="Bankruptcy Rules Simulation")
    parser.add_argument("-N", type=int, default=None, help="Number of agents (N)")
    parser.add_argument("-E", type=int, default=None, help="Total estate to distribute (E). Defaults to N * AVG_CLAIM if not set.")
    parser.add_argument("--avg_claim", type=int, default=None, help="Average claim cap for each agent.")
    parser.add_argument("--theta_steps", type=int, default=None, help="Granularity of theta-Talmud rules")
    
    args = parser.parse_args()
    
    return args.N, args.avg_claim, args.E, args.theta_steps



def plot_allocations(N, E, rules_list, simulate_func):
    """
    Plots the absolute allocation for Agent 1.
    The output is rendered as a clean 3D smooth surface map (X=c1, Y=c2, Z=avg_allocation).
    For N=2, it maps to a 2D triangulated contour.
    """
    if N < 2:
        print("Error: Allocation surface plotting is only supported for N >= 2.")
        return

    fig, rows, cols = setup_plotting_grid(len(rules_list))
    from collections import defaultdict
    
    for idx, rule_func in enumerate(rules_list):
        if N == 2:
            ax = fig.add_subplot(rows, cols, idx + 1)
        else:
            ax = fig.add_subplot(rows, cols, idx + 1, projection='3d')
            
        results = simulate_func(N, E, rule_func)
        alloc_map: typing.DefaultDict[typing.Tuple[int, int], typing.List[float]] = defaultdict(list)
        
        for res in results:
            claims = list(res['claims'])
            alloc_base = res['allocation'][0]
            
            c1 = claims[0]
            c2 = claims[1]
            alloc_map[(c1, c2)].append(alloc_base)

        X = []
        Y = []
        Z = []
        for (c1, c2), allocs in alloc_map.items():
            X.append(c1)
            Y.append(c2)
            Z.append(sum(allocs) / len(allocs))

        if N == 2:
            surf = ax.tricontourf(X, Y, Z, levels=40, cmap='plasma')
            ax.set_xlabel('Agent 1 Claim ($c_1$)')
            ax.set_ylabel('Agent 2 Claim ($c_2$)')
        else:
            surf = ax.plot_trisurf(X, Y, Z, cmap='plasma', edgecolor='none', alpha=0.9, antialiased=True)
            ax.set_xlabel('Agent 1 Claim ($c_1$)')
            ax.set_ylabel('Agent 2 Claim ($c_2$)')
            ax.set_zlabel('Avg Allocation $x_1$')
            
        ax.set_title(f'{rule_func.__name__} (Allocation $x_1$)')
        fig.colorbar(surf, ax=ax, label='Allocation Magnitude', pad=0.1)

    plt.suptitle(f'Agent 1 Allocation Surface Map (N={N}, E={E})')
    plt.tight_layout()
    plt.show()

def plot_gradients(N, E, rules_list, simulate_func):
    """
    Plots the marginal gradient for Agent 1: 
    f(E, (c1 + 1, c2, ..., cn))[0] - f(E, (c1, c2, ..., cn))[0]
    The output is rendered as a clean 3D smooth surface map (X=c1, Y=c2, Z=avg_gradient).
    For N=2, it maps to a 2D triangulated contour.
    """
    if N < 2:
        print("Error: Gradient surface plotting is only supported for N >= 2.")
        return
        
    fig, rows, cols = setup_plotting_grid(len(rules_list))
    from collections import defaultdict
    
    for idx, rule_func in enumerate(rules_list):
        if N == 2:
            ax = fig.add_subplot(rows, cols, idx + 1)
        else:
            ax = fig.add_subplot(rows, cols, idx + 1, projection='3d')
            
        results = simulate_func(N, E, rule_func)
        grad_map: typing.DefaultDict[typing.Tuple[int, int], typing.List[float]] = defaultdict(list)
        
        for res in results:
            claims = list(res['claims'])
            alloc_base = res['allocation'][0]
            
            grad = get_marginal_gradient(E, claims, rule_func, alloc_base)
            
            c1 = claims[0]
            c2 = claims[1]
            grad_map[(c1, c2)].append(grad)

        X = []
        Y = []
        Z = []
        for (c1, c2), grads in grad_map.items():
            X.append(c1)
            Y.append(c2)
            Z.append(sum(grads) / len(grads))

        if N == 2:
            surf = ax.tricontourf(X, Y, Z, levels=40, cmap='RdYlGn_r', vmin=0, vmax=1)
            ax.set_xlabel('Agent 1 Claim ($c_1$)')
            ax.set_ylabel('Agent 2 Claim ($c_2$)')
            fig.colorbar(surf, ax=ax, label='Gradient Magnitude', pad=0.1)
        else:
            surf = ax.plot_trisurf(X, Y, Z, cmap='RdYlGn_r', edgecolor='none', alpha=0.9, antialiased=True, vmin=0, vmax=1)
            ax.set_zlim(0, 1)
            ax.set_xlabel('Agent 1 Claim ($c_1$)')
            ax.set_ylabel('Agent 2 Claim ($c_2$)')
            ax.set_zlabel('Avg Marginal Gradient $\\Delta x_1$')
            fig.colorbar(surf, ax=ax, label='Avg Gradient Magnitude', pad=0.1)
            
        ax.set_title(f'{rule_func.__name__} ($\\Delta x_1$)')

    plt.suptitle(f'Agent 1 Gradient Surface Map (N={N}, E={E})')
    plt.tight_layout()
    plt.show()

def plot_gradients_heatmap(N, E, rules_list, simulate_func):
    """
    Plots the marginal gradient for Agent 1 as a discrete 2D Heatmap.
    This clearly shows the step-behavior characteristic of bankruptcy rules without blurring boundaries.
    """
    import math
    from collections import defaultdict
    
    fig, rows, cols = setup_plotting_grid(len(rules_list))
    
    for idx, rule_func in enumerate(rules_list):
        ax = fig.add_subplot(rows, cols, idx + 1)
            
        results = simulate_func(N, E, rule_func)
        grad_map: typing.DefaultDict[typing.Tuple[int, int], typing.List[float]] = defaultdict(list)
        
        for res in results:
            claims = list(res['claims'])
            alloc_base = res['allocation'][0]
            
            grad = get_marginal_gradient(E, claims, rule_func, alloc_base)
            
            c1 = claims[0]
            c2 = claims[1]
            grad_map[(c1, c2)].append(grad)

        # Create E x E grid (claims range from 1 to E)
        grid = np.full((E, E), np.nan)
        for (c1, c2), grads in grad_map.items():
            grid[c2-1, c1-1] = sum(grads) / len(grads)

        im = ax.imshow(grid, origin='lower', extent=[0.5, E+0.5, 0.5, E+0.5], cmap='RdYlGn_r', vmin=0, vmax=1)
        ax.set_xlabel('Agent 1 Claim ($c_1$)')
        ax.set_ylabel('Agent 2 Claim ($c_2$)')
            
        fig.colorbar(im, ax=ax, label='Avg Marginal Gradient $\\Delta x_1$', pad=0.1)
        ax.set_title(f'{rule_func.__name__} ($\\Delta x_1$)')

    plt.suptitle(f'Agent 1 Gradient Heatmap Map (N={N}, E={E})')
    plt.tight_layout()
    plt.show()

def plot_gradients_bar3d(N, E, rules_list, simulate_func):
    """
    Plots the marginal gradient for Agent 1 as a 3D bar chart.
    This emphasizes that both claims and gradients are mathematically discrete.
    """
    if N < 3:
        print("Error: 3D gradient bar plot mapping c2 and c3 is only supported for N >= 3.")
        return
        
    import math
    from collections import defaultdict
    
    fig, rows, cols = setup_plotting_grid(len(rules_list))
    
    for idx, rule_func in enumerate(rules_list):
        ax = fig.add_subplot(rows, cols, idx + 1, projection='3d')
            
        results = simulate_func(N, E, rule_func)
        grad_map: typing.DefaultDict[typing.Tuple[int, int], typing.List[float]] = defaultdict(list) # type: ignore
        
        for res in results:
            claims = list(res['claims'])
            alloc_base = res['allocation'][0]
            
            grad = get_marginal_gradient(E, claims, rule_func, alloc_base)
            
            c2 = claims[1]
            c3 = claims[2]
            grad_map[(c2, c3)].append(grad)

        X, Y, Z = [], [], []
        for (c2, c3), grads in grad_map.items():
            X.append(c2)
            Y.append(c3)
            Z.append(sum(grads) / len(grads))

        x = np.array(X) - 0.5
        y = np.array(Y) - 0.5
        z = np.zeros_like(x)
        dx = np.ones_like(x)
        dy = np.ones_like(x)
        dz = np.array(Z)

        cmap = plt.get_cmap('RdYlGn_r')
        norm = plt.Normalize(0, 1)
        colors = cmap(norm(dz))

        ax.bar3d(x, y, z, dx, dy, dz, color=colors, shade=True, alpha=0.9)
        ax.set_xlabel('Agent 2 Claim ($c_2$)')
        ax.set_ylabel('Agent 3 Claim ($c_3$)')
        ax.set_zlabel("Agent 1's Avg Marginal Gradient $\\Delta x_1$")
        ax.set_zlim(0, 1)
        
        sm = cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        fig.colorbar(sm, ax=ax, label='Avg Gradient Magnitude', pad=0.1)

        ax.set_title(f'{rule_func.__name__} ($\\Delta x_1$)')

    plt.suptitle(f'Agent 1 Gradient 3D Bar Plot (N={N}, E={E})')
    plt.tight_layout()
    plt.show()

def plot_gradients_aggregated_heatmap(N, E, rules_list, simulate_func):
    """
    Plots the marginal gradient for Agent 1 as a heatmap for each rule.
    X-axis: Agent 1's claim (c1)
    Y-axis: Sum of all claims (C)
    Color: Avg Marginal Gradient (Delta x_1)
    """
    fig, rows, cols = setup_plotting_grid(len(rules_list))
    
    # Determine range of X (c1) and Y (C)
    x_min, x_max = 1, E
    y_min, y_max = N, N * E
    
    x_range = x_max - x_min + 1
    y_range = y_max - y_min + 1

    for idx, rule_func in enumerate(rules_list):
        ax = fig.add_subplot(rows, cols, idx + 1)
        
        results = simulate_func(N, E, rule_func)
        # Map (c1, sum_all) -> list of gradients
        aggregated_data: typing.DefaultDict[typing.Tuple[int, int], typing.List[float]] = defaultdict(list)
        
        for res in results:
            claims = list(res['claims'])
            c1 = claims[0]
            c_total = sum(claims)
            
            alloc_base = res['allocation'][0]
            grad = get_marginal_gradient(E, claims, rule_func, alloc_base)
            
            aggregated_data[(c1, c_total)].append(grad)

        grid = np.full((y_range, x_range), np.nan)
        
        for (c1, c_total), grads in aggregated_data.items():
            # Use average gradient for the pixel color
            val = np.mean(grads)
            # Grid indexing: y is rows (c_total), x is columns (c1)
            grid[c_total - y_min, c1 - x_min] = val

        im = ax.imshow(grid, origin='lower', 
                       extent=[x_min - 0.5, x_max + 0.5, y_min - 0.5, y_max + 0.5],
                       aspect='auto', cmap='RdYlGn_r', vmin=0, vmax=1)
        
        ax.set_title(f'{rule_func.__name__} (Avg $\\Delta x_1$)')
        ax.set_xlabel('Agent 1 Claim ($c_1$)')
        ax.set_ylabel('Sum of All Claims ($C$)')
        fig.colorbar(im, ax=ax, label='Gradient Magnitude')

    plt.suptitle(f'Agent 1 Gradient Aggregation Map (N={N}, E={E})')
    plt.tight_layout()
    plt.show()

def plot_gradients_histogram(N, E, rules_list, simulate_func):
    """
    Plots a histogram of the marginal gradient for Agent 1 for each rule.
    X-axis: Marginal gradient value (0 to 1)
    Y-axis: Frequency (how many claim combinations produced that gradient)
    This allows easy comparison of the gradient distributions across rules.
    """
    fig, rows, cols = setup_plotting_grid(len(rules_list))
    
    for idx, rule_func in enumerate(rules_list):
        ax = fig.add_subplot(rows, cols, idx + 1)
            
        results = simulate_func(N, E, rule_func)
        gradients = []
        
        for res in results:
            claims = list(res['claims'])
            alloc_base = res['allocation'][0]
            grad = get_marginal_gradient(E, claims, rule_func, alloc_base)
            gradients.append(grad)

        ax.hist(gradients, bins=50, range=(0, 1), color='steelblue', edgecolor='black', alpha=0.85)
        ax.set_xlabel('Marginal Gradient $\\Delta x_1$')
        ax.set_ylabel('Frequency')
        ax.set_xlim(0, 1)
        ax.set_title(f'{rule_func.__name__}')

    plt.suptitle(f'Agent 1 Marginal Gradient Distribution (N={N}, E={E})')
    plt.tight_layout()
    plt.show()
