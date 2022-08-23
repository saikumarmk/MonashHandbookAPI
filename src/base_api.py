from requests import post
from abc import ABC, abstractmethod


class BaseAPI(ABC):

    BASE_URL = "https://handbook.monash.edu/api/es/search"

    def __init__(self) -> None:
        return

    @abstractmethod
    def _build_post_content(self, content: dict, options: dict) -> dict:
        pass

    def _post(self, content: dict, options: dict) -> dict:

        json_content = self._build_post_content(content, options)
        request = post(self.BASE_URL, json=json_content)

        if request.status_code != 200:
            raise ValueError(f'Error code: {request.status_code}')

        return request.json()
