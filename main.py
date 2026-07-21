import yaml
from matplotlib import pylab
from pillar_deformation_analysis.stack import make_before_and_after_stacks
from pillar_deformation_analysis.pick import pick_points_before_and_after
from pillar_deformation_analysis.analysis import analyse_deformation


def read_pillar_data(datasets: list[str]) -> None:
    """Read the pillar data."""
    pillar_data = []
    for name in datasets:
        with open(f"{name}/deformation.yaml") as infile:
            data = yaml.safe_load(infile)
            pillar_data.append((name, data["diameter"], data["angle"], data["scale"]))
    return pillar_data


def plot_deformation(pillar_data: list) -> None:
    """Plot the pillar data."""

    # Plot the points
    fig, ax = pylab.subplots(nrows=2, figsize=(12, 8))
    for name, diameter, angle, scale in pillar_data:
        print(name, diameter, angle, scale)
        ax[0].scatter(diameter, scale, label=name)
        ax[1].scatter(diameter, angle)  # , label=name)

    # Setup the axes
    ax[0].set_xlabel("Diameter (nm)")
    ax[0].set_ylabel("Deformation")
    ax[1].set_xlabel("Diameter (nm)")
    ax[1].set_ylabel("Rotation (deg)")
    ax[0].set_ylim(0.9, 1.5)
    ax[0].axhline(1, color="gray", linestyle="--")
    ax[1].axhline(0, color="gray", linestyle="--")
    # fig.legend(loc='upper center', ncols=5)
    pylab.show()
    fig.savefig("deformation.png", dpi=600, bbox_inches="tight")


def main(data_dir: str, datasets: list[str], pixel_size=1.93) -> None:
    """Process the datasets."""

    # Loop through datasets
    for name in datasets:
        # Make the before and after stacks
        make_before_and_after_stacks(data_dir, name)

        # Now pick points before and after
        pick_points_before_and_after(name)

        # Now compute the deformation
        analyse_deformation(name, pixel_size)

    # Read the pillar data
    pillar_data = read_pillar_data(datasets)

    # Plot the deformation
    plot_deformation(pillar_data)


if __name__ == "__main__":
    data_dir = "/media/jmp/RFI/2025/Pillars/data"
    datasets = ["./FuManchuPillars/TheCasrleOfPillar-2"]
    pixel_size = 1.93
    main(data_dir, datasets, pixel_size)
