import numpy as np
import pandas as pd

class cryptoSolver:
    matrix: np.ndarray
    predictions: dict[list] # no pongo tipo porque tendrá el primero como int, resto como diccionarios
    letters: list[str]
    result_in_matrix: list[int]
    letters_appears_columns: dict
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
        self.letters_appears_columns = self.getLettersAppearsColumns()

        self.result_in_matrix = self.matrix[-1]
        self.predictions = {}
        #self.hasSolution = self.solveLetters()
    
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

    def solveLetters(self, index: int = 0, digits_available: list = None) -> bool:
        if digits_available is None:
            digits_available = list(range(10))
        
        # caso base
        if index == len(self.letters):
            return self.verifyCongruenceWithCarry()
        
        letter: str = self.letters[index]
        
        for digit in digits_available:
            # probamos con todos los digitos disponibles en este nivel, si ninguno da, nos devolvemos.
            if self.verifyCongruence(letter, digit):

                self.predictions[letter] = digit
                # "actualizamos" digit_avaible (en otra var) para ignorar el digit que falló
                remaining: list = [d for d in digits_available if d != digit]

                #intentamos con sig letra
                if self.solveLetters(index + 1, remaining):
                    return True
                
                # eliminamos predicción para intentar con otra porque en siguiente letra ninguna funcionó, entonces hay que hacer backtracking
                self.predictions.pop(letter)
        
        return False

    def verifyCongruence(self, letter: str, possible_value: int) -> bool:
        # obtener indices de columnas donde sale esa letra
        for index_col in self.getLettersAppearsColumns[letter]:
            addens: list = [x for x in self.matrix[:-1, index_col].tolist() if x != '']
            result_letter: str = self.result_in_matrix[index_col]

            values: list = [self.getDigit(adden, letter, possible_value) for adden in addens] + [self.getDigit(result_letter, letter, possible_value)]

            if(None in values): # si alguno de los valores es none, no se puede hacer suma (incluso el result)
                return True # se puede añadir, porque todavia no hay forma de saber
            
            total: int = sum(values[:-1])
            if total == values[-1]:
                return True
            
        return False
    
    def verifyCongruenceWithCarry(self) -> bool:
        carry: int = 0
        # recorremos de derecha a izq
        for index in range(np.fliplr(self.matrix).T):
            
            index_inv = len(self.matrix[0] - 1) - index

            #obtenemos sumandos y resultado
            addens: list = [x for x in self.matrix[:-1, index_inv].tolist() if x != '']
            result_letter: str = self.result_in_matrix[index_inv]

            #obtenemos int asociados a cada elemento
            values: list = [self.predictions[adden] for adden in addens]
            result_value = self.predictions[result_letter]

            # sumamos teniendo en cuenta carry
            total: int = sum(values) + carry

            if total % 10 != result_value:
                return False    
        
            carry = total // 10
        
        # si llega acá, nada falló, entonces está bien, todo coincide
        return carry == 0



    def getDigit(self, letter: str, new_letter: str = None, possible_value: int = None) -> int:
        # letter es cualquier letra que nos salga en adden
        # new letter es para verificar si es la letra que estamos verificando para añadir a 
        # predictions, y como todavia no esta ahi, tenemos que retornar el valor manualmente 
        if letter == new_letter and possible_value is not None:
            return possible_value
        return self.predictions[letter]

    
    def getLettersAppearsColumns(self):
        self.getLettersAppearsColumns = dict.fromkeys(self.letters)
        for letter in self.letters:
            rows, cols = np.where(self.matrix == letter)
            print(rows, cols)

            col_indexes = list(set(cols))
            self.getLettersAppearsColumns[letter] = col_indexes

    def solveCode():
        pass


def main():
    crypto_solver = cryptoSolver()

if __name__ == "__main__":
    main()