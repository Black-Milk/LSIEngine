import collections, os, re, glob
from string import whitespace
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import pylab

def create_doclist(dir):
    """
        Returns list of document paths to text files
        inside specified directory.

        dir: path for folder containing document collection

    """
    dir = dir + '/*.txt'
    doclist = glob.glob(dir)
    return doclist

def process_stopwords(dir):
    """
        Returns set of words obtained stopwords text file

        dir: path to stopword text file
    """
    stopwords = set(line.strip() for line in open(dir))
    return stopwords


class LSI:
    """
        Class definitions for Latent Semantic Analysis Object
    """
    
    def __init__(self,stopwords,doclist):
        """
            stopwords: a set type object containing stopwords
            doclist : a list object containing text document paths 
        """
        self.stopwords = stopwords
        self.doclist = doclist

            
    #generate term-document matrix
    def term_matrix(self):
        """
            Construct Term Document Matrix. The matrix entries are weighted as term frequencies.
            Other weighting schemes will be implmented in the future...
        """
        
        #function to create counter for terms in each document
        def _word_count(docname):
            """
                Return dictionary type object storing document words as keys
                and their respective counts as values.
            """
            with open(docname) as doc:
                doc_contents = doc.read()
                bagofwords = re.split(r'[0-9\W_]+', doc_contents.lower())
                tokenlist = [token for token in bagofwords
                             if len(token) > 3 and token not in self.stopwords]
                token_count = collections.Counter(tokenlist)
                return token_count
        
        #create empty term-document dataframe
        term_df = pd.DataFrame()
        # iterate over each document in document list
        for docfile in self.doclist:
            #tally each term inside each document of doclist
            word_counter = _word_count(docfile)
            #create document data frame containing tallies for each term in document
            doc_df = pd.DataFrame.from_dict(word_counter,
                                             orient = 'index')
            #tidy up column names for document data frame
            docfile = re.sub(r'.*[/\\\\]', '',docfile).replace('.txt', '')
            doc_df.columns = [docfile]
            #instead of using counts as entries, use relative frequencies
            doc_df.ix[:, 0] = doc_df.values.flatten() / float(doc_df.values.sum())
            #aggregate doc data frame to term-document data frame
            term_df = term_df.join(doc_df, how ='outer',)
            #replace NANs in term dataframe with Zero
            term_df = term_df.fillna(0)    
         # construct term-doc matrix         
        self.A = term_df
        return self.A
    
    #EXPERIMENTAL: create a vocabulary set
    def create_vocabulary(self):
        """EXPERIMENTAL: TO BE USED WITH QUERY VECTORIZE METHOD, YET TO BE IMPLEMENTED"""
        tokenlist = []
        for doc in self.doclist:
            doc_contents = open(doc).read()
            bagofwords = re.split(r'[0-9\W_]+', doc_contents.lower())
            for token in bagofwords:
                if len(token)>3 and token not in self.stopwords:
                    tokenlist.append(token)  
        return set(tokenlist)   
        
    
    
    #perform singular value decomposition
    def svd_compute(self):
        """Performs singular value decomposition of the Term Document Matrix
            TODO: Provide Support for Sparse Matrices to minimize strain on memory
        """
        #return 3-tuple of three arrays as part of SVD Decomposition
        SVD = np.linalg.svd(self.A)
        self.U, self.Sigma, self.V = SVD      
        return SVD
    
                
    #heuristic to measure contribution of singular values
    def singular_contribution(self):
        """
            Returns list of Singular Value Total Variation Scores.
            Refer to documentation for further study.
        """
        contributionlist = []
        sum_square = sum([i**2 for i in self.Sigma])
        for i in self.Sigma:
            f_i = i**2/sum_square
            contributionlist.append(f_i)
        return contributionlist
    
    #plot variation contribution of singular values 
    def plot_contribution(self):
        """
            Returns plot displaying the variation that each singular value
            contributes.
        """
        contrib = self.singular_contribution()
        fig = plt.plot(list(range(1,len(contrib)+1)),contrib)
        plt.ylabel('Variation Contribution')
        plt.xlabel('Singular Value Index')
        return fig

    #perform low-rank approximation of Term-Document Matrix
    def svd_dimensionreduce(self, k):
        """
        Returns SVD constituents of low-rank approximation matrix for term-document matrix A.
        The low-rank approximation of term-doc matrix A is merely obtained
        by retaining the first k columns of U, first k rows of V, and first k
        singular values along the diagonal of Sigma, where the singular values are
        in decreasing order.
        """
        self.Uk = self.U[:,0:k]
        self.Vk = self.V[0:k,:]
        self.Sigmak = np.diag(self.Sigma[0:k])
        return self.Uk, self.Sigmak, self.Vk
    
    def doc_similarity(self, resultspath = None):
        """
            Returns results displaying similarities amongst documents. Also writes
            results to text file.
        """
        if resultspath is None:
            resultspath = 'output.txt'
        else:
            resultspath = resultspath
        
        def frobenius_dist(di,dj, sigma = self.Sigmak):
            """
                A similarity metric utilizing the Frobenius norm to measure document
                similarities. Refer to documentation.
            """
            return np.linalg.norm(np.array(di-dj)*sigma)
        
        vk_df = pd.DataFrame(self.Vk, columns = self.A.columns)
        vk_df.apply(lambda x: np.round(x,decimals =2))
        dist_df = pd.DataFrame(index=vk_df.columns, columns=vk_df.columns)
        for cname in vk_df.columns:
            dist_df[cname] = vk_df.apply(lambda x: frobenius_dist(vk_df[cname].values, x.values))
        fig = plt.imshow(dist_df.values, interpolation = 'nearest')
        axleg = plt.gca()
        plt.xticks(range(len(dist_df.columns.values)))
        plt.yticks(range(len(dist_df.index.values)))
        axleg.set_xticklabels(dist_df.columns.values, rotation=90)
        axleg.set_yticklabels(dist_df.index.values)
        plt.title("Similarity between documents\nLower value = more similar")
        plt.colorbar()
            
        with open(resultspath, 'w') as text:
            for doc in dist_df.columns:
                sim_doc_df = dist_df.sort(columns=doc)[doc]
                sim_docs = sim_doc_df.drop([doc]).index
                print('Documents most similar to ' + doc + ':\n'
                        + '(in decreasing order)\n'
                        + ', '.join(sim_docs)
                        + '\n')

                text.write('Documents most similar to ' + doc + ':\n'
                            + '(in decreasing order)\n'
                            + ', '.join(sim_docs)
                            + '\n\n')
        return fig

if __name__ == '__main__':
	pass
