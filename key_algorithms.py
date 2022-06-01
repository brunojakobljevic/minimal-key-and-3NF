from func_dep_algorithms import composition

# ABC gives ['ABC', 'A', 'B', 'C', 'AB', 'AC', 'BC']
def find_all_combinations(possible_attributes):

    from itertools import combinations

    all_combinations = []
    all_combinations.append(possible_attributes)

    for i in range(len(possible_attributes)):
        if i == 0:
            continue
        subkey_combinations = combinations(possible_attributes, i)
        for subkey in list(subkey_combinations):
            all_combinations.append(subkey)

    def tuple_to_string(tuple):
        return "".join(tuple)

    return list(map(tuple_to_string, all_combinations))

# take minimal dependencies as possible keys and extend their closer as much as possible with functional_dependencies
def find_kcs(minimal_dependencies, functional_dependencies):

    possible_superkeys = set()
    # take left sides of minimal dependencies as possible keys
    for md in minimal_dependencies:
        (left_side, right_side) = md.split("->")

        key = left_side
        closer = "".join(sorted(set(left_side + right_side)))

        new_closer = closer
        # extend the closer as much as possible with functional_dependencies
        while True:
            subkeys = find_all_combinations(key)
            subclosers = find_all_combinations(closer)
            
            for fd in functional_dependencies:
                (left_side, right_side) = fd.split("->")
                # check if every combination of key is on the left side of FO, if it is add the right sid
                for subkey in subkeys:
                    if subkey == left_side:
                        new_closer = "".join(sorted(set(new_closer + right_side)))
                # check if every combination of closer is on the left side of FO, if it is add the right side
                for subcloser in subclosers:
                    if subcloser == left_side:
                        new_closer = "".join(sorted(set(new_closer + right_side)))

            if new_closer == closer:
                break

            closer = new_closer
            
        possible_superkeys.add(key + "->" + new_closer)

    return possible_superkeys

# checking if a key defines all attributes
def check_if_super_key(all_attributes, closer):

    if closer == all_attributes:
        return True

    return False

# find superkeys from possible keys
def get_superkeys(all_attributes, possible_superkeys, functional_dependencies):
    
    print("Possible superkeys:\n", possible_superkeys, "\n")

    composed_possible_superkeys = set()

    # if keys are not superkeys make composition on them
    # ex. all attributes are ABCD, possible superkey is AB->ABC, composition gives ABD->ABCD
    for possible_superkey in possible_superkeys:
        for attribute in all_attributes:
            if attribute not in possible_superkey:
                composed_possible_superkeys.add(composition(possible_superkey, attribute))
    
    print("Composed possible superkeys:\n", composed_possible_superkeys, "\n")

    superkeys = set()

    values_to_delete = []
    # check if there are superkeys in composed_possible_superkeys, if there are remove them from set, and add them to superkeys
    for composed_possible_superkey in composed_possible_superkeys:
        (key, closer) = composed_possible_superkey.split("->")
        if check_if_super_key(all_attributes, closer):
            superkeys.add(key)
            values_to_delete.append(composed_possible_superkey)
    # removing superkeys from set
    for value in values_to_delete:
        composed_possible_superkeys.remove(value)
    
    superkeys.update(create_superkeys(all_attributes, composed_possible_superkeys, functional_dependencies))

    return superkeys

# takes remaining possible superkeys and composes them until they define all attributes
def create_superkeys(all_attributes, composed_possible_superkeys, functional_dependencies):

    new_superkeys = set()
    # do while all composed possible superkeys isn't empty
    while len(composed_possible_superkeys) != 0:
            (key, closer) = composed_possible_superkeys.pop().split("->")

            subkeys = find_all_combinations(key)
            subclosers = find_all_combinations(closer)

            for dependency in functional_dependencies:
                (left_side, right_side) = dependency.split("->")
                # check if every combination of key is on the left side of FO, if it is add the right side
                for subkey in subkeys:
                    if subkey == left_side:
                        closer = "".join(sorted(set(closer + right_side)))
                # check if every combination of closer is on the left side of FO, if it is add the right side
                for subcloser in subclosers:
                    if subcloser == left_side:
                        closer = "".join(sorted(set(closer + right_side)))
            # if it is a supperkey add it to superkeys
            if check_if_super_key(all_attributes, closer):
                new_superkeys.add(key)
            # if it isn't a superkey compose it again
            else:
                for attribute in all_attributes:
                    if attribute not in key and attribute not in closer:
                        composed_possible_superkeys.add(composition(key + "->" + closer, attribute))

    return new_superkeys

'''
def check_if_subkeys_are_candidate(all_attributes, superkey, functional_dependencies):

    possible_candidate_keys = set()

    subkeys = find_all_combinations(superkey)
    
    if len(subkeys) > 1:
        subkeys.pop(0)

    for subkey in subkeys:
        closer = subkey
        new_closer = closer
        subkeys_of_subkey = find_all_combinations(subkey)

        while True:
            subclosers_of_subkey = find_all_combinations(new_closer)

            for fd in functional_dependencies:
                (left_side, right_side) = fd.split("->")
                for subkey_of_subkey in subkeys_of_subkey:
                    if subkey_of_subkey == left_side:
                        new_closer = "".join(sorted(set(new_closer + right_side)))

                for subcloser in subclosers_of_subkey:
                    if subcloser == left_side:
                        new_closer = "".join(sorted(set(new_closer + right_side)))
            
            if new_closer == closer:
                break

            closer = new_closer
        
        if new_closer == all_attributes:
            possible_candidate_keys.add(subkey)

    return possible_candidate_keys'''

'''
def create_candidates(all_attributes, superkeys, functional_dependencies):
    
    possible_candidate_keys = set()
    
    for superkey in superkeys:
        subkey_candidates = check_if_subkeys_are_candidate(all_attributes, superkey, functional_dependencies)
        if subkey_candidates:
            possible_candidate_keys.update(subkey_candidates)
        else:
            possible_candidate_keys.add(superkey)
    
    return possible_candidate_keys
'''
# find the minimal keys in superkeys and add it to candidate keys
def find_candidate_keys(all_attributes, superkeys):

    candidate_keys = set()

    min_len = len(all_attributes)

    for superkey in superkeys:
        if len(superkey) < min_len:
            min_len = len(superkey)
    
    for superkey in superkeys:
        if len(superkey) == min_len:
            candidate_keys.add(superkey)

    return candidate_keys