from PyPDF2 import PdfReader

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


def main():
    ''' Main method
    ---------------------------------------
    Returns:
    ---------------------------------------
        void
    '''

    # Parses PDF into word_list of strings
    word_list = get_wordlist_from_pdf("CS375f22_proj4_DynamicProgramming.pdf")

    # Prints it
    print(word_list)


if __name__ == "__main__":
    main()