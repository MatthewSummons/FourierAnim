# Installation

Please ensure that manimCE (>v18.0.0) is installed on your machine before using this package. We reccomend running the program in a conda environment. This requires you to install [anaconda](https://www.anaconda.com/download/) or [miniconda](https://docs.anaconda.com/free/miniconda/miniconda-install/). Otherwise, you may also wish to install manim locally please refer to the official guide [here](https://docs.manim.community/en/stable/installation.html).

To install this package in a conda environment follow the steps on manim's conda installation [here](https://docs.manim.community/en/stable/installation.html#conda-installation).

Otherwise run the following,

```
conda create -n my-manim-environment
conda activate my-manim-environment
conda install -c conda-forge manim
```

Finally install the package (still in the conda environment)

`pip install FourierAnim`

# Usage

To use the package, import the package into your file and work as usual. As example is displayed below.

```
# T1.py
from manim import *
import FourierAnim as FSA
class F_T1(MovingCameraScene):
    def construct(self):
        self.camera.background_color = WHITE
        Tex.set_default(color=BLACK, font_size=35)

        FSA.FourierAnim(
            self,
            radii = [1, 1/2, 1/3],
            freqs = [1, 2, 3],
            ScnMobjects=[],
            run_time=10,
        )
```

This file is saved as T1.py (although it could be called anything)

To generate the video run,

`python -m manim T1.py F_T1`

You can find the sample output [here](https://youtu.be/E4ipxXQqtDc)
