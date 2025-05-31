# === ANALIZADOR SINTÁCTICO (Parser) ===


# Definición de la precedencia de operadores.
# Los operadores con menor número tienen menor precedencia (se evalúan al final).
# Los operadores con mayor número tienen mayor precedencia (se evalúan primero).
precedence = {
    '==': 0,
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2
}

def parser(tokens):
    """
    Función principal del parser.
    Recibe una lista de tokens (tuplas de tipo y valor) y devuelve el árbol de sintaxis abstracta (AST).
    """
    tokens = tokens.copy()  # Copia para no modificar la lista original
    ast = []  # AST: lista de sentencias analizadas

    # Mientras haya tokens por analizar, procesa una sentencia
    while tokens:
        ast.append(parse_statement(tokens))  # Agrega el resultado del análisis al AST
    return ast


def parse_statement(tokens):
    """
    Determina si una sentencia es una declaración o una asignación.
    """
    # Declaración si el primer token es un tipo válido (int o float)
    if tokens[0][0] == 'IDENTIFIER' and tokens[0][1] in ('int', 'float'):
        return parse_declaration(tokens)
    
    # If
    if tokens[0][0] == 'IDENTIFIER' and tokens[0][1] == 'if':
        return parse_if_statement(tokens)

    # Asignación si el primer token es un identificador de variable
    if tokens[0][0] == 'IDENTIFIER':
        return parse_assignment(tokens)
    
    # Si no es ninguna de las anteriores, lanza error de sintaxis
    line = tokens[0][2]
    raise SyntaxError(f"Linea {line}: Sentencia inválida. Token inesperado: {tokens[0]}")


def parse_declaration(tokens):
    """
    Analiza una declaración de variable.
    Forma esperada: tipo ID '=' expresión ';'
    """
    tipo = parse_type(tokens)            # Tipo: int o float
    identificador = parse_id(tokens)     # Nombre de la variable

    # Si el siguiente token es '=', parsear una expresión
    if tokens and tokens[0][0] == 'OPERATOR' and tokens[0][1] == '=':
        parse_equals(tokens)
        expr = parse_expression(tokens)
        parse_semi(tokens)
        return ('DECLARATION', tipo, identificador, expr)

    # Si no hay '=', debe venir un ';'
    parse_semi(tokens)
    return ('DECLARATION', tipo, identificador)



def parse_assignment(tokens):
    """
    Analiza una asignación de variable.
    Forma esperada: ID '=' expresión ';'
    """
    identificador = parse_id(tokens)     # Nombre de la variable
    parse_equals(tokens)                 # Verifica que siga un '='
    expr = parse_expression(tokens)      # Expresión a asignar
    parse_semi(tokens)                   # Verifica que termine con ';'
    return ('ASSIGNMENT', identificador, expr)  # Nodo del AST


def parse_type(tokens):
    """
    Extrae y verifica el tipo de dato ('int' o 'float').
    """
    if not tokens:
        raise SyntaxError("Se esperaba un tipo, pero no hay más tokens.")
    tk_type, tk_val, line = tokens.pop(0)
    if tk_type == 'IDENTIFIER' and tk_val in ('int', 'float'):
        return tk_val
    raise SyntaxError(f"Línea {line}: Tipo inválido: {tk_val}")


def parse_id(tokens):
    """
    Extrae y verifica un identificador (nombre de variable).
    """
    if not tokens:
        raise SyntaxError("Se esperaba un identificador, pero no hay más tokens.")
    tk_type, tk_val, line = tokens.pop(0)
    if tk_type == 'IDENTIFIER':
        return tk_val
    raise SyntaxError(f"Línea {line}: Identificador inválido: {tk_val}")


def parse_num(tokens):
    """
    Extrae y convierte un número (int o float).
    """
    if not tokens:
        raise SyntaxError("Se esperaba un número, pero no hay más tokens.")
    tk_type, tk_val, line = tokens.pop(0)
    if tk_type == 'NUMBER':
        return float(tk_val) if '.' in tk_val else int(tk_val)  # Convierte a float si tiene punto decimal
    raise SyntaxError(f"Línea {line}: Número inválido: {tk_val}")


