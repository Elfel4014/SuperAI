
import urllib.request
import urllib.parse
from html.parser import HTMLParser

class SimpleHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = []

    def handle_data(self, data):
        self.data.append(data)

    def get_text(self):
        return ".".join(self.data)

class WebNavigator:
    def fetch_url(self, url, headers=None, data=None):
        """
        Busca o conteúdo de uma URL.
        :param url: A URL a ser buscada.
        :param headers: Dicionário de cabeçalhos HTTP.
        :param data: Dicionário de dados para requisições POST.
        :return: O conteúdo da página como string.
        """
        if data:
            data = urllib.parse.urlencode(data).encode("ascii")

        req = urllib.request.Request(url, data=data, headers=headers or {})
        
        with urllib.request.urlopen(req) as response:
            return response.read().decode("utf-8")

    def parse_html_to_text(self, html_content):
        """
        Analisa o conteúdo HTML e extrai o texto visível.
        :param html_content: O conteúdo HTML como string.
        :return: O texto extraído como string.
        """
        parser = SimpleHTMLParser()
        parser.feed(html_content)
        return parser.get_text()

# Exemplo de uso (para testes internos)
if __name__ == "__main__":
    navigator = WebNavigator()
    # Exemplo de GET
    print("\n--- Teste de GET ---")
    try:
        html = navigator.fetch_url("https://www.google.com")
        text = navigator.parse_html_to_text(html)
        print(f"Conteúdo do Google (parcial): {text[:500]}...")
    except Exception as e:
        print(f"Erro ao buscar Google: {e}")

    # Exemplo de POST (simulado, sem um endpoint real para testar)
    print("\n--- Teste de POST (simulado) ---")
    try:
        # Para testar POST, você precisaria de um servidor que aceite POST
        # Este é apenas um exemplo de como a função seria chamada
        post_data = {"name": "Agent", "message": "Hello World"}
        # html_post = navigator.fetch_url("http://httpbin.org/post", data=post_data)
        # print(f"Conteúdo do POST (parcial): {html_post[:500]}...")
        print("Teste de POST simulado. Nenhuma requisição POST real foi feita.")
    except Exception as e:
        print(f"Erro ao simular POST: {e}")

