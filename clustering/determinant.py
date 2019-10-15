def determinant(A):
    #value check for square matrix
    if len(A) != len(A[0]):
        raise ValueError("The determinant only exists for square matrices")
    #base case for recursive algorithm
    if len(A) == 1:
        return A[0][0]
    
    sign = 1
    det = 0
    for i in range(len(A[0])):
        sub_matrix = [row[0:i] + row[i+1:] for row in A[1:]]
        det += sign * A[0][i] * determinant(sub_matrix)
        sign *= -1
    return det