from app.models import Journal, Article, Author
import pytest


def test_journal_defaults():
    journal = Journal()
    assert journal.year == ""
    assert journal.issue == ""
    assert journal.articles == []


def test_journal_fill():
    journal = Journal()
    journal.year = "2000"
    journal.issue = "sv"
    journal.articles.append(1)

    assert journal.year == "2000"
    assert journal.issue == "sv"
    assert journal.articles == [1]


def test_article_defaults():
    article = Article()
    assert article.id == None
    assert article.doi == None
    assert article.title == {"ENG": None, "RUS": None}
    assert article.authors == []
    assert article.abstract == {"ENG": None, "RUS": None}
    assert article.keywords == {"ENG": [], "RUS": []}


def test_article_fill():
    article = Article()
    article.id = "123"
    article.doi = "123"
    article.title = {"ENG": "aoeu", "RUS": "snth"}
    article.authors = ["123"]
    article.abstract = {"ENG": "aoeu", "RUS": "snth"}
    article.keywords = {"ENG": ["aoeu", "snth"], "RUS": ["nthd", "dhtn"]}

    assert article.id == "123"
    assert article.doi == "123"
    assert article.title == {"ENG": "aoeu", "RUS": "snth"}
    assert article.authors == ["123"]
    assert article.abstract == {"ENG": "aoeu", "RUS": "snth"}
    assert article.keywords == {"ENG": ["aoeu", "snth"], "RUS": ["nthd", "dhtn"]}


def test_author_defaults():
    author = Author()

    assert author.first_name == {"RUS": None, "ENG": None}
    assert author.last_name == {"RUS": None, "ENG": None}
    assert author.full_name == None


def test_author_fill():
    author = Author()
    author.first_name = {"RUS": "Иван", "ENG": "Ivan"}
    author.last_name = {"RUS": "Иванов", "ENG": "Ivanov"}

    assert author.first_name == {"RUS": "Иван", "ENG": "Ivan"}
    assert author.last_name == {"RUS": "Иванов", "ENG": "Ivanov"}
    assert author.full_name["RUS"] == "И. Иванов"
    assert author.full_name["ENG"] == "I. Ivanov"
