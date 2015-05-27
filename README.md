# LSIEngine
Basic Implementation of Latent Semantic Analysis Engine in Python

REQUIREMENTS:
1. You will need pandas, numpy, and matplotlib packages installed on your python distribution
	
2. Examine LSIEngine.py import statements to double check 
	use pip to install or use the anaconda distribution of python available here: https://	store.continuum.io/cshop/anaconda/
	
3. There are two parts: LSIscript.py and LSIEngine.py
	
4. LSIscript.py is meant to be invoked in terminal via $ python LSIscript.py 

		$ python LSIscript.py -h to see how it works. The help summary is given below.
		
SCRIPT HELP SUMMARY:
usage: LSIscript.py [-h] [-o OUTPUTPATH] docsetpath stopwordspath

Perform latent semantic analysis on collection of documents.

positional arguments:
  docsetpath            the collection of .txt documents path
  stopwordspath         the stopword text file path

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUTPATH, --outputpath OUTPUTPATH
                        path to txt file where results are to be stored
                        Default is output.txt: stored where script is
                        executed.

TESTING:
For ease of use there's an Input folder to test the program on a few document collections.
	WHAT'S INSIDE:
	Input/docset2 contains a collection of math texts
	Input/docset1 contains a collection of project Gutenberg texts
	Input/stopwords.txt is a text file containing stopwords

TRY THIS:
Here's an example of how to run the script (assuming LSIscript.py and LSIengine.py are in the same directory where the Input folder is stored...):

	$ python LSIscript.py Input/docset2 Input/stopwords.txt

	or

	$ python LSIscript.py Input/docset2 Input/stopwords.txt -o Output/docset2results.txt

LITERATURE:
Refer to the PDF article for technical documentation discussing Latent Semantic Indexing.
