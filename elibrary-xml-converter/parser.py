import xml.etree.ElementTree as ET

from models import Article, Author, Journal


class ElibraryParser:
    def __init__(self, xml):
        self.tree = ET.ElementTree(ET.fromstring(xml))
        self.root = self.tree.getroot()

    def fill(self, journal: Journal):
        journal.year = self._year
        journal.issue = self._issue
        journal.articles = self._articles

    @property
    def _year(self) -> str:
        return self.root.find("issue").find("dateUni").text

    @property
    def _issue(self) -> str:
        val = self.root.find("issue").find("number").text
        if val == "S1":
            return "SV"
        elif val == "S2":
            return "SK"
        elif val == "S3":
            return "PT"
        else:
            return val

    @property
    def _articles(self):
        articles = []
        for num, entry in enumerate(self.root.iter("article"), 1):
            article = Article()
            article.id = self._get_article_id(num)
            article.doi = self._get_article_doi(entry)
            article.title = self._get_article_title(entry)
            article.authors = self._get_article_authors(entry)
            article.abstract = self._get_article_abstract(entry)
            article.keywords = self._get_article_keywords(entry)
            articles.append(article)
        return articles

    def _get_article_id(self, count):
        return "-".join(["zzr", self._year, self._issue.zfill(2), str(count).zfill(3)])

    def _get_article_doi(self, entry):
        try:
            return entry.find("codes").find("doi").text
        except:
            return None

    def _get_article_title(self, entry):
        titles = {}
        title_xml = entry.find("artTitles").findall("artTitle")
        for title in title_xml:
            titles[title.get("lang")] = title.text
        return titles

    def _get_article_authors(self, entry):
        authors = []
        try:
            authors_xml = entry.find("authors").findall("author")
            for author_meta in authors_xml:
                author = Author()
                author_info = author_meta.findall("individInfo")
                for a in author_info:
                    author.first_name[a.get("lang")] = a.find("initials").text
                    author.last_name[a.get("lang")] = a.find("surname").text

                authors.append(author)
        except:
            pass
        return authors

    def _get_article_abstract(self, entry):
        abstracts = {"RUS": None, "ENG": None}
        try:
            abstracts_xml = entry.find("abstracts").findall("abstract")
            for abstract in abstracts_xml:
                abstracts[abstract.get("lang")] = abstract.text
        except:
            pass
        return abstracts

    def _get_article_keywords(self, entry):
        keywords = {"RUS": [], "ENG": []}
        try:
            keywords_xml = entry.find("keywords").findall("kwdGroup")
            for keyword_group in keywords_xml:
                for keyword in keyword_group.findall("keyword"):
                    keywords[keyword_group.get("lang")].append(keyword.text)

        except:
            pass
        return keywords
