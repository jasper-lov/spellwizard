from PyPDF2 import PdfReader
import json, re, os, sys, time
import collections


#recursive approach for finding edit distance from S to T

#INPUT: string S and string T with length of S being m and length of T being n
#OUTPUT: minimum edit from S to T
def editDistanceRec(S , T ):
    #recursive case: when S is empty, it will require n appends to transform S into T, thus the edit distance from S to T is n; 
    #when T is empty, it will require m deletes to transform S into T, thus the edit distance from S to T is m; 
    #however no matter what the case is the edit distance will always equal to m *n
    if len(S) == 0 or len(T) == 0:
        return len(T) + len(S)
    else:
        #recursive cases
        m = len(S)
        n = len(T)
        #when the last two elements are equal to eachother, the amount of operations required to transform S to T will be the amounf of 
        #operations needed to transform all of S excluding its last item to all of T excluding its last item
        if S[m-1] == T[n-1]:
            return editDistanceRec(S[0:m-1],T[0:n-1])
        #When the last two elements are not equal to eachother, the edit distance from S to T is the minimum of a replacement of S[m-1] with 
        # T[n-1] and edit distance upon S[0...m-2] and T[0...n-2], a deletion of S[m-1] and edit distance upon S[0...m-2] and T[0...n-1], or 
        # a insertion of T[m-1] at the end of S and edit distance upon S[0...m-1] and T[0...n-2]
        else:
            return 1 + min(editDistanceRec(S[0:m-1],T[0:n-1]),editDistanceRec(S[0:m-1],T),editDistanceRec(S,T[0:n-1]))


            

#INPUT: string S and string T with length of S being m and length of T being n
#OUTPUT: minimum edit from S to T
def editDistanceIterative(S,T):
    M = len(S)
    N = len(T)

    #table to hold the distance of editDistances of all substrings of S and T
    distance_table = [[0] * (M+1) for i in range(N+1)]
    
    #initializes the base cases when S or T are empty and the edit distance is equal to len(S) + len(T)
    for i in range(M+1): distance_table[0][i] = i
    for i in range(N+1): distance_table[i][0] = i

    #this will iteratively find the edit distance between S and T in the following method: when the the last characters of S and T are equal
    #the edit distance is given by the edit distance of S[0...m-2] and T[0...n-2]. When the last characters of S and t are not equal the edit 
    #distance is given by the minimum edit distance resutlting from a replacement, insertion, or deletion.
    for n in range(1,N+1):
        for m in range(1,M+1):
   
            if S[m-1] == T[n-1]:
                distance_table[n][m] = distance_table[n-1][m-1]
            else:
                distance_table[n][m] = 1 + min(distance_table[n-1][m-1], distance_table[n][m-1], distance_table[n-1][m])

    return distance_table[N][M]



S = "analysis"
T = "algorithms"

#print(editDistanceIterative(S,T))

#INPUT: t, a list of words in the text and d, a list that represents a dictionary
#OUTPUT: A dictionary with all the mispelled words and 5 possible corrections
def spell_checker(t, d):
    #Dictionary to hold the answer
    output_dict = collections.defaultdict(list)

    #Iterate over every word in T
    for word in t:
        #If word is not in the dictionary calculate its edit distance and append it to a list
        if word not in d:
            possible_corrections = []

            for correct_word in d:
                dist = editDistanceIterative(word, correct_word)
                possible_corrections.append((correct_word, dist))

            #Sort the possible corrections by edit distance
            possible_corrections = sorted(possible_corrections, key = lambda x: x[1])
            #Assign 
            for i in range(5):
                output_dict[word].append(possible_corrections[i][0])

    return output_dict

def spell_checker_recursive(t, d):
    #Dictionary to hold the answer
    output_dict = collections.defaultdict(list)

    #Iterate over every word in T
    for word in t:
        #If word is not in the dictionary calculate its edit distance and append it to a list
        if word not in d:
            possible_corrections = []

            for correct_word in d:
                dist = editDistanceRec(word, correct_word)
                possible_corrections.append((correct_word, dist))

            #Sort the possible corrections by edit distance
            possible_corrections = sorted(possible_corrections, key = lambda x: x[1])
            #Assign 
            for i in range(5):
                output_dict[word].append(possible_corrections[i][0])

    return output_dict


#INPUT: t, a list of words in the text and d, a list that represents a dictionary
#OUTPUT: A dictionary with all the mispelled words and 5 possible corrections
def improved_spell_checker(t, d):

    #output dictionary that the algorithm will return
    output_dict = collections.defaultdict(list)

    #for all the words in the input text
    for word in t:

        #if the word is not a correct word
        if word not in d:
            
            possible_corrections = [] #the list of possible corrections for the word
            distance_table = {} #table containing all of the correct words in the dictionary that we've checked and their edit distance

            word_length = len(word) #length of word
            length_difference = 1 #represents the difference in length between word and correct words searched in loop below
            lower_bound = word_length - length_difference #lower bound of best-case edit distance
            upper_bound = word_length + length_difference #upper bound of best-case edit distance
            
            #while we don't yet have our 5 closest word suggestions
            while len(possible_corrections) < 5:
                
                #for all the correct words in the dictionary
                for correct_word in d:
                    
                    #if the correct word is within length difference from word and we have not already appended it to possible corrections
                    #and we have not yet found 5 possible corrections
                    if ((len(correct_word) in range(lower_bound, upper_bound + 1)) and (correct_word not in possible_corrections)
                        and (len(possible_corrections) < 5)):
                        
                        #if correct word and its distance not in distance table, find distance and add to distance table:
                        if correct_word not in distance_table:
                            dist = editDistanceIterative(word, correct_word)
                            distance_table[correct_word] = dist
                            
                        #if we have already computed correct word's distance, look up the value in the table
                        else:
                            dist = distance_table[correct_word]
                            
                        #if the distance is best case given the length difference
                        if dist <= length_difference:
                            possible_corrections.append(correct_word)

                #increment and increase best case range size
                length_difference += 1
                
                #prevent negative lower bound
                if lower_bound > 0:
                    lower_bound = word_length - length_difference
                upper_bound = word_length + length_difference
                
            #add word along with 5 possible corrections to output dictionary
            output_dict[word].append(possible_corrections)
            
    return output_dict

def get_wordlist_from_pdf(filepath):
    ''' Reads in a PDF from filepath, and returns list of words in that PDF
    ---------------------------------------
    Returns:
    ---------------------------------------
        Python List. type = String, len = pdf_word_length
    '''
    
    pdfReader = PdfReader(filepath)
    word_list = []

    for page in pdfReader.pages:
        text = page.extract_text()

        words = re.split(' |\n', text)
        # Splits page (string) into words (smaller strings), and removes 
        #   non-alphabetical chars (-, 123, etc.) and adds to return list
        
        for word in words:
            parsed_word = ''.join(char for char in word if char.isalpha()).lower()

            if parsed_word != '':
                word_list.append(parsed_word)
                

    return word_list

def get_dictionary(filepath):
    ''' Reads in a txt from filepath, and returns list of words in that txt
    ---------------------------------------
    Returns:
    ---------------------------------------
        Python List. type = String, len = dictionary_length
    '''
    

    dictionary = []
    with open(filepath, 'r') as f:
        line = f.readline()
        while line:
            dictionary.append(line.strip())
            line = f.readline()

    return dictionary

def import_cs375_domain_dictionary():
    ''' Write a .txt file of words found in CS375 documents
    ---------------------------------------
    Returns:
    ---------------------------------------
        void
    '''

    directory = os.getcwd() + '/CS375resources'

    domain_words = []

    for filename in os.listdir(directory):
        if filename != ".DS_Store":

            print("Reading in CS375 resources (this may take a minute...)")
            print("Reading " + filename)

            filepath = os.path.join(directory, filename)
            word_list = get_wordlist_from_pdf(filepath)
            
            # Parses dictionary
            dictionary = get_dictionary("wordlist/en_US-large.txt")

            for word in word_list:
                if word in dictionary and word not in domain_words:
                    domain_words.append(word)

    with open('wordlist/cs375_words.txt', 'w') as f:
        for word in domain_words:
            f.write(f"{word}\n")

def main( argv ):
    ''' Main method
    ---------------------------------------
    Returns:
    ---------------------------------------
        void
    '''
    
    # Un-comment to import .pdf files (from /CS375resources directory)
    #import_cs375_domain_dictionary(
    

    #Parses PDF into word_list of strings
    word_list = get_wordlist_from_pdf("" + argv[4])

    #CS375resources/CS375f22_proj4_DynamicProgramming.pdf
    

    # Parses dictionary
    dictionary = get_dictionary("wordlist/en_US-large.txt")
    #dictionary = get_dictionary("wordlist/cs375_words.txt")


    start = time.time()

    # Command line arguments    
    if argv[2] == "base":
        if argv[3] == "generic":
            dictionary = dictionary[:100]
            if argv[4] == "demo.pdf":
                if argv[1] == "i":
                    word_list = ["helldsa", "mynd", "namersd", "isss", "algorrsz", "algoraa", "tsdf"]
                    output = spell_checker(word_list, dictionary)
                if argv[1] == "r":
                    word_list = ["helldsa", "mynd", "namersd", "isss", "algorrsz", "algoraa", "tsdf"]
                    output = spell_checker_recursive(word_list, dictionary)
            if argv[4] != "demo.pdf":
                    word_list = get_wordlist_from_pdf("" + argv[4])
                    output = spell_checker_recursive(word_list, dictionary)
        if argv[3] == "domain":
            dictionary = get_dictionary("wordlist/cs375_words.txt")
            output = spell_checker(word_list, dictionary)
    if argv[2] == "imp":
        dictionary = get_dictionary("wordlist/cs375_words.txt")
        output = improved_spell_checker(word_list, dictionary)

    end = time.time()

    print("Time elapsed: " + str(end - start) + " seconds")

    #print('started')
    # Runs the spell checker on the pdf
    
    #output = improved_spell_checker(word_list, dictionary)

    

    json_obj = json.dumps(output, indent = 4)
    with open('output.json', 'w') as outfile:
        outfile.write(json_obj)

if __name__ == "__main__":
    main(sys.argv)