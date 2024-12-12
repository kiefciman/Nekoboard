from text_format import *
import os
import json
import readline

def Note(arg, path):
    file = os.path.join(path[0], path[1][0])
    
    with open(file, 'r') as f:
        try:
            note_data = json.load(f)
        except:
            note_data = {}

    if len(arg) == 2:
        NoteUsage()
        return

    match arg[2].lower():
        case 'add' | 'new':
            try:
                AddNote(arg[3], arg[4:], file, note_data)
            except Exception as e:
                NoteUsage()

                #print(e)
        case 'categories' | 'cat':
            try:
                NoteCategories(note_data)
            except Exception as e:
                NoteUsage()
                #print(e)

        case 'list' | 'ls':
            try:
                ListNotes(arg[3], note_data)
            except Exception as e:
                NoteUsage()
                #print(e)

        case 'delete'| 'del' | 'rm' | 'remove':
            try:
                DeleteNote(arg[3], arg[4], file, note_data)
            except Exception as e:
                NoteUsage()
                #print(e)

        case 'edit' | 'ed':
            try:
                EditNote(arg[3], arg[4], file, note_data)
            except Exception as e:
                NoteUsage()
                #print(e)

        case _:
            NoteUsage()

def NoteUsage():
    noteusage = [
        ['add/new {category} {content}', 'add new note note containing {content} to {category}, no "" required, multiword {content} supported, press enter after {category} to enter multiline edit mode, press enter on blank line to finish the note'],
        ['note categories/cat', 'list all note categories'],
        ['list/ls {category}', 'list all notes from {category}'],
        ['delete/del/rm/remove {category} {index}', 'delete note no. {index} from {category}'],
        ['edit/ed {category} {index}', 'edit note no. {index} from {category}']
    ]

    print('\n ' + bold + underline + red + 'Nekoboard note usage\n' + normal)
    for line in noteusage:
        print(bold + ' - ' + blue + line[0] + normal + ': ' + line[1])
    print('')

def AddNote(category, content, file, note_data): 
        try:
            notes = note_data[category]
        except:
            notes = []

        if len(content) > 0:
            note = [' '.join(content)]
            notes.append(note)

        else:
            print('')
            note = []
            while True:
                line = input(' > ')
                note.append(line)
                if line == '':
                    break
            note = note[:-1]
            notes.append(note)

        note_data[category] = notes
        with open(file, 'w') as f:
            json.dump(note_data, f)
        print(bold + blue + '\n Note saved to ' + category + '\n')

def NoteCategories(note_data):
    print('\n ' + red + underline + bold + 'Notes categories:\n' + normal)
    for i, category in enumerate(note_data):
        print(' ' + blue + bold + str(i + 1) + '. ' + normal + category)
    print('')

def ListNotes(category, note_data):
    if category == None:
        return

    try:
        if len(note_data[category]) > 0:
            print('\n ' + bold + red + underline + category + ' notes\n' + normal)
            for i, note in enumerate(note_data[category]):
                print(' ' + bold + blue + str(i + 1) + '. ' + normal + (bold + '\n |  ' + normal).join(note))
            print('')

    except:
        print(bold + red + '\n Note category not found\n')

def DeleteNote(category, index, file, note_data):
    try:
        note_data[category].remove(note_data[category][int(index) - 1])

        if len(note_data[category]) == 0:
            del note_data[category]

        with open(file, 'w') as f:
            json.dump(note_data, f)
        
        print('\n' + red + bold + ' Note removed\n')

    except:
        if not category in note_data:
            error = category + ' is not a valid note category'

        elif not index.isdigit():
            error = 'Please enter a valid index number'

        else:
            error = category + ' only contains ' + str(len(note_data[category])) + ' notes'

        print('\n ' + bold + red + error + '\n')

def EditNote(category, index, file, note_data):
    print('')

    try:
        note = note_data[category][int(index) - 1]

        for i in range(len(note)):
            readline.set_startup_hook(lambda: readline.insert_text(note[i]))

            try:
                new_line = input(' > ')
            finally:
                readline.set_startup_hook()

            note[i] = new_line

        while True:
            line = input(' > ')
            if line == '':
                break
            note.append(line)

        with open(file, 'w') as f:
            json.dump(note_data, f)
        print(bold + blue + '\n Note saved to ' + category + '\n')

    except Exception as e:
        if not category in note_data:
            error = category + ' is not a valid note category'

        elif not index.isdigit():
            error = 'Please enter a valid index number'

        else:
            error = category + ' only contains ' + str(len(note_data[category])) + ' notes'
            #print(e)

        print('\n ' + bold + red + error + '\n')
