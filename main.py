from CryptoSolver import CryptoSolver

def main():
    matrix: list = [
        ['h', 'a', 'r', 'r', 'y'],
        ['p', 'o', 't', 't', 'e', 'r'],
        ['t', 'r', 'o', 'l', 'l', 's']
    ]

    encoded_message: list = [9,0,3,9,0,0,4,3,9,6,5,1,8,4,8]
    solver = CryptoSolver(matrix, encoded_message)


if __name__ == "__main__":
    main()