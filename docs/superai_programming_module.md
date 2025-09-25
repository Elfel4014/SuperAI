# Módulo de Programação Robusta com Auto-Correção

O `superai_programming_module` é o componente do sistema SuperAI responsável pela geração, execução, teste e auto-correção de código Python. Ele permite que a IA crie e refine suas próprias ferramentas e scripts de forma autônoma.

## `CodeGenerator` Class

Esta classe encapsula as funcionalidades de geração, execução e auto-correção de código.

### Métodos:

#### `generate_simple_function(self, function_name, operation, a_name='a', b_name='b')`

-   **Descrição:** Gera uma função Python simples que realiza uma operação matemática básica (adição, subtração, multiplicação, divisão) entre dois argumentos.
-   **Parâmetros:**
    -   `function_name` (str): O nome da função a ser gerada.
    -   `operation` (str): A operação a ser realizada ('add', 'subtract', 'multiply', 'divide').
    -   `a_name` (str, opcional): O nome do primeiro argumento da função (padrão: 'a').
    -   `b_name` (str, opcional): O nome do segundo argumento da função (padrão: 'b').
-   **Retorna:** (str) Uma string contendo o código Python da função gerada.
-   **Exceções:** `ValueError` se a operação não for suportada.

#### `execute_and_test_code(self, code_string, test_cases)`

-   **Descrição:** Executa uma string de código Python e testa a função definida nela com uma lista de casos de teste. É capaz de lidar com resultados esperados e exceções esperadas.
-   **Parâmetros:**
    -   `code_string` (str): A string de código Python a ser executada.
    -   `test_cases` (list): Uma lista de tuplas, onde cada tupla contém `(inputs, expected_output)`. `inputs` é uma tupla de argumentos para a função, e `expected_output` é o resultado esperado ou o tipo de exceção esperado (e.g., `ValueError`, `ZeroDivisionError`).
-   **Retorna:** (dict) Um dicionário contendo:
    -   `"all_passed"` (bool): `True` se todos os testes passaram, `False` caso contrário.
    -   `"output"` (str): Uma string formatada com os resultados de cada teste.

#### `self_correct_code(self, original_code, error_message, function_name, operation, a_name='a', b_name='b')`

-   **Descrição:** Tenta corrigir o código gerado com base em uma mensagem de erro. Atualmente, implementa uma lógica básica para corrigir erros de divisão por zero.
-   **Parâmetros:**
    -   `original_code` (str): O código Python original que falhou.
    -   `error_message` (str): A mensagem de erro recebida durante a execução do código.
    -   `function_name` (str): O nome da função que está sendo corrigida.
    -   `operation` (str): A operação que a função deveria realizar.
    -   `a_name` (str, opcional): O nome do primeiro argumento da função (padrão: 'a').
    -   `b_name` (str, opcional): O nome do segundo argumento da função (padrão: 'b').
-   **Retorna:** (str) O código corrigido se uma correção for aplicada, caso contrário, o `original_code`.

## Uso

Este módulo é utilizado pelo orquestrador principal (`main.py`) para gerar e validar código dinamicamente, permitindo que a SuperAI adapte e crie novas funcionalidades de programação conforme necessário.
