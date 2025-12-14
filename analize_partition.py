import os
import sys

from core_stats import scan_partition, print_results


def show_usage():
    print("Utilizare:")
    print("  python analize_partition.py <cale_sau_partitie>")
    print()
    print("Exemple:")
    print("  python analize_partition.py D:")
    print("  python analize_partition.py C:\\Users\\Nume")


def main():
    if len(sys.argv) != 2:
        show_usage()
        return

    root_path = sys.argv[1]

    if not root_path.strip():
        print("Eroare: calea primita este goala.")
        show_usage()
        return

    if not os.path.exists(root_path):
        print("Eroare: calea nu exista:", root_path)
        return

    if not os.path.isdir(root_path):
        print("Avertisment: calea nu este un director. Se va incerca scanarea oricum.")

    try:
        total_dirs, total_files, stats_by_ext, skipped_dirs, skipped_files = scan_partition(root_path)
    except Exception as e:
        print("Eroare neasteptata in timpul scanarii:", e)
        return

    print_results(total_dirs, total_files, stats_by_ext, skipped_dirs, skipped_files)


if __name__ == "__main__":
    main()
