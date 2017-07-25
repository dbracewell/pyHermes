from hermes.core import Document
from hermes.language import ENGLISH
from io import BufferedReader
from collections import defaultdict
import csv


def json_reader(stream: BufferedReader, one_per_line=False, language=ENGLISH, preprocessors=None, parameters=None):
    with stream:
        if one_per_line:
            for line in stream:
                if len(line.strip()) > 0:
                    yield Document.from_json(line)
        else:
            Document.from_json(stream.read())


def plain_text_reader(stream: BufferedReader, one_per_line=False, language=ENGLISH, preprocessors=None,
                      parameters=None):
    with stream:
        if one_per_line:
            for line in stream:
                if len(line.strip()) > 0:
                    yield Document(line.rstrip(), preprocessors=preprocessors, language=language)
        else:
            Document(stream.read().rstrip(), preprocessors=preprocessors, language=language)


def csv_reader(stream: BufferedReader, one_per_line=False, language=ENGLISH, preprocessors=None, parameters=None):
    if parameters is None:
        parameters = {"id": 0, "content": 1}
    with stream:
        dialect = parameters['dialect'] if parameters and 'dialect' in parameters else 'excel'
        has_header = True if 'header' in parameters and parameters['header'] else False
        reader = csv.reader(stream, dialect=dialect)
        columns = defaultdict(lambda: None)
        if has_header:
            for (i, r) in enumerate(reader.__next__()):
                columns[r] = i
        for row in reader:
            if len(columns) == 0:
                for i in range(0, len(row)):
                    columns[i] = i
            doc_id = row[parameters['id']] if 'id' in parameters else None
            content_id = parameters['content'] if 'content' in parameters else 0
            yield Document(row[content_id], doc_id=doc_id, preprocessors=preprocessors, language=language)
