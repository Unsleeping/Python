# coding: utf-8

import os
import sys
import psutil
import shutil


def duplicate_file(filename):
    if os.path.isfile(filename):
        newfile = filename + '.dupl'  # to concat
        shutil.copy(filename, newfile)
        if os.path.exists(newfile):
            print('</> File ', newfile, ' created successfully')
            return True
        else:
            print('</> Oh, some copy error')
            return False


def del_duplicates(dirname):
    file_list = os.listdir(dirname)
    dupl_count = 0
    for f in file_list:
        fullname = os.path.join(dirname, f)  # \ /
        if fullname.endswith('.dupl'):
            os.remove(fullname)
            if not os.path.exists(fullname):
                dupl_count += 1
                print('</> File ', fullname, ' removed successfully')
    return dupl_count




def sys_info():
    print('</> So I know this info about your system: ')
    print('</> Number of processes: ', psutil.cpu_count())
    print('</> The platform: ', sys.platform)
    print('</> The system encoding: ', sys.getfilesystemencoding())
    print('</> Current directory: ', os.getcwd())


print('</> Hello, my name is bot Jack and I am your computer assistant')
answer = ''

while answer != 'q':
    answer = input('</> Would u like to know smth new about your system? (y/n/q)')
    if answer == 'y':
        print('</> Alright')
        print('</> I can do that:')
        print('-->  [1] - display the file list')
        print('-->  [2] - display the system information')
        print('-->  [3] - display the processes list')
        print('-->  [4] - make duplicates in current directory')
        print('-->  [5] - make duplicate of the select file')
        print('-->  [6] - delete duplicates in current directory')
        do = int(input('</> Select the option: '))

        if do == 1:
            print(os.listdir())

        elif do == 2:
            sys_info()

        elif do == 3:
            print(psutil.pids())

        elif do == 4:
            print('</> Making some magic with duplications in current directory..')
            file_list = os.listdir()
            i = 0
            while i < len(file_list):
                duplicate_file(file_list[i])
                i += 1

        elif do == 5:
            print('</> Making some magic with duplication of the select file in current directory..')
            filename = input('</> Input the file name u want to duplicate: ')
            duplicate_file(filename)

        elif do == 6:
            print('</> Making some magic with removing duplications in current directory..')
            dirname = input('</> Input the directory name: ')
            count = del_duplicates(dirname)
            print('--> Number of removed duplicates: ', count)

        else:
            pass
