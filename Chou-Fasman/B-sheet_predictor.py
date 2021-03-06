"""\
Usage:	python B-sheet_predictor.py <fasta_file>

Options:

	<fasta_file>	protein FASTA file
	--help		print help message
"""


import sys

...

# Chou-Fasman Amino Acids Propensities Value For Helix
helix_pro = {"A":1.45, "C":0.77,"D":0.98,"E":1.53,"F":1.12,"G":0.53,"H":1.24,"I":1.00,"K":1.07,
"L":1.34,"M":1.20,"N":0.73,"P":0.59,"Q":1.17,"R":0.79,"S":0.79,"T":0.82,"V":1.14,"W":1.14,"Y":0.61}

# Chou-Fasman Amino Acids Propensities Value For B-Sheet
beta_pro = {"A":0.97, "C":1.30,"D":0.80,"E":0.26,"F":1.28,"G":0.81,"H":0.71,"I":1.60,"K":0.74,
"L":1.22,"M":1.67,"N":0.65,"P":0.62,"Q":1.23,"R":0.90,"S":0.72,"T":1.20,"V":1.65,"W":1.19,"Y":1.29}

# argv[1] is not defined
if len(sys.argv) == 1:
	print (__doc__)

# argv[1] is --help
elif sys.argv[1] == "--help":
	print (__doc__)

# argv[1] is a fasta file
else:
# reading the fasta file
	print("\nParsing Protein Sequence...\n")
	file_f = sys.argv[1]
	fasta_file = open(file_f)
	fasta_rec = fasta_file.readlines()

# separating header from sequence
	header =""
	seq =""
	for line in fasta_rec:
		if line[0:1] == ">":
			header = line
		else:
			seq += line.strip()
	print("Sequence Information")
	print("Sequence Origin: "+header.strip()[1:])
	print("Sequence Length:",len(seq),"\n")
	print("Job: Predicting B-sheet Using Chou-Fasman Algorithm\n")

####################################__CHOU- FASMAN ALGORITHM__###################################

	print("|-------------------{ RUNNING CHOU-FASMAN ALGORITHM }-------------------|\n")
	print("Finding B-sheet Nucleation Regions...")
	probable_beta_index=[]
	temp_seq1 = ""
	prot_helix_prob = []
	prot_beta_prob = []
	for i in range(0,len(seq)):
		prot_helix_prob.append(helix_pro.get(seq[i]))
		prot_beta_prob.append(beta_pro.get(seq[i]))
		if beta_pro.get(seq[i]) > 1:
			temp_seq1 += "B"
		elif beta_pro.get(seq[i]) < 1:
			temp_seq1 += "-"
	nucl_index = [i for i in range(len(temp_seq1)) if temp_seq1.startswith("BBB", i)]
	break_index = [i for i in range(len(temp_seq1)) if temp_seq1.startswith("----", i)]
	print("Finding  Possible B-sheet Indexes...")
	for nucl in nucl_index:
		n1 = nucl
		n3 = nucl+3
		n5 = nucl+5
		for brk in break_index:
			if brk > nucl and brk > n3:
				sum_in_index = brk - n3
				if n1-sum_in_index < 0:
					probable_beta_index.append([0,n3+sum_in_index])
				else:
					probable_beta_index.append([n1-sum_in_index,n3+sum_in_index])
			elif brk < nucl:
				sum_in_index = n1-brk-1
				if n3+sum_in_index > len(seq):
					probable_beta_index.append([n1-sum_in_index,len(seq)])
				else:
					probable_beta_index.append([n1-sum_in_index,n3+sum_in_index])
			elif brk > nucl and brk > n5:
				sum_in_index = brk - n5
				if n1-sum_in_index < 0:
					probable_beta_index.append([0,n5+sum_in_index])
				else:
					probable_beta_index.append([n1-sum_in_index,n5+sum_in_index])
			elif brk < nucl:
				sum_in_index = n1-brk-1
				if n5+sum_in_index > len(seq):
					probable_beta_index.append([n1-sum_in_index,len(seq)])
				else:
					probable_beta_index.append([n1-sum_in_index,n5+sum_in_index])

	if break_index == []:
		probable_beta_index.append([0,len(seq)])
	print("Removing Duplicate B-sheet Indexes...")
	probable_beta_index_drm = [] 
	count = 0
	for x in probable_beta_index:
		if x not in probable_beta_index_drm:
			probable_beta_index_drm.append(x)
		else:
			count +=1
	print("Duplicates Removed: "+str(count))
	print("Checking Tetrapeptide B-sheet Breakers...")
	probable_beta_index_f1 = []
	for data in probable_beta_index_drm:
		if "----" not in temp_seq1[data[0]:data[1]]:
			probable_beta_index_f1.append(data)
	print("Removed: B-sheet Indexes With Tetrapeptide B-sheet Breakers")
	
	print("Predicting B-sheet Segments...")
	print("Condition: { P_beta > 1.05 and P_beta > P_alpha}")
	for data in probable_beta_index_f1:
		p_alpha = sum(prot_helix_prob[data[0]:data[1]]) / len(prot_helix_prob[data[0]:data[1]])
		p_beta = sum(prot_beta_prob[data[0]:data[1]]) / len(prot_beta_prob[data[0]:data[1]])
		if p_beta > 1.05 and p_beta > p_alpha:
			seq = seq.replace(seq[data[0]:data[1]],len(seq[data[0]:data[1]])*"B")
	print("Prediction Done/-\n")
	print("|-------------------{ EXITING CHOU-FASMAN ALGORITHM }-------------------|\n")

#####################################################################################################

	print("Generating Output in FASTA Format...\n")
	fasta_predicted_beta_seq = ""
	for i in range(0, len(seq), 70):
		fasta_predicted_beta_seq += seq[i:i+70]+"\n"
	print("Job Done/-\n\n")
	print("	Output: Protein Sequence With Predicted B-sheet Segments")
	print("	--------------------------------------------------------\n\n")
	print(header+fasta_predicted_beta_seq)
...

# python B-sheet_predictor.py <fasta_file>

### Reference:
### Prevelige, P. Jr. and Fasman, G.D., "Chou-Fasman Prediction of the
### Secondary Structure of Proteins," in Prediction of Protein Structure
### and The Priniciples of Protein Conformation (Fasman, G.D., ed.)
### Plenum Press, New York, pp. 391-416 (1989).
