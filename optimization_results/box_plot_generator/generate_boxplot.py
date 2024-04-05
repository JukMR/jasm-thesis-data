from pathlib import Path
from typing import Any, TypeAlias

from matplotlib import pyplot as plt

PltObject: TypeAlias = Any  # this should be a plt object but i don't know how to import it


def box_plot_metrics(execution_times: list) -> None:
    # Generate the box plot
    plt.boxplot(execution_times, patch_artist=True, boxprops=dict(facecolor="lightblue"))
    plt.xlabel("Execution Time")
    plt.ylabel("Seconds")
    plt.title("Execution Time Distribution")
    plt.show()


class _FolderGetter:
    def __init__(self) -> None:
        self.optimization_folder = Path(__file__).parent.parent

    def get_new_folder_path(self) -> Path:
        return self._folder_getter("new_parser")

    def get_old_folder_path(self) -> Path:
        return self._folder_getter("old_parser")

    def _folder_getter(self, name: str) -> Path:
        folder = self.optimization_folder / name
        assert folder.exists(), f"{name} folder not found"

        return folder


class FileGetter:
    def __init__(self) -> None:
        self.folder_getter = _FolderGetter()

    def get_new_file_path(self) -> Path:
        return self._get_file_path("new")

    def get_old_file_path(self) -> Path:
        return self._get_file_path("old")

    def _get_file_path(self, name: str) -> Path:
        match name:
            case "old":
                folder = self.folder_getter.get_old_folder_path()
            case "new":
                folder = self.folder_getter.get_new_folder_path()
            case _:
                raise ValueError("Invalid name")

        result_file = folder / "results.txt"

        assert result_file.exists(), "Results file not found"
        return result_file


class MetricsGetter:
    def parse_metrics(self, file: Path) -> list[float]:
        """Retrieve execution times"""
        execution_times: list[float] = self._load_results(file)
        return execution_times

    @staticmethod
    def _load_results(file: Path) -> list[float]:
        "Loads the results from the file and returns a list of execution times"
        with open(file, "r", encoding="utf-8") as fd:
            execution_times = [float(line.replace("seconds", "").split(":")[1]) for line in fd]
        return execution_times


class SinglePlotter:
    @staticmethod
    def plot_new() -> None:
        result_file = FileGetter().get_new_file_path()

        # Load execution times
        execution_times: list[float] = MetricsGetter().parse_metrics(result_file)

        # Plot the images
        box_plot_metrics(execution_times)

    @staticmethod
    def plot_old() -> None:
        result_file = FileGetter().get_old_file_path()

        # Load execution times
        execution_times: list[float] = MetricsGetter().parse_metrics(result_file)

        # Plot the images
        box_plot_metrics(execution_times)


class DoublePlotter:

    def __init__(self) -> None:
        self.config_add_mean = True
        self.save_image = False

    def plot(self) -> None:
        """Plot the execution times of the new and old parser together"""

        # Load execution times
        result_file_new = FileGetter().get_new_file_path()
        execution_times_new: list[float] = MetricsGetter().parse_metrics(result_file_new)

        result_file_old = FileGetter().get_old_file_path()
        execution_times_old: list[float] = MetricsGetter().parse_metrics(result_file_old)

        # Plot the images
        self._generate_plots_side_by_side(
            execution_times_new=execution_times_new, execution_times_old=execution_times_old
        )

    def _generate_plots_side_by_side(self, execution_times_new: list[float], execution_times_old: list[float]) -> None:
        # Plot the images
        plt.subplot(1, 2, 1)
        plt.boxplot(execution_times_old, patch_artist=True, boxprops=dict(facecolor="lightblue"), showmeans=True)
        plt.ylabel("Segundos")
        plt.title("Antes de optimizar")

        if self.config_add_mean:
            self.add_mean_to_plot(plt, execution_times_old)

        plt.subplot(1, 2, 2)
        plt.boxplot(execution_times_new, patch_artist=True, boxprops=dict(facecolor="lightblue"), showmeans=True)
        plt.ylabel("Segundos")
        plt.title("Después   de optimizar")

        plt.suptitle("Comparación de Tiempos de Ejecución con n=30")  # Add a single title for both plots

        if self.config_add_mean:
            self.add_mean_to_plot(plt, execution_times_new)

        plt.tight_layout()
        if self.save_image:
            plt.savefig("parser_improvement_boxplot.png")

        plt.show()

    @staticmethod
    def calculate_mean(execution_times: list[float]) -> float:
        return round(sum(execution_times) / len(execution_times), 2)

    def add_mean_to_plot(self, custom_plt: PltObject, execution_times: list[float]) -> None:
        "Add the mean to the plot"
        custom_plt.text(
            1,
            0.95,
            f"Media: {self.calculate_mean(execution_times)}",
            transform=custom_plt.gca().transAxes,
        )


def main() -> None:
    "Main function to plot the box plot"
    DoublePlotter().plot()


if __name__ == "__main__":
    main()
