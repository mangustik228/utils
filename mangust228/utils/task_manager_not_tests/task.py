from dataclasses import dataclass


@dataclass
class Task:
    url: str
    id: int
    retries: int
    result_url: str | None = None

    @property
    def file_name(self):
        return self.url\
            .replace("https://", "")\
            .replace(".", "___")\
            .replace("/", "__")

    def __repr__(self):
        return f"{self.id} - {self.url}"
