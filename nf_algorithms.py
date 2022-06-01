from key_algorithms import find_all_combinations

# removes middle parts of transitive relations - IF X->Y AND Y->Z AND X->Z THEN REMOVE Y->Z
def remove_transitive(minimal_dependencies):
    
    helper_bool = False

    while True:
        new_minimal_dependencies = minimal_dependencies.copy()

        for dependency_1 in minimal_dependencies:

            (left_side_1, right_side_1) = dependency_1.split("->")

            for dependency_2 in minimal_dependencies:

                # stops useless assignment in case of self-comparing
                if dependency_1 == dependency_2:
                    continue

                (left_side_2, right_side_2) = dependency_2.split("->")

                # IF X->Y AND Y->Z AND X->Z THEN REMOVE Y->Z
                if right_side_1 == left_side_2 and right_side_2 != left_side_1 and (left_side_1 + "->" + right_side_2 in minimal_dependencies):
                    new_minimal_dependencies.remove(dependency_2)
                    helper_bool = True
                    break
            
            if helper_bool:
                break

        if new_minimal_dependencies == minimal_dependencies:
            return new_minimal_dependencies
        else:
            minimal_dependencies = new_minimal_dependencies.copy()
            helper_bool = False

# decomposes to 3.NF by checking dependencies without transitivity
def decomposition_to_3_nf(functional_dependencies, min_key):
    tables_with_min_keys = dict()

    for dependency in functional_dependencies:
        (left_side, right_side) = dependency.split("->")

        closer = "".join(sorted(set(left_side + right_side)))
        all_values = tables_with_min_keys.values()
        for values in all_values:
            if closer in values:
                break
        else:        
            if left_side in tables_with_min_keys:
                tables_with_min_keys[left_side].add(closer)
            else:
                tables_with_min_keys[left_side] = set()
                tables_with_min_keys[left_side].add(closer)
    
    all_combs = set()
    for values in tables_with_min_keys.values():
        for value in values:
            all_combs.update(find_all_combinations(str(value)))

    # if minimal key isn't in a given relation add it
    if min_key not in all_combs:
        tables_with_min_keys[min_key] = set()
        tables_with_min_keys[min_key].add(min_key)
    
    return tables_with_min_keys
    



             