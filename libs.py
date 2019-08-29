import os

def go(directory):
    directory = clean_dir(directory)
    os.chdir(directory)

def clean_dir(directory):
    cleaned_directory = ''
    for letter in directory:
        if letter == '/':
            cleaned_directory += '\\'
        else:
            cleaned_directory += letter

    return cleaned_directory

def copy_dir(dir_home, dir_target):
    os.chdir(dir_home)

    dir_home = clean_dir(dir_home)
    dir_target = clean_dir(dir_target)
    
    for root, dirs, files in os.walk("."):
        for filename in files:
            os.popen('copy ' + dir_home + '\\' + filename + ' ' + dir_target)

def copy_files(dir_home, dir_target, files):
    os.chdir(dir_home)

    dir_home = clean_dir(dir_home)
    dir_target = clean_dir(dir_target)
    
    for root, dirs, archives in os.walk("."):
        for filename in archives:
            if filename in files:
                os.popen('copy ' + dir_home + '\\' + filename + ' ' + dir_target)

def remove_all_files(directory):
    os.chdir(directory)
    for root, dirs, archives in os.walk("."):
        for filename in archives:
            if root == ".":
                os.remove(filename)
            

def remove_files(directory, files):
    cwd = os.getcwd()
    directory = clean_dir(directory)
    os.chdir(directory)

    for root, dirs, archives in os.walk("."):
        for filename in archives:
            if filename in files:
                os.remove(filename)

    go(cwd)

def remove_dir(directory):
    directory = clean_dir(directory)
    cwd = os.getcwd()

    os.chdir(directory)
    #Delete all folders in directory
    for root, dirs, archives in os.walk("."):
        if len(dirs) > 0:
            for folder_name in dirs:
                remove_dir(directory + "\\" + folder_name)

    #When all folders are deleted, delete all files
    remove_all_files(directory)
    
    #Delete folder
    folder_name_divided = directory.split('\\')
    folder_name_index = len(folder_name_divided) - 1
    folder_name = folder_name_divided[folder_name_index]
    folder_name_divided.pop(folder_name_index)
    
    folder_container = ''
    for i in range(len(folder_name_divided)):
        folder_container += folder_name_divided[i] + '\\'
    
    os.chdir(folder_container)
    os.rmdir(folder_name)

def create_files(n, directory, name, data, extension):
    cwd = os.getcwd()
    os.chdir(directory)

    if n == 1:
        file = open(name + '.' + extension, 'w+')
        if data != None:
            file.write(data)
        file.close()
    else: 
        for i in range(n):
            file = open(name + str(i) + '.' + extension, 'w+')
            if data != None:
                file.write(data)
            file.close()

    go(cwd)

def clean_name(name_):
    new_name = ''
    for letter in name_:
        if letter in '<>*:/|?\\"':
            if letter == ':':
                new_name += ';'
            else:
                new_name += "+"
        else:
            new_name += letter

    return new_name

def create_dir(n, directory, name):
    directory = clean_dir(directory)
    os.chdir(directory)
    
    if n == 1:
        if not os.path.isdir(directory + '\\' + name):
            os.mkdir(name)
    else:
        for i in range(n):
            if not os.path.isdir(directory + '\\' + name + str(i)):
                os.mkdir(name + str(i))

def hard_restart(msg):
    os.popen('shutdown /r /c ' + msg + ' /d 2:17')

def run(command):
    os.popen(command)