# seqres_analysis
Set of functions to get some useful information about the subunits present in a protein from a pdb file.  
There are a total of four functions, all them rely in the first one: `retrieve_information_pdb()` which parses the `SEQRES` section of a pdb file.  

- `retrieve_information_pdb()`: this function parses the `SEQRES` section of a pdb file and is the most important function of the module. It only requires the path to the file as arguments in order to work and return a list of two items. The first item is a list with the number of subunits the protein has. The second element is another list where each element is the sequence of aminoacids present in the protein.  

- `check_equal_chains()`: this is a simple function that check if all the subunits are the same or not. This function call the function `retrieve_information_pdb()` to work. It returns a number meaning the number of different subunits the protein has. As arguments, only needs the path to the pdb file.  

