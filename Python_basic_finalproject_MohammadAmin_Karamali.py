# modules
from shutil import rmtree
from shutil import copytree
import argparse
import os
import json
import sys
import datetime

# test path
# C:\\Users\\saraye tel\\Desktop\\Filoger\\test_file

# global variable
mv_variable = False


# setup function
def setup():
    # parser
    parser = argparse.ArgumentParser(description='Linux Command Line')
    # options
    # ls
    parser.add_argument('-ls', action='store_true', help='-ls: List Items in Directory')
    # change directory - cd
    parser.add_argument('-cd', action='store_true', help='-cd: Change Directory')
    # get current directory - pwd
    parser.add_argument('-pwd', action='store_true', help='-pwd: Show Current Directory')
    # cd ..
    parser.add_argument('-cd_dd', action='store_true', help='-cd_dd is cd .. ===> Go Back One Step!')
    # mkdir
    parser.add_argument('-mkdir', action='store_true', help='-mkdir: Create a New Directory')
    # rmdir
    parser.add_argument('-rmdir', action="store_true", help="-rmdir: Remove an EMPTY directory")
    # rm file
    parser.add_argument('-rm', action='store_true', help='-rm: Always use it with -file')
    # rm-r
    parser.add_argument('-rm-r', action='store_true', help='-rm-r: delete a file and its stored data')
    # cp
    parser.add_argument('-cp', action='store_true', help='-cp: Copy file or directory')
    # mv_variable
    parser.add_argument('-mv_variable', action='store_true', help='-mv_variable: Move a file or directory')
    # find
    parser.add_argument('-find', action='store_true', help="-find: Search for files or directories matching 'pattern' starting from 'path'")
    # cat
    parser.add_argument('-cat', action='store_true', help="-cat: Output the contents of the file 'file'")

    # variables
    # path
    parser.add_argument('-path', type=str, help='just a path')
    # change dir to a folder in current working directory
    parser.add_argument('-dir', type=str, help="-dir: Enter a folder which exists in CWD - NOTE: You must use -cd before using -dir")
    # file_name
    parser.add_argument('-file', type=str, help='path of the file to be removed | always use it with -rm')
    # source
    parser.add_argument('-src', type=str, help='Source Path')
    # destination
    parser.add_argument('-dest', type=str, help='Destination Path')
    # pattern
    parser.add_argument('-pattern', type=str, help='Patter for searching')

    # setting all the arguments
    args = parser.parse_args()
    return args


# ----------------------- ls -----------------------
# ls inner function
def ls_inner(path_):
    for path, dirs, files in os.walk(path_):
            print(f'Path: {path}\n')
            if len(files) != 0:
                print(f'Files:')
                for f in files:
                    print(f'>>> {f}')
                print()
            if len(dirs) != 0:
                print(f'Directories:')
                for d in dirs:
                    print(f">>> {d}")
            break

# ls function
def ls(path):
    if args.path == None:
        with open('dir.json', 'r') as f:
            r_file = json.load(f)
        ls_inner(r_file[-1])
    else:
        ls_inner(path)
    

# ----------------------- show current directory -----------------------
def pwd():
    with open('dir.json', 'r') as r_file:
        j_file = json.load(r_file)
    print(f'\nCurrent Directory: {j_file[-1]}')
    

# ----------------------- path validator -----------------------
def dir_validator(path):
    if path == None or path == '':
        return
    path_split = path.split('\\')
    back_slash = path.count('\\')
    if not(back_slash == len(path_split) - 1):
        print(back_slash, len(path_split))
        print('not enough \\ !!!')
        return False
    if '\\' not in path:
        print('not \\')
        return False
    if (':' not in path) or path.count(':') != 1:
        print("not ':' or more than one!!!")
        return False
    if not os.path.exists(path):
        return False
    return True


# ----------------------- directory saver -----------------------
def dir_saver(new_path):
    if dir_validator(new_path):
        # reading and loading data
        with open('dir.json', 'r') as r_file:
            j_file = json.load(r_file)
        # adding data
        j_file.append(new_path)
        # writing data on json file
        with open('dir.json', 'w') as w_file:
            json.dump(j_file, w_file)
        print('new path added :)')
        return
    print("path didn't add!")
    

# ----------------------- change directory, one step back -----------------------
def cd_double_dot():
    with open('dir.json', 'r') as f:
        data = json.load(f)
    data = data[-1]
    parent = os.path.abspath(os.path.join(data, os.pardir))
    if os.path.exists(parent):
        dir_saver(parent)
        print(f"Current Directory: {parent}")


