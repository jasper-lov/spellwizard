
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

print(editDistanceIterative(S,T))

#INPUT: t, a list of words in the text and d, a list that represents a dictionary
#OUTPUT: A dictionary with all the mispelled words and 5 possible corrections
def spell_checker(t, d):
    #Dictionary to hold the answer
    output_dict = collections.defaultdict(list)
    d_set = set(d)

    #Iterate over every word in T
    for word in t:
        #If word is not in the dictionary calculate its edit distance and append it to a list
        if word not in d_set:
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

t = ['hell',"myn", "names", "is", "dylan"]
d = ['hello','my',"name", "is", "dylan"]

print(spell_checker(t,d))
