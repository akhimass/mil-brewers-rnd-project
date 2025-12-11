"""
Q3: Contract Extension Simulation — Pitcher Valuation
Author: Akshith Chappidi
Description:
  Monte Carlo simulation comparing a 6-year year-to-year contract
  versus an 8-year guaranteed deal to solve for X (2032–2033 salary)
  where both contracts have equal expected team value.
"""

import random
import numpy as np

# --- Parameters ---
WAR_to_dollars = 8.0          # $8M per WAR (market conversion)
injury_prob = 0.20            # 20% chance of full-season injury
WAR_drop_if_injured = 1.5     # Next-season WAR penalty
trials = 100_000              # Monte Carlo trials

# --- Season data ---
years = [2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033]
proj_WAR = [3.2, 3.5, 3.7, 3.4, 3.2, 3.0, 2.8, 2.6]

# Year-to-year salary matrix (if injured prev / if healthy prev / guaranteed)
salaries = {
    2026: (0.8, 0.8, 2.0),
    2027: (0.85, 0.85, 2.5),
    2028: (0.9, 0.9, 4.5),
    2029: (2.8, 4.8, 7.5),
    2030: (5.25, 9.0, 10.5),
    2031: (9.10, 15.6, 14.5),
}

def simulate_contract(X, rng=random.Random(2025)):
    """Simulate expected team value difference between the two contracts."""
    total_y2y_value = 0.0
    total_guaranteed_value = 0.0

    for _ in range(trials):
        prev_injured = False
        war_projection = proj_WAR.copy()
        y2y_value = 0.0
        guaranteed_value = 0.0

        for i, year in enumerate(years):
            # Determine injury this season
            injured = rng.random() < injury_prob

            # --- WAR outcome ---
            war = 0.0 if injured else war_projection[i]
            salary_y2y = 0.0

            # --- Year-to-year logic (stop after 2031) ---
            if year <= 2031:
                # Determine salary depending on prior injury
                s_inj, s_healthy, s_g = salaries[year]
                salary_y2y = s_inj if prev_injured else s_healthy
                y2y_value += (war * WAR_to_dollars) - salary_y2y

            # --- Guaranteed contract logic (full 8 years) ---
            if year <= 2031:
                s_inj, s_healthy, s_g = salaries[year]
                guaranteed_value += (war * WAR_to_dollars) - s_g
            else:
                guaranteed_value += (war * WAR_to_dollars) - X  # use X for 2032–2033

            # Apply next-year WAR penalty if injured
            if injured and i + 1 < len(war_projection):
                war_projection[i + 1] = max(0, war_projection[i + 1] - WAR_drop_if_injured)
            prev_injured = injured

        total_y2y_value += y2y_value
        total_guaranteed_value += guaranteed_value

    # Return average expected values
    return total_y2y_value / trials, total_guaranteed_value / trials


def find_break_even(low=5, high=20, tol=0.01):
    """Binary search for X that equalizes expected team value."""
    rng = random.Random(2025)
    while high - low > tol:
        mid = (low + high) / 2
        y2y, guaranteed = simulate_contract(mid, rng)
        if guaranteed > y2y:
            high = mid  # Guaranteed too favorable to player → lower X
        else:
            low = mid   # Guaranteed too cheap → raise X
    return (low + high) / 2


if __name__ == "__main__":
    X_break_even = find_break_even()
    print(f"Break-even guaranteed salary (X) for 2032–2033 ≈ ${X_break_even:.2f}M per year")