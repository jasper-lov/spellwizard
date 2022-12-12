from PyPDF2 import PdfReader
import json, re, os
from edit_distance_algorithms import spell_checker

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

    with open('cs375_words.txt', 'w') as f:
        for word in domain_words:
            f.write(f"{word}\n")


def main():
    ''' Main method
    ---------------------------------------
    Returns:
    ---------------------------------------
        void
    '''
    
    #Parses PDF into word_list of strings
    word_list = get_wordlist_from_pdf("CS375resources/CS375f22_proj4_DynamicProgramming.pdf")

    # Parses dictionary
    #dictionary = get_dictionary("wordlist/en_US-large.txt")
    dictionary = get_dictionary("wordlist/cs375_words.txt")


    correct_words = []

    for word in word_list:
        if word in dictionary and word not in correct_words:
            correct_words.append(word)

    with open('cs375_words.txt', 'w') as f:
        for word in correct_words:
            f.write(f"{word}\n")


    print('started')
    # Runs the spell checker on the pdf
    output = spell_checker(word_list, dictionary)

    json_obj = json.dumps(output, indent = 4)
    with open('output.json', 'w') as outfile:
        outfile.write(json_obj)

if __name__ == "__main__":
    main()