# Protein-RNA-interactions 
Interaction analysis of protein-RNA complexes 
The program is built on Python2.7;
To run the program, a PDB file and van der Waals parameter files for protein (named: aa_20vdrch) and RNA (named: rna_4vdrch) are required; 
__init__:  Function initializes the instance of protein_RNA_interaction class with PDB file name (with path), protein chain and RNA chain;
f1_header: Function extracts the header of PDB file;
f2_atom_coords: Extracts the atom records from PDB file in the format of a list;
f3_extract_seqres: Extracts SEQRES records of the PDB file;
f4_seqres_to_fasta: Converts the SEQRES records to the fasta format (from seqres and header information);
f5_seq_comp: Shows the sequence composition (i.e. amino acids count) from the output of f3_extract_seqres function;
f6_proteinRNAcontact2: Calculates contacts between atoms of protein and nucleotides and generate a dataframe; 
f7_energy2: Using the output dataframe of f6_proteinRNAcontact2 function and amino acid and nucleotide van der Waals parameter files energy is generated. The 'Vdw_energy' column contains the energy values.;
f8_interaction_type: Number of atoms based contacts are calculated from the output dataframe of f6_proteinRNAcontact2 function;
f9_energy_div: From the output of f7_energy2 program the energy is divided into main chain-main chain, main chain-side chain, side chain-main chain and side chain-side chain
