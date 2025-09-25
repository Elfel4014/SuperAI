
import ast
import inspect

def generate_simple_function(function_name, operation, a_name='a', b_name='b'):
    """
    Gera uma função Python simples que realiza uma operação entre dois argumentos.
    """
    if operation == 'add':
        body = f"    return {a_name} + {b_name}"
    elif operation == 'subtract':
        body = f"    return {a_name} - {b_name}"
    elif operation == 'multiply':
        body = f"    return {a_name} * {b_name}"
    elif operation == 'divide':
        body = f"    return {a_name} / {b_name}"
    else:
        raise ValueError("Operação não suportada")

    function_code = f"""def {function_name}({a_name}, {b_name}):
{body}"""
    return function_code

def execute_and_test_code(code_string, test_cases):
    """
    Executa o código gerado e testa com os casos fornecidos.
    Retorna True se todos os testes passarem, False caso contrário, e a saída dos testes.
    """
    local_vars = {}
    all_passed = True
    results = []

    try:
        exec(code_string, globals(), local_vars)
        # Encontra a primeira função definida no código
        func = None
        for name, obj in local_vars.items():
            if inspect.isfunction(obj):
                func = obj
                break
        if func is None:
            return False, "Erro: Nenhuma função encontrada no código fornecido."

        for inputs, expected_output in test_cases:
            try:
                actual_output = func(*inputs)
                if isinstance(expected_output, type) and issubclass(expected_output, Exception):
                    results.append(f"Test with inputs {inputs}: Expected exception {expected_output.__name__}, Got result {actual_output} - FAILED")
                    all_passed = False
                else:
                    passed = (actual_output == expected_output)
                    status = "PASSED" if passed else "FAILED"
                    results.append(f"Test with inputs {inputs}: Expected {expected_output}, Got {actual_output} - {status}")
                    if not passed:
                        all_passed = False
            except Exception as e:
                if isinstance(expected_output, type) and issubclass(expected_output, Exception) and isinstance(e, expected_output):
                    results.append(f"Test with inputs {inputs}: Expected exception {expected_output.__name__}, Got exception {type(e).__name__} - PASSED")
                else:
                    results.append(f"Test with inputs {inputs}: Raised unexpected exception {type(e).__name__}: {e} - FAILED")
                    all_passed = False
        return all_passed, "\n".join(results)
    except Exception as e:
        return False, f"Erro de execução do código: {e}"

def self_correct_code(original_code, error_message, function_name, operation, a_name='a', b_name='b'):
    """
    Tenta corrigir o código gerado com base na mensagem de erro.
    """
    if "division by zero" in error_message and operation == 'divide':
        # Tenta adicionar a verificação de divisão por zero se não estiver presente
        if f"if {b_name} == 0:" not in original_code:
            corrected_body = f"    if {b_name} == 0: raise ValueError('Cannot divide by zero')\n    return {a_name} / {b_name}"
            corrected_code = f"""def {function_name}({a_name}, {b_name}):
{corrected_body}"""
            return corrected_code
    return original_code

