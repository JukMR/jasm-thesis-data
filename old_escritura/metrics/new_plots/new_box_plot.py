from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np


class BoxplotGenerator:
    @staticmethod
    def generate_separate_boxplots(data: Dict[Path, np.ndarray], output_filename: Path) -> None:
        fig, axs = plt.subplots(1, len(data), figsize=(15, 5), sharey=True)
        for ax, (method, times) in zip(axs, data.items()):
            ax.boxplot(times, patch_artist=True)
            ax.set_title(method.stem.replace("_execution_times", ""))
        fig.text(0.04, 0.5, "Time in Seconds", va="center", rotation="vertical")
        plt.savefig(output_filename)
        plt.close()

    @staticmethod
    def generate_combined_boxplot(data: Dict[Path, np.ndarray], output_filename: Path) -> None:
        plt.figure(figsize=(10, 6))
        # Prepare data and labels for plotting
        times = list(data.values())
        labels = [path.stem.replace("_execution_times", "") for path in data.keys()]
        plt.boxplot(times, labels=labels, patch_artist=True)
        plt.title("List Appending vs ByteArray Extend")
        plt.ylabel("Time in Seconds")
        plt.savefig(output_filename)
        plt.close()

    @staticmethod
    def generate_boxplot(times: List[float], filename: Path, title: str = "Execution Time Boxplot") -> None:
        plt.figure(figsize=(10, 6))
        plt.boxplot(times, vert=True, patch_artist=True)
        plt.title(title)
        plt.ylabel("Time in seconds")
        plt.savefig(filename)
        plt.close()


def generate_boxplots(paths: List[Path], output_filename: Path) -> None:
    execution_times: Dict[Path, np.ndarray] = {}
    statistics: Dict[Path, Tuple[float, float]] = {}

    for filepath in paths:
        times = read_execution_times_from_file(filepath)
        execution_times[filepath] = times
        statistics[filepath] = calculate_statistics(times)

    for filepath, (avg, std) in statistics.items():
        print(f"{filepath} - Average: {avg:.6f}, Std Dev: {std:.6f}")

    if len(paths) > 1:
        BoxplotGenerator.generate_combined_boxplot(execution_times, output_filename)
    else:
        execution_time = list(execution_times.values())[0]
        title = paths[0].stem.replace("_execution_times", "")
        BoxplotGenerator.generate_boxplot(execution_time, output_filename, title=title)


def read_execution_times_from_file(filename: Path) -> np.ndarray:
    with open(filename, "r", encoding="utf-8") as f:
        times = [float(line.strip()) for line in f.readlines() if line.strip()]
    return np.array(times)


def calculate_statistics(times: np.ndarray) -> Tuple[float, float]:
    avg = np.mean(times)
    std_dev = np.std(times)
    return avg, std_dev


def get_execution_times_file_from_folder(folder: Path) -> Path:
    for filepath in folder.iterdir():
        if str(filepath).endswith("execution_times.txt"):
            return filepath
    raise FileNotFoundError("File not found")


def main() -> None:

    project_folder = Path(__file__).parent
    assert project_folder.exists(), "Project folder not found"

    result_folder = project_folder / "results"
    assert result_folder.exists(), "Folder not found"

    string_concat_folder_path = result_folder / "string_execution"
    assert string_concat_folder_path.exists(), "Folder not found"

    list_execution_folder_path = result_folder / "list_execution"
    assert list_execution_folder_path.exists(), "Folder not found"

    bytearray_folder_path = result_folder / "bytearray"
    assert bytearray_folder_path.exists(), "Folder not found"

    string_concat_path = get_execution_times_file_from_folder(string_concat_folder_path)
    list_execution_path = get_execution_times_file_from_folder(list_execution_folder_path)
    bytearray_path = get_execution_times_file_from_folder(bytearray_folder_path)

    assert string_concat_path.exists(), "File not found"
    assert list_execution_path.exists(), "File not found"
    assert bytearray_path.exists(), "File not found"

    graphs_folder = project_folder / "graphs"
    graphs_folder.mkdir(exist_ok=True, parents=True)

    string_method = [string_concat_path]
    generate_boxplots(string_method, graphs_folder / "string_concat.png")

    paths = [list_execution_path, bytearray_path]
    generate_boxplots(paths, graphs_folder / "combined_boxplot_faster.png")


if __name__ == "__main__":
    main()
