# Copyright 2021 Tomàs Montserrat Ayuso

"""
Set of functions to quickly analize the subunits of a protein in a pdb file.
"""

def retrieve_information_pdb(filename):
    """
    Returns a list: first element is the names of the subunits, 
    and second element is a list with the aminoacid sequence of
    each chain.
    """
    # Create empty lists to store the information we'll retrieve
    subunits = []
    subunits_seq = []
    subunit_residues = []
    # Declare counting variables to use as index
    count = -1
    # Read the pdb file
    with open(filename) as f:
        for line in f:
            # Only interested with lines containing the aminoacids sequence
            if line.startswith("SEQRES"):
                # Make the list of different subunits on the fly
                if line[11] not in subunits:
                    if not subunit_residues:
                        count += 1
                        subunits.append(line[11])
                        subunit_residues = [line[19:70]]
                    else: 
                        subunits_seq.append(subunit_residues)
                        count += 1
                        subunits.append(line[11])
                        subunit_residues = [line[19:70]]
                elif line[11] == subunits[count]:
                    subunit_residues.append(line[19:70])

    # Append the last subunit sequence
    subunits_seq.append(subunit_residues)
    index = 0
    sequences = []
    # Make one item for each sequence
    for seq in subunits_seq:
        sequence = " ".join(subunits_seq[index])
        sequences.append(sequence)
        index += 1

    # Elminate blank spaces at the end of the sequences
    formatted_sequences = [seq.rstrip() for seq in sequences]
    info = [subunits, formatted_sequences]
    return info

def check_equal_chains(filename):
    """From a pdb file, check if the different subunits are equal."""
    # Call the function
    info = retrieve_information_pdb(filename)
    subunits = info[0]
    formatted_sequences = info[1]
    # Check if the subunits are equal
    for seq_number in range(len(subunits)):
        comparisons_results = len(set(formatted_sequences))
    return comparisons_results

def count_aminoacids_subunit(filename):
    """Count the number of aminoacids in each subunit given a pdb file."""
    # Call the function
    info = retrieve_information_pdb(filename)
    subunits = info[0]
    formatted_sequences = info[1]
    # Count the number of aminoacids per subunit
    sequences_len = []
    if len(subunits) == 1:
        for seq_number in range(len(subunits)):
            seq_len = len(formatted_sequences[0].split(' '))
            seq_len = len(formatted_sequences[0].split(' '))
            sequences_len = seq_len
    else:
        for seq_number in range(len(subunits)):
            seq_len = len(formatted_sequences[seq_number].split(' '))
            result = f"Chain {subunits[seq_number]} = {seq_len}"
            sequences_len.append(result)
    return sequences_len

def format_results(filename):
    """
    Formatted simple anylisis of the subunits of a protein.
    """
    # Functions calls
    info = retrieve_information_pdb(filename)
    subunits = info[0]
    formatted_sequences = info[1]
    comparisons_results = check_equal_chains(filename)
    sequences_len = count_aminoacids_subunit(filename)

    # Give format to subunits object
    formatted_subunits = ", ".join(subunits)
    print("\n#### Number of subunits ####")
    # For proteins with just one chain
    if len(subunits) == 1:
        print(f"- {len(subunits)} subunit called {formatted_subunits}")
        print("\n#### Number of residues ####")
        print(f"- {sequences_len}")
    # For proteins with more than one chain
    else: 
        print(f"- {len(subunits)} subunits called {formatted_subunits}")
        print("\n#### Number of residues per subunit ####")
        for result in sequences_len:
            print(f"- {result}")
        print("\n#### Subunits sequences comparisons ####")
        if comparisons_results == 1:
            print(f"- All subunits are equal.\n")
        else:
            print(f"- There are {comparisons_results} different subunits.\n")
