# Pillar Deformation Analysis

## Usage

1. Check out the repository and run the following command to install:

`uv pip install -e .`

2. Then modify (or copy) "run_example_analysis.py" and put the files to analyse.

3. Finally run the following command to analyse the files:

`uv python run_example_analysis.py`

4. During the picking step the first two points will be used to compute the diameter of the pillar and the second two points will be used to compute the length of the pillar so pick points in the following order:
  a. When napari opens, add a new points layer
  b. Navigate to the first first (-90)
  c. Add 4 points to the frame, in this order: [ bottom, top, right, left ] of pillar
  d. Navigate to the next frame and repeat
