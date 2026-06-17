import argparse
import os
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Консольный индексатор папок (Упрощенный вариант)"
    )
    parser.add_argument(
        "path",
        type=str,
        help="Путь к папке, которую необходимо просканировать"
    )

    args = parser.parse_args()
    target_path = args.path

    if not os.path.exists(target_path):
        print(f"Ошибка: Указанный путь '{target_path}' не существует.", file=sys.stderr)
        sys.exit(1)

    if not os.path.isdir(target_path):
        print(f"Ошибка: Указанный путь '{target_path}' не является папкой.", file=sys.stderr)
        sys.exit(1)

    absolute_path = os.path.abspath(target_path)
    print(f"Целевая папка для сканирования: {absolute_path}")

if __name__ == "__main__":
    main()