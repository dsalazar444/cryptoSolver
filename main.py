import numpy as np
import pandas as pd
import logging

class cryptoSolver:
    matrix: np.ndarray
    codeToDecode: list[int]
    letters: list[str]
    letters_cannot_be_zero: list
    result_in_matrix: list[int]
    letters_appears_columns: dict
    predictions: dict[list] # no pongo tipo porque tendrá el primero como int, resto como diccionarios
    hasSolution: bool
    messageDecoded: list[str]

    def __init__(self):
        # Configurar logging
        logging.basicConfig(
            filename='crypto_solver.log',
            level=logging.INFO,
            format='%(message)s',
            filemode='w'
        )
        self.logger = logging.getLogger(__name__)
        
        matrix =  [
            ['h', 'a' ,'r', 'r', 'y'],
            ['p', 'o', 't', 't', 'e', 'r'],
            ['t', 'r', 'o', 'l', 'l', 's'],
        ]
        self.matrix = self.normalizeMatrix(matrix)
        self.codeToDecode = [9,0,3,9,0,0,4,3,9,6,5,1,8,4,8]
        self.logger.info(str(self.matrix))
        self.letters = self.getLetters()
        self.letters_cannot_be_zero = self.getLettersCannotBeZero()
        self.logger.info(str(self.letters))
        self.result_in_matrix = self.matrix[-1]
        self.letters_appears_columns = self.getLettersAppearsColumns()
        self.predictions = {}
        self.hasSolution = self.solveLetters()
        self.messageDecoded = self.decodeMessage() 
    
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

        self.logger.info(f"\nColumnas en orden de importancia: {letters}")

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

        self.logger.info(f"Total de elementos repetidos por columna: {number_repeats_per_column}")

    def getLettersCannotBeZero(self):
        letters: list = []
        #1. Crear una máscara booleana (True donde NO es '')
        mask = (self.matrix!= '')

        # 2. Obtener los PRIMEROS elementos válidos de cada fila
        # argmax devuelve el índice del primer True en cada fila (axis=1)
        first_indexes: list = mask.argmax(axis=1)
        letters.extend(self.matrix[np.arange(self.matrix.shape[0]), first_indexes])

        # 3. Obtener los ÚLTIMOS elementos válidos de cada fila
        # Volteamos la máscara de derecha a izquierda con ::-1 para hallar el "primer" True desde el final
        last_indexes: list = self.matrix.shape[1] - 1 - mask[:, ::-1].argmax(axis=1)
        letters.extend(self.matrix[np.arange(self.matrix.shape[0]), last_indexes])

        self.logger.info(f"elementos que no pueden ser 0: {letters}")
        return letters

        
    def solveLetters(self, index: int = 0, digits_available: list = None) -> bool:
        if digits_available is None:
            digits_available = list(range(10))
        
        # caso base
        if index == len(self.letters):
            result = self.verifyCongruenceWithCarry()
            self.logger.info(f"[solveLetters] Verificación final, hasSolution: {result}")
            return result
        
        letter: str = self.letters[index]
        self.logger.info(f"\n[solveLetters] Intentando letra '{letter}'  con dígitos disponibles: {digits_available}")
        
        for digit in digits_available:
            if digit == 0 and letter in self.letters_cannot_be_zero:
                continue
            # probamos con todos los digitos disponibles en este nivel, si ninguno da, nos devolvemos.
            result = self.verifyCongruence(letter, digit)
            if result is None:
                break
            elif result:
                self.logger.info(f"  [solveLetters] ✓ '{letter}' = {digit} es válido, agregando...")
                self.predictions[letter] = digit
                # "actualizamos" digit_avaible (en otra var) para ignorar el digit que falló
                remaining: list = [d for d in digits_available if d != digit]

                #intentamos con sig letra
                if self.solveLetters(index + 1, remaining):
                    return True
                
                # eliminamos predicción para intentar con otra porque en siguiente letra ninguna funcionó, entonces hay que hacer backtracking
                self.logger.info(f"  [solveLetters] ✗ Backtracking: removiendo '{letter}' = {digit}")
                self.predictions.pop(letter)
            else:
                self.logger.info(f"  [solveLetters] ✗ '{letter}' = {digit} no es válido")
        
        self.logger.info(f"[solveLetters] No hay solución para letra '{letter}', retornando False")
        return False

    def verifyCongruence(self, letter: str, possible_value: int) -> bool | None:
        # obtener indices de columnas donde sale esa letra
        
        self.logger.info(f"    [verifyCongruence] Verificando '{letter}' = {possible_value} en columnas: {self.letters_appears_columns[letter]}")
        for index_col in self.letters_appears_columns[letter]:
            addens: list = [x for x in self.matrix[:-1, index_col].tolist() if x != '']
            result_letter: str = self.result_in_matrix[index_col]

            values: list = [self.getDigit(adden, letter, possible_value) for adden in addens] + [self.getDigit(result_letter, letter, possible_value)]
            self.logger.info(f"      [verifyCongruence] Columna {index_col}: sumandos={addens}, resultado={result_letter}, valores={values}")

            if(None in values): # si alguno de los valores es none, no se puede hacer suma (incluso el result)
                self.logger.info(f"      [verifyCongruence] hay none en values, continue next column")
                continue
                #return True # se puede añadir, porque todavia no hay forma de saber
            
            total: int = sum(values[:-1])
            self.logger.info(f"      [verifyCongruence] Sum={total}, esperado={values[-1]}")
            
            if (values[-1] > total):
                self.logger.info(f"      [verifyCongruence] No tiene sentido seguir, result es mayor a total sumandos")
                return None
            if total % 10 != values[-1]:
                self.logger.info(f"      [verifyCongruence] No Coincide! Retornando False")
                return False
            
        self.logger.info(f"    [verifyCongruence] todo ok, return True")
        return True
    
    def verifyCongruenceWithCarry(self) -> bool:
        self.logger.info(f"\n[verifyCongruenceWithCarry] Verificando solución final: {self.predictions}")
        carry: int = 0
        # recorremos de derecha a izq
        for index in range(len(self.matrix[0])):
            index_inv = len(self.matrix[0]) - 1 - index

            #obtenemos sumandos y resultado
            addens: list = [x for x in self.matrix[:-1, index_inv].tolist() if x != '']
            result_letter: str = self.result_in_matrix[index_inv]

            #obtenemos int asociados a cada elemento
            values: list = [self.predictions[adden] for adden in addens]
            result_value = self.predictions[result_letter]

            # sumamos teniendo en cuenta carry
            total: int = sum(values) + carry
            self.logger.info(f"  Columna {index_inv}: sumandos={addens}→{values}, resultado={result_letter}→{result_value}, total={total}, carry_in={carry}, total%10={total%10}")

            if total % 10 != result_value:
                self.logger.info(f"    ✗ ERROR: {total} % 10 = {total % 10} ≠ {result_value}")
                return False    
        
            carry = total // 10
        
        # si llega acá, nada falló, entonces está bien, todo coincide
        final_result = carry == 0
        self.logger.info(f"[verifyCongruenceWithCarry] Solución final válida: {final_result} (carry final: {carry})")
        return final_result



    def getDigit(self, letter: str, new_letter: str = None, possible_value: int = None) -> int:
        # letter es cualquier letra que nos salga en adden
        # new letter es para verificar si es la letra que estamos verificando para añadir a 
        # predictions, y como todavia no esta ahi, tenemos que retornar el valor manualmente 
        if letter == new_letter and possible_value is not None:
            self.logger.info(f"[getDigit] letter: {letter}, new_letter: {new_letter}), possible_value: {possible_value}")

            return possible_value
        result = self.predictions.get(letter)
        self.logger.info(f"[getDigit] letter: {letter}, guardado en predicted: {result}")

        return result

    
    def getLettersAppearsColumns(self) -> dict:
        self.logger.info(f"[getLettersAppearsColumns] Calculando columnas para cada letra...")
        letter_appearences_in_columns: dict = dict.fromkeys(self.letters)
        for letter in self.letters:
            rows, cols = np.where(self.matrix == letter)
            col_indexes = list(map(int, set(cols)))
            self.logger.info(f"  '{letter}' aparece en columnas: {col_indexes}")
            letter_appearences_in_columns[letter] = col_indexes
        return letter_appearences_in_columns

    def decodeMessage(self) -> list:
        self.logger.info(f"\n[decodeMessage] Decodificando mensaje...")
        if(not self.hasSolution):
            self.logger.info(f"  No hay solución, retornando lista vacía")
            print("NO hay solución")
            return []
        
        self.logger.info(f"  Predicciones: {self.predictions}")
        self.logger.info(f"  Código a decodificar: {self.codeToDecode}")
        message: list = []
        for digit in self.codeToDecode:
            letter: int = next((key for key, value in self.predictions.items() if value == digit), None)
            self.logger.info(f"  Dígito {digit} → letra '{letter}'")
            message.append(letter)
        self.logger.info(f"  Mensaje decodificado: {message}")
        print(f"Mensaje decodificado: {message}")
        return message


def main():
    crypto_solver = cryptoSolver()

if __name__ == "__main__":
    main()