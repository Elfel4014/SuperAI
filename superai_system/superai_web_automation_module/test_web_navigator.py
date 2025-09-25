
import pytest
from unittest.mock import patch, MagicMock, call
import urllib.request
import urllib.parse
from superai_web_automation_module.web_navigator import WebNavigator, SimpleHTMLParser

# Mock para urllib.request.urlopen
@pytest.fixture
def mock_urlopen():
    with patch("urllib.request.urlopen") as mock_url_open:
        yield mock_url_open

@pytest.fixture
def web_navigator_instance():
    return WebNavigator()

def test_fetch_url_get(mock_urlopen, web_navigator_instance):
    mock_response = MagicMock()
    mock_response.read.return_value = b"<html><body>Hello World</body></html>"
    mock_response.getcode.return_value = 200
    mock_urlopen.return_value.__enter__.return_value = mock_response

    url = "http://example.com"
    content = web_navigator_instance.fetch_url(url)

    # Verificar se urllib.request.Request foi chamado com a URL correta
    assert mock_urlopen.call_args[0][0].full_url == url
    assert mock_urlopen.call_args[0][0].data is None
    assert content == "<html><body>Hello World</body></html>"

def test_fetch_url_post(mock_urlopen, web_navigator_instance):
    mock_response = MagicMock()
    mock_response.read.return_value = b"<html><body>POST Success</body></html>"
    mock_response.getcode.return_value = 200
    mock_urlopen.return_value.__enter__.return_value = mock_response

    url = "http://example.com/post"
    data = {"key": "value"}
    content = web_navigator_instance.fetch_url(url, data=data)

    expected_data = urllib.parse.urlencode(data).encode("ascii")
    # Verificar se urllib.request.Request foi chamado com a URL e dados corretos
    assert mock_urlopen.call_args[0][0].full_url == url
    assert mock_urlopen.call_args[0][0].data == expected_data
    assert content == "<html><body>POST Success</body></html>"

def test_fetch_url_headers(mock_urlopen, web_navigator_instance):
    mock_response = MagicMock()
    mock_response.read.return_value = b"<html><body>With Headers</body></html>"
    mock_response.getcode.return_value = 200
    mock_urlopen.return_value.__enter__.return_value = mock_response

    url = "http://example.com/headers"
    headers = {"User-Agent": "Test-Agent"}
    content = web_navigator_instance.fetch_url(url, headers=headers)

    # Verificar se urllib.request.Request foi chamado com a URL e cabeçalhos corretos
    assert mock_urlopen.call_args[0][0].full_url == url
    assert mock_urlopen.call_args[0][0].get_header("User-agent") == headers["User-Agent"]
    assert content == "<html><body>With Headers</body></html>"

def test_parse_html_to_text(web_navigator_instance):
    html_content = """<html><head><title>Test</title></head><body><h1>Hello</h1><p>This is a paragraph.</p></body></html>"""
    expected_text = "TestHelloThis is a paragraph."
    actual_text = web_navigator_instance.parse_html_to_text(html_content)
    assert actual_text == expected_text

def test_simple_html_parser():
    parser = SimpleHTMLParser()
    parser.feed("<div>Text1<span>Text2</span></div>")
    assert parser.get_text() == "Text1Text2"

