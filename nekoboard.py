import sys
from path import Path
from note import Note
from task import Task
from project import Project
from journal import Journal
from money import Money
from usage import Usage

def Nekoboard():
    arg = sys.argv
    Path()

    if len(arg) == 1:
        Usage()
        return

    match arg[1].lower():
        case 'note' | 'nt':
            Note(arg, Path())

        case 'task' | 'todo' | 'td':
            Task(arg, Path())

        case 'project' | 'proj' | 'pr':
            Project()

        case 'journal' | 'journ' | 'jn':
            Journal()

        case 'money' | 'mon' | 'mn':
            Money()

        case _:
            Usage()

if __name__ == '__main__':
    Nekoboard()
