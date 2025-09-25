
import pytest
from unittest.mock import patch, mock_open, MagicMock
import os
import subprocess
from superai_os_interactor_module.os_interactor import create_file, read_file, delete_file, create_directory, delete_directory, execute_command

@pytest.fixture
def mock_os_path_exists():
    with patch("os.path.exists") as mock_exists:
        yield mock_exists

@pytest.fixture
def mock_os_remove():
    with patch("os.remove") as mock_remove:
        yield mock_remove

@pytest.fixture
def mock_os_makedirs():
    with patch("os.makedirs") as mock_makedirs:
        yield mock_makedirs

@pytest.fixture
def mock_os_rmdir():
    with patch("os.rmdir") as mock_rmdir:
        yield mock_rmdir

@pytest.fixture
def mock_subprocess_run():
    with patch("subprocess.run") as mock_run:
        yield mock_run

def test_create_file_success():
    m = mock_open()
    with patch("builtins.open", m):
        success, message = create_file("test.txt", "hello")
        assert success is True
        assert "criado com sucesso" in message
        m.assert_called_once_with("test.txt", "w")
        m().write.assert_called_once_with("hello")

def test_create_file_failure():
    with patch("builtins.open", side_effect=IOError("Permission denied")):
        success, message = create_file("test.txt", "hello")
        assert success is False
        assert "Erro ao criar arquivo" in message

def test_read_file_success():
    m = mock_open(read_data="file content")
    with patch("builtins.open", m):
        success, content = read_file("test.txt")
        assert success is True
        assert content == "file content"
        m.assert_called_once_with("test.txt", "r")

def test_read_file_failure():
    with patch("builtins.open", side_effect=IOError("File not found")):
        success, message = read_file("test.txt")
        assert success is False
        assert "Erro ao ler arquivo" in message

def test_delete_file_success(mock_os_remove):
    success, message = delete_file("test.txt")
    assert success is True
    assert "deletado com sucesso" in message
    mock_os_remove.assert_called_once_with("test.txt")

def test_delete_file_failure(mock_os_remove):
    mock_os_remove.side_effect = OSError("No such file")
    success, message = delete_file("test.txt")
    assert success is False
    assert "Erro ao deletar arquivo" in message

def test_create_directory_success(mock_os_makedirs):
    success, message = create_directory("test_dir")
    assert success is True
    assert "criado com sucesso" in message
    mock_os_makedirs.assert_called_once_with("test_dir", exist_ok=True)

def test_create_directory_failure(mock_os_makedirs):
    mock_os_makedirs.side_effect = OSError("Permission denied")
    success, message = create_directory("test_dir")
    assert success is False
    assert "Erro ao criar diretório" in message

def test_delete_directory_success(mock_os_rmdir):
    success, message = delete_directory("test_dir")
    assert success is True
    assert "deletado com sucesso" in message
    mock_os_rmdir.assert_called_once_with("test_dir")

def test_delete_directory_failure(mock_os_rmdir):
    mock_os_rmdir.side_effect = OSError("Directory not empty")
    success, message = delete_directory("test_dir")
    assert success is False
    assert "Erro ao deletar diretório" in message

def test_execute_command_success(mock_subprocess_run):
    mock_subprocess_run.return_value = MagicMock(stdout="command output", stderr="", returncode=0)
    success, output = execute_command(["echo", "hello"])
    assert success is True
    assert output == "command output"
    mock_subprocess_run.assert_called_once_with(["echo", "hello"], shell=False, capture_output=True, text=True, check=True)

def test_execute_command_failure(mock_subprocess_run):
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, "cmd", stderr="error output")
    success, output = execute_command(["bad_command"])
    assert success is False
    assert output == "error output"
    mock_subprocess_run.assert_called_once_with(["bad_command"], shell=False, capture_output=True, text=True, check=True)

def test_execute_command_shell_success(mock_subprocess_run):
    mock_subprocess_run.return_value = MagicMock(stdout="shell output", stderr="", returncode=0)
    success, output = execute_command("ls -l", shell=True)
    assert success is True
    assert output == "shell output"
    mock_subprocess_run.assert_called_once_with("ls -l", shell=True, capture_output=True, text=True, check=True)

def test_execute_command_shell_failure(mock_subprocess_run):
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, "cmd", stderr="shell error")
    success, output = execute_command("bad_command_shell", shell=True)
    assert success is False
    assert output == "shell error"
    mock_subprocess_run.assert_called_once_with("bad_command_shell", shell=True, capture_output=True, text=True, check=True)

