
import pytest
import os
import json
from unittest.mock import patch, mock_open
from superai_self_learning_module.self_learner import SelfLearner

@pytest.fixture
def temp_rules_file(tmp_path):
    file = tmp_path / "test_rules.json"
    yield str(file)
    if os.path.exists(file):
        os.remove(file)

def test_init_and_load_rules(temp_rules_file):
    # Teste de inicialização com arquivo inexistente
    learner = SelfLearner(temp_rules_file)
    assert learner.rules == {}

    # Teste de inicialização com arquivo existente
    initial_rules = {"rule1": {"condition": "True", "action": "pass"}}
    with open(temp_rules_file, "w") as f:
        json.dump(initial_rules, f)
    
    learner = SelfLearner(temp_rules_file)
    assert learner.rules == initial_rules

def test_add_rule(temp_rules_file):
    learner = SelfLearner(temp_rules_file)
    success, message = learner.add_rule("test_rule", "1 == 1", "print(\'Hello\')")
    assert success is True
    assert "adicionada/atualizada com sucesso" in message
    assert learner.rules["test_rule"] == {"condition": "1 == 1", "action": "print(\'Hello\')"}
    
    # Verificar se a regra foi salva no arquivo
    with open(temp_rules_file, "r") as f:
        saved_rules = json.load(f)
    assert saved_rules["test_rule"] == {"condition": "1 == 1", "action": "print(\'Hello\')"}

def test_get_rule(temp_rules_file):
    learner = SelfLearner(temp_rules_file)
    learner.add_rule("get_rule_test", "True", "pass")
    rule = learner.get_rule("get_rule_test")
    assert rule == {"condition": "True", "action": "pass"}
    assert learner.get_rule("non_existent_rule") is None

def test_apply_rules_success(temp_rules_file):
    learner = SelfLearner(temp_rules_file)
    learner.add_rule("rule_true", "True", 'context["output"] = "Rule True Applied"')
    learner.add_rule("rule_false", "False", 'context["output"] = "Rule False Applied"')
    
    context = {"output": "initial"}
    executed_actions = learner.apply_rules(context)
    
    assert sorted(executed_actions) == sorted([("rule_true", 'context["output"] = "Rule True Applied"')])
    assert "Rule False Applied" not in context["output"]
    assert context["output"] == "Rule True Applied"

def test_apply_rules_error(temp_rules_file):
    learner = SelfLearner(temp_rules_file)
    learner.add_rule("error_rule", "1 / 0", "pass") # Condição que causa erro
    
    context = {}
    executed_actions = learner.apply_rules(context)
    
    assert ("error_rule", "ERROR: division by zero") in executed_actions

def test_evaluate_performance_all_passed(temp_rules_file):
    learner = SelfLearner(temp_rules_file)
    learner.add_rule("test_rule_1", 'context["value"] > 5', 'context["status"] = "high"')
    learner.add_rule("test_rule_2", 'context["value"] <= 5', 'context["status"] = "low"')

    test_cases = [
        {
            "context": {"value": 10},
            "expected_actions": [("test_rule_1", 'context["status"] = "high"')]
        },
        {
            "context": {"value": 3},
            "expected_actions": [("test_rule_2", 'context["status"] = "low"')]
        }
    ]

    results = learner.evaluate_performance(test_cases)
    assert results["total_tests"] == 2
    assert results["passed_tests"] == 2
    assert results["failure_rate"] == 0.0
    assert results["detailed_results"][0]["status"] == "PASSED"
    assert results["detailed_results"][1]["status"] == "PASSED"

def test_evaluate_performance_some_failed(temp_rules_file):
    learner = SelfLearner(temp_rules_file)
    learner.add_rule("test_rule_1", 'context["value"] > 5', 'context["status"] = "high"')

    test_cases = [
        {
            "context": {"value": 10},
            "expected_actions": [("test_rule_1", 'context["status"] = "high"')]
        },
        {
            "context": {"value": 3},
            "expected_actions": [("test_rule_1", 'context["status"] = "high"')] # Este caso deve falhar, pois a regra não se aplica
        }
    ]

    results = learner.evaluate_performance(test_cases)
    assert results["total_tests"] == 2
    assert results["passed_tests"] == 1 # Apenas o primeiro caso de teste deve passar
    assert results["failure_rate"] == 0.5
    assert results["detailed_results"][0]["status"] == "PASSED"
    assert results["detailed_results"][1]["status"] == "FAILED"

def test_evaluate_performance_no_rules(temp_rules_file):
    learner = SelfLearner(temp_rules_file)
    test_cases = [
        {
            "context": {"value": 10},
            "expected_actions": []
        }
    ]
    results = learner.evaluate_performance(test_cases)
    assert results["total_tests"] == 1
    assert results["passed_tests"] == 1
    assert results["failure_rate"] == 0.0
    assert results["detailed_results"][0]["status"] == "PASSED"

