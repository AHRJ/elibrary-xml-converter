from dataclasses import dataclass, field
from typing import Dict, List

RU = "RUS"
EN = "ENG"
LANGUAGES = [RU, EN]


@dataclass
class Author:
    first_name: Dict[str, str] = field(default_factory=lambda: {RU: None, EN: None})
    last_name: Dict[str, str] = field(default_factory=lambda: {RU: None, EN: None})

    @property
    def full_name(self):
        full_name = {}
        for lang in LANGUAGES:
            try:
                full_name[lang] = "".join(
                    [self.first_name[lang][0], ". ", self.last_name[lang]]
                )
            except:
                return None
        return full_name


@dataclass
class Article:
    id: str = None
    doi: str = None
    title: Dict[str, str] = field(default_factory=lambda: {RU: None, EN: None})
    authors: List[Author] = field(default_factory=lambda: [])
    abstract: Dict[str, str] = field(default_factory=lambda: {RU: None, EN: None})
    keywords: Dict[str, List[str]] = field(default_factory=lambda: {RU: [], EN: []})


@dataclass
class Journal:
    year: str = ""
    issue: str = ""
    articles: List[Article] = field(default_factory=lambda: [])
