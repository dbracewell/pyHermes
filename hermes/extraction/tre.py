from .transition import *
import re

__converter = {
    'stopword': StopWordTransition.create,
    'number': NumberTransition.create,
    'punct': PunctTransition.create,
    'word': WordTransition.create,
    'tag': TagTransition.create,
    'regex': RegexTransition.create,
    'attribute': AttributeTransition.create,
    'any': AnyTransition.create
}

__lexer = re.compile(r"""(
   (?P<attribute>\#{(?:[a-zA-Z_]+):\s*[\w_]+\s*})  #Attribute match
   |
   (?P<tag>\#\w+)
   |
   (?P<stopword>\[:STOPWORD:\])
   |
   (?P<group>\(\?<[\w_]+>)
   |
   (?P<number>\[:NUMBER:\])
   |
   (?P<punct>\[:PUNCT:\])
   |
   (?P<parent>/>)
   |
   (?P<annotation>\${\w+:)      #Annotation Match
   |
   (?P<lexicon>%\w+)
   |
   (?P<any>~)
   |
   (?P<look_ahead>\(\?!?>) #look ahead
   |
   (?P<star>\*)
   |
   (?P<plus>\+)
   |
   (?P<not>\^)
   |
   (?P<and>&)
   |
   (?P<or>\|)
   |
   (?P<open_paren>\()
   |
   (?P<close_paren>\))
   |
   (?P<close_bracket>\})
   |
   (?P<question>\?)
   |
   (?P<range>{\d+(?:,\d+)?}) #range
   |
   (?P<word>(\\.|[^$\s{}()/<?+.*])+(\(\?[il]\))?)
   |
   (?P<regex>/[^/]+/[il]?)
)""", re.I | re.UNICODE | re.VERBOSE)


def __make_expression(expressions, position, stack):
    m = expressions[position]
    m_type = next((k for k, v in m.groupdict().items() if v is not None), None)

    if m_type is None:
        raise Exception("Unknown lexical type %s" % m.group())

    elif m_type in __converter:
        stack.append(__converter[m_type](m.group()))
        return position + 1

    elif m_type == 'open_paren' or m_type == 'group':
        name = None if m_type == 'open_paren' else m.group()[3:-1]
        position += 1
        terminated = False
        stack_start = len(stack)
        while position < len(expressions):
            position = __make_expression(expressions, position, stack)
            if stack[-1] == ')':
                stack.pop()
                terminated = True
                break

        if not terminated:
            raise Exception('Non terminated parenthesis near %s' % stack[stack_start:])

        group = stack[stack_start:]
        if name:
            grouped_exp = GroupTransition(group, name)
        else:
            grouped_exp = SequenceTransition(group)

        for i in range(stack_start, len(stack)):
            del stack[-1]
        stack.append(grouped_exp)
        return position

    elif m_type == 'close_paren':
        stack.append(')')
        return position + 1

    elif m_type == 'not':
        position = __make_expression(expressions, position + 1, stack)
        stack.append(NotTransition(stack.pop()))
        return position

    elif m_type == 'question':
        stack.append(ZeorOrOne(stack.pop()))
        return position + 1


def compile(pattern: str):
    stack = []
    expressions = list(__lexer.finditer(pattern))
    position = 0
    while position < len(expressions):
        position = __make_expression(expressions, position, stack)
    return SequenceTransition(stack).construct()
