from text_format import *

def Usage():
    usage = [
        ['note/nt', 'manage notes'],
        ['task/todo/td', 'manage todo items'],
        ['project/proj/pr', 'manage projects'],
        ['journal/journ/jn', 'manage journal'],
        ['money/mon/mn', 'manage finances']
    ]

    print('\n ' + bold + underline + red + 'Nekoboard usage\n' + normal)
    for line in usage:
        print(bold + ' - ' + blue + line[0] + normal + ': ' + line[1])
    print('')
