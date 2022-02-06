import datetime
import json
from pathlib import Path
import sys
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
import pprint

from config import Config


def get_module_name(soup):
    ele = soup.find("b", text="Command Line: ")
    return Path(ele.next_sibling).stem


def get_faulting_frame(soup):
    ele = soup.find("b", text="Faulting Frame: ")
    return ele.next_sibling


def get_dump_file(soup):
    ele = soup.find("b", text="Dump File: ")
    return ele.next_sibling


def main(report_html_filename, extra_data):
    html = open(report_html_filename, encoding='utf-8').read()
    soup = BeautifulSoup(html, "html.parser")

    es = Elasticsearch(Config.get('ES_URL'), http_auth=(
        Config.get('ES_ID'), Config.get('ES_PW')))

    pprint.pprint(es)

    doc = {
        "dump_file": get_dump_file(soup),
        "faulting_frame": get_faulting_frame(soup),
        "module_name": get_module_name(soup),
        "extra": extra_data,
        "@timestamp": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    }

    pprint.pprint(doc)

    today = datetime.date.today()
    day = today.strftime("%Y-%m-%d")
    index = Config.get('ES_INDEX') + "-" + day
    pprint.pprint(f"index : {index}")

    es.index(index=index, doc_type="_doc", document=doc)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("using python dumpreporttoes <report_html_filename> <extra_data_filename")
        exit(1)

    argument = sys.argv

    try:
        f = open(argument[2])
        extra = json.loads(f.read())
        f.close()
    except Exception as e:
        print("extra_data must be a json string")
        exit(1)

    main(argument[1], extra)
