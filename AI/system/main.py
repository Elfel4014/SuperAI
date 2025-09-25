
import time
import datetime
import os
import sys

# Adicionar o diretório atual (system) ao PYTHONPATH para importações relativas
sys.path.append(os.path.dirname(__file__))

from superai_programming_module.code_generator import CodeGenerator
from superai_web_automation_module.web_navigator import WebNavigator
from superai_os_interactor_module.os_interactor import OSInteractor
from superai_self_learning_module.self_learner import SelfLearner

class SuperAI:
    def __init__(self):
        self.code_generator = CodeGenerator()
        self.web_navigator = WebNavigator()
        self.os_interactor = OSInteractor()
        self.self_learner = SelfLearner(rules_file="rules.json") # rules.json está no mesmo diretório
        self.training_log_file = os.path.join(os.path.dirname(__file__), "training_log.txt")
        self.start_time = None
        self.training_duration_hours = 10

    def _log_training_event(self, event_type, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.training_log_file, "a") as f:
            f.write(f"[{timestamp}] [{event_type}] {message}\n")

    def start_training(self):
        self.start_time = datetime.datetime.now()
        self._log_training_event("INFO", f"Iniciando treinamento da SuperAI em {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self._log_training_event("INFO", f"Duração total do treinamento: {self.training_duration_hours} horas.")

        end_time = self.start_time + datetime.timedelta(hours=self.training_duration_hours)
        self._log_training_event("INFO", f"Treinamento previsto para terminar em {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

        while datetime.datetime.now() < end_time:
            elapsed_time = datetime.datetime.now() - self.start_time
            remaining_time = end_time - datetime.datetime.now()
            self._log_training_event("PROGRESS", f"Tempo decorrido: {elapsed_time}, Tempo restante: {remaining_time}")

            # Simular atividades de treinamento
            self._train_programming_module()
            self._train_web_navigation_module()
            self._train_os_interaction_module()
            self._train_self_learning_module()

            # Verificar a cada 5 minutos
            time.sleep(300) # 300 segundos = 5 minutos
        
        self._log_training_event("INFO", "Treinamento da SuperAI concluído.")

    def _train_programming_module(self):
        # Exemplo de treinamento do módulo de programação
        code_to_test = "def add(a, b): return a + b"
        tests = [((1, 2), 3), ((5, 5), 10), ((-1, 1), 0)]
        result = self.code_generator.execute_and_test_code(code_to_test, tests)
        if not result["all_passed"]:
            self._log_training_event("WARNING", f"Falha no teste de programação: {result['output']}")
            # Aqui poderia haver lógica de auto-correção do código
        else:
            self._log_training_event("DEBUG", "Módulo de programação testado com sucesso.")

    def _train_web_navigation_module(self):
        # Exemplo de treinamento do módulo de navegação web
        try:
            url = "https://www.google.com"
            content = self.web_navigator.fetch_url(url)
            if content:
                self._log_training_event("DEBUG", f"Navegação web para {url} bem-sucedida. Conteúdo parcial: {content[:100]}...")
            else:
                self._log_training_event("WARNING", f"Navegação web para {url} falhou ou retornou conteúdo vazio.")
        except Exception as e:
            self._log_training_event("ERROR", f"Erro na navegação web: {e}")

    def _train_os_interaction_module(self):
        # Exemplo de treinamento do módulo de interação com OS
        try:
            command = ["ls", "-l"]
            success, result_output = self.os_interactor.execute_command(command)
            if success:
                self._log_training_event("DEBUG", f"Comando OS \'{command}\' executado com sucesso. Saída parcial: {result_output[:100]}...")
            else:
                self._log_training_event("WARNING", f"Comando OS \'{command}\' falhou: {result_output}")
        except Exception as e: 
            self._log_training_event("ERROR", f"Erro na interação com OS: {e}")

    def _train_self_learning_module(self):
        # Exemplo de treinamento do módulo de auto-aprendizado
        test_cases = [
            {
                "context": {"value": 10},
                "expected_actions": [("test_rule_1", 'context["status"] = "high"')]
            },
            {
                "context": {"value": 3},
                "expected_actions": []
            }
        ]
        # Adicionar uma regra de exemplo se ainda não existir
        if not self.self_learner.get_rule("test_rule_1"):
            self.self_learner.add_rule("test_rule_1", 'context["value"] > 5', 'context["status"] = "high"')

        results = self.self_learner.evaluate_performance(test_cases)
        if results["failure_rate"] > 0:
            self._log_training_event("WARNING", f"Falha no auto-aprendizado. Taxa de falha: {results['failure_rate']}")
            # Aqui poderia haver lógica para ajustar as regras
        else:
            self._log_training_event("DEBUG", "Módulo de auto-aprendizado testado com sucesso.")

if __name__ == "__main__":
    ai = SuperAI()
    ai.start_training()

