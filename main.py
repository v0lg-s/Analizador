from lexer import lexer
from parser import parser

def run_tests(lexer_func, parser_func):
    ejemplos = [
        {
            "codigo": "int a = 10;",
            "descripcion": "Declaración simple de int",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'int'),
                ('IDENTIFIER', 'a'),
                ('OPERATOR', '='),
                ('NUMBER', '10'),
                ('SEMICOLON', ';')
            ],
            "salida_esperada_ast": [
                ('DECLARATION', 'int', 'a', 10)
            ]
        },
        {
            "codigo": "int b = a + 5;",
            "descripcion": "Declaración con expresión suma",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'int'),
                ('IDENTIFIER', 'b'),
                ('OPERATOR', '='),
                ('IDENTIFIER', 'a'),
                ('OPERATOR', '+'),
                ('NUMBER', '5'),
                ('SEMICOLON', ';')
            ],
            "salida_esperada_ast": [
                ('DECLARATION', 'int', 'b', ('+', 'a', 5))
            ]
        },
        {
            "codigo": "c = a + 1;",
            "descripcion": "Asignación simple con expresión",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'c'),
                ('OPERATOR', '='),
                ('IDENTIFIER', 'a'),
                ('OPERATOR', '+'),
                ('NUMBER', '1'),
                ('SEMICOLON', ';')
            ],
            "salida_esperada_ast": [
                ('ASSIGNMENT', 'c', ('+', 'a', 1))
            ]
        },
        {
            "codigo": "float x = 3.14;",
            "descripcion": "Declaración tipo float",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'float'),
                ('IDENTIFIER', 'x'),
                ('OPERATOR', '='),
                ('NUMBER', '3.14'),
                ('SEMICOLON', ';')
            ],
            "salida_esperada_ast": [
                ('DECLARATION', 'float', 'x', 3.14)
            ]
        },
        {
            "codigo": "x = x * 2;",
            "descripcion": "Asignación con multiplicación",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'x'),
                ('OPERATOR', '='),
                ('IDENTIFIER', 'x'),
                ('OPERATOR', '*'),
                ('NUMBER', '2'),
                ('SEMICOLON', ';')
            ],
            "salida_esperada_ast": [
                ('ASSIGNMENT', 'x', ('*', 'x', 2))
            ]
        }
    ]

    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"\n=== Test {i}: {ejemplo['descripcion']} ===")
        print("Código fuente:")
        print(ejemplo['codigo'])
        
        # Análisis Léxico
        try:
            tokens = lexer_func(ejemplo['codigo'])
            print("Tokens obtenidos:")
            print(tokens)
            print("Tokens esperados:")
            print(ejemplo['salida_esperada_tokens'])
        except Exception as e:
            print(f"Error en análisis léxico: {e}")
            continue
        
        # Comprobar tokens (simple comparación)
        if tokens == ejemplo['salida_esperada_tokens']:
            print("Tokens correctos ✔️")
        else:
            print("Tokens incorrectos ❌")
        
        # Análisis Sintáctico
        try:
            ast = parser_func(tokens)
            print("AST obtenido:")
            print(ast)
            print("AST esperado:")
            print(ejemplo['salida_esperada_ast'])
        except Exception as e:
            print(f"Error en análisis sintáctico: {e}")
            continue
        
        # Comprobar AST (simple comparación)
        if ast == ejemplo['salida_esperada_ast']:
            print("AST correcto ✔️")
        else:
            print("AST incorrecto ❌")


if __name__ == "__main__":
    run_tests(lexer, parser)
