# Módulo de Interação Completa com Sistemas Operacionais

O `superai_os_interactor_module` é o componente do sistema SuperAI que permite à IA interagir diretamente com o sistema operacional subjacente (Windows/Linux). Ele fornece funcionalidades para gerenciar arquivos, diretórios e executar comandos do sistema, sem depender de APIs externas, utilizando módulos padrão do Python como `os` e `subprocess`.

## `OSInteractor` Class

Esta classe encapsula as funcionalidades de interação com o sistema operacional.

### Métodos:

#### `create_file(self, path, content="")`

-   **Descrição:** Cria um arquivo no caminho especificado com o conteúdo fornecido.
-   **Parâmetros:**
    -   `path` (str): O caminho completo, incluindo o nome do arquivo, onde o arquivo será criado.
    -   `content` (str, opcional): O conteúdo a ser escrito no arquivo (padrão: string vazia).
-   **Retorna:** (tuple) Uma tupla `(bool, str)` indicando `(sucesso, mensagem_de_status)`.

#### `read_file(self, path)`

-   **Descrição:** Lê o conteúdo de um arquivo especificado.
-   **Parâmetros:**
    -   `path` (str): O caminho completo do arquivo a ser lido.
-   **Retorna:** (tuple) Uma tupla `(bool, str)` indicando `(sucesso, conteúdo_do_arquivo_ou_mensagem_de_erro)`.

#### `delete_file(self, path)`

-   **Descrição:** Deleta um arquivo especificado.
-   **Parâmetros:**
    -   `path` (str): O caminho completo do arquivo a ser deletado.
-   **Retorna:** (tuple) Uma tupla `(bool, str)` indicando `(sucesso, mensagem_de_status)`.

#### `create_directory(self, path)`

-   **Descrição:** Cria um diretório no caminho especificado. Se o diretório já existir, nenhuma ação é tomada.
-   **Parâmetros:**
    -   `path` (str): O caminho completo do diretório a ser criado.
-   **Retorna:** (tuple) Uma tupla `(bool, str)` indicando `(sucesso, mensagem_de_status)`.

#### `delete_directory(self, path)`

-   **Descrição:** Deleta um diretório especificado. O diretório deve estar vazio.
-   **Parâmetros:**
    -   `path` (str): O caminho completo do diretório a ser deletado.
-   **Retorna:** (tuple) Uma tupla `(bool, str)` indicando `(sucesso, mensagem_de_status)`.

#### `execute_command(self, command, shell=False)`

-   **Descrição:** Executa um comando do sistema operacional e captura sua saída.
-   **Parâmetros:**
    -   `command` (list ou str): O comando a ser executado. Se for uma lista de strings, o comando é executado diretamente. Se for uma string e `shell=True`, o comando é executado através do shell do sistema.
    -   `shell` (bool, opcional): Se `True`, o comando será executado através do shell do sistema (padrão: `False`).
-   **Retorna:** (tuple) Uma tupla `(bool, str)` indicando `(sucesso, stdout_ou_stderr)`.

## Uso

Este módulo é fundamental para a capacidade da SuperAI de interagir com o ambiente computacional, permitindo a automação de tarefas locais, gerenciamento de arquivos e execução de scripts ou programas externos.
