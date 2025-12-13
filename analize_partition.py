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

    stats_by_ext = {}

    for current_root, dir_names, file_names in os.walk(root_path):
        total_dirs += len(dir_names)

        for file_name in file_names:
            total_files += 1

            full_path = os.path.join(current_root, file_name)

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


def compute_ext_stats(stats_by_ext):
    total_files = 0
    total_size = 0

    for info in stats_by_ext.values():
        total_files += info["count"]
        total_size += info["size"]

    ext_stats = []

    for ext, info in stats_by_ext.items():
        count = info["count"]
        size = info["size"]

        if total_files > 0:
            pct_count = count * 100.0 / total_files
        else:
            pct_count = 0.0

        if total_size > 0:
            pct_size = size * 100.0 / total_size
        else:
            pct_size = 0.0

        ext_stats.append(
            {
                "ext": ext,
                "count": count,
                "size": size,
                "pct_count": pct_count,
                "pct_size": pct_size,
            }
        )

    return ext_stats, total_files, total_size


def add_other_bucket(sorted_list, total_files, total_size, max_types=10):
    if len(sorted_list) <= max_types:
        return sorted_list

    main_list = sorted_list[:max_types]
    other_list = sorted_list[max_types:]

    other_count = 0
    other_size = 0

    for entry in other_list:
        other_count += entry["count"]
        other_size += entry["size"]

    if other_count == 0 and other_size == 0:
        return main_list

    if total_files > 0:
        other_pct_count = other_count * 100.0 / total_files
    else:
        other_pct_count = 0.0

    if total_size > 0:
        other_pct_size = other_size * 100.0 / total_size
    else:
        other_pct_size = 0.0

    main_list.append(
        {
            "ext": "Other",
            "count": other_count,
            "size": other_size,
            "pct_count": other_pct_count,
            "pct_size": other_pct_size,
        }
    )

    return main_list


def print_table(title, rows):
    print(title)
    print("Extensie | Fisiere | % numar | Dimensiune (bytes) | % dimensiune")
    print("-" * 80)

    for entry in rows:
        print(
            "%-8s | %7d | %7.2f | %17d | %11.2f"
            % (
                entry["ext"],
                entry["count"],
                entry["pct_count"],
                entry["size"],
                entry["pct_size"],
            )
        )
    print()


def print_results(total_dirs, total_files, stats_by_ext):
    ext_stats, total_files_checked, total_size = compute_ext_stats(stats_by_ext)
    print()
    print("Total directoare :", total_dirs)
    print("Total fisiere    :", total_files)
    print("Dimensiune totala (bytes):", total_size)
    print()

    # sortam dupa numar de fisiere
    by_count = sorted(ext_stats, key=lambda e: e["count"], reverse=True)
    by_count = add_other_bucket(by_count, total_files_checked, total_size)

    # sortam dupa dimensiune totala
    by_size = sorted(ext_stats, key=lambda e: e["size"], reverse=True)
    by_size = add_other_bucket(by_size, total_files_checked, total_size)

    print_table("Top extensii dupa numar de fisiere:", by_count)
    print_table("Top extensii dupa dimensiune totala:", by_size)


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
