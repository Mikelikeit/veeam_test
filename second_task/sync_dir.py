import os
import shutil
import argparse
import logging
import time


def sync_folders_and_files(path1, path2, log_path):
    # Функция выполняет синхронизацию каталого источник и каталога копия
    try:
        file_log = logging.FileHandler(f'{log_path}/sync_dir_log.log')
        console_out = logging.StreamHandler()
        logging.basicConfig(
            handlers=(file_log, console_out),
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s',
        )
        logging.info('Sync dir started')
        lst_path_original = []  # Список со всеми путями папки/файлы каталога источник
        lst_path_replica = []  # Список со всеми путями папки/файлы каталога копия
        for dir1, folders1, files1 in os.walk(path1):
            for folder1 in folders1:
                lst_path_original.append(os.path.join(dir1, folder1))
            for file1 in files1:
                lst_path_original.append(os.path.join(dir1, file1))

        for dir2, folders2, files2 in os.walk(path2):
            for folder2 in folders2:
                lst_path_replica.append(os.path.join(dir2, folder2))
            for file2 in files2:
                lst_path_replica.append(os.path.join(dir2, file2))
        # Проверка на наличие и создание папок/файлов в каталоге копия
        for path_dir1 in lst_path_original:
            if os.path.isdir(path_dir1) and not os.path.isdir(os.path.join(path_dir1).replace(path1, path2)):
                os.mkdir(os.path.join(path_dir1).replace(path1, path2))
                logging.info(f'Make directory {os.path.join(path_dir1).replace(path1, path2)}')
            if os.path.isfile(path_dir1) and not os.path.isfile(os.path.join(path_dir1).replace(path1, path2)):
                shutil.copy2(path_dir1, os.path.join(path_dir1).replace(path1, path2))
                logging.info(f'Copy file {os.path.join(path_dir1).replace(path1, path2)}')
            if os.path.isfile(path_dir1) and os.path.getmtime(path_dir1) != os.path.getmtime(
                    os.path.join(path_dir1).replace(path1, path2)):
                shutil.copy2(path_dir1, os.path.join(path_dir1).replace(path1, path2))
                logging.info(f'Copy file {os.path.join(path_dir1).replace(path1, path2)}')
        # Проверка на наличие папок/файлов в каталоге источник и удаление несоответсвий из каталога копия
        for path_dir2 in lst_path_replica:
            if os.path.isdir(path_dir2) and os.path.join(path_dir2).replace(path2, path1) not in lst_path_original:
                shutil.rmtree(path_dir2)
                logging.info(f'Remove directory {path_dir2}')

            if os.path.isfile(path_dir2) and os.path.join(path_dir2).replace(path2, path1) not in lst_path_original:
                os.remove(path_dir2)
                logging.info(f'Remove file {path_dir2}')

    except Exception as e:
        logging.debug(f'ERROR {e}')


def main():
    parser = argparse.ArgumentParser(description='Sync directories')
    parser.add_argument('original_dir', type=str, help='Input dir for original')
    parser.add_argument('replica_dir', type=str, help='Input dir for replica')
    parser.add_argument('loging_file_dir', type=str, help='Input dir for make logging_file')
    parser.add_argument('interval', type=float, help='Input time interval for sync in seconds')
    args = parser.parse_args()
    while True:
        sync_folders_and_files(args.original_dir, args.replica_dir, args.loging_file_dir)
        time.sleep(args.interval)


if __name__ == '__main__':
    main()
