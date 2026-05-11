import numpy as np
import pandas as pd
from itertools import zip_longest

class cryptoSolver:
    matrix: np.ndarray
    predictions: list # no pongo tipo porque tendrá el primero como int, resto como diccionarios
    letters: list[str]

    def __init__(self):
        matrix =  [
            ['h', 'a' ,'r', 'r', 'y'],
            ['p', 'o', 't', 'r', 'e', 'r'],
            ['t', 'r', 'o', 'r', 'l', 's'],
            ['t', 'r', 'o', 'e', 'l', 's'],
            ['t', 'r', 'o', 'e', 'l', 's']
        ]
        self.matrix = self.normalizeMatrix(matrix)
        self.letters = self.getLetters()
        print(self.letters)
    
    @staticmethod
    def normalizeMatrix(matrix: list) -> np.array:
        # pasamos todas las listas, recorre elemento fila por fila, y cuando llega a corta, la rellena con ''
        normalized_matrix: list = zip_longest(*matrix, fillvalue='')

        # aplica transmposición porque zip_longest trabaja con ella al reves
        return np.array(list(normalized_matrix)).T


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


def main():
    crypto_solver = cryptoSolver()


if __name__ == "__main__":
    main()