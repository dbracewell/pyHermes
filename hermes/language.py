from importlib import import_module

"""
   Copyright 2017 David B. Bracewell

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

_languages = {}


class Language(object):
    def __init__(self, name: str, code: str, is_rtl=False):
        self.__name = name.upper()
        self.__is_rtl = is_rtl
        self.__code = code.lower()
        if self.__name in _languages or self.__code in _languages:
            raise Exception("{0} is already defined".format(self.__name))
        _languages[self.__name] = self
        _languages[self.__code] = self
        self.__annotators = {}

    def set_annotator(self, annotation: str, annotator):
        self.__annotators[annotation] = annotator

    def get_annotator(self, annotation: str):
        return self.__annotators[annotation] if annotation in self.__annotators else None

    @property
    def code(self):
        return self.__code

    @property
    def name(self):
        return self.__name

    @property
    def is_rtl(self):
        return self.__is_rtl

    def __str__(self):
        return self.__name

    def __repr__(self):
        return self.__name

    def __eq__(self, other):
        if isinstance(other, Language):
            return self.__name == other.__name
        return False

    def load(self):
        import_module("hermes.{}".format(self.__code))

    @staticmethod
    def of(language):
        language = language.upper()
        if language in _languages:
            return _languages[language]
        return UNKNOWN


UNKNOWN = Language("UNKNOWN", "unknown")
ENGLISH = Language("ENGLISH", "en")
CHINESE = Language("CHINESE", "zh")
JAPANESE = Language("JAPANESE", "ja")
