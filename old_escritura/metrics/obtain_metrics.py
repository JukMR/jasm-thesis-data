import subprocess
import time
from pathlib import Path
from typing import List

import numpy as np


def run_script(script_path: str, num_runs: int, args: List[str]) -> List[float]:
    times = []
    for _ in range(num_runs):
        start_time = time.time()
        subprocess.run(["python", script_path] + args, check=True)
        end_time = time.time()
        times.append(end_time - start_time)
    return times


def write_results_to_file(times: List[float], filename: Path) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        for res_time in times:
            f.write(f"{res_time}\n")


def calculate_std_dev(times: List[float]) -> float:
    return np.std(times)


def write_to_avg_std_to_res_file(avg: float, std: float, folder_path: Path) -> None:
    assert folder_path.exists(), "File not found"
    filepath = folder_path / "avg_and_std.txt"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("Results:\n")
        f.write(f"Average: {avg:.6f} seconds\n")
        f.write(f"Standard Deviation: {std:.6f} seconds\n")


def get_title() -> str:
    return "StringConcat"
    # return "ListAppending"
    # return "ByteArrayExtend"


def main() -> None:

    project_folder = Path(__file__).parent.parent / "asm_regex_tesis"

    assert project_folder.exists(), "Project folder not found"

    script_path = str(project_folder / "main.py")
    num_runs = 30

    results_folder = Path(__file__).parent / "results"
    results_folder.mkdir(exist_ok=True, parents=True)

    title = get_title()

    result_sub_folder_path = results_folder / title
    result_sub_folder_path.mkdir(exist_ok=True, parents=True)

    results_filename = result_sub_folder_path / f"{title}_execution_times.txt"

    yaml_file_pathstr = str(project_folder / "tests/yamls/function_return_0.yaml")
    binary_file_pathstr = str(project_folder / "tests/binary/bash.bin")

    args = ["-p", yaml_file_pathstr, "-b", binary_file_pathstr]
    execution_times = run_script(script_path, num_runs, args=args)

    write_results_to_file(execution_times, results_filename)
    std_dev = calculate_std_dev(execution_times)

    average_time = sum(execution_times) / len(execution_times)

    write_to_avg_std_to_res_file(avg=average_time, std=std_dev, folder_path=result_sub_folder_path)

    print(f"Average execution time: {average_time:.6f} seconds")
    print(f"Standard Deviation: {std_dev:.6f} seconds")


if __name__ == "__main__":
    main()