# ----------------------- walking history -----------------------
def dir_hist():
    with open('dir.json', 'r') as f:
        print("\nChange Directory History")
        data = json.load(f)
    for i, d in enumerate(iterable, start)(data):
        print(f'{i}. {d}')
    print()


# ----------------------- change directory -----------------------
def change_dir(path, dir_):
    if dir_:
        dirs = []
        with open('dir.json', 'r') as f:
            latest_path = json.load(f)[-1]
        for p, d, f in os.walk(latest_path):
            for d_ in d:
                dirs.append(d_)
        if dir_ in dirs:
            new_path = os.path.join(latest_path, dir_)
            # new_path = Path(new_path)
            print(f'new path: {new_path}')
            if os.path.exists(new_path):
                dir_saver(new_path)
                print("Dir Changed :)")
                return
            else:
                print("Directory doesn't exist or you didn't go step by step! :(")
                return
        else:
            print("Directory doesn't exist! :(")
            return
    if path:
        os.chdir(path)
        print(f'\nCurrent Directory: {os.getcwd()}')


# ----------------------- make directory -----------------------
def mkdir_(path):
    # when path is entered
    if path:
        if not(os.path.exists(path)):
            if dir_validator(path):
                os.mkdir(path)
                # dir_saver(path)
                print('New directory created! :)')
                return
            else:
                print("This directory is not valid! :(")
                return
        else:
            print("This directory already exists! :(")
            return
    # when path is None
    else:
        with open('dir.json', 'r') as f:
            cwd = json.load(f)[-1]
        new_dir_name = input("Enter a name for your new directory: ")
        new_path = os.path.join(cwd, new_dir_name)
        if not(os.path.exists(new_path)):
            os.mkdir(new_path)
            # dir_saver(new_path)
            print('New directory created! :)')
            return
        else:
            print("This directory already exists! :(")
            return


# ----------------------- remove an empty path -----------------------
def rmdir(path):
    if path:
        if dir_validator(path):
            is_empty = os.listdir(path)
            if len(is_empty) == 0:
                os.rmdir(path)
                cd_double_dot()
                print("Dir removed! :)")
                return
            else:
                print("dir is not empty! :(")
                return
        else:
            print("dir is not valid! :(")
            return


# ----------------------- remove file -----------------------
def rm_file(file_):
    if not file_:
        print("You didn't entered a path so we use your current working directory. (use -pwd to check it)")
        # reading data
        with open('dir.json', 'r') as f:
            c_path = json.load(f)[-1]
        file_exist = False
        for root, dirs, files in os.walk(c_path):
            if len(files) != 0:
                files_len = len(files)
                file_exist = True
            for f in files:
                file_path = os.path.join(root, f)
        if file_exist:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print("File successfully removed! :)")
                return
        else:
            print('There is no file to remove! :(')
            return
    else:
        if dir_validator(file_):
            if os.path.isfile(file_):
                os.remove(file_)
                print("File successfully removed! :)")
                return
            else:
                print('Not a File Path! :(')
                return
        else:
            print('Not a Valid Path! :(')
            return


# ----------------------- remove a directory and all it countains -----------------------
def rm_r(dir_):
    global mv_variable
    if not mv_variable:
        user = input("This command will delete all entire files and folder in this directory.\nAre you sure? (y/n): ")
    else:
        user = 'y'
    if user == 'y':
        if dir_:
            if dir_validator(dir_):
                try:
                    if not mv_variable:
                        cd_double_dot()
                    rmtree(dir_)
                    if not mv_variable:
                        print("All files and folders and current directory deleted! :)")
                    return
                except:
                    print("Directory doesn't exist! :(")
        else:
            with open('dir.json', 'r') as f:
                cwd = json.load(f)[-1]
            try:
                if not mv_variable:
                    cd_double_dot()
                rmtree(cwd)
                if not mv_variable:
                    print("All files and folders and current directory deleted! :)")
                return
            except:
                print("Directory doesn't exist! :(")
    else:
        return


# ----------------------- copy a file or folder -----------------------
def cp(src, dest):
    global mv_variable
    is_file = lambda x : os.path.isfile(x)
    is_folder = lambda y : os.path.isdir(y)
    if is_file(src):
        try:
            with open(src, 'r') as f:
                data = f.read()
        except:
            print("File can't be read! :(")
            return
        try:
            file_name = os.path.basename(src)
            dest_file = os.path.join(dest, file_name)
            with open(dest_file, 'x') as w:
                w.write(data)
                print('file successfully copied! :)')
        except:
            print("Error file with the same name already exist! :(")
    # when src is a directory
    if is_folder(src):
        # or os.path.basename(src) == os.path.basename(dest)
        if src == dest:
            print("Error! source and destination are the same!!! :(")
            return
        src_files = []
        src_folders = []
        for root, folders, files in os.walk(src):
            # folders
            for folder in folders:
                src_folders.append(os.path.join(root, folder))
            # files
            for file_ in files:
                src_files.append(os.path.join(root, file_))
        # new file path based on destination
        dest_files = []
        for i in src_files:
            x = i.replace(src, dest)
            dest_files.append(x)
        # new folder path based on destination
        dest_folders = []
        for j in src_folders:
            y = j.replace(src, dest)
            dest_folders.append(y)
        # making directory based on destination
        try:
            for d in dest_folders:
                os.mkdir(d)
        except:
            if not mv_variable:
                print("this directory already exists! :(")
            return
        # copy files located on src and paste them on dest
        for f in range(len(src_files)):
            old_file = src_files[f]
            new_file = dest_files[f]
            try:
                with open(old_file, 'r') as o_file:
                    data = o_file.read()
                with open(new_file, 'x') as n_file:
                    n_file.write(data)
            except:
                print(f"file {new_file} already exist! :(")
                return


# ----------------------- cut a file or folder -----------------------
def mv(src, dest):
    global mv_variable
    mv_variable = True
    cp(src, dest)
    rm_r(src)
    print("move done!")


# ----------------------- cut a file or folder -----------------------
def cat(file_):
    if dir_validator(file_):
        if os.path.isfile(file_):
            try:
                with open(file_, 'r') as f:
                    data = f.read()
                print("Here is the result:\n" + ">"*30 + f" {os.path.basename(file_)} " + "<"*30)
                print(data)
                return
            except:
                print("File is not readable! :(")
                return
        else:
            print("Not a file path!!! :(")
            return
    else:
        print("Not a Valid File Path! :(")
        return


# ----------------------- cut a file or folder -----------------------
def search(path, pattern):
    search = False
    if dir_validator(path):
        folders_ = []
        files_ = []
        pattern_file = []
        pattern_folder = []
        for root, folders, files in os.walk(path):
            # folders
            for f in folders:
                folders_.append(os.path.join(root, f))
            # files
            for file_ in files:
                files_.append(os.path.join(root, file_))
        print(f"Pattern: {pattern}")
        print("Here are the result(s): \n")
        
        if os.path.isdir(path):
            for i in folders_:
                folder_name = os.path.basename(i)
                if pattern in folder_name:
                    pattern_folder.append(i)
                    search = True
        for j in files_:
            file_name = os.path.basename(j)
            if pattern in file_name:
                pattern_file.append(j)
                search = True
        
        if pattern_folder:
            print("="*30 + "Folders" + "="*30)
            for s in pattern_folder:
                print(s)
        
        if pattern_file:
            print("\n" + "="*30 + "Files" + "="*30)
            for js in pattern_file:
                print(js)
        
        if search:
            print("\nSearch is done!!! :)")
            return
        else:
            print("\nNothing Found! :(")
    else:
        print("\nInvalid Path! :(")
        return


# ----------------------- command.log | saving commands on a .log file -----------------------
def log_saver(sys_argv):
    argv = " ".join(sys_argv)
    with open('command.log', 'a') as f:
        time_now = datetime.datetime.now().strftime("%Y-%m-%d")
        f.write(f"{time_now}: {argv}\n")


# ----------------------------------------------------------------------------------------------------------------
# ------------------------------------------------  main program  ------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
args = setup()
print(f'\nArgs: {args}\n')

# sys.argv
sys_argv = sys.argv
log_saver(sys_argv)

if args.ls:
    ls(args.path)

# cd
if args.cd and dir_validator(args.path):
    change_dir(args.path, args.dir)

# cd and dir
if args.cd and args.dir and not args.path:
    change_dir(args.path, args.dir)

# pwd
if args.pwd:
    pwd()

# cd ..
if args.cd_dd:
    cd_double_dot()

# mkdir
if args.mkdir:
    mkdir_(args.path)
    
# rmdir path
if args.rmdir and args.path:
    rmdir(args.path)

# rm file
if args.rm:
    rm_file(args.file)

if args.rm_r:
    rm_r(args.dir)

if args.cp:
    cp(args.src, args.dest)

if args.mv_variable:
    mv(args.src, args.dest)

if args.cat:
    cat(args.file)

if args.find:
    search(args.path, args.pattern)
    