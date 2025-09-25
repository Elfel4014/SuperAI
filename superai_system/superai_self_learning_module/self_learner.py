
import json
import os

class SelfLearner:
    def __init__(self, rules_file="rules.json"):
        self.rules_file = rules_file
        self.rules = self._load_rules()

    def _load_rules(self):
        if os.path.exists(self.rules_file):
            with open(self.rules_file, "r") as f:
                return json.load(f)
        return {}

    def _save_rules(self):
        with open(self.rules_file, "w") as f:
            json.dump(self.rules, f, indent=4)

    def add_rule(self, rule_name, condition, action):
        """
        Adiciona ou atualiza uma regra de aprendizado.
        :param rule_name: Nome único da regra.
        :param condition: Condição para a regra ser ativada (string Python avaliável).
        :param action: Ação a ser executada quando a condição for verdadeira (string Python avaliável).
        """
        self.rules[rule_name] = {"condition": condition, "action": action}
        self._save_rules()
        return True, f"Regra \'{rule_name}\' adicionada/atualizada com sucesso."

    def get_rule(self, rule_name):
        """
        Retorna uma regra específica.
        :param rule_name: Nome da regra.
        :return: Dicionário com a condição e ação da regra, ou None se não encontrada.
        """
        return self.rules.get(rule_name)

    def apply_rules(self, context):
        """
        Aplica as regras ao contexto fornecido.
        :param context: Dicionário com variáveis e valores para avaliação das condições.
        :return: Lista de tuplas (rule_name, action_string) para ações executadas, ou (rule_name, error_message) para erros.
        """
        executed_actions = []
        scope = {"context": context}

        for rule_name, rule_data in self.rules.items():
            condition = rule_data["condition"]
            action = rule_data["action"]
            try:
                if eval(condition, {}, scope):
                    exec(action, {}, scope)
                    executed_actions.append((rule_name, action))
            except Exception as e:
                executed_actions.append((rule_name, f"ERROR: {e}"))
        
        return executed_actions

    def evaluate_performance(self, test_cases):
        """
        Avalia o desempenho das regras com base em casos de teste.
        :param test_cases: Lista de dicionários, cada um com 'context' e 'expected_actions'.
                           'expected_actions' agora é uma lista de tuplas (rule_name, action_string).
        :return: Dicionário com resultados da avaliação.
        """
        total_tests = len(test_cases)
        passed_tests = 0
        detailed_results = []

        for i, test_case in enumerate(test_cases):
            context = test_case["context"].copy()
            expected_actions = sorted(test_case["expected_actions"])
            
            executed_actions = sorted(self.apply_rules(context))
            
            # A comparação agora é direta entre as listas de tuplas, que devem ser idênticas
            is_correct = (executed_actions == expected_actions)

            if is_correct:
                passed_tests += 1
                status = "PASSED"
            else:
                status = "FAILED"
            
            detailed_results.append({
                "test_id": i + 1,
                "context": test_case["context"],
                "executed_actions": executed_actions,
                "expected_actions": expected_actions,
                "status": status
            })

        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failure_rate": (total_tests - passed_tests) / total_tests if total_tests > 0 else 0,
            "detailed_results": detailed_results
        }

# Exemplo de uso (para testes internos)
if __name__ == "__main__":
    learner = SelfLearner("temp_rules.json")

    # Adicionar regras
    learner.add_rule("saudacao_manha", "context[\"hora\"] < 12", "context[\"saudacao\"] = \"Bom dia\"")
    learner.add_rule("saudacao_tarde", "context[\"hora\"] >= 12 and context[\"hora\"] < 18", "context[\"saudacao\"] = \"Boa tarde\"")
    learner.add_rule("saudacao_noite", "context[\"hora\"] >= 18", "context[\"saudacao\"] = \"Boa noite\"")
    learner.add_rule("acao_importante", "context[\"prioridade\"] == \"alta\"", "context[\"acao\"] = \"Executar tarefa crítica\"")

    # Testar aplicação de regras
    print("\n--- Aplicação de Regras ---")
    context1 = {"hora": 10, "prioridade": "baixa"}
    actions1 = learner.apply_rules(context1)
    print(f"Contexto: {context1}, Ações: {actions1}")
    print(f"Resultado do contexto: {context1}")

    context2 = {"hora": 15, "prioridade": "alta"}
    actions2 = learner.apply_rules(context2)
    print(f"Contexto: {context2}, Ações: {actions2}")
    print(f"Resultado do contexto: {context2}")

    # Avaliar desempenho
    print("\n--- Avaliação de Desempenho ---")
    test_cases = [
        {
            "context": {"hora": 9, "prioridade": "normal"},
            "expected_actions": [("saudacao_manha", "context[\"saudacao\"] = \"Bom dia\"")]
        },
        {
            "context": {"hora": 14, "prioridade": "alta"},
            "expected_actions": [
                ("acao_importante", "context[\"acao\"] = \"Executar tarefa crítica\""),
                ("saudacao_tarde", "context[\"saudacao\"] = \"Boa tarde\"")
            ]
        },
        {
            "context": {"hora": 20, "prioridade": "baixa"},
            "expected_actions": [("saudacao_noite", "context[\"saudacao\"] = \"Boa noite\"")]
        },
        {
            "context": {"hora": 10, "prioridade": "alta"},
            "expected_actions": [
                ("acao_importante", "context[\"acao\"] = \"Executar tarefa crítica\""),
                ("saudacao_manha", "context[\"saudacao\"] = \"Bom dia\"")
            ]
        }
    ]
    
    evaluation_results = learner.evaluate_performance(test_cases)
    print(f"Resultados da Avaliação: {evaluation_results}")

    # Limpar arquivo de regras temporário
    os.remove("temp_rules.json")

