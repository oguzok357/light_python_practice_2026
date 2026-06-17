import os
import sys
from datetime import datetime


def scan_folder(target_path):
    """Рекурсивно обходит папку и выводит метаданные файлов."""
    print(f"\n{'Относительный путь':<60} | {'Размер (Байт)':<15} | {'Дата изменения':<20}")
    print("-" * 102)

    for root, dirs, files in os.walk(target_path):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                file_stats = os.stat(full_path)
                size = file_stats.st_size
                mod_time = datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                rel_path = os.path.relpath(full_path, target_path)

                print(f"{rel_path:<60} | {size:<15} | {mod_time:<20}")
            except Exception as e:
                print(f"Ошибка чтения файла {file}: {e}", file=sys.stderr)