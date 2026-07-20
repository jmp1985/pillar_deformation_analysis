import mrcfile
import os
import numpy as np
from pathlib import Path


def alphanum_key(filename: str) -> int:
    """Turn a string into a list of string and number chunks.
    "z23a" -> ["z", 23, "a"]
    """
    num = filename.split("_")[-1].split(".mrc")[0]
    return int(num)


def sort_nicely(filenames: list[str]) -> list[str]:
    """Sort the given list in the way that humans expect."""
    return sorted(filenames, key=alphanum_key)


def make_stack(data_dir: str, name: str, before_or_after: str) -> None:
    """Make a stack of images."""

    # Get the list of images
    images = []
    for filename in sort_nicely(
        [
            str(p)
            for p in Path(f"{data_dir}/{name}").glob(
                f"{before_or_after}*.mrc", case_sensitive=False
            )
        ]
    ):
        print(filename)
        voxel_size = mrcfile.open(filename).voxel_size
        images.append(mrcfile.open(filename).data)

    # Write the stack
    handle = mrcfile.new(os.path.join(name, f"{before_or_after}.mrc"), overwrite=True)
    handle.set_data(np.array(images, dtype=images[0].dtype))
    handle.voxel_size = voxel_size


def make_before_and_after_stacks(data_dir: str, name: str) -> None:
    """Make the before and after stacks."""

    # Check the directory exists
    if not os.path.exists(name):
        os.makedirs(name)

    # Make the before and after stacks
    make_stack(data_dir, name, "before")
    make_stack(data_dir, name, "after")
