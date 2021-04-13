#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 14:14:26 2021

@author: ambuj
"""

import numpy as np
import re
import pandas as pd
import math
from Bio import PDB
import warnings
from Bio.PDB.PDBExceptions import PDBConstructionException, PDBConstructionWarning
#class BOOTSTRAP:
#    num_of_sample = 58
#    def __init__(self):
#        rnd_no = 0
#    def gen_rand(self, first, second):
#        rnd_no = random.randint(first, second)
#        return rnd_no


class Protein_RNA_ineraction:
    def __init__(self, pdb_file,prot_chain='A',rna_chain='B'):
        self.pdb_file = pdb_file
        self.prot_chain = prot_chain
        self.rna_chain = rna_chain
        self.pattern ='^ATOM.{16}'
#        self.coords_line = []
#        self.coords = []
#    coords_xyz = np.zeros((3))
    def f1_header(self):
        record = open(self.pdb_file,'r').readlines()[0]
        dict1 = {'title':record[10:50].rstrip(),'date':record[51:60].rstrip(),'ID':record[62:66]}
        return dict1
    def f2_atom_coords(self, chain='A'):
        coords_line = []
        if len(chain) == 1:
            chain = '.'+chain
#            print chain
            pdb_ptr = open(self.pdb_file,'r')
            
            for line in pdb_ptr:
                
                pat_srch = re.search(self.pattern+chain, line)
#                chx = line[21:23]
#                print chx
#                break
                if pat_srch or line[21:22] == 'chain':
#                    print line
                    coords_line.append(line)
#                    self.coords.append(list([line[31:38], line[39:46], line[47:54]]))
#                    self.coords[i].append(float(line[39:46]))
#                    self.coords[i].append(float(line[47:54]))
#            print self.coords
        return coords_line

    def f3_extract_seqres(self, chain='A'):
        seq_line = []
        pattern2 = '^SEQRES.{4}'
#        pattern3 = '^
        if len(chain) == 1:
            chain = '.'+chain
            pdb_ptr = open(self.pdb_file,'r')
            for line in pdb_ptr:
                pat_srch = re.search(pattern2+chain, line)
                if pat_srch:
                    seq_line.append(line[19:])
                    
        #            spt_line = line[19:].rstrip().split()
                    
#        check = molecule_type(pdb_file, chain)        
#        seq=inst.fasta_format(seq_line)
        return seq_line
    
    def f4_seqres_to_fasta(self, seq_line,header):    #Output of f3_extract_seqres is input for this function
        aa = {'ALA':'A','ARG':'R','ASN':'N','ASP':'D', 'CYS':'C', 'GLN':'Q', 'GLU':'E', 'GLY':'G', 'HIS':'H', 'ILE':'I', 'LEU':'L', 'LYS':'K', 'MET':'M','PHE':'F', 'PRO':'P', 'SER':'S', 'THR':'T', 'TRP':'W', 'TYR':'Y', 'VAL':'V'}
        nt = {'DA':'A','DG':'G','DU':'U','DC':'C','DT':'T', 'DI':'I'}
        newseq = ''
        finalseq =[]
        finalseq.append('>'+header['ID'])
        for line in seq_line:
            spt_line = line.rstrip().split()
            for res in spt_line:
                res = res.upper()
                if len(res) == 3:
                    if res in aa:
                        newseq += aa[res]
                    else:
                        print (res+' not present')
                if len(res) == 2:
                    if res in nt:
                        newseq += nt[res]
                if len(res) == 1:
                    newseq += res;
        finalseq.append(newseq)
        return finalseq
    def f5_seq_comp(self, seq_line):          #Output of f3_extract_seqres is input for this function
        aa = {'ALA':0,'ARG':0,'ASN':0,'ASP':0, 'CYS':0, 'GLN':0, 'GLU':0, 'GLY':0, 'HIS':0, 'ILE':0, 'LEU':0, 'LYS':0, 'MET':0,'PHE':0, 'PRO':0, 'SER':0, 'THR':0, 'TRP':0, 'TYR':0, 'VAL':0}
        dnt = {'DA':0,'DG':0,'DU':0,'DC':0,'DT':0, 'DI':0}
        nt = {'A': 0, 'G':0, 'C':0, 'U':0, 'I':0}
        x1 = 0
        x2 = 0
        x3 = 0
        
        for line in seq_line:
            spt_line = line.rstrip().split()
#            print (spt_line)
            for res in spt_line:
                res = res.upper()
#                print len(res)
                if len(res) == 3:
                    if res in aa:
                        aa[res] += 1
                        x1 += 1
                if len(res) == 2:
                    if res in dnt:
                        dnt[res] += 1
                        x2 = x2 + 1
#                        print x2
                if len(res) == 1:
                    nt[res] += 1
                    x3 += 1
                    
#        print dnt
        if x1 >= x2 and x1 >= x3:
            return aa
        elif x2 >= x1 and x2 >= x3:
            return dnt
        elif x3 >= x1 and x3 >= x2:
            return nt


    
    def f6_proteinRNAcontact2(self, dist_cutoff=5):
        
        warnings.simplefilter('ignore', PDBConstructionWarning)
        int_df1 = pd.DataFrame()
        flag = 0
        parser = PDB.PDBParser()
        structure = parser.get_structure("pdb", self.pdb_file)
        model = structure[0]
        prot_chain = model[self.prot_chain] 
        rna_chain = model[self.rna_chain]
        nal1 = ['A','G','C','U']
        pal1 = ['ALA','ARG','ASN','ASP', 'CYS', 'GLN', 'GLU', 'GLY', 'HIS', 'ILE', 'LEU', 'LYS', 'MET','PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR', 'VAL']
        c1 = [str(x).split()[1] for x in list(prot_chain.get_residues())]
        c2 = [str(x).split()[1] for x in list(rna_chain.get_residues())]
        checkp = set(c1).intersection(set(nal1))
        checkn = set(c2).intersection(set(pal1))
        if (len(checkp) > 0):
            print("check the chains of pdb file "+self.pdb_file+" error in protein or RNA molecule\n See protein set "+str(checkp))
            flag = 1
            return int_df1, flag
        if (len(checkn) >= 2):
            print("check the chains of pdb file "+self.pdb_file+" error in protein or RNA molecule\n See na set "+(str(checkn)))
            flag = 1
            return int_df1, flag
        for prot_res in prot_chain:
            for prot_atoms in prot_res:
                for rna_res in rna_chain:
                    rna_resname = rna_res.resname
                    for rna_atoms in rna_res:
                        distance = prot_atoms-rna_atoms
                        # print (distance)
                        if (distance< dist_cutoff):
                            dict1 = {'distance':distance, 'na_atm':rna_atoms.get_full_id()[4][0], 'na_atmno':rna_atoms.get_serial_number(),
                                     'na_res':rna_res.resname, 'na_resno':rna_atoms.get_full_id()[3][1], 'na_coord':rna_atoms.get_coord(), 'prot_atm':prot_atoms.get_full_id()[4][0], 
                                     'prot_atmno':prot_atoms.get_serial_number(), 'prot_res':prot_res.resname, 'prot_resno':prot_atoms.get_full_id()[3][1], 
                                     'prot_coord':prot_atoms.get_coord() }
                            
                            int_df1 = int_df1.append(dict1,ignore_index=True)
        
        b1 = [x.strip() in nal1 for x in int_df1['na_res']]
        temp1 = int_df1[b1]
        b2 = [x.strip() in pal1 for x in temp1['prot_res']]
        df_inter = temp1[b2]
        return df_inter


    def f7_energy2(self, df_inter, aa_param,na_param):     #Output of f6_proteinRNAcontact2 is to be used as df_inter for this function
                                                            # aa_param and na_param are the parameters optimized for amino acids and RNA nucleotides, respectively
                                                            
        df1 = df_inter.copy(deep=True)
        
        
        vdwrad = 'Vdwradrna'
        vdweps = 'Vdwepsrna'
        
        total_energy = 0
        df1['prot_atmtype'] ='NA'
        df1['prot_charge'] = 0
        df1['prot_vdwradius'] =0
        df1['prot_vdweps'] =0
        df1['na_atmtype'] ='NA'
        df1['na_charge'] =0
        df1['na_vdwradius'] =0
        df1['na_vdweps'] =0
        df1['Vdw_energy'] =0
        
#        numcols = len(df1.columns)
        for i in df1.index:
            idx1 = aa_param[(str(df1['prot_atm'][i]).strip() == aa_param['Atm_name']) & (str(df1['prot_res'][i]).strip() == aa_param['Res_name'])].index
            # print (idx1)
            if (len(idx1) == 0 ):
                print ("Unavailable in protein parameter: Residue - "+ str(df1['prot_res'][i]).strip()+ " , Atom - "+ str(df1['prot_atm'][i]).strip())
            else:
                df1.loc[i,'prot_atmtype'] = list(aa_param['Atm_type'][idx1])[0]
                df1.loc[i,'prot_charge'] = list(aa_param['Charge'][idx1])[0]
                df1.loc[i,'prot_vdwradius'] = list(aa_param['Vdwrad'][idx1])[0]
                df1.loc[i,'prot_vdweps'] = list(aa_param['Vdweps'][idx1])[0]
            idx2 = na_param[(str(df1['na_atm'][i]).strip() == na_param['Atm_name']) & (str(df1['na_res'][i]).strip() == na_param['Res_name'])].index
            if (len(idx2) == 0 ):
                # print (list(df1.columns))
                print ("Unavailable in RNA parameter: Residue - "+ str(df1['na_res'][i]).strip()+ " , Atom - "+ str(df1['na_atm'][i]).strip())
            else:
                df1.loc[i,'na_atmtype'] = list(na_param['Atm_type'][idx2])[0]
                df1.loc[i,'na_charge'] = list(na_param['Charge'][idx2])[0]
                df1.loc[i,'na_vdwradius'] = list(na_param[vdwrad][idx2])[0]
                df1.loc[i,'na_vdweps'] = list(na_param[vdweps][idx2])[0]
            eps = float(df1.loc[i,'prot_vdweps']) *float(df1.loc[i,'na_vdweps'])
            vdwr = float(df1.loc[i,'prot_vdwradius']) +float(df1.loc[i,'na_vdwradius'])
            chrg = float(df1.loc[i,'prot_charge']) *float(df1.loc[i,'na_charge'])
            vdwr2 = vdwr*vdwr
            vdwr6 = vdwr2*vdwr2*vdwr2
            vdwr12 = vdwr6*vdwr6
            epssqrt = math.sqrt(eps)
            
            aec12ab = epssqrt*vdwr12
            aec6ab = 2*epssqrt*vdwr6
            rijs = float(df1.loc[i,'distance'])*float(df1.loc[i,'distance'])
            rs = float(1)/rijs
            rij2=rs
            
            rij6 = rij2*rij2*rij2
            rij12 = rij6*rij6
            
            
            # print (rij12, aec12ab)
            v1 = (aec12ab*rij12)-(aec6ab*rij6)
            v2 = chrg*rij2
            v12 =v1+v2
            # print (v1,v2,v12)
            total_energy += v12
    #            print v12
            if (v12 < 0):
                df1.loc[i,'Vdw_energy'] = v12
            else:
                df1.loc[i,'Vdw_energy'] = 0
        
    
#            v1 = (aec12ab*rij12)-(aec6ab*rij6)
#            v2 = chrg*rij2
#            v12 =v1+v2
        return df1

    def f8_interaction_type (self, df_inter):                     #Output of f6_proteinRNAcontact2 is input for this function
        int_dict = {'CO':0,'OC':0,'NO':0,'ON':0}
        temp_ptr = open('temp.txt','w')
        for index, dfrow in df_inter.iterrows():
            temp_ptr.write('\n'+dfrow["prot_atm"]+'\t'+dfrow["na_atm"])
            in_t = dfrow["prot_atm"][0:1]+dfrow["na_atm"][0:1]
            if in_t in int_dict:
                int_dict[in_t] += 1
            else:
                int_dict.update({in_t:1})
        temp_ptr.close()
        return int_dict




    def f9_energy_div (self, energy_df):              #Total energy calculation between main chain and side chains
#        print df_inter
        energy_dict = {'mc_mc':0,'mc_sc':0,'sc_mc':0, 'sc_sc':0,'total1':0}
        if len(energy_df) ==0:
            return energy_dict
        
        
        prot_main_atm = ['N','CA','C']
        na_mainch_b1 = np.array([x.rstrip()[-1:] == '\'' or x.rstrip() == 'P' for x in energy_df['na_atm'] ])
        
        na_sidech_b4 = np.invert(na_mainch_b1)
        prot_mainch_b2 = np.array([x.rstrip() in prot_main_atm for x in energy_df['prot_atm'] ])
        prot_sidech_b3 = np.invert(prot_mainch_b2)
        energy_dict['mc_mc'] = energy_df[np.array(prot_mainch_b2) & np.array(na_mainch_b1)]['Vdw_energy'].sum()
        energy_dict['mc_sc'] = energy_df[np.array(prot_sidech_b3) & np.array(na_mainch_b1)]['Vdw_energy'].sum()
        energy_dict['sc_mc'] = energy_df[np.array(prot_mainch_b2) & np.array(na_sidech_b4)]['Vdw_energy'].sum()
        energy_dict['sc_sc'] = energy_df[np.array(prot_sidech_b3) & np.array(na_sidech_b4)]['Vdw_energy'].sum()
        energy_dict['total1'] = energy_df['Vdw_energy'].sum()
        return energy_dict
        
aa_param = pd.read_csv('aa_20vdrch.csv')
na_param = pd.read_csv('rna_4vdrch.csv')
inst2 = Protein_RNA_ineraction('1j1u.pdb')
h1 = inst2.f1_header()
atom_coords = inst2.f2_atom_coords(chain='A')
seq_line=inst2.f3_extract_seqres()
seq = inst2.f4_seqres_to_fasta(seq_line,h1)
seq_comp = inst2.f5_seq_comp(seq_line)
df_inter = inst2.f6_proteinRNAcontact2()
energy_df = inst2.f7_energy2(df_inter,aa_param,na_param)
atoms_involve = inst2.f8_interaction_type(df_inter)
energy_dict = inst2.f9_energy_div(energy_df)


