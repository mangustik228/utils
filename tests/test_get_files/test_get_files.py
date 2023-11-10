from mangust228 import get_files_paths
import pytest


def test_get_files_paths():
    fp = "tests/src/get_files"
    counter = 0
    for _ in get_files_paths(fp, ".html"):
        counter += 1
    assert counter == 315


def test_get_files_paths_items():
    fp = "tests/src/get_files_2"
    gen = get_files_paths(fp, ".html")
    item = next(gen)
    assert item.path == "tests/src/get_files_2/2023/November/10/7/www___example___com__page_90.html"
    assert item.params == ["www.example.com/page", 90]


def test_get_files_paths_sep():
    fp = "tests/src/get_files_3"
    gen = get_files_paths(fp, ".html", "|")
    item = next(gen)
    assert item.path == "tests/src/get_files_3/2023/November/10/7/www___example___com__page_3|90.html"
    assert item.params == ["www.example.com/page_3", 90]


def test_get_content():
    fp = "tests/src/get_files_3"
    gen = get_files_paths(fp, ".html", "|", return_content=True)
    item = next(gen)
    assert item.content == "hello world"


def test_get_content_xz():
    fp = "tests/src/get_files_4"
    gen = get_files_paths(fp, ".xz", return_content=True)
    item = next(gen)
    assert item.content == "hello world"
    assert item.params == ["world"]
    assert item.path == "tests/src/get_files_4/2023/world.html.xz"
