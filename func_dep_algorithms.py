# IF X->Y AND Y->Z THEN X->Z
# IF X->YZ AND Y->W THEN X->W
def transitivity(functional_dependencies):

    new_functional_dependencies = functional_dependencies.copy()

    for dependency_1 in functional_dependencies:

        (left_side_1, right_side_1) = dependency_1.split("->")

        for dependency_2 in functional_dependencies:

            # stops useless assignment in case of self-comparing
            if dependency_1 == dependency_2:
                continue

            (left_side_2, right_side_2) = dependency_2.split("->")

            # IF X->Y AND Y->Z THEN X->Z
            if right_side_1 == left_side_2 and right_side_2 != left_side_1:
                new_functional_dependencies.add(left_side_1 + "->" + right_side_2)

    return new_functional_dependencies

# IF A->BC THEN A->B AND A->C
def decomposition(functional_dependencies):

    new_functional_dependencies = functional_dependencies.copy()

    for dependency in functional_dependencies:

        (left_side, right_side) = dependency.split("->")

        if len(right_side) > 1:
            for attribute in right_side:
                new_functional_dependencies.add(left_side + "->" + attribute)

    return new_functional_dependencies

# add attributes to both sides (ex. 'AB->ABC' turns into 'ABD->ABCD' or 'ABE'->'ABCE')
def composition(kc, attribute):

    (key, closer) = kc.split("->")

    key = "".join(sorted(set(key + attribute)))
    closer = "".join(sorted(set(closer + attribute)))

    return key + "->" + closer

# IF X->Y AND YZ->W THEN XZ->W
# IF X->YZ AND YZA->W THEN XZ->W
def pseudo_transitivity(functional_dependencies): 

    new_functional_dependencies = functional_dependencies.copy()

    for dependency_1 in functional_dependencies:

        (left_side_1, right_side_1) = dependency_1.split("->")

        for dependency_2 in functional_dependencies:

            # stops useless assignment in case of self-comparing
            if dependency_1 == dependency_2:
                continue

            (left_side_2, right_side_2) = dependency_2.split("->")

            if (right_side_1 in left_side_2 and right_side_1 != left_side_2) and left_side_1 != right_side_2:
                new_left_side = ""
                new_right_side = right_side_2

                for attribute in left_side_2:
                    if attribute not in right_side_1:
                        new_left_side += attribute
                
                new_left_side += left_side_1

                new_left_side = "".join(sorted(set(new_left_side)))
                new_functional_dependencies.add(new_left_side + "->" + new_right_side)

    return new_functional_dependencies

# IF X->Y AND X->Z THEN X->YZ
def dependency_union(functional_dependencies):

    new_functional_dependencies = functional_dependencies.copy()

    for dependency_1 in functional_dependencies:

        (left_side_1, right_side_1) = dependency_1.split("->")

        for dependency_2 in functional_dependencies:

            # stops useless assignment in case of self-comparing
            if dependency_1 == dependency_2:
                continue

            (left_side_2, right_side_2) = dependency_2.split("->")

            if left_side_1 == left_side_2:
                new_functional_dependencies.add(left_side_1 + "->" + "".join(sorted(set(right_side_1 + right_side_2))))
    
    return new_functional_dependencies

# sorts left and right side of dependencies
def sort_dependencies(functional_dependencies):

    new_functional_dependencies = set()

    for dependency in functional_dependencies:

        (left_side, right_side) = dependency.split("->")

        new_left_side = "".join(sorted(left_side))
        new_right_side = "".join(sorted(right_side))

        for attribute_1 in new_left_side:
            for attribute_2 in new_right_side:
                if attribute_1 == attribute_2:
                    new_right_side = new_right_side.replace(attribute_2, "")
        

        if new_left_side != "" and new_right_side != "":
            new_functional_dependencies.add(new_left_side + "->" + new_right_side)

    return new_functional_dependencies

# adds decomposition, transitivity, pseudotransitivity and union until there's no changes to be made, then sorts
def extend_dependencies(minimal_dependencies):
    new_functional_dependencies = minimal_dependencies.copy()
    
    while True:
        new_functional_dependencies.update(dependency_union(pseudo_transitivity(transitivity(decomposition(minimal_dependencies)))))

        if new_functional_dependencies == minimal_dependencies:
            return sort_dependencies(new_functional_dependencies)
        
        minimal_dependencies = new_functional_dependencies.copy()
