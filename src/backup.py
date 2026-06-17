import os
from duplicates import calculate_md5


def get_folder_manifest(target_path):
    """Собирает манифест папки в формате {относительный_путь: md5_хэш}."""
    manifest = {}
    for root, dirs, files in os.walk(target_path):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                rel_path = os.path.relpath(full_path, target_path)
                md5_hash = calculate_md5(full_path)
                if md5_hash:
                    manifest[rel_path] = md5_hash
            except Exception:
                continue
    return manifest


def compare_with_backup(source_path, backup_path):
    """Сравнивает исходную папку с бэкапом и выводит разницу."""
    print(f"\nЗапуск сравнения с резервной копией...")
    print(f"Оригинал: {os.path.abspath(source_path)}")
    print(f"Бэкап:   {os.path.abspath(backup_path)}")

    # Собираем данные о файлах в обеих папках
    source_manifest = get_folder_manifest(source_path)
    backup_manifest = get_folder_manifest(backup_path)

    missing_files = []  # Есть в оригинале, но нет в бэкапе (отсутствующие)
    modified_files = []  # Есть и там, и там, но отличаются (измененные)
    extra_files = []  # Нет в оригинале, но есть в бэкапе (лишние)

    # Проверяем файлы из оригинальной папки
    for rel_path, source_hash in source_manifest.items():
        if rel_path not in backup_manifest:
            missing_files.append(rel_path)
        elif source_hash != backup_manifest[rel_path]:
            modified_files.append(rel_path)

    # Проверяем бэкап на наличие лишних файлов
    for rel_path in backup_manifest:
        if rel_path not in source_manifest:
            extra_files.append(rel_path)

    # Красивый вывод результатов
    print(f"\n{'=' * 20} РЕЗУЛЬТАТЫ СРАВНЕНИЯ БЭКАПА {'=' * 20}")

    if not missing_files and not extra_files and not modified_files:
        print("✔ Резервная копия полностью идентична оригинальной папке!")
        print("=" * 69)
        return

    if missing_files:
        print(f"\n❌ ОТСУТСТВУЮТ В БЭКАПЕ (нужно докопировать): {len(missing_files)}")
        for f in missing_files:
            print(f"  -> {f}")

    if modified_files:
        print(f"\n⚠ ИЗМЕНЕНЫ (содержимое отличается от оригинала): {len(modified_files)}")
        for f in modified_files:
            print(f"  -> {f}")

    if extra_files:
        print(f"\n➕ ЛИШНИЕ В БЭКАПЕ (нет в оригинале, можно удалить): {len(extra_files)}")
        for f in extra_files:
            print(f"  -> {f}")

    print("=" * 69)