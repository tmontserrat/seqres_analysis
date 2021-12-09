class Seqres:
    """
    A class representing the different subunits of a protein
    """
    def __init__(self, filename):
        """
        Returns a list: first element is the names of the subunits, 
        and second element is a list with the aminoacid sequence of
        each chain.
        """
        self.name = filename
        # Create a list with the subunits' names
        subunits = self.retrieve_information_pdb().keys()
        subunits_list = []
        for subunit in subunits:
            subunits_list.append(subunit)
        self.subunits = subunits_list

        # Create a list with the subunits' sequences
        sequences = self.retrieve_information_pdb().values()
        sequences_list = []
        for sequence in sequences:
            sequences_list.append(sequence)
        self.sequences =  sequences_list

    def retrieve_information_pdb(self):
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
        with open(self.name) as f:
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
        subunits_dict = {}
        index = 0
        for subunit in info[0]:
            subunits_dict[subunit] = info[1][index]
            index += 1
        return subunits_dict

    def check_equal_chains(self):
        """Check if the different subunits are equal."""
        comparisons_results = len(set(self.sequences))
        return (comparisons_results, len(set(self.sequences)))
    
    def check_two_chains(self, chain_a, chain_b):
        """Compare two chains."""
        if len(self.subunits) == 1:
            message = "There is only one chain."
            return message
        else:
            try:
                return self.sequences[chain_a] == self.sequences[chain_b]
            except:
                return "That chain does not exist. Beware that chain number is 0 indexed."
    
    def compare_all_subunits(self):
        """Compare all chains."""
        # Empty string
        message = ''
        # Empty list to store the pairs checked
        checked_pairs = []
        # Iterate through the chains
        for index1 in range(len(self.subunits)):
            # Iterate through the chains to and compare
            for index in range(len(self.subunits)):
                # Don't compare a chain with itself
                if index1 != index:
                    # Avoid the out of range error
                    if index < len(self.subunits):
                        # Don't compare two chains two times
                        if not f"{index1} and {index}" in checked_pairs and not f"{index} and {index1}" in checked_pairs:
                            # Compare and append the message
                            if self.check_two_chains(index1, index):
                                message += f"{self.subunits[index1]} and {self.subunits[index]} are equal.\n"
                                checked_pairs.append(f"{index1} and {index}")
                            else:
                                message += f"{self.subunits[index1]} and {self.subunits[index]} are different.\n"
                                checked_pairs.append(f"{index1} and {index}")
        return message

    def count_aminoacids_subunit(self):
        """Count the number of aminoacids in each subunit given a pdb file."""
        sequences_length = {}
        subunits_dict = self.retrieve_information_pdb()
        for chain, sequence in subunits_dict.items():
            sequence_list = sequence.split(' ')
            sequences_length[chain] = len(sequence_list)
        return sequences_length
    

    def summary(self):
        """
        Formatted simple anylisis of the subunits of a protein.
        """
        # Functions calls
        comparisons_results = self.check_equal_chains()
        sequences_length = self.count_aminoacids_subunit()

        # Give format to subunits object
        formatted_subunits = ", ".join(self.subunits)
        print("\n#### Number of subunits ####")
        # For proteins with just one chain
        if len(self.subunits) == 1:
            print(f"- {len(self.subunits)} subunit called {formatted_subunits}")
            print("\n#### Number of residues ####")
            print(f"- {sequences_length[0]}")
        # For proteins with more than one chain
        else: 
            print(f"- {len(self.subunits)} subunits called {formatted_subunits}")
            print("\n#### Number of residues per subunit ####")
            for subunit, length in sequences_length.items():
                print(f"- {subunit}\t{length}")
            print("\n#### Subunits sequences comparisons ####")
            if comparisons_results[0]:
                print(f"- All subunits are equal.\n")
            else:
                print(f"- There are {comparisons_results[1]} different subunits.\n")