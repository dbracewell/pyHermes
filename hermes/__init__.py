from hermes.core.attributes import set_encoder
from hermes.language import Language
from hermes.tag.pos import PartOfSpeech
import hermes.types as htypes

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
__author__ = 'David B. Bracewell'

set_encoder(htypes.PART_OF_SPEECH, lambda x: PartOfSpeech.of(x))
set_encoder(htypes.LANGUAGE, lambda x: Language.of(x))
