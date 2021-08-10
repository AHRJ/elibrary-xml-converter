from app.parsers import ElibraryParser
from app.models import Journal
import pytest


@pytest.fixture
def parser():
    return ElibraryParser("tests/example.xml", isFile=True)


@pytest.fixture
def articles(parser):
    return [article for article in parser.root.iter("article")]


def test_year(parser):
    assert parser._year == "2021"


def test_issue(parser):
    assert parser._issue == "7"


def test_articles_num(parser):
    assert len(parser._articles) == 20


def test_article_id(parser):
    assert parser._get_article_id(3) == "zzr-2021-07-003"
    assert parser._get_article_id(20) == "zzr-2021-07-020"


def test_article_doi(parser, articles):
    assert parser._get_article_doi(articles[0]) == None
    assert parser._get_article_doi(articles[7]) == "10.25701/ZZR.2021.23.32.001"


def test_article_title(parser, articles):
    title1 = parser._get_article_title(articles[0])
    title2 = parser._get_article_title(articles[19])

    assert title1["RUS"] == "«Каждое хозяйство края достойно называться флагманом»"
    assert title1["ENG"] == "«Every farm of the Territory deserves calling a leader»"
    assert title2["RUS"] == "CLAAS SHREDLAGE®: универсальное решение"
    assert title2["ENG"] == "CLAAS SHREDLAGE®: a versatile solution"


def test_article_authors(parser, articles):
    authors1 = parser._get_article_authors(articles[0])
    authors2 = parser._get_article_authors(articles[2])
    authors3 = parser._get_article_authors(articles[19])

    assert len(authors1) == 1
    assert len(authors2) == 4
    assert len(authors3) == 0

    assert authors1[0].full_name["RUS"] == "А. Чеботаев"
    assert authors1[0].full_name["ENG"] == "A. Chebotaev"
    assert authors2[3].full_name["RUS"] == "А. Рудковская"
    assert authors2[3].full_name["ENG"] == "A. Rudkovskaya"


def test_article_abstract(parser, articles):
    abstract1 = parser._get_article_abstract(articles[0])
    abstract2 = parser._get_article_abstract(articles[16])

    assert (
        abstract1["RUS"]
        == "В минувшем году многие районы Алтайского края постигла сильная засуха. О том, как местные аграрии справились с ее последствиями, в интервью нашему журналу рассказывает министр сельского хозяйства Алтайского края Александр Чеботаев."
    )
    assert abstract1["ENG"] == None
    assert (
        abstract2["RUS"]
        == "Руководитель компании «Бионика» - официального представителя проекта Силостоп® в России - Сергей Ермолаев рассказывает об особенностях и преимуществах применения инновационной технологии герметизации хранилищ при производстве основных кормов."
    )
    assert abstract1["ENG"] == None


def test_article_keywords(parser, articles):
    keywords1 = parser._get_article_keywords(articles[0])
    keywords2 = parser._get_article_keywords(articles[12])

    assert len(keywords1["RUS"]) == 6
    assert len(keywords1["ENG"]) == 0
    assert len(keywords2["RUS"]) == 10
    assert len(keywords2["ENG"]) == 0

    assert keywords1["RUS"][5] == "экспорт продукции АПК из Алтайского края"
    assert keywords2["RUS"][4] == "Availa®Dairy 6"


def test_fill(parser):
    journal = Journal()
    parser.fill(journal)

    assert journal.year == "2021"
    assert journal.issue == "7"
    assert len(journal.articles) == 20


def test_init_from_string():
    xml = """<?xml version="1.0" encoding="utf-16" standalone="no"?>
<journal>
  <titleid>9780</titleid>
  <issn>2313-5980</issn>
  <journalInfo lang="RUS">
    <title>Животноводство России</title>
  </journalInfo>
  <issue>
    <number>7</number>
    <dateUni>2021</dateUni>
    <pages>1-64</pages>
    <articles>
      <section>
        <secTitle lang="RUS">РЕГИОНЫ РОССИИ</secTitle>
      </section>
      <article>
        <pages>2-5</pages>
        <artType>UNK</artType>
        <authors>
          <author num="001">
            <individInfo lang="RUS">
              <surname>Чеботаев</surname>
              <initials>Александр</initials>
            </individInfo>
            <individInfo lang="ENG">
              <surname>Chebotaev</surname>
              <initials>A.</initials>
            </individInfo>
          </author>
        </authors>
        <artTitles>
          <artTitle lang="RUS">«Каждое хозяйство края достойно называться флагманом»</artTitle>
          <artTitle lang="ENG">«Every farm of the Territory deserves calling a leader»</artTitle>
        </artTitles>
        <abstracts>
          <abstract lang="RUS">В минувшем году многие районы Алтайского края постигла сильная засуха. О том, как местные аграрии справились с ее последствиями, в интервью нашему журналу рассказывает министр сельского хозяйства Алтайского края Александр Чеботаев.</abstract>
        </abstracts>
        <text lang="RUS">Алтайский край многие годы остается одним из крупнейших аграрных регионов России. </text>
        <keywords>
          <kwdGroup lang="RUS">
            <keyword>сельское хозяйство Алтайского края</keyword>
            <keyword>засуха в Алтайском крае</keyword>
            <keyword>развитие скотоводства</keyword>
            <keyword>свиноводства</keyword>
            <keyword>птицеводства в Алтайском крае</keyword>
            <keyword>экспорт продукции АПК из Алтайского края</keyword>
          </kwdGroup>
        </keywords>
        <files>
          <file desc="fullText">1.pdf</file>
        </files>
      </article>
    </articles>
  </issue>
</journal>
    """

    parser = ElibraryParser(xml)
    assert parser._year == "2021"
    assert len(parser._articles) == 1
