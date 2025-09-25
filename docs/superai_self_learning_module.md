# Módulo de Auto-Aprendizado Seguro

O `superai_self_learning_module` é o coração do sistema SuperAI para auto-aprimoramento. Ele permite que a IA aprenda com suas experiências, adapte suas regras e melhore seu desempenho ao longo do tempo, garantindo que a evolução seja controlada e segura. Este módulo utiliza um sistema baseado em regras para tomar decisões e avaliar seu próprio desempenho.

## `SelfLearner` Class

Esta classe gerencia as regras de aprendizado, aplica-as a contextos específicos e avalia o desempenho do sistema.

### Métodos:

#### `__init__(self, rules_file="rules.json")`

-   **Descrição:** Inicializa o `SelfLearner`, carregando as regras de um arquivo JSON especificado. Se o arquivo não existir, um conjunto de regras vazio é iniciado.
-   **Parâmetros:**
    -   `rules_file` (str, opcional): O nome do arquivo JSON onde as regras são armazenadas (padrão: "rules.json").

#### `_load_rules(self)`

-   **Descrição:** Método interno para carregar as regras do arquivo JSON.
-   **Retorna:** (dict) Um dicionário contendo as regras carregadas.

#### `_save_rules(self)`

-   **Descrição:** Método interno para salvar as regras no arquivo JSON.

#### `add_rule(self, rule_name, condition, action)`

-   **Descrição:** Adiciona ou atualiza uma regra de aprendizado. As regras são definidas por uma condição (uma expressão Python que avalia para `True` ou `False`) e uma ação (uma instrução Python a ser executada).
-   **Parâmetros:**
    -   `rule_name` (str): Um nome único para a regra.
    -   `condition` (str): Uma string contendo uma expressão Python que será avaliada. Esta expressão deve usar o dicionário `context`.
    -   `action` (str): Uma string contendo uma instrução Python que será executada se a condição for verdadeira. Esta instrução também opera no dicionário `context`.
-   **Retorna:** (tuple) Uma tupla `(bool, str)` indicando `(sucesso, mensagem_de_status)`.

#### `get_rule(self, rule_name)`

-   **Descrição:** Retorna os dados de uma regra específica pelo seu nome.
-   **Parâmetros:**
    -   `rule_name` (str): O nome da regra a ser recuperada.
-   **Retorna:** (dict ou `None`) Um dicionário com a condição e a ação da regra, ou `None` se a regra não for encontrada.

#### `apply_rules(self, context)`

-   **Descrição:** Aplica todas as regras carregadas a um determinado contexto. As condições são avaliadas e as ações correspondentes são executadas, modificando o contexto conforme necessário.
-   **Parâmetros:**
    -   `context` (dict): Um dicionário que representa o estado atual ou as informações sobre as quais as regras serão aplicadas.
-   **Retorna:** (list) Uma lista de tuplas `(rule_name, action_string)` para cada ação que foi executada com sucesso. Em caso de erro na execução de uma ação, retorna `(rule_name, error_message)`.

#### `evaluate_performance(self, test_cases)`

-   **Descrição:** Avalia o desempenho do conjunto de regras usando uma lista de casos de teste. Cada caso de teste inclui um contexto inicial e uma lista de ações esperadas.
-   **Parâmetros:**
    -   `test_cases` (list): Uma lista de dicionários, onde cada dicionário contém:
        -   `"context"` (dict): O contexto inicial para o teste.
        -   `"expected_actions"` (list): Uma lista de tuplas `(rule_name, action_string)` que representam as ações que deveriam ser executadas para este contexto.
-   **Retorna:** (dict) Um dicionário contendo:
    -   `"total_tests"` (int): O número total de casos de teste.
    -   `"passed_tests"` (int): O número de testes que passaram (onde as ações executadas corresponderam às esperadas).
    -   `"failure_rate"` (float): A taxa de falha (0.0 se todos os testes passaram).
    -   `"detailed_results"` (list): Uma lista de dicionários com os resultados detalhados de cada teste, incluindo o contexto, ações executadas, ações esperadas e o status (PASSED/FAILED).

## Uso

Este módulo é crucial para a capacidade de auto-aprendizado da SuperAI. Ele permite que a IA adapte seu comportamento e lógica de decisão com base em feedback e experiências, ajustando suas regras para melhorar continuamente seu desempenho em diversas tarefas.
