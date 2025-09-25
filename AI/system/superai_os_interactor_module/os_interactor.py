
import os
import subprocess

def create_file(path, content=""):
    """
    Cria um arquivo com o conteúdo especificado.
    :param path: Caminho completo do arquivo.
    :param content: Conteúdo a ser escrito no arquivo.
    """
    try:
        with open(path, "w") as f:
            f.write(content)
        return True, f"Arquivo {path} criado com sucesso."
    except Exception as e:
        return False, f"Erro ao criar arquivo {path}: {e}"

def read_file(path):
    """
    Lê o conteúdo de um arquivo.
    :param path: Caminho completo do arquivo.
    :return: Conteúdo do arquivo como string ou mensagem de erro.
    """
    try:
        with open(path, "r") as f:
            return True, f.read()
    except Exception as e:
        return False, f"Erro ao ler arquivo {path}: {e}"

def delete_file(path):
    """
    Deleta um arquivo.
    :param path: Caminho completo do arquivo.
    """
    try:
        os.remove(path)
        return True, f"Arquivo {path} deletado com sucesso."
    except Exception as e:
        return False, f"Erro ao deletar arquivo {path}: {e}"

def create_directory(path):
    """
    Cria um diretório.
    :param path: Caminho completo do diretório.
    """
    try:
        os.makedirs(path, exist_ok=True)
        return True, f"Diretório {path} criado com sucesso."
    except Exception as e:
        return False, f"Erro ao criar diretório {path}: {e}"

def delete_directory(path):
    """
    Deleta um diretório (deve estar vazio).
    :param path: Caminho completo do diretório.
    """
    try:
        os.rmdir(path)
        return True, f"Diretório {path} deletado com sucesso."
    except Exception as e:
        return False, f"Erro ao deletar diretório {path}: {e}"

def execute_command(command, shell=False):
    """
    Executa um comando do sistema operacional e retorna a saída.
    :param command: O comando a ser executado (lista de strings ou string se shell=True).
    :param shell: Se True, o comando será executado através do shell.
    :return: Tupla (True/False, stdout/stderr).
    """
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True, check=True)
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()
    except Exception as e:
        return False, f"Erro ao executar comando: {e}"

# Exemplo de uso (para testes internos)
if __name__ == "__main__":
    # Teste de criação e leitura de arquivo
    print("\n--- Teste de Arquivo ---")
    success, message = create_file("test_file.txt", "Hello OS Interactor!")
    print(message)
    if success:
        success, content = read_file("test_file.txt")
        print(f"Conteúdo lido: {content}")
        success, message = delete_file("test_file.txt")
        print(message)

    # Teste de diretório
    print("\n--- Teste de Diretório ---")
    success, message = create_directory("test_dir")
    print(message)
    if success:
        success, message = delete_directory("test_dir")
        print(message)

    # Teste de comando
    print("\n--- Teste de Comando ---")
    success, output = execute_command(["echo", "Hello from OS!"])
    print(f"Saída do comando: {output}")
    success, output = execute_command("ls -l", shell=True)
    print(f"Saída do comando (shell):\n{output}")