def parse_equals(tokens):
    """
    Verifica que el siguiente token sea el operador de asignación '='.
    """
    if not tokens:
        raise SyntaxError("Se esperaba '=' pero no hay más tokens.")
    tk_type, tk_val, line = tokens.pop(0)
    if not (tk_type == 'OPERATOR' and tk_val == '='):
        raise SyntaxError(f"Línea {line}: Se esperaba '=' pero se encontró {tk_val}")


def parse_semi(tokens):
    """
    Verifica que el siguiente token sea un punto y coma ';'.
    """
    if not tokens:
        raise SyntaxError("Se esperaba ';' pero no hay más tokens.")
    tk_type, tk_val, line = tokens.pop(0)
    if tk_type != 'SEMICOLON':
        raise SyntaxError(f"Línea {line}: Se esperaba ';' pero se encontró {tk_val}")


def parse_expression(tokens, min_prec=0):
    """
    Analiza una expresión aritmética con paréntesis y precedencia.
    Utiliza recursividad para respetar la prioridad de los operadores.
    """
    if not tokens:
        raise SyntaxError("Expresión vacía.")

    # Parsea el primer operando: número, identificador o expresión entre paréntesis
    if tokens[0][0] == 'NUMBER':
        node = parse_num(tokens)
    elif tokens[0][0] == 'IDENTIFIER':
        node = parse_id(tokens)
    elif tokens[0][0] == 'PAREN' and tokens[0][1] == '(':
        tokens.pop(0)  # Consumir '('
        node = parse_expression(tokens)
        if not tokens or tokens[0][0] != 'PAREN' or tokens[0][1] != ')':
            raise SyntaxError(f"Linea {tokens[0][2]}: Se esperaba ')' en la expresión.")
        tokens.pop(0)  # Consumir ')'
    else:
        raise SyntaxError(f"Linea {tokens[0][2]}: Expresión inválida. Se encontró {tokens[0][1]}")

    # Parsea operadores y operandos posteriores según la precedencia
    while tokens and (tokens[0][0] in ('OPERATOR', 'EQUALS')):
        op = tokens[0][1]
        op_prec = precedence.get(op, -1)
        if op_prec < min_prec:
            break

        tokens.pop(0)  # Consumir operador
        rhs = parse_expression(tokens, op_prec + 1)  # Operando derecho

        # Crea un nodo de expresión binaria: (operador, izquierdo, derecho)
        node = (op, node, rhs)

    return node  # Retorna el nodo final de la expresión


def parse_if_statement(tokens):
    """
    Analiza una estructura condicional if.
    Forma esperada: if (condición) { sentencias }
    """
    tk_type, tk_val, line = tokens.pop(0)
    if tk_type != 'IDENTIFIER' or tk_val != 'if':
        raise SyntaxError(f"Línea {line}: Se esperaba 'if' pero se encontró {tk_val}")

    if not tokens or tokens[0][0] != 'PAREN' or tokens[0][1] != '(':
        raise SyntaxError(f"Línea {line}: Se esperaba '(' después de 'if'")
    tokens.pop(0)  # Consumir '('

    condition = parse_expression(tokens)

    if not tokens or tokens[0][0] != 'PAREN' or tokens[0][1] != ')':
        raise SyntaxError(f"Línea {line}: Se esperaba ')' después de la condición")
    tokens.pop(0)  # Consumir ')'

    if not tokens or tokens[0][0] != 'BRACE' or tokens[0][1] != '{':
        raise SyntaxError("Línea",{line},": Se esperaba '{' después de ')'")
    tokens.pop(0)  # Consumir '{'

    body = []
    while tokens and not (tokens[0][0] == 'BRACE' and tokens[0][1] == '}'):
        body.append(parse_statement(tokens))

    if not tokens or tokens[0][0] != 'BRACE' or tokens[0][1] != '}':
        raise SyntaxError("Línea",{line},": Se esperaba '}' para cerrar el bloque if")
    tokens.pop(0)  # Consumir '}'

    return ('IF', condition, body)
