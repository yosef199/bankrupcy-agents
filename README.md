# 📉 Bankruptcy Rules & Gradient Analysis

Welcome to the **Bankruptcy Rules & Gradient Analysis** toolkit. This project explores the mathematical patterns and marginal gains of various allocation rules used in the classic "Bankruptcy Problem" from cooperative game theory.

---

## 🏗️ Background: The Bankruptcy Problem

The **Bankruptcy Problem** occurs when a set of agents $N$ have claims $c_1, c_2, \dots, c_N$ on an estate $E$, but the total demands exceed the available resources:
$$\sum_{i=1}^{n} c_i > E$$

The goal is to determine a "fair" allocation $x = (x_1, x_2, \dots, x_N)$ such that:
1.  **Efficiency**: $\sum x_i = E$
2.  **Claim Boundedness**: $0 \le x_i \le c_i$ for all $i$.

This project implements and visualizes several iconic rules that solve this problem, dating back to the Talmud and modern game theory.

---

## 🎯 Goal of This Codebase

The primary objective of this library is to **simulate and visualize** how different allocation rules behave under various claim distributions. Specifically, it focuses on:
*   **Marginal Gains (Gradients)**: Analyzing how an agent's allocation changes if their claim increases by a discrete unit.
*   **Comparative Analysis**: Side-by-side comparison of rules like proportional, CEA, and the Talmud rule.
*   **Structural Visualization**: Using 3D surface maps, heatmaps, and 3D bar plots to reveal the "step-functions" and "plateaus" inherent in these rules.

---

## ⚖️ Key Variables Explained

| Variable | Description |
| :--- | :--- |
| **$N$ (Agents)** | Number of participants competing for the estate. |
| **`AVG_CLAIM`** | The average claim cap for each agent. |
| **$E$ (Estate)** | Total amount to be distributed. In the default configuration, this is dynamically simulated as $N \times AVG\_CLAIM$. This acts as the "resource constraint." |
| **Claims ($c_i$)** | The demand made by each agent. The simulation iterates through combinations where $c_i \in [1, E]$. |
| **`theta_steps`** | Determines the granularity of the $\theta$-Talmud rules simulation. It defines how many discrete $\theta$ values are tested between 0 (CEL) and 1 (CEA). |

---

## 🧪 Implemented Rules

1.  **Proportional (PROP)**: Divides the estate in proportion to claims ($x_i = E \cdot \frac{c_i}{\sum c_j}$).
2.  **Constrained Equal Awards (CEA)**: Divides the estate equally among all agents, capped at their respective claims. Favors agents with smaller claims.
3.  **Constrained Equal Losses (CEL)**: Divides the *loss* ($\sum c_j - E$) equally among agents. Favors agents with larger claims.
4.  **Talmud Rule**: A hybrid approach proposed by Aumann and Maschler (1985). It behaves like CEA on half-claims when the estate is small, and like CEL when the estate is large.
5.  **$\theta$-Talmud**: A generalization of the Talmud rule using a parameter $\theta \in [0, 1]$ to shift the behavior between CEL ($\theta=0$) and CEA ($\theta=1$). In the code, `theta_steps` controls how many such rules are dynamically generated for plotting.

---

## 📊 Visualizations

### 1. Allocation Surface Plot
Visualizes the absolute allocation $x_1$ for Agent 1 as a function of $c_1$ and $c_2$.
*   **Insight**: Smooth slopes indicate proportional sharing, while plateaus show where an agent has hit their "claim cap" or "estate floor".

### 2. Marginal Gradient (2D Heatmap & 3D Surface)
Calculates $\Delta x_1 = f(E, c_1+1, \dots) - f(E, c_1, \dots)$.
*   **Heatmap ($N=2$)**: Shows the discrete "marginal utility" of increasing your claim.
*   **Surface Plot ($N>2$)**: Averages the gradient over multiple claim configurations to show general trends.

### 3. 3D Bar Plots (The Discrete View)
For $N = 3$, this plot maps the marginal gradient of Agent 1 against the claims of Agent 2 and Agent 3 ($c_2, c_3$).
*   **Why Bars?**: Bankruptcy rules operate on discrete claims. Bar plots emphasize that these are not continuous functions, but step-wise allocations.
*   **Color Coding**: Uses a `RdYlGn` colormap, where Green (1.0) indicates a full marginal gain and Red (0.0) indicates zero marginal gain for an extra unit of claim.

### 4. Aggregated Gradient Heatmap (N >= 4)
For larger groups of agents, we generate a consolidated multi-rule heatmap:
*   **X-axis**: $c_1$ (Agent 1's claim).
*   **Y-axis**: $C$ (The total sum of all agents' claims).
*   **Color Coding**: Displays the Average Marginal Gradient ($\Delta x_1$) for that point.
*   **Insight**: This allows us to map Agent 1's absolute claim against the macroeconomic state of the total estate debt ($C$), reducing high-dimensional configurations into clean, digestible heat constraints.

---

## 🚀 How to Run

### Prerequisites
```bash
pip install matplotlib numpy
```

### Execution
Run the main simulation script directly with default parameters ($N=3$, $AVG\_CLAIM=10$, $E=30$, $theta\_steps=4$):
```bash
python main.py
```

You can now easily configure the simulation parameters via command-line arguments:
```bash
# Override N and theta steps (E dynamically becomes 4 * 10 = 40)
python main.py -N 4 --theta_steps 8

# Override N, and explicitly set a custom Estate size bypassing avg_claim calculation
python main.py -N 5 -E 60

# Check all available flag options
python main.py --help
```
You can still modify the rules instantiated inside `rules_to_plot` directly in `main.py` to explore custom rule comparisons.

---

## 💡 Pro-Tips & Design Notes

*   **Caching**: The `cache.py` module handles sum calculations for claim combinations, which significantly speeds up simulations with many agents ($N > 10$).
*   **Extensibility**: To add a new rule, simply define a function `my_rule(E, claims)` in `rules.py` and add it to the `rules_to_plot` list in `main.py`.
*   **Mathematical Fact**: For the Talmud rule ($N=2$), you will notice a distinct "kink" at $\sum c_i = 2E$, representing the transition between equal awards and equal losses.

---
*Created with ❤️ for Game Theorists and Economic Data Scientists.*
