import pulp
from .models import Player

def optimize_team(players, num_bowlers, num_batsmen):
    # Define the problem
    prob = pulp.LpProblem("OptimalCricketTeam", pulp.LpMaximize)

    # Define decision variables
    player_vars = pulp.LpVariable.dicts("Player", players, cat='Binary')

    # Define the objective function (e.g., maximize total runs scored)
    prob += pulp.lpSum([player.total_runs_scored * player_vars[player] for player in players])

    # Define constraints based on creator's preferences
    prob += pulp.lpSum([player_vars[player] for player in players if player.role == 'bowler']) == num_bowlers
    prob += pulp.lpSum([player_vars[player] for player in players if player.role == 'batsman']) == num_batsmen

    # Solve the problem
    prob.solve()

    # Get the selected players
    selected_players = [player for player in players if player_vars[player].varValue == 1]

    return selected_players