
import pytest
from code_generator import generate_simple_function, execute_and_test_code, self_correct_code

def test_generate_simple_function():
    # Teste de adição
    add_func = generate_simple_function("add_numbers", "add")
    expected_add_code = """def add_numbers(a, b):
    return a + b"""
    assert add_func == expected_add_code

    # Teste de subtração
    sub_func = generate_simple_function("subtract_numbers", "subtract")
    expected_sub_code = """def subtract_numbers(a, b):
    return a - b"""
    assert sub_func == expected_sub_code

    # Teste de multiplicação
    mul_func = generate_simple_function("multiply_numbers", "multiply")
    expected_mul_code = """def multiply_numbers(a, b):
    return a * b"""
    assert mul_func == expected_mul_code

    # Teste de divisão (sem tratamento de erro inicial)
    div_func = generate_simple_function("divide_numbers", "divide")
    expected_div_code = """def divide_numbers(a, b):
    return a / b"""
    assert div_func == expected_div_code

    # Teste de operação não suportada
    with pytest.raises(ValueError, match="Operação não suportada"):
        generate_simple_function("invalid_op", "power")

def test_execute_and_test_code():
    # Teste de função de adição bem-sucedida
    add_code = generate_simple_function("add_func", "add")
    add_test_cases = [
        ((1, 2), 3),
        ((5, 5), 10),
        ((-1, 1), 0)
    ]
    passed, results = execute_and_test_code(add_code, add_test_cases)
    assert passed is True
    assert "PASSED" in results

    # Teste de função de divisão com erro (divisão por zero)
    div_code = generate_simple_function("div_func", "divide")
    div_test_cases = [
        ((10, 2), 5),
        ((5, 0), ZeroDivisionError) # Espera uma exceção
    ]
    passed, results = execute_and_test_code(div_code, div_test_cases)
    assert passed is True # Deve passar porque a exceção esperada foi capturada
    assert "Expected exception ZeroDivisionError, Got exception ZeroDivisionError - PASSED" in results

    # Teste de função com resultado incorreto
    incorrect_add_code = """def incorrect_add(a, b):
    return a + b + 1"""
    incorrect_add_test_cases = [
        ((1, 2), 3) # Espera 3, mas a função retornará 4
    ]
    passed, results = execute_and_test_code(incorrect_add_code, incorrect_add_test_cases)
    assert passed is False
    assert "FAILED" in results

def test_self_correct_code():
    # Teste de auto-correção para divisão por zero
    original_div_code = generate_simple_function("div_func", "divide")
    error_message = "division by zero"
    corrected_code = self_correct_code(original_div_code, error_message, "div_func", "divide")

    expected_corrected_code = """def div_func(a, b):
    if b == 0: raise ValueError(\'Cannot divide by zero\')
    return a / b"""
    assert corrected_code == expected_corrected_code

    # Testar que a correção não ocorre se a verificação já existe
    already_corrected_code = """def div_func(a, b):
    if b == 0: raise ValueError(\'Cannot divide by zero\')
    return a / b"""
    no_change_code = self_correct_code(already_corrected_code, error_message, "div_func", "divide")
    assert no_change_code == already_corrected_code

    # Testar que a correção não ocorre para outras operações
    add_code = generate_simple_function("add_func", "add")
    no_change_add_code = self_correct_code(add_code, error_message, "add_func", "add")
    assert no_change_add_code == add_code

    # Testar a função corrigida com execute_and_test_code
    div_test_cases = [
        ((10, 2), 5),
        ((5, 0), ValueError), # Agora espera ValueError
    ]
    passed, results = execute_and_test_code(corrected_code, div_test_cases)
    assert passed is True
    assert "PASSED" in results
    assert "Expected exception ValueError, Got exception ValueError - PASSED" in results

