"""
Q2: Probability Brewers Face Padres in NLDS (with wins/losses tracked)
Author: Akshith Chappidi
"""

import random

# --- Initial Wins/Losses as of Sept 23, 2025 ---
teams = {
    "Brewers": {"W": 95, "L": 62},
    "Phillies": {"W": 92, "L": 64},
    "Dodgers": {"W": 88, "L": 68},
    "Cubs": {"W": 88, "L": 68},
    "Padres": {"W": 86, "L": 71},
    "Mets": {"W": 80, "L": 76},
    "Reds": {"W": 80, "L": 76},
    "DBacks": {"W": 79, "L": 77},
}

# --- Remaining Head-to-Head Series (team1, team2, number of games) ---
series = [
    ("Dodgers", "DBacks", 3),
    ("Cubs", "Mets", 3),
    ("Brewers", "Padres", 2),
]

# --- Tiebreaker Order (given standings) ---
tiebreak_order = ["Brewers", "Phillies", "Dodgers", "Cubs", "Padres", "Mets", "Reds", "DBacks"]

# --- Helper Functions ---
def simulate_regular_season(rng: random.Random) -> dict:
    """Simulate remaining games and return final win/loss totals."""
    # Deep copy starting records
    wins = {t: d["W"] for t, d in teams.items()}
    losses = {t: d["L"] for t, d in teams.items()}

    for t1, t2, games in series:
        for _ in range(games):
            if rng.random() < 0.5:  # 50/50 win chance
                wins[t1] += 1
                losses[t2] += 1
            else:
                wins[t2] += 1
                losses[t1] += 1

    # Other teams (Phillies, Reds) assumed 3 random neutral games
    for team in ["Phillies", "Reds"]:
        for _ in range(3):
            if rng.random() < 0.5:
                wins[team] += 1
            else:
                losses[team] += 1

    return {"W": wins, "L": losses}


def assign_seeds(wins: dict) -> list:
    """Assign top 6 teams by win total and tiebreaker order."""
    sorted_teams = sorted(wins.items(), key=lambda x: (-x[1], tiebreak_order.index(x[0])))
    return [team for team, _ in sorted_teams[:6]]


def simulate_series(team_high: str, team_low: str, rng: random.Random, p_high=0.55) -> str:
    """Simulate best-of-three series; higher seed wins each game with probability p_high."""
    wins_high = wins_low = 0
    while wins_high < 2 and wins_low < 2:
        if rng.random() < p_high:
            wins_high += 1
        else:
            wins_low += 1
    return team_high if wins_high == 2 else team_low


def simulate_season(rng: random.Random) -> dict:
    """Simulate a full season + Wild Card and record various outcomes."""
    season = simulate_regular_season(rng)
    wins = season["W"]

    # Assign final playoff seeds (top 6)
    seeds = assign_seeds(wins)
    seed_map = {i + 1: seeds[i] for i in range(6)}

    padres_5_seed = seed_map.get(5) == "Padres"

    # Wild Card Round (3 vs 6 and 4 vs 5)
    four, five = seed_map[4], seed_map[5]
    wc45_winner = simulate_series(four, five, rng)

    padres_vs_cubs_wc = (four == "Padres" and five == "Cubs") or (four == "Cubs" and five == "Padres")
    padres_wc_win = wc45_winner == "Padres"

    # Brewers face 4–5 winner in NLDS if they remain seed #1
    brewers_vs_padres_nlds = seed_map[1] == "Brewers" and wc45_winner == "Padres"

    return {
        "padres_5_seed": padres_5_seed,
        "padres_vs_cubs_wc": padres_vs_cubs_wc,
        "padres_wc_win": padres_wc_win,
        "brewers_vs_padres_nlds": brewers_vs_padres_nlds,
    }


def estimate_probability(trials: int = 200_000, seed: int = 2025) -> dict:
    """Monte Carlo estimate for various Padres and Brewers playoff outcomes."""
    rng = random.Random(seed)
    counts = {
        "padres_5_seed": 0,
        "padres_vs_cubs_wc": 0,
        "padres_wc_win": 0,
        "brewers_vs_padres_nlds": 0,
    }

    for _ in range(trials):
        result = simulate_season(rng)
        for key in counts:
            if result[key]:
                counts[key] += 1

    frequencies = {k: v / trials for k, v in counts.items()}
    return frequencies


if __name__ == "__main__":
    trials = 200_000
    freq = estimate_probability(trials)
    print(f"Padres #5 seed frequency: {freq['padres_5_seed']:.3f}")
    print(f"Padres vs Cubs Wild Card matchup frequency: {freq['padres_vs_cubs_wc']:.3f}")
    print(f"Padres Wild Card win rate: {freq['padres_wc_win']:.3f}")
    print(f"Estimated Probability (Brewers vs Padres NLDS): {freq['brewers_vs_padres_nlds']:.4f}")