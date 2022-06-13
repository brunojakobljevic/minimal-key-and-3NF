# minimal-key-and-3NF
A script that finds a minimal key in a given relation and decomposes the relation into 3NF. Done in Python.

It iterates through all the minimal functional dependencies and extends them until no more changes can be made.

Then it iterates through all the extended functional dependecies and it finds all candidate keys. It selects one key from the set and then it begins the 3NF algorithm. First it removes the middle part of the transitive dependencies(ex. A->B, B->C, A->C => A->B, A->C), secondly it iterates through all the altered minimal depenencies, and lastly it decomposes all attributes into 3NF.
