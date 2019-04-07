import sys

def exit_pooz(code=1):
    sys.exit(code)

def raise_interpreter_error(line, info):
    sys.stderr.write('Interpreter error:\n\t{0}\n{1}'.format(line, info))

def raise_error(line_no, 
                msg, target_file, 
                line=None,
                alert=False):

    if alert:
        sys.stderr.write('\a')

    sys.stderr.write('Error at {0} of \'{1}\'\n'.format(line_no, target_file))

    if line:
        sys.stderr.write('\t{0}'.format(line))
    
    sys.stderr.flush()

    input('Press any key to exit...')

    exit_pooz()
