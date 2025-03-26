import itertools
import pandas as pd


def load_decision_system():
    """
    Load the decision system directly as a hardcoded list.
    The last column is considered the decision attribute.
    Returns a DataFrame with the decision system.
    """
    data = [
        [1, 1, 1, 1, 3, 1, 1],
        [1, 1, 1, 1, 3, 2, 1],
        [1, 1, 1, 3, 2, 1, 0],
        [1, 1, 1, 3, 3, 2, 1],
        [1, 1, 2, 1, 2, 1, 0],
        [1, 1, 2, 1, 2, 2, 1],
        [1, 1, 2, 2, 3, 1, 0],
        [1, 1, 2, 2, 4, 1, 1]
    ]
    df = pd.DataFrame(data)
    return df


def indiscernibility_matrix(df):
    """
    Create the indiscernibility matrix for the decision system.
    Returns a dictionary of sets representing indistinguishable objects.
    """
    n = len(df)
    matrix = {}
    for i in range(n):
        matrix[i] = set()
        for j in range(n):
            if i != j and df.iloc[i, -1] != df.iloc[j, -1]:
                common_attrs = frozenset()
                for k in range(len(df.columns) - 1):
                    if df.iloc[i, k] == df.iloc[j, k]:
                        common_attrs = common_attrs.union(frozenset([k]))
                matrix[i].add((j, common_attrs))
    return matrix


def find_rules(matrix, df):
    """
    Find exhaustive decision rules from the indiscernibility matrix.
    Returns a list of rules with support count.
    Stops when finding a single rule of a given rank.
    Properly skips already used attributes in higher ranks.
    """
    rules = {}
    n = len(df.columns) - 1
    used_attributes = set()

    for r in range(1, n + 1):
        rule_count = 0
        current_rules = {}
        for obj, conflicts in matrix.items():
            candidate_rules = []
            available_attributes = [i for i in range(n) if i not in used_attributes]
            for comb in itertools.combinations(available_attributes, r):
                valid = True
                for j, common_attrs in conflicts:
                    if frozenset(comb).issubset(common_attrs):
                        valid = False
                        break
                if valid:
                    rule = tuple(comb)
                    decision = df.iloc[obj, -1]
                    if (rule, decision) in current_rules:
                        current_rules[(rule, decision)] += 1
                    else:
                        current_rules[(rule, decision)] = 1
                        rule_count += 1
        # Jeśli w danym rzędzie jest tylko jedna reguła, kończymy algorytm
        if len(current_rules) == 1:
            rules.update(current_rules)
            break
        # Zaktualizuj zbiór użytych atrybutów
        for rule, _ in current_rules.keys():
            used_attributes.update(rule)
        rules.update(current_rules)
    return rules


def print_rules(rules):
    """
    Print the found decision rules with support count.
    """
    for (attributes, decision), support in rules.items():
        rule_str = " ∧ ".join([f"a{k+1}" for k in attributes])
        print(f"({rule_str}) ⇒ (d = {decision}) [{support}]")


if __name__ == "__main__":
    df = load_decision_system()
    matrix = indiscernibility_matrix(df)
    rules = find_rules(matrix, df)
    print_rules(rules)
