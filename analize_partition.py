import os
import sys


def get_extension(file_name):
    base_name = os.path.basename(file_name)
    dot_pos = base_name.rfind(".")

    if dot_pos == -1:
        return "<no-ext>"

    ext = base_name[dot_pos + 1:]
    if ext == "":
        return "<no-ext>"

    return ext.lower()


def scan_partition(root_path):
    total_dirs = 0
    total_files = 0

    # dictionar: extensie -> {"count": numar_fisiere, "size": dimensiune_totala}
    stats_by_ext = {}

    for current_root, dir_names, file_names in os.walk(root_path):
        total_dirs += len(dir_names)
        for file_name in file_names:
            total_files += 1

            full_path = os.path.join(current_root, file_name)

            # incercam sa obtinem dimensiunea fisierului
            try:
                file_size = os.path.getsize(full_path)
            except OSError:
                file_size = 0

            ext = get_extension(file_name)

            if ext not in stats_by_ext:
                stats_by_ext[ext] = {"count": 0, "size": 0}

            stats_by_ext[ext]["count"] += 1
            stats_by_ext[ext]["size"] += file_size

    return total_dirs, total_files, stats_by_ext


def print_results(total_dirs, total_files, stats_by_ext):
    print("=== Rezultate scanare partitie ===")
    print("Total directoare :", total_dirs)
    print("Total fisiere    :", total_files)
    print()

    print("Statistici pe extensii:")
    print("Extensie | Numar fisiere | Dimensiune totala (bytes)")
    print("-" * 60)

    # sortam dupa numele extensiei, ca sa fie mai usor de citit
    for ext in sorted(stats_by_ext.keys()):
        info = stats_by_ext[ext]
        print("%-8s | %13d | %21d" % (ext, info["count"], info["size"]))


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
