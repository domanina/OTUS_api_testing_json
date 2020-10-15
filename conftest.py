import pytest
import requests


class APIClient:
    """
    Упрощенный клиент для работы с API
    Инициализируется базовым url на который пойдут запросы
    """

    def __init__(self, base_address):
        self.base_address = base_address

    def get_brew(self, path="/", params=None, query="?",cond="="):
        url = self.base_address + path + query + cond
        print("GET request to {}".format(url))
        return requests.get(url=url, params=params)

    def post_brew(self, path="/", params=None, data=None, headers=None):
        url = self.base_address + path
        print("POST request to {}".format(url))
        return requests.post(url=url, params=params, data=data, headers=headers)


# Тестовое API: ttps://jsonplaceholder.typicode.com/posts/
def pytest_addoption(parser):
    parser.addoption(
        "--url",
        action="store",
        default="https://jsonplaceholder.typicode.com",
        help="This is request url"
    )


@pytest.fixture(scope="session")
def api_client_brew(request):
    base_url = request.config.getoption("--url")
    return APIClient(base_address=base_url)
