import re

# === DEFINICIÓN DE TOKENS ===
# Cada tupla contiene un nombre de token y su patrón de expresión regular.
# El orden es importante: los patrones más específicos deben ir primero.
token_definitions = [
    ('EQUALS', r'=='),                   # Token para el operador de igualdad '=='
    ('COMMENT', r'//.*'),               # Token para comentarios de una línea que comienzan con //
    ('NUMBER', r'\d+\.\d+|\d+'),        # Token para números: decimales o enteros
    ('IDENTIFIER', r'[a-zA-Z_]\w*'),    # Token para identificadores: letra o guion bajo seguido de letras, dígitos o guion bajo
    ('OPERATOR', r'[+\-*/=]'),          # Token para operadores: suma, resta, multiplicación, división, asignación
    ('PAREN', r'[()]'),                 # Token para paréntesis: ( o )
    ('BRACE', r'[\{\}]'),               # Token para llaves: { o }
    ('SEMICOLON', r';'),                # Token para punto y coma ;
    ('WHITESPACE', r'\s+'),             # Token para espacios en blanco, tabulaciones y saltos de línea
]

def lexer(source_code):
    """
    Analizador léxico que recibe el código fuente como texto y devuelve
    una lista de tokens reconocidos en el código.
    """
    position = 0              # Posición actual dentro del texto fuente
    line_number = 1             # Contador de linea inicia en 1
    found_tokens = []        # Lista donde se almacenarán los tokens válidos

    # Mientras no se haya llegado al final del texto fuente
    while position < len(source_code):
        match = None         # Variable para almacenar la coincidencia actual

        # Iterar sobre cada tipo de token y su expresión regular
        for token_type, pattern in token_definitions:
            regex = re.compile(pattern)          # Compila el patrón regex
            match = regex.match(source_code, position)  # Busca coincidencia desde la posición actual

            if match:                           # Si encontró una coincidencia
                token_value = match.group(0)   # Extrae el texto coincidente

                # aumentar la linea dependiendo del numero de saltos
                if token_type == 'WHITESPACE' and '\n' in token_value:
                    line_number += token_value.count('\n')

                # Ignorar los tokens de espacio en blanco y comentarios
                if token_type not in ('WHITESPACE', 'COMMENT'):
                    # Añade el token (tipo, valor) a la lista de tokens encontrados
                    found_tokens.append((token_type, token_value, line_number))

                # Avanza la posición hasta el final del texto que coincidió
                position = match.end()
                break                           # Ya se encontró un token, se sale del for

        # Si no se encontró ningún token válido en la posición actual, hay un error
        if not match:
            raise SyntaxError(f"Token no reconocido en la posición {position}")

    # Retorna la lista completa de tokens válidos encontrados en el código fuente
    return found_tokens