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