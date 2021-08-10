import csv
import io

from models import Journal


class CSVMaker:
    @staticmethod
    def render(journal: Journal):
        output = io.StringIO()
        fieldnames = [
            "ID",
            "Заголовок",
            "Заголовок (англ)",
            "Авторы",
            "Авторы (англ)",
            "Анонс",
            "Анонс (англ)",
            "Ключевые слова",
            "Ключевые слова (англ)",
            "Рубрика",
            "Год выхода",
            "Номер журнала или Код спецвыпуска",
            "DOI",
            "Партнер",
        ]

        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for article in journal.articles:
            writer.writerow(
                {
                    "ID": article.id,
                    "Заголовок": article.title["RUS"],
                    "Заголовок (англ)": article.title["ENG"],
                    "Авторы": ", ".join(
                        [
                            author.full_name["RUS"]
                            for author in article.authors
                            if author.full_name
                        ]
                    ),
                    "Авторы (англ)": ", ".join(
                        [
                            author.full_name["ENG"]
                            for author in article.authors
                            if author.full_name
                        ]
                    ),
                    "Анонс": article.abstract["RUS"],
                    "Анонс (англ)": article.abstract["ENG"],
                    "Ключевые слова": ", ".join(article.keywords["RUS"]),
                    "Ключевые слова (англ)": ", ".join(article.keywords["ENG"]),
                    "Рубрика": "",
                    "Год выхода": journal.year,
                    "Номер журнала или Код спецвыпуска": journal.issue,
                    "DOI": article.doi,
                    "Партнер": "",
                }
            )
        return output.getvalue()
