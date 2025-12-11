"""
Q1: Walk-Off Probability Simulation
Author: Akshith Chappidi
Description:
  Estimate the single probability p for Batters 4 and 5 such that
  the home team has a 20% chance to win (score >=3 runs before 3 outs).
"""

import random

# Batter outcome probabilities (K, 1B, HR), except 4 & 5 depend on p
FIXED = [
    (0.6, 0.3, 0.1),
    (0.6, 0.3, 0.1),
    (0.6, 0.25, 0.15),
    None,  # Batter 4
    None,  # Batter 5
    (0.6, 0.25, 0.15),
    (0.6, 0.3, 0.1),
    (0.6, 0.3, 0.1),
    (0.6, 0.3, 0.1),
]

def simulate_inning(p: float, rng: random.Random) -> bool:
    """Simulate one inning; return True if team scores >=3 before 3 outs."""
    batters = list(FIXED)
    batters[3] = (0.9 - p, p, 0.1)
    batters[4] = (0.9 - p, p, 0.1)

    runs, outs = 0, 0
    on1 = on2 = on3 = 0
    i = 0
    while outs < 3 and runs < 3:
        k, s, hr = batters[i % 9]
        r = rng.random()
        if r < k:
            outs += 1
        elif r < k + s:
            # Single: advance two bases
            runs += on2 + on3
            on1, on2, on3 = 1, on1, 0
        else:
            # Homerun: batter + all runners score
            runs += 1 + on1 + on2 + on3
            on1 = on2 = on3 = 0
        i += 1
    return runs >= 3

def win_prob(p: float, sims: int = 200_000, seed: int = 42) -> float:
    rng = random.Random(seed)
    return sum(simulate_inning(p, rng) for _ in range(sims)) / sims

def find_p_for_target(target: float = 0.20, tol: float = 0.002):
    lo, hi = 0.0, 0.9
    for step in range(12):
        mid = (lo + hi) / 2
        prob = win_prob(mid, 120_000, seed=step * 31)
        if prob < target:
            lo = mid
        else:
            hi = mid
    p_star = (lo + hi) / 2
    final_prob = win_prob(p_star, 500_000, seed=2025)
    return p_star, final_prob

if __name__ == "__main__":
    p_est, prob = find_p_for_target()
    print(f"Estimated p: {p_est:.4f}  ->  Win Prob: {prob:.4f}")