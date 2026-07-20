from pillar_deformation_analysis.stack import make_before_and_after_stacks


def main(data_dir: str, datasets: list[str]) -> None:
    """Process the datasets."""
    for name in datasets:
        make_before_and_after_stacks(data_dir, name)


if __name__ == "__main__":
    data_dir = "/media/jmp/RFI/2025/Pillars/data"
    datasets = ["./FuManchuPillars/TheCasrleOfPillar-2"]
    main(data_dir, datasets)
