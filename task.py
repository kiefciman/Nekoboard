from text_format import *
import os
import json
import readline
import datetime

def Task(arg, path):
    file = os.path.join(path[0], path[1][1])

    with open(file, 'r') as f:
        try:
            task_data = json.load(f)
        except:
            task_data = {}

    if len(arg) == 2:
        TaskUsage()
        return

    match arg[2].lower():
        case 'add' | 'new':
            try:
                AddTask(arg[3], arg[4], arg[5], arg[6:], file, task_data)
            except Exception as e:
                TaskUsage()
                #print(e)

        case 'categories' | 'cat':
            try:
                TaskCategories(task_data)
            except Exception as e:
                TaskUsage()
                #print(e)

        case 'list' | 'ls':
            try:
                ListTasks(arg[3:7], task_data)
            except Exception as e:
                TaskUsage()
                #print(e)

        case 'delete' | 'del' | 'remove' | 'rm':
            try:
                DeleteTask(arg[3], arg[4], file, task_data)            
            except Exception as e:
                TaskUsage()
                #print(e)

        case 'edit' | 'ed':
            try:
                EditTask(arg[3], arg[4], file, task_data)
            except Exception as e:
                TaskUsage()
                #print(e)

        case 'state' | 'stat' | 'st':
            try:
                TaskState(arg[3], arg[4], arg[5], file, task_data)
            except Exception as e:
                TaskUsage()
                #print(e)

        case 'toggle' | 'tog' | 'tg':
            try:
                ToggleTask(arg[3], arg[4], file, task_data)
            except Exception as e:
                TaskUsage()
                #print(e)

        case _:
            TaskUsage()

def TaskUsage():
    taskusage = [
        ['add/new {from-date} {until-date} {category} {task}', 'add new {task} to {category} that must be done between {from-date} and {until-date}, {from-date} and {until-date} are optional'],
        ['categories/cat', 'list all task categories'],
        ['list/ls {category} {state} {from-date} {until-date}', 'list tasks from {category} matching {state} between {from-date} and {until-date}, {state} {from-date} and {until-date} are optional'],
        ['delete/del/remove/rm {category} {index}', 'delete task no. {index} from {category}'],
        ['edit/ed {category} {index}', 'edit note no. {index} from {category}'],
        ['state/stat/st {category} {index} {state}', 'changes the state of task no. {index} from {category} to {state}'],
        ['toggle/tog/tg {category}, {index}', 'toggles the state of task no. {index} from {category} between todo and done'],
    ]

    print('\n ' + red + underline + bold + 'Nekoboard tasks\n' + normal)
    for line in taskusage:
        print(bold + ' - ' + blue + line[0] + ': ' + normal + line[1])
    print(bold + ' - ' + normal + 'use' + bold + blue + ' . ' + normal + 'as wildcard for arguments(except when adding tasks), ex: "task ls . done . tomorrow", "task ls important . . 7d", if no argument would follow the ., the . is not required, ex: "task ls quick"\n')

def AddTask(from_date, until_date, category, content, file, task_data):
    today = datetime.date.today()
    error = ''
    start_date_err = bold + red + '\n Start date format: +/- number d/m/y (day/month/year), ex: +1d, -3m, or today/tomorrow/yesterday'
    end_date_err = bold + red + '\n End date format: +/- number d/m/y (day/month/year), ex: +1d, -3m, or today/tomorrow/yesterday'
    task = {}
    
    try:
        tasks = task_data[category]
    except:
        tasks = []


    task['name'] = ' '.join(content)
    tasks.append(task)

    match from_date:
        case 'today':
            start_date = today
        case 'tomorrow':
            start_date = today + datetime.timedelta(days = 1)
        case 'yesterday':
            start_date = today - datetime.timedelta(days = 1)
        case '.':
            start_date = 'None'
        case _:
            if not from_date[1:-1].isdigit():
                error += start_date_err

            match from_date[-1]:
                # TODO NEXT RELEASE: add week, month, year
                case 'd':
                    time_to_add = int(from_date[1:-1])
                    match from_date[0]:
                        case '+':
                            start_date = today + datetime.timedelta(days = time_to_add)
                        case '-':
                            start_date = today - datetime.timedelta(days = time_to_add)
                        case _:
                            error += start_date_err

                case _:
                    error += start_date_err
            
    #TODO NEXT RELEASE: add insert date support
    if not error == start_date_err:
        if start_date == 'None':
            task['start'] = 'None'
        else:
            task['start'] = start_date.strftime(dateformat)

    match until_date:
        case 'today':
            end_date = today
        case 'tomorrow':
            end_date = today + datetime.timedelta(days = 1)
        case 'yesterday':
            end_date = today - datetime.timedelta(days = 1)
        case '.':
            end_date = 'None'
        case _:
            if not until_date[1:-1].isdigit():
                error = end_date_err

            match until_date[-1]:
                case 'd':
                    time_to_add = int(until_date[1:-1])

                    match until_date[0]:
                        case  '+':
                            end_date = today + datetime.timedelta(days = time_to_add)
                        case '-':
                            end_date = today - datetime.timedelta(days = time_to_add)
                        case _:
                            error += end_date_err

                case _:
                    error += end_date_err
                     
    if not error == end_date_err:
        if end_date == 'None':
            task['end'] = 'None'
        else:
            task['end'] = end_date.strftime(dateformat)

    task['state'] = 'todo'

    if not error == '':
        print(error + '\n')

    else:
        task_data[category] = tasks
        with open(file, 'w') as f:
            json.dump(task_data, f) 
        print('\n ' + bold + blue + 'Task added to ' + category + '\n')

