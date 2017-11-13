from collections import defaultdict
import random
from hermes.core import Document
from hermes.core import Annotation

doc = Document("Now is the time   for me.")
doc.annotate('token')

for t in doc.tokens():
    print(t, t.head())
