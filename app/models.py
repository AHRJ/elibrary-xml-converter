from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Author:
    first_name: Dict[str, str] = field(
        default_factory=lambda: {"RUS": None, "ENG": None}
    )
    last_name: Dict[str, str] = field(
        default_factory=lambda: {"RUS": None, "ENG": None}
    )

    @property
    def full_name(self):
        full_name = {}
        for lang in ["RUS", "ENG"]:
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
    title: Dict[str, str] = field(default_factory=lambda: {"RUS": None, "ENG": None})
    authors: List[Author] = field(default_factory=lambda: [])
    abstract: Dict[str, str] = field(default_factory=lambda: {"RUS": None, "ENG": None})
    keywords: Dict[str, List[str]] = field(
        default_factory=lambda: {"RUS": [], "ENG": []}
    )


@dataclass
class Journal:
    year: str = ""
    issue: str = ""
    articles: List[Article] = field(default_factory=lambda: [])