def TaskCategories(task_data):
    task_categories = []

    print('\n ' + red + bold + underline + 'Tasks categories:' + normal + '\n')

    for category in task_data:
        task_categories.append(category)

    for i in range(len(task_categories)):
        print(' ' + blue + bold + str(i + 1) + '. ' + normal + task_categories[i])
    print('')

def ListTasks(args, task_data):
    category = args[0]
    tasks = []

    if category == None:
        return

    if len(args) > 1:
        state = args[1]
    else:
        state = '.'

    if len(args) > 2:
        from_date = args[2]
    else:
        from_date = '.'


    if len(args) > 3:
        until_date = args[3]
    else:
        until_date = '.'
 
    try:
        if len(task_data[category]) <= 0:
            return

        print('\n ' + red + underline + bold + category + ' tasks\n' + normal)

        for cat in task_data:
            if not cat == category:
                return

            for i, task in enumerate(task_data[cat]):
                formatted_task = task['name']

                if not task['start'] == 'None':
                    formatted_task += bold + ' from: ' + normal + task['start']
                if not task['end'] == 'None':
                    formatted_task += bold + ' until: ' + normal + task['end']

                output = ' ' + blue + bold + str(i + 1) + '. ' + normal + formatted_task

                if not state == '.':
                    if task['state'] == state:
                        print(output)
                else:
                    print(output + bold + ' state: ' + normal + task['state'])

        print('')
    except:
        print(bold + red + '\n Todo category not found\n')


def DeleteTask(category, index, file, task_data):
    try:
        task_data[category].remove(task_data[category][int(index) - 1])

        if len(task_data[category]) == 0:
            del task_data[category]

        with open(file, 'w') as f:
            json.dump(task_data, f)

        print('\n ' + red + bold + 'Task removed\n')

    except:
        if not category in task_data:
            error = category + ' is not a valid note category'

        elif not index.isdigit():
            error = 'Please enter a valid index number'

        else:
            error = category + ' only contains ' + str(len(task_data[category])) + ' notes'

        print('\n ' + bold + red + error + '\n')

def EditTask(category, index, file, task_data):
    print('')

    try:
        task = task_data[category][int(index) - 1]
        for i in task:
            readline.set_startup_hook(lambda: readline.insert_text(task[i]))
            try:
                new_line = input(' ' + bold + i + normal + ' > ')
            finally:
                readline.set_startup_hook()

            task[i] = new_line

        print('')

        with open(file, 'w') as f:
            json.dump(task_data, f)
        #TODO NEXT RELEASE: add proper date changing

    except:
        if not category in task_data:
            error = category + ' is not a valid task category'

        elif not index.isdigit():
            error = 'Please enter a valid index number'

        else:
            error = category + ' only contains ' + str(len(task_data[category])) + ' tasks'

        print('\n ' + bold + red + error + '\n')

def TaskState(category, index, state, file, task_data):
    try:
        task = task_data[category][int(index) - 1]
        task['state'] = state

        with open(file, 'w') as f:
            json.dump(task_data, f)

        print('\n ' + red + bold + 'Task state changed to ' + state + '\n')

    except:
        if not category in task_data:
            error = category + ' is not a valid task category'

        elif not index.isdigit():
            error = 'Please enter a valid index number'

        else:
            error = category + ' only contains ' + str(len(task_data[category])) + ' tasks'

        print('\n ' + bold + red + error + '\n')

def ToggleTask(category, index, file, task_data):
    try:
        task = task_data[category][int(index) - 1]
        state = task['state']
        state_changed = False

        match state:
            case 'todo':
                new_state = 'done'
                state_changed = True
            case 'done':
                new_state = 'todo'
                state_changed = True
            case _:
                print('\n ' + red + bold + 'You can only toggle between todo and done\n')

        if state_changed:
            #note: changing the state directly does not modiy the json
            task['state'] = new_state

            with open(file, 'w') as f:
                json.dump(task_data, f)

            print('\n ' + red + bold + 'Task state changed to ' + new_state + '\n')

    except:
        if not category in task_data:
            error = category + ' is not a valid task category'

        elif not index.isdigit():
            error = 'Please enter a valid index number'

        else:
            error = category + ' only contains ' + str(len(task_data[category])) + ' tasks'

        print('\n ' + bold + red + error + '\n')

