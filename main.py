import numpy as np
import pandas as pd

class cryptoSolver:
    matrix: np.ndarray
    predictions: dict[list] # no pongo tipo porque tendrá el primero como int, resto como diccionarios
    letters: list[str]
    result_in_matrix: list
    hasSolution: bool
    codeToDecode: list[int]

    def __init__(self):
        matrix =  [
            ['h', 'a' ,'r', 'r', 'y'],
            ['p', 'o', 't', 'r', 'e', 'r'],
            ['t', 'r', 'o', 'r', 'l', 's'],
            ['t', 'r', 'o', 'e', 'l', 's'],
            ['t', 'r', 'o', 'e', 'l', 's']
        ]
        self.matrix = self.normalizeMatrix(matrix)
        print(self.matrix)
        self.letters = self.getLetters()
        print(self.letters)
        self.result_in_matrix = self.matrix[-1]
        self.predictions = {}
        self.hasSolution = self.solveLetters()
    
    @staticmethod
    def normalizeMatrix(matrix: list) -> np.array:

        max_len: int = max(len(row) for row in matrix) #obtenemos fila más larga
        normalized_matrix: list = np.array([[''] * (max_len - len(row)) + row for row in matrix]) # rellenamos al inicio lo que les falta a las demas con '' 
        # -> sumas se asumiran alineadas a derecha

        return normalized_matrix


    def getLetters(self) -> list:
        # obtener cantidad de letras repetidas por columna
        number_repeats_per_column: list = []
        self.getRepeatedQuantityPerColumn(number_repeats_per_column)

        # añadir columnas de mayor a menor

        # obtenemos los indices "originales" de los elementos de mayor a menor
        ordered_index: list = np.argsort(number_repeats_per_column)[::-1]
        letters: list = []

        for idx in ordered_index:
            column: list = self.matrix[:, idx].tolist()
            column_repetless: list = list(dict.fromkeys(column)) # column sin repetidos

            # añadimos solo elementos que no esten en letters ya
            letters.extend([e for e in column_repetless if e != '' and e not in letters])

        print("\nColumnas en orden de importancia:", letters)

        return letters

    def getRepeatedQuantityPerColumn(self, number_repeats_per_column: list) -> None:
        # obtiene suma de cantidad de elementos repetidos de una columna (por ejemplo, si tenemos t:3, r:2, a:1, esta funcion nos da 5, porque solo suma los que estan repetidos, a solo tiene 1, por eso no se toma en cuenta)
        for i in range(self.matrix.shape[1]):
            column: list = self.matrix[:, i]

            # np.unique nos devuelve los valores y cuántas veces aparecen
            values: str; quantity: list
            values, quantity = np.unique(column, return_counts=True)

            # Filtramos solo las cuentas que son mayores a 1 y las sumamos
            # Si 'a' aparece 3 veces, suma 3 al total de esa columna
            repeated_quantity: int = quantity[quantity > 1].sum()
            number_repeats_per_column.append(int(repeated_quantity))

        print("Total de elementos repetidos por columna:", number_repeats_per_column)

    def solveLetters(self, index=0, digits_available=None):
        if digits_available is None:
            digits_available = list(range(10))
        
        # caso base
        if index == len(self.letters):
            return self.verifyCongruence()
        
        letter = self.letters[index]
        
        for digit in digits_available:
            # probamos con todos los digitos disponibles en este nivel, si ninguno da, nos devolvemos.
            if self.verifyCongruence(letter, digit):

                self.predictions[letter] = digit
                # "actualizamos" digit_avaible (en otra var) para ignorar el digit que falló
                remaining = [d for d in digits_available if d != digit]

                #intentamos con sig letra
                if self.solveLetters(index + 1, remaining):
                    return True
                
                # eliminamos predicción para intentar con otra porque en siguiente letra ninguna funcionó, entonces hay que hacer backtracking
                self.predictions.pop(letter)
        
        return False

    def verifyCongruence(self, letter: str, possible_value: int) -> bool:
        
        # verifica que valor pasado si encage en todo el result
        pass
    
    @staticmethod
    def getDigit(digits_available: list, ignore_digit: int | None) -> int | None:
        if not digits_available:
            return None

        if ignore_digit is None:
            return digits_available[0]

        for digit in digits_available:
            if digit != ignore_digit:
                return digit

        return None
        

    def solveCode():
        pass

    


def main():
    crypto_solver = cryptoSolver()


if __name__ == "__main__":
    main()