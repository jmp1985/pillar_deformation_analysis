import os

import mrcfile
import numpy as np
import yaml


def pick_points(projections_filename: str, points_filename: str):
    """
    Pick the fiduccials manually

    """
    import napari
    import napari.layers

    def read_projections(filename):
        print("Reading projections from %s" % filename)
        return mrcfile.mmap(filename)

    def read_contours(filename):
        if filename:
            print("Reading contours from %s" % filename)
            return np.load(filename)
        else:
            contours = None
        return contours

    def read_model(filename):
        if filename:
            print("Reading model from %s" % filename)
            model = yaml.safe_load(open(filename))
        else:
            model = None
        return model

    def write_points(filename, points):
        yaml.safe_dump(points.tolist(), open(filename, "w"))

    def get_points(viewer, image_size):
        for layer in viewer.layers:
            if isinstance(layer, napari.layers.Points):
                points = np.array(layer.data.tolist())[:, 1:]
                break
        points = points.reshape(-1, 8)
        print(points)
        assert points.shape[0] == 7
        assert points.shape[1] == 8
        return points

    # Load the projections data
    projections = read_projections(projections_filename).data

    # Initialise the viewer
    viewer = napari.Viewer()

    # Add the image layer
    viewer.add_image(projections, name="Projections")

    # Start Napari
    napari.run()

    # Get the points layers
    points = get_points(viewer, projections.shape[1:])

    # Write the contours
    write_points(points_filename, points)


def pick_points_before_and_after(name: str):
    """Pick the points."""

    # Pick before and after stacks
    if not os.path.exists(os.path.join(name, "before_points.yaml")):
        pick_points(
            os.path.join(name, "before.mrc"), os.path.join(name, "before_points.yaml")
        )
    if not os.path.exists(os.path.join(name, "after_points.yaml")):
        pick_points(
            os.path.join(name, "after.mrc"), os.path.join(name, "after_points.yaml")
        )
