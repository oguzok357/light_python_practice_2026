import hashlib
import os


def calculate_md5(file_path):
    """Вычисляет хэш-сумму MD5 для файла (читает его блоками, чтобы не забивать память)."""
    hasher = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            # Читаем файл кусками по 4 КБ
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return None


def find_duplicates(target_path):
    """Ищет дубликаты файлов по размеру и MD5 хэшу."""
    # Словарь, где ключ — (размер, md5_хэш), а значение — список путей к файлам
    files_registry = {}

    for root, dirs, files in os.walk(target_path):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                size = os.path.getsize(full_path)
                # Чтобы не считать хэш для пустых файлов, их можно пропускать,
                # но для точности посчитаем для всех
                md5_hash = calculate_md5(full_path)

                if md5_hash is None:
                    continue

                # Ключ уникальности файла — это его размер + хэш содержимого
                file_key = (size, md5_hash)

                if file_key not in files_registry:
                    files_registry[file_key] = []

                # Сохраняем относительный путь
                rel_path = os.path.relpath(full_path, target_path)
                files_registry[file_key].append(rel_path)
            except Exception:
                continue

    # Фильтруем словарь: оставляем только те ключи, где файлов больше 1 (т.е. есть дубликаты)
    duplicates = {key: paths for key, paths in files_registry.items() if len(paths) > 1}

    # Выводим результат
    if not duplicates:
        print("\nДубликаты файлов не найдены.")
    else:
        print(f"\n{'=' * 20} НАЙДЕНЫ ДУБЛИКАТЫ ФАЙЛОВ {'=' * 20}")
        group_number = 1
        for (size, md5_hash), paths in duplicates.items():
            print(f"\nГруппа {group_number} (Размер: {size} Байт, MD5: {md5_hash}):")
            for path in paths:
                print(f"  -> {path}")
            group_number += 1
        print("=" * 66)