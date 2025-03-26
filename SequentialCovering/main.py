import numpy as np
from itertools import combinations

data = np.array([
    [1, 1, 1, 1, 3, 1, 1],
    [1, 1, 1, 1, 3, 2, 1],
    [1, 1, 1, 3, 2, 1, 0],
    [1, 1, 1, 3, 3, 2, 1],
    [1, 1, 2, 1, 2, 1, 0],
    [1, 1, 2, 1, 2, 2, 1],
    [1, 1, 2, 2, 3, 1, 0],
    [1, 1, 2, 2, 4, 1, 1]
])

decision_idx = data.shape[1] - 1
covered = [False] * len(data)
rules = []


def check_rule(rule):
    decisions = set(row[decision_idx] for row in data if all(row[attr] == val for attr, val in rule))
    if len(decisions) == 1:
        return decisions.pop()
    return None


order = 1
max_order = data.shape[1] - 1  # Maksymalna długość reguły

while not all(covered) and order <= max_order:
    found_new_rule = False

    for i, row in enumerate(data):
        if covered[i]:
            continue

        for combo in combinations(range(data.shape[1] - 1), order):
            rule = [(attr, row[attr]) for attr in combo]
            decision = check_rule(rule)

            if decision is not None:
                # Oblicz wsparcie i zaktualizuj pokrycie
                support = 0
                for j, other_row in enumerate(data):
                    if all(other_row[attr] == val for attr, val in rule) and other_row[decision_idx] == decision:
                        support += 1
                        covered[j] = True

                rules.append((rule, decision, support))
                found_new_rule = True
                break

        if found_new_rule:
            break

    # Jeśli nie znaleziono nowej reguły, zwiększ długość reguły
    if not found_new_rule:
        order += 1

# Wypisz reguły
for rule, decision, support in rules:
    rule_str = ' i '.join([f'a{attr + 1} = {val}' for attr, val in rule])
    print(f'{rule_str} => decyzja = {decision} [[[wsparcie]]: {support}]')