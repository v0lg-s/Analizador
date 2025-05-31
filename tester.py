from lexer import lexer
from parser import parser

def run_tests(lexer_func, parser_func):
    ejemplos = [
        {
            "codigo": """
            // Declaración con comentario
            int count = 0; // comentario sobre la linea de código
            """,
            "descripcion": "Declaración con comentario al inicio",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'int', 3), 
                ('IDENTIFIER', 'count', 3),
                ('OPERATOR', '=', 3),
                ('NUMBER', '0', 3),
                ('SEMICOLON', ';', 3),
            ],
            "salida_esperada_ast": [
                ('DECLARATION', 'int', 'count', 0)
            ]
        },
        {
            "codigo": "result = (a + b) * 2;",
            "descripcion": "Expresión con paréntesis y multiplicación",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'result', 1),
                ('OPERATOR', '=', 1),
                ('PAREN', '(', 1),
                ('IDENTIFIER', 'a', 1),
                ('OPERATOR', '+', 1),
                ('IDENTIFIER', 'b', 1),
                ('PAREN', ')', 1),
                ('OPERATOR', '*', 1),
                ('NUMBER', '2', 1),
                ('SEMICOLON', ';', 1)
            ],
            "salida_esperada_ast": [
                ('ASSIGNMENT', 'result', ('*', ('+', 'a', 'b'), 2))
            ]
        },
        {
            "codigo": """
            if (a == b) {
                c = 10;
            }
            """,
            "descripcion": "Condicional simple con igualdad y bloque",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'if', 2), # Línea 2
                ('PAREN', '(', 2),
                ('IDENTIFIER', 'a', 2),
                ('EQUALS', '==', 2),
                ('IDENTIFIER', 'b', 2),
                ('PAREN', ')', 2),
                ('BRACE', '{', 2),
                ('IDENTIFIER', 'c', 3), # Línea 3
                ('OPERATOR', '=', 3),
                ('NUMBER', '10', 3),
                ('SEMICOLON', ';', 3),
                ('BRACE', '}', 4),
            ],
            "salida_esperada_ast": [
                ('IF', ('==', 'a', 'b'), [
                    ('ASSIGNMENT', 'c', 10)
                ])
            ]
        },
        {
            "codigo": """
            float x = 1.5;
            float y = 2.5;
            float z = x / y;
            """,
            "descripcion": "Declaraciones y expresión con división",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'float', 2),
                ('IDENTIFIER', 'x', 2),
                ('OPERATOR', '=', 2),
                ('NUMBER', '1.5', 2),
                ('SEMICOLON', ';', 2),

                ('IDENTIFIER', 'float', 3),
                ('IDENTIFIER', 'y', 3),
                ('OPERATOR', '=', 3),
                ('NUMBER', '2.5', 3),
                ('SEMICOLON', ';', 3),

                ('IDENTIFIER', 'float', 4),
                ('IDENTIFIER', 'z', 4),
                ('OPERATOR', '=', 4),
                ('IDENTIFIER', 'x', 4),
                ('OPERATOR', '/', 4),
                ('IDENTIFIER', 'y', 4),
                ('SEMICOLON', ';', 4)
            ],
            "salida_esperada_ast": [
                ('DECLARATION', 'float', 'x', 1.5),
                ('DECLARATION', 'float', 'y', 2.5),
                ('DECLARATION', 'float', 'z', ('/', 'x', 'y'))
            ]
        },
        {
            "codigo": """
            a = 5;
            b = a - 3;
            c = b * (a + 2);
            """,
            "descripcion": "Asignaciones con diferentes operaciones y paréntesis",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'a', 2),
                ('OPERATOR', '=', 2),
                ('NUMBER', '5', 2),
                ('SEMICOLON', ';', 2),

                ('IDENTIFIER', 'b', 3),
                ('OPERATOR', '=', 3),
                ('IDENTIFIER', 'a', 3),
                ('OPERATOR', '-', 3),
                ('NUMBER', '3', 3),
                ('SEMICOLON', ';', 3),

                ('IDENTIFIER', 'c', 4),
                ('OPERATOR', '=', 4),
                ('IDENTIFIER', 'b', 4),
                ('OPERATOR', '*', 4),
                ('PAREN', '(', 4),
                ('IDENTIFIER', 'a', 4),
                ('OPERATOR', '+', 4),
                ('NUMBER', '2', 4),
                ('PAREN', ')', 4),
                ('SEMICOLON', ';', 4)
            ],
            "salida_esperada_ast": [
                ('ASSIGNMENT', 'a', 5),
                ('ASSIGNMENT', 'b', ('-', 'a', 3)),
                ('ASSIGNMENT', 'c', ('*', 'b', ('+', 'a', 2)))
            ]
        },

        {
            "codigo": "result = a + b * c - 2 / 4;",
            "descripcion": "Expresión compleja con múltiples operaciones y paréntesis",
            "salida_esperada_tokens": [
                ("IDENTIFIER", "result", 1),
                ("OPERATOR", "=", 1),
                ("IDENTIFIER", "a", 1),
                ("OPERATOR", "+", 1),
                ("IDENTIFIER", "b", 1),
                ("OPERATOR", "*", 1),
                ("IDENTIFIER", "c", 1),
                ("OPERATOR", "-", 1),
                ("NUMBER", "2", 1),
                ("OPERATOR", "/", 1),
                ("NUMBER", "4", 1),
                ("SEMICOLON", ";", 1)
            ],
            "salida_esperada_ast": [
                ('ASSIGNMENT', 'result',
                    ('-',
                        ('+',
                            'a',
                            ('*', 'b', 'c')
                        ),
                        ('/', 2, 4)
                    )
                )
            ]
        },

        {
            "codigo": "int x;",
            "descripcion": "Inicialización de una variable sin asignación de valor",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'int', 1),
                ('IDENTIFIER', 'x', 1),
                ('SEMICOLON', ';', 1)
            ],
            "salida_esperada_ast": [
                ('DECLARATION', 'int', 'x')
            ]
        },

        {
            "codigo": """int x = ;
            int y;
            """,
            "descripcion": "Error de valor",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'int', 1),
                ('IDENTIFIER', 'x', 1),
                ('OPERATOR', '=', 1),
                ('SEMICOLON', ';', 1),
                ('IDENTIFIER', 'int', 2),
                ('IDENTIFIER', 'y', 2),
                ('SEMICOLON', ';', 2),
            ],
            "salida_esperada_ast": None  
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

            if ejemplo['salida_esperada_ast'] is None:
                print("Se esperaba un error pero no ocurrió ❌")
            elif ast == ejemplo['salida_esperada_ast']:
                print("AST correcto ✔️")
            else:
                print("AST incorrecto ❌")

        except Exception as e:
            if ejemplo['salida_esperada_ast'] is None:
                print(f"Se esperaba un error y ocurrió correctamente ✔️\nMensaje de error: {e}")
            else:
                print(f"Error inesperado en análisis sintáctico: {e}")
                print("Test fallido ❌")



if __name__ == "__main__":
    run_tests(lexer, parser)
