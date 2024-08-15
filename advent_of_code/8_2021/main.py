import numpy as np

# https://adventofcode.com/2021/day/8

def main():
    # Read input file
    with open('/Users/sixteoriolllenassegura/code_training/advent_of_code/8_2021/input.txt', 'r') as file:
        input = file.read().splitlines()

    # PART ONE
    counts = [len(x) for x in ' '.join([x.split('| ')[1] for x in input]).split(' ')]
    a = counts.count(2) # Count 1s
    b = counts.count(3) # Count 7s
    c = counts.count(4) # Count 4s
    d = counts.count(7) # Count 8s
    # print(a + b + c + d)

    # PART TWO
    # For each digit, we write which characters are highlighted on a seven-segment display
    segments = ['abcefg',
                'cf',
                'acdeg',
                'acdfg',
                'bcdf',
                'abdfg',
                'abdefg',
                'acf',
                'abcdefg',
                'abcdfg']
    
    # Letters and their corresponding order
    letter2num = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6}
    num2letter = list(letter2num.keys())

    # Given a string, obtain a binary vector
    # For example, 'abd' yields [1,1,0,1,0,0,0]
    def str2vec(string):
        vec = np.zeros(7, dtype = int)
        for char in string:
            vec[letter2num[char]] = 1
        return vec

    # Simplify the matrix applying the following logic
    # ab -> cf means that either (a,b) -> (c,f) or (a,b) -> (f,c)
    # Therefore, no other letter, apart from a or b, can be mapped to f or c
    # This logic allows us to simplify the matrix
    def clean_matrix(matrix):
        for i in range(7): # For each row
            row_i = matrix.tolist()[i]
            x = matrix.tolist().count(row_i)
            # If the n. of repeated rows is the same as the n. of ones on each row,
            # use this subgroup to make zeros
            if x == np.sum(matrix[i]):
                for j in range(7):
                    row_j = matrix.tolist()[j]
                    if row_i != row_j:
                        matrix[j] *= 1 - matrix[i]

    # Example: instructions = ['eafcbg', 'dbage', 'egbcdf', 'eagbfdc', 'gf', 'edbfc', 'gfb', 'cafbde', 'fdgeb', 'gdcf']
    instructions_list = [x.split(' | ')[0].split(' ') for x in input]
    # Example: ['cdfeb', 'fcadb', 'cdfeb', 'cdbaf']
    to_decode_list = [x.split(' | ')[1].split(' ') for x in input]

    numbers = [] # To store final result
    for instructions, to_decode in zip(instructions_list, to_decode_list):
        matrix = np.ones([7,7])
        
        # Identify easy numbers first
        # 1 is the only number whose string has length 1
        # 7 is the only number whose string has length 3
        # 4 is the only number whose string has length 4
        # 8 does not help, since it always has all the possible characters
        for x in instructions:
            if len(x) == 2: # Number 1
                str_1 = x
            elif len(x) == 3: # Number 7
                str_7 = x
            elif len(x) == 4: # Number 4
                str_4 = x

        # Create the first zeros in our matrix
        # ab -> cf means a is either c or f && b is either c or f
        # a: 0 0 1 0 0 1 0
        # b: 0 0 1 0 0 1 0
        # c: 1 1 1 1 1 1 1
        # d: 1 1 1 1 1 1 1
        # e: 1 1 1 1 1 1 1
        # f: 1 1 1 1 1 1 1
        # g: 1 1 1 1 1 1 1
        for n, string in zip([1,7,4],[str_1, str_7, str_4]):
            vec = str2vec(segments[n])
            for x in string:
                matrix[letter2num[x]] *= vec

        # Clean the matrix a sufficient amount of times
        for _ in range(10):
            clean_matrix(matrix)

        # Normalize so that each row sums up to 1
        matrix_div = matrix.copy()
        matrix_div /= np.sum(matrix, axis = 1, keepdims=True)

        # Simplify the matrix applying the following logic
        # 'cdfbe' can correspond to either 'acdeg', 'acdfg' or 'abdfg'
        # However, ef -> bd, so 'acdeg' and 'acdfg' should have 'b'
        # The only option left is cdfbe -> abdfg
        for x in [ins for ins in instructions if len(ins) == 5]: # Either 2, 3, or 5
            vec_x = str2vec(x).astype(bool)
            submatrix = matrix_div[vec_x]
            sum = np.sum(submatrix, axis = 0)
            for y in [seg for seg in segments if len(seg) == 5]: # Either 2, 3, or 5
                vec_y = str2vec(y)
                compatible = True # Does 'cdfbe' correspond to the segment y?
                for i in range(7):
                    # sum[i] == 1 requires i-th letter to be an option
                    # If vec_y[i] == 0, i-th letter cannot be chosen -> contradiction
                    if vec_y[i] == 0 and sum[i] == 1:
                        compatible = False
                        break
                
                # We found the corresponding segment to 'cdfbe' :)
                if compatible:
                    matrix[vec_x] *= vec_y
                    break

        # Clean the matrix a sufficient amount of times
        for _ in range(10):
            clean_matrix(matrix)

        # Having found the correlation between letters, find hidden output
        new_words = []
        for word in to_decode:
            for j in range(7):
                x = num2letter[j]
                y = np.argwhere(matrix[j])[0][0]
                y = num2letter[y].capitalize() # We capitalize not to mix old and new letters
                word = word.replace(x, y) # Translate
            
            new_words.append(''.join(sorted(word)).lower())

        number = ''
        for word in new_words:
            number += str(segments.index(word))
        numbers.append(int(number)) # Append to sum

    print('Result:')
    print(np.sum(numbers))


if __name__ == "__main__":
    main()