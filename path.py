import os

def Path():
    data_path = os.path.expanduser('~/.config/nekoboard')
    files = ['note.json', 'task.json', 'journal.json', 'project.json', 'money.json']

    if not os.path.isdir(data_path):
        os.makedirs(data_path)
    
    for file in files:
        new_file = os.path.join(data_path, file)

        if not os.path.isfile(new_file):
            with open(new_file, 'w') as f:
                f.write('')

    return [data_path, files]
