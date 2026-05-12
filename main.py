import numpy as np
from collections.abc import Iterator

class CryptoSolver:

    def __init__(self):

        matrix = [
            ['h', 'a', 'r', 'r', 'y'],
            ['p', 'o', 't', 't', 'e', 'r'],
            ['t', 'r', 'o', 'l', 'l', 's']
        ]

        self.matrix = self.normalize_matrix(matrix)

        self.result_row = self.matrix[-1]
        self.addend_rows = self.matrix[:-1]

        self.predictions = {}

        self.non_zero_letters = self.get_letters_cannot_be_zero()

        self.has_solution = self.solve_column(col=self.matrix.shape[1] - 1, carry=0)

        print(self.predictions)
        print(self.has_solution)


    @staticmethod
    def normalize_matrix(matrix: list) -> np.ndarray:
        """Añadimos espacios en blanco, si es necesario, al inicio de las filas cortas, para que queden todas del mismo tamaño"""

        max_len: int = max(len(row) for row in matrix)
        normalized_matrix: np.ndarray = np.array([[''] * (max_len - len(row)) + row for row in matrix])

        return normalized_matrix


    def get_letters_cannot_be_zero(self) -> set:
        """Obtenemos el primer caracter diferente de '' de cada letra (row), pues, como cada palabra es un numéro, estos no deben empezar por 0."""
        
        letters: set = set()

        for row in self.matrix:

            for char in row:
                if char != '':
                    letters.add(char)
                    break

        return letters


    def get_digit(self, letter: str) -> int | None:
        """Obtiene el digito predicho para alguna letra"""

        return self.predictions.get(letter)


    def assign(self, letter: str, digit: int) -> None:
        """Asigna un digit a una letra"""

        self.predictions[letter] = digit


    def unassign(self, letter: str) -> None:
        """Elimina la prediccion de una letra de forma segura"""

        self.predictions.pop(letter, None)


    def usedDigits(self) -> set:
        """Retorna los digitos ya asignados"""

        return set(self.predictions.values())


    def possibleDigits(self, letter: str) -> Iterator[int]:
        """Retorna iterador con digitos disponibles, que pasa de a uno en cada llamada"""

        used: set = self.usedDigits()

        for d in range(10):

            if d in used:
                continue

            if d == 0 and letter in self.non_zero_letters:
                continue

            yield d


    def solve_column(self, col: int, carry: int) -> bool:
        """ Funcion que llama a funcion recursiva (solve_addends) para una columna, pasandole sus addens, y su result """

        # terminamos todas las columnas
        if col < 0:
            return carry == 0

        # obtener letras de esta columna
        add_letters: list = []

        for row in self.addend_rows:

            letter: str = row[col]

            if letter != '':
                add_letters.append(letter)
        
        # obtiene letra resultado de esa columna
        result_letter: str = self.result_row[col]

        # pasamos con 0 index y current_sum, porque acá todavía no se ha sumado nada, porque empezamos desde la primera letra de la col
        return self.solve_addends(
            col=col,
            carry=carry,
            add_letters=add_letters,
            result_letter=result_letter,
            index=0,
            current_sum=0
        )


    def solve_addends(
        self,
        col: int,
        carry: int,
        add_letters: list,
        result_letter: str,
        index: int,
        current_sum: int) -> bool:
        """Función recursiva que verifica si todos los sumandos tienen dígitos asignados y gestiona la lógica de verificación/deducción"""

        # ya todos los sumandos de la columna tienen digits, entonces verificamos congruencia o hacemos deducción
        if index == len(add_letters):

            # calculamos el total con los sumandos y el carry
            total: int = current_sum + carry

            expected_digit: int = total % 10 # el digito que se obtuvo con la suma de los sumandos
            next_carry: int = total // 10 # carry para siguiente col

            result_digit: str = self.get_digit(result_letter)

            # resultado ya asignado
            if result_digit is not None:
                 
                # se compara, si son diferentes, ese digit no es posible
                if result_digit != expected_digit: 
                    return False

                #si sí es correcto, seguimos a siguiente col
                return self.solve_column(col - 1, next_carry)

            # resultado NO asignado -> hacemos deducción
            else:

                if expected_digit in self.usedDigits(): # si digit ya esta asignado, no se puede usar
                    return False

                if (expected_digit == 0 and result_letter in self.non_zero_letters): # verifica que no se asignen 0 a digits que no deberian serlo
                    return False

                self.assign(result_letter, expected_digit) # asignamos a resultado el digit de la suma

                if self.solve_column(col - 1, next_carry): #probamos que si funcione para siguiente columna, si no, deshacemos
                    return True

                self.unassign(result_letter)

                return False
        
        # nos faltan digits, entonces los generamos
        return self.generate_digits(col,
            carry,
            add_letters,
            result_letter,
            index,
            current_sum)


    def generate_digits(
        self,
        col: int,
        carry: int,
        add_letters: list,
        result_letter: str,
        index: int,
        current_sum: int) -> bool:

        """Asignamos digitos a letras no asignadas"""
        # letra actual
        letter: str = add_letters[index]

        digit: int = self.get_digit(letter)

        # ya asignada
        if digit is not None:

            # acumulamos digit en suma, y llamamos otra vez esta funcion para sumar/calcular siguiente digit
            return self.solve_addends(
                col,
                carry,
                add_letters,
                result_letter,
                index + 1,
                current_sum + digit
            ) 

        # no asignada -> probar
        for d in self.possibleDigits(letter):

            self.assign(letter, d)

            # si funciona con ese digit, es decir, se puede calcular sig col, true, si no, desasignamos
            if self.solve_addends(
                col,
                carry,
                add_letters,
                result_letter,
                index + 1,
                current_sum + d
            ):
                return True

            self.unassign(letter)

        return False

def main():

    solver = CryptoSolver()


if __name__ == "__main__":
    main()