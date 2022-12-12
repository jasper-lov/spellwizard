from PyPDF2 import PdfReader
import json
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

        # Splits page (string) into words (smaller strings), and removes 
        #   non-alphabetical chars (-, 123, etc.) and adds to return list
        words = text.split(' ')
        
        for word in words:
            parsed_word = ''.join(char for char in word if char.isalpha())
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


def main():
    ''' Main method
    ---------------------------------------
    Returns:
    ---------------------------------------
        void
    '''

    # Parses PDF into word_list of strings
    word_list = get_wordlist_from_pdf("CS375f22_proj4_DynamicProgramming.pdf")

    # Parses dictionary
    dictionary = get_dictionary("wordlist/en_US-large.txt")
    #print(len(dictionary))
    print('started')
    # Runs the spell checker on the pdf
    output = spell_checker(word_list, dictionary)

    json_obj = json.dumps(output, indent = 4)
    with open('output.json', 'w') as outfile:
        outfile.write(json_obj)

    print(output)




if __name__ == "__main__":
    main()