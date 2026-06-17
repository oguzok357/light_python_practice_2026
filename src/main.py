import argparse
import os
import sys
from scanner import scan_folder
from duplicates import find_duplicates
from backup import compare_with_backup


def main():
    parser = argparse.ArgumentParser(
        description="Консольный индексатор папок (Упрощенный вариант)"
    )
    parser.add_argument(
        "path",
        type=str,
        help="Путь к оригинальной папке для сканирования"
    )
    # Добавляем необязательный флаг --backup или -b
    parser.add_argument(
        "--backup", "-b",
        type=str,
        help="Путь к папке резервной копии для сравнения"
    )

    args = parser.parse_args()
    target_path = args.path

    # Валидация основной папки
    if not os.path.exists(target_path) or not os.path.isdir(target_path):
        print(f"Ошибка: Исходный путь '{target_path}' не существует или не является папкой.", file=sys.stderr)
        sys.exit(1)

    # Валидация папки бэкапа (если она передана)
    if args.backup:
        if not os.path.exists(args.backup) or not os.path.isdir(args.backup):
            print(f"Ошибка: Путь бэкапа '{args.backup}' не существует или не является папкой.", file=sys.stderr)
            sys.exit(1)

    print(f"Целевая папка для сканирования: {os.path.abspath(target_path)}")

    # 1. Сканирование папки
    print("\nЗапуск сканирования директории...")
    scan_folder(target_path)
    print("\nСканирование успешно завершено!")

    # 2. Поиск дубликатов
    print("\nПоиск дубликатов файлов...")
    find_duplicates(target_path)

    # 3. Сравнение с бэкапом (выполняется только если передан флаг -b)
    if args.backup:
        compare_with_backup(target_path, args.backup)


if __name__ == "__main__":
    main()