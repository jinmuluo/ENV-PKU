# read me
# this python file is use to find the clusted data set below address, and the address is root dir,
# every files below the address will be find, you should know this function can't discriminate the different files
# address like 'C:/you/and/me/'
import os


def find_file(dir, suffix):
    file_name = list()
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file[-len(suffix):] == suffix:
                file_name.append(os.path.join(root, file))
        for dir in dirs:
            find_file(dir, suffix)
    return(file_name)

