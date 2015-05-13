#!/usr/bin/env python
import argparse, os, re
import LSIEngine as LS
import matplotlib.pyplot as plt



parser = argparse.ArgumentParser(description = 'Perform latent semantic analysis' +
								' on collection of documents.')
parser.add_argument('docsetpath', help = "the collection of .txt documents path")
parser.add_argument('stopwordspath', help = "the stopword text file path")
parser.add_argument('-o','--outputpath', type = str, action = 'store', default = 'output.txt', help = "path to txt file where"
						+ " results are to be stored\n Default is output.txt: stored where script is executed.")
args = parser.parse_args()

doc_collection_path = args.docsetpath 
stopword_path = args.stopwordspath
output_path = args.outputpath

#create output text file path if it doesn't exist!
if output_path is 'output.txt':
	pass
else:
	if not  os.path.exists(re.sub(r'[^\/\\]+\/?$', '',output_path)):
		os.makedirs(re.sub(r'[^\/\\]+\/?$', '',output_path))

#Create list of text document paths for analysis
doclist = LS.create_doclist(doc_collection_path)

#Process stopwords text file into set
stopwords = LS.process_stopwords(stopword_path)

#create instance of LSI class
LSI = LS.LSI(stopwords,doclist)

#Produce Term-Document Matrix: entries are weighted as relative frequencies
LSI.term_matrix()
#print("Term document matrix with weighted entries is \n")
#print(LSI.A)

#Perform SVD on Term-Document Matrix
LSI.svd_compute()

#Obtain constituents of SVD of A
#print("The matrix U in the SVD of A is given by:\n")
#print(LSI.U)

#print("The matrix Sigma in the SVD of A is given by:\n")
#print(LSI.Sigma)

#print("The matrix V in the SVD of A is given by:\n")
#print(LSI.V)

#Analyze variation contribution of singular values in Sigma
#print(LSI.singular_contribution())


#Plot contribution
print("The contribution of each singular value is plotted below:\n")
print("PLEASE CHOOSE THE FIRST FEW k SINGULAR VALUES THAT CONTRIBUTE MOST VARIATION\n"
	+ "EXAMINE THIS PLOT TO MAKE THE CHOICE..\n")
print("FOR EXAMPLE: if the first knee or elbow occurs at singular value index 2:\n"
	+"then make a choice of 2 singular values and exit the plot window.\n")
fig1 = LSI.plot_contribution()
plt.draw()
plt.show(block = False)
#Prompt user to specify how many singular values to retain
#It is recommended to retain those singular values that contribute most variation
retain  = input('Judging from the  plot, how many singular values would you like to retain? ')
k = int(retain)
LSI.svd_dimensionreduce(k)
plt.cla()

#Obtain document similarity listings in decreasing order
print("DOCUMENT SIMILARITIES ARE LISTED BELOW:\n")
fig2 = LSI.doc_similarity(output_path)
print("DOCUMENT SIMILARITY RESULTS ARE STORED IN {}, BE SURE TO EXAMINE!".format(output_path))
print("BE SURE TO CLOSE PLOT WINDOW TO EXIT SCRIPT")
plt.draw()
plt.show()




