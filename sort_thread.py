from threading import Thread
from pathlib import Path
import sys
import random
from time import time


EXT_DICT = {'images' : ('JPEG', 'PNG', 'JPG', 'SVG'),
            'video' : ('AVI', 'MP4', 'MOV', 'MKV'),
            'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLS', 'XLSX', 'PPTX'),
            'audio' : ('MP3', 'OGG', 'WAV', 'AMR'),
            'archives' : ('ZIP', 'GZ', 'TAR'),
            'unsorted': ''}

cash_extensions = {}
non_checked_folders = []    
sort_with_thread = True

def move_file_to_folder(file):
    """Переміщує файл згідно з EXT_DICT"""
    extension = Path(file).suffix.split('.')[-1]
    file_name = Path(file).name
    if extension in cash_extensions:
        new_path = Path.joinpath(cash_extensions[extension], file_name)
    else:
        new_path = Path.joinpath(cash_extensions['unsorted'], file_name)
    
    file.rename(new_path)
    

def sort_files(directory):
    '''Функція сортує файли по їх розширенню'''

    for file in directory.iterdir():
        if sort_with_thread:
            if file.is_dir():
                tread = Thread(target=sort_files, args=(file,))
            else:
                tread = Thread(target=move_file_to_folder, args=(file,))
            
            tread.run()
        else:
            if file.is_dir():
                sort_files(file)
            else:
                move_file_to_folder(file)
            

 

def main():
    if len(sys.argv) < 2:
        path = input("Please enter path to directory: ")
    else:
        path = sys.argv[1]
    directory = Path(path)
    if not directory.is_dir():
        print('Path incorrect')
        exit()

    for key, extensions in EXT_DICT.items():
        folder_name = Path.joinpath(directory, key)
        folder_name.mkdir(parents=True, exist_ok=True)
        non_checked_folders.append(folder_name)
        for extension in extensions:
            cash_extensions[extension] = folder_name
            
            
    folder_name = Path.joinpath(directory, 'unsorted')
    cash_extensions['unsorted'] = folder_name
    folder_name.mkdir(parents=True, exist_ok=True)
    non_checked_folders.append(folder_name)
        
    for i in range(100000):
        extension = random.choice(list(cash_extensions.keys()))
        if extension == 'unsorted':
            file = Path.joinpath(directory, '_' + str(i) + '.xyz')
        else:
            file = Path.joinpath(directory, '_' + str(i) + '.' + extension)
        file.touch(exist_ok=True)
        
    time_start = time()
    sort_files(directory)
    print(f'Time to sort files {time() - time_start}')


if __name__ == '__main__':
    exit(main())

