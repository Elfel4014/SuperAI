
import pytest
import os
from superai_os_interactor_module.os_interactor import OSInteractor

@pytest.fixture
def os_interactor_instance():
    return OSInteractor()

@pytest.fixture
def temp_file(tmp_path):
    file = tmp_path / "test_file.txt"
    yield str(file)
    if os.path.exists(file):
        os.remove(file)

@pytest.fixture
def temp_dir(tmp_path):
    directory = tmp_path / "test_dir"
    yield str(directory)
    if os.path.exists(directory):
        os.rmdir(directory)

def test_create_and_read_file(os_interactor_instance, temp_file):
    content = "Hello, Test File!"
    success, message = os_interactor_instance.create_file(temp_file, content)
    assert success is True
    assert f"Arquivo {temp_file} criado com sucesso." in message

    success, read_content = os_interactor_instance.read_file(temp_file)
    assert success is True
    assert read_content == content

def test_read_non_existent_file(os_interactor_instance):
    success, message = os_interactor_instance.read_file("non_existent_file.txt")
    assert success is False
    assert "Erro ao ler arquivo" in message

def test_delete_file(os_interactor_instance, temp_file):
    os_interactor_instance.create_file(temp_file, "Content to delete")
    assert os.path.exists(temp_file)

    success, message = os_interactor_instance.delete_file(temp_file)
    assert success is True
    assert f"Arquivo {temp_file} deletado com sucesso." in message
    assert not os.path.exists(temp_file)

def test_create_and_delete_directory(os_interactor_instance, temp_dir):
    success, message = os_interactor_instance.create_directory(temp_dir)
    assert success is True
    assert f"Diretório {temp_dir} criado com sucesso." in message
    assert os.path.exists(temp_dir)

    success, message = os_interactor_instance.delete_directory(temp_dir)
    assert success is True
    assert f"Diretório {temp_dir} deletado com sucesso." in message
    assert not os.path.exists(temp_dir)

def test_execute_command_success(os_interactor_instance):
    success, output = os_interactor_instance.execute_command(["echo", "hello"])
    assert success is True
    assert output == "hello"

def test_execute_command_failure(os_interactor_instance):
    success, error = os_interactor_instance.execute_command(["non_existent_command"])
    assert success is False
    assert "No such file or directory" in error or "command not found" in error

def test_execute_command_shell(os_interactor_instance):
    success, output = os_interactor_instance.execute_command("echo hello from shell", shell=True)
    assert success is True
    assert output == "hello from shell"

