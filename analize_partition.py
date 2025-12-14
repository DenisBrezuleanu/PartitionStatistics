import os
import sys

from core_stats import scan_partition, print_results


def main():
    if len(sys.argv) != 2:
        print("Utilizare:")
        print("  python analize_partition.py <cale_sau_partitie>")
        print()
        print("Exemple:")
        print("  python analize_partition.py D:")
        print("  python analize_partition.py C:\\Users\\Nume")
        return

    root_path = sys.argv[1]

    if not os.path.exists(root_path):
        print("Eroare: calea nu exista:", root_path)
        return

    total_dirs, total_files, stats_by_ext = scan_partition(root_path)
    print_results(total_dirs, total_files, stats_by_ext)


if __name__ == "__main__":
    main()
