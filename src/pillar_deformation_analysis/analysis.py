import os
import yaml
import numpy as np
import scipy
from scipy.spatial.transform import Rotation


def read_pillar_data(name: str) -> np.ndarray:
    """Read the pillar data."""

    # Read the before and after points
    before = yaml.safe_load(open(os.path.join(name, "before_points.yaml")))
    after = yaml.safe_load(open(os.path.join(name, "after_points.yaml")))

    # Set the angles
    angles = np.arange(-90, 91, 30)

    # Return the pillar data
    return np.concatenate([angles[:, None], np.array(before), np.array(after)], axis=1)


def compute_pillar_vectors(
    pillar: np.ndarray, pixel_size: float
) -> tuple[float, np.ndarray, np.ndarray]:
    """Compute the pillar vectors."""

    # Get the angles and points
    angles = pillar[:, 0]

    # Before points.
    # p and q are used for the diameter
    # a and b are used for the stretch/rotation
    px0 = pillar[:, 1]
    py0 = pillar[:, 2]
    qx0 = pillar[:, 3]
    qy0 = pillar[:, 4]
    ax0 = pillar[:, 5]
    ay0 = pillar[:, 6]
    bx0 = pillar[:, 7]
    by0 = pillar[:, 8]

    # After points.
    # p and q are used for the diameter
    # a and b are used for the stretch/rotation
    px1 = pillar[:, 9]
    py1 = pillar[:, 10]
    qx1 = pillar[:, 11]
    qy1 = pillar[:, 12]
    ax1 = pillar[:, 13]
    ay1 = pillar[:, 14]
    bx1 = pillar[:, 15]
    by1 = pillar[:, 16]

    # Compute the diameter
    diameter0 = np.sqrt((px0 - qx0) ** 2 + (py0 - qy0) ** 2) * pixel_size
    np.sqrt((px1 - qx1) ** 2 + (py1 - qy1) ** 2) * pixel_size

    # Get the length of the pillar
    length_x0 = (ax0 - bx0) * pixel_size
    length_y0 = (ay0 - by0) * pixel_size
    length_x1 = (ax1 - bx1) * pixel_size
    length_y1 = (ay1 - by1) * pixel_size

    def f(beta, dx, dy, angles):
        ddx = []
        ddy = []
        for theta in angles:
            R = Rotation.from_rotvec([0, theta, 0]).as_matrix()
            d = R @ beta
            ddx.append(d[0])
            ddy.append(d[1])
        r = np.concatenate(
            [(np.array(ddx) - np.array(dx)), (np.array(ddy) - np.array(dy))]
        )
        return r

    # Compute the mean length
    angles = angles
    dx = length_x0
    dy = length_y0
    ly = np.mean(dy)

    # Find the best fit pillar axis
    result = scipy.optimize.least_squares(
        f, (0, ly, 0), args=(dx, dy, np.radians(angles)), loss="linear"
    )
    beta = result.x

    # The before pillar vector
    before = np.array(tuple(beta))

    # Compute the mean length
    angles = angles
    dx = length_x1
    dy = length_y1
    ly = np.mean(dy)

    # Find the best fit pillar axis
    result = scipy.optimize.least_squares(
        f, (0, ly, 0), args=(dx, dy, np.radians(angles)), loss="linear"
    )
    beta = result.x

    # The before pillar vector
    after = np.array(tuple(beta))

    # Compute the diameter
    diameter = np.mean(diameter0)

    # Return the diamater and before/after pillar vectors
    return float(diameter), before, after


def compute_rotation_and_deformation(
    before: np.ndarray, after: np.ndarray
) -> tuple[float, float]:
    """Compute the rotation and deformation."""

    # The pillar vector before and after
    A = before
    B = after

    # Normalize the vectors
    At = A / np.linalg.norm(A)
    Bt = B / np.linalg.norm(B)

    # Compute the rotation matrix between the vectors
    c = np.dot(At, Bt)
    v = np.cross(At, Bt)
    np.linalg.norm(v)
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    R = np.eye(3) + vx + np.dot(vx, vx) / (1 + c)
    angle = np.linalg.norm(np.degrees(Rotation.from_matrix(R).as_rotvec()))

    # Compute the scale factor between the length after and before. A scale > 1
    # indicates a stretch in size.
    scale = np.linalg.norm(after) / np.linalg.norm(before)

    # Return the angle and the scale
    return float(angle), float(scale)


def analyse_deformation(name: str, pixel_size: float = 1.93) -> None:

    # Read the pillar data
    pillar = read_pillar_data(name)

    # Get the pillar vector before and after
    diameter, before, after = compute_pillar_vectors(pillar, pixel_size)

    # Compute the deformation and rotation
    angle, scale = compute_rotation_and_deformation(before, after)

    print(f"{name}: d={diameter}, r={angle}, s={scale}")

    # Save the deformation
    with open(f"{name}/deformation.yaml", "w") as outfile:
        yaml.safe_dump({"diameter": diameter, "angle": angle, "scale": scale}, outfile)
