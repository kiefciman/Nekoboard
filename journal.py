from text_format import *
import os
import json
import readline
from datetime import datetime

def Journal(arg, path):
    file = os.path.join(path[0], path[1][2])
    current_date = datetime.today().strftime('%d.%m.%Y')

    with open(file, 'r') as f:
        try:
            journal_data = json.load(f)
        except:
            journal_data = {}

    if len(arg) == 2:
        JournalUsage()
        return

    match arg[2].lower():
        case 'add' | 'new':
            try:
                AddJournal(arg[3:], current_date, file, journal_data)
            except Exception as e:
                JournalUsage()
                #print(e)

        case 'delete' | 'del' | 'rm' | 'remove':
            try:
                DeleteJournal(arg[3], file, journal_data)
            except Exception as e:
                JournalUsage()
                #print(e)

        case 'list' | 'ls':
            try:
                ListJournal(journal_data)
            except Exception as e:
                JournalUsage()
                #print(e)

        case 'read' | 'rd':
            try:
                ReadJournal(arg[3], journal_data)
            except Exception as e:
                JournalUsage()
                #print(e)

        case _:
            JournalUsage()

def JournalUsage():
    journalusage = [
        ['add/new {content}', 'add new journal entry for current date containing {content}, no "" required, multiword and multiline {content} supported, press enter before writing {content} to enter multiline edit mode, press enter on blank line to finish the journal entry, in case if journal entry for current date exists, that will be edited instead of creating a new one'],
        ['delete/del/rm/remove {date}', 'delete journal entry for {date}, if no {date} provided, deletes journal entry for current date'],
        ['list/ls', 'lists all dates that have journal entries'],
        ['read/rd {date}', 'shows content of journal entry from {date}, {date} should be in dd.mm.yyy format, if no {date} provided, shows content of current date\'s entry']
    ]

    print('\n' + bold + underline + red + 'Nekoboard journal usage\n' + normal)
    print(bold + blue + 'Note that only journal entry for current date can be edited')
    for line in journalusage:
        print(bold + ' - ' + blue + line[0] + normal + ': ' + line[1])
    print('')

def AddJournal(content, current_date, file, journal_data):
    try:
        journal_entry = journal_data[current_date]
    except:
        journal_entry = []

    if len(journal_entry) == 0:
        if len(content) > 0:
            journal_entry = [' '.join(content)]

        else:
            print('')
            journal_entry = []
            while True:
                line = input(' > ')
                if line == '':
                    break
                journal_entry.append(line)

        journal_data[current_date] = journal_entry
        
    else:
        if len(content) > 0:
            journal_entry.append(' '.join(content))
        else:
            for i in range(len(journal_entry)):
                readline.set_startup_hook(lambda: readline.insert_text(journal_entry[i]))
                try:
                    new_line = input(' > ')
                finally:
                    readline.set_startup_hook()

                journal_entry[i] = new_line

            while True:
                line = input(' > ')
                if line == '':
                    break
                journal_entry.append(line)

    with open(file, 'w') as f:
            json.dump(journal_data, f)
    print(bold + blue + '\n Journal entry saved for ' + current_date + '\n')

def DeleteJournal(date, file, journal_data):
    try:
        del journal_data[date]

        print('\n' + red + bold + ' Journal entry removed for ' + date + '\n')
        with open(file, 'w') as f:
            json.dump(journal_data, f)

    except Exception as e:
        print(bold + red + '\n No journal entry found for ' + date + '\n')
        #print(e)

def ListJournal(journal_data):
    print('\n ' + bold + red + underline +'Journal entries\n' + normal)
    for date in journal_data:
        print(bold + blue + ' - ' + normal + date)
    print('')

def ReadJournal(date, journal_data):
    try:
        print('\n ' + bold + red + underline +'Journal entry for ' + date + '\n' + normal)
        for line in journal_data[date]:
            print(' ' + line)
        print('')
    
    except:
        print(bold + red + '\n No journal entry found for ' + date + '\n')
