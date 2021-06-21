from parser import ElibraryParser

import utils
from csv_maker import CSVMaker
from models import Journal


def handler(event, context):
    journal = Journal()
    xml = utils.extract_xml(event)
    parser = ElibraryParser(xml)
    parser.fill(journal)
    payload = CSVMaker.render(journal)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Disposition": 'attachment; filename="articles-import.csv"'
        },
        "body": payload,
    }
