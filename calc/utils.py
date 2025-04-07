from collections import defaultdict
from pulp import LpMaximize, LpProblem, LpVariable, lpSum

def solve_lp(data, group_size=3):
    students = list(range(len(data)))
    groups = list(range(len(data) // group_size))

    prob = LpProblem("StudyGroupBalancer", LpMaximize)

    x = {(i, g): LpVariable(f"x_{i}_{g}", cat='Binary') for i in students for g in groups}

    # 1. Each student is assigned to one group
    for i in students:
        prob += lpSum(x[i, g] for g in groups) == 1

    # 2. Group size constraint
    for g in groups:
        prob += lpSum(x[i, g] for i in students) <= group_size

    # 3. Maximize skill balance across groups
    skill_balances = []
    for g in groups:
        group_skill = lpSum(x[i, g] * data[i]['skill'] for i in students)
        skill_balances.append(group_skill)
    prob += lpSum(skill_balances)

    prob.solve()

    # Group result
    final_groups = defaultdict(list)
    for i in students:
        for g in groups:
            if x[i, g].varValue == 1:
                final_groups[g].append(data[i])

    return dict(final_groups)
