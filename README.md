# Protein-RNA-interactions
Interaction analysis of protein-RNA complexes
__init__:  Function initialize the instance of protein_RNA_interaction class with PDF file name (with path), protein chain and RNA chain;
f1_header: Function extract the header of PDB file;
f2_atom_coords: Extract the atom records from PDB file in the format of list;
f3_extract_seqres: Extract SEQRES records of PDB file;
f4_seqres_to_fasta: Convert the SEQRES records to the fasta format (from seqres and header information);
f5_seq_comp: Shows the sequence composition (i.e. amino acids count) from the output of f3_extract_seqres function;
f6_proteinRNAcontact2: Calculate contacts between atoms of protein and nucleotides and generate a dataframe; 
f7_energy2: Using the output dataframe of f6_proteinRNAcontact2 function and amino acid and nucleotide van der Waals parameter file energy is generated;
f8_interaction_type: Number of atom based contacts are calculated from the output dataframe of f6_proteinRNAcontact2 function;
f9_energy_div: From the output of f7_energy2 program the energy is divided into main chain-main chain, main chain-side chain, side chain-main chain and side chain-side chain
