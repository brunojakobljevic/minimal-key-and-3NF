from func_dep_algorithms import sort_dependencies, extend_dependencies
from key_algorithms import check_if_super_key, find_candidate_keys, find_kcs, get_superkeys
from nf_algorithms import decomposition_to_3_nf, remove_transitive

# main_superkey = "ABC"
# main_superkey = "ABCDE"
main_superkey = "ABCDEFGHIJ"

all_attributes = main_superkey

minimal_dependencies = set()
minimal_dependencies_no_trans = set()
superkeys = set()
candidate_keys = set()

# 1. {A->B, B->A, B->C, A->C, C->A}
'''
minimal_dependencies.add("A->B")
minimal_dependencies.add("B->A")
minimal_dependencies.add("B->C")
minimal_dependencies.add("A->C")
minimal_dependencies.add("C->A")
'''

# 2. {RaAr->Ku, Ar->Oa, Ku->Mj}
'''
minimal_dependencies.add("AD->B")
minimal_dependencies.add("D->E")
minimal_dependencies.add("B->C")
'''

# 3. {A->B, CD->E, B->D, E->A}
'''
minimal_dependencies.add("A->B")
minimal_dependencies.add("CD->E")
minimal_dependencies.add("B->D")
minimal_dependencies.add("E->A")
'''

# 4. {DI->B , AJ->F , GB->FJE , AJ->HD , I->CG}
'''
minimal_dependencies.add("DI->B")
minimal_dependencies.add("AJ->F")
minimal_dependencies.add("GB->FJE")
minimal_dependencies.add("AJ->HD")
minimal_dependencies.add("I->CG")
'''

# 5. {A->EF , F->CH , I->DB , CJ->I , BF->JE, E->CD}

minimal_dependencies.add("A->EF")
minimal_dependencies.add("F->CH")
minimal_dependencies.add("I->DB")
minimal_dependencies.add("CJ->I")
minimal_dependencies.add("BF->JE")
minimal_dependencies.add("E->CD")

'''
minimal_dependencies.add("A->B")
minimal_dependencies.add("C->B")
minimal_dependencies.add("B->E")
minimal_dependencies.add("I->J")
minimal_dependencies.add("H->G")
minimal_dependencies.add("A->D")
minimal_dependencies.add("D->F")
minimal_dependencies.add("A->H")
'''
print("Minimal functional dependencies:\n", minimal_dependencies, "\n")

functional_dependencies = extend_dependencies(sort_dependencies(minimal_dependencies))
print("Extended functional dependencies:\n", functional_dependencies, "\n")

# taking minimal dependencies and extending the right side as much as possible with functional_dependencies
possible_keys = find_kcs(minimal_dependencies, functional_dependencies)
print("Possible keys:\n", possible_keys, "\n")

# check if there's a superkey, if there is delete it from possible keys and add it to superkeys
values_to_delete = []
for possible_key in possible_keys:
    (key, closer) = possible_key.split("->")
    if check_if_super_key(all_attributes, closer):
        superkeys.add(key)
        values_to_delete.append(possible_key)

if len(superkeys) == 0:
    print("No superkeys found yet\n")
else:
    print("Superkeys for now:\n", superkeys, "\n")

for value in values_to_delete:
    possible_keys.remove(value)

superkeys.update(get_superkeys(all_attributes, possible_keys, functional_dependencies))

print("Superkeys:\n", superkeys, "\n")

candidate_keys = find_candidate_keys(all_attributes, superkeys)

print("Candidate keys:\n", candidate_keys, "\n")

min_key = list(candidate_keys)[0]
print("Minimal key:\n", min_key, "\n")

print("Table for now:\n", all_attributes, " with '", min_key,"' as a minimal key\n")

print("Decomposing the table...\n")

minimal_dependencies_no_trans = remove_transitive(sort_dependencies(minimal_dependencies))
print("Minimal dependencies with transitive relations removed:\n", minimal_dependencies_no_trans, "\n")
all_tables = decomposition_to_3_nf(minimal_dependencies_no_trans, min_key)

print("Tables in this relation:\n")
counter = 1
for table_key, table_attributes_set in all_tables.items():
    for table_attributes in table_attributes_set:
        print("TABLE #" + str(counter) + "\nPrimary key - " + table_key + "\nAttributes - " + table_attributes + "\n")
        counter += 1