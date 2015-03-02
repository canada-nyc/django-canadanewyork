from distutils.util import strtobool

from invoke.exceptions import ParseError


def confirm(prompt='Continue?\n', failure_prompt='User cancelled task'):
    '''
    Prompt the user to continue. Repeat on unknown response. Raise
    ParseError on negative response
    '''
    response = raw_input(prompt)

    try:
        response_bool = strtobool(response)
    except ValueError:
        print 'Unkown Response. Confirm with y, yes, t, true, on or 1; cancel with n, no, f, false, off or 0.'
        confirm(prompt, failure_prompt)

    if not response_bool:
        raise ParseError(failure_prompt)
