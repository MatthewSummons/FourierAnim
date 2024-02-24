from manim import *

def FourierAnim(
        self:MovingCameraScene,
        radii:list[float],
        freqs:list[float],
        ScnMobjects:list[Mobject],
        **kwaargs
    ):

    '''
    A function that animates the Fourier Series of a wave.

    To use make sure that you use MovingCameraScene and not Scene in your manim class

    Parameters
    ----------
    radii : list[float]
        A list of the radii of the circles in the Fourier Series.
    freqs : list[float]
        A list of the frequencies of the circles in the Fourier Series.
    ScnMobjects : list[Mobject]
        A list of the mobjects in the scene that are not part of the Fourier Series.
    **kwaargs : dict
        Keyword Arguments for the function.

    Keyword Arguments
    -----------------   
    run_time : float
        The time for which the animation will run.
    graphArrDist : float
        The distance between the end of the arrow and the main circle.
    cameraOffset : float
        The distance between the camera and the main circle.
    freqScale : float
        The scaling factor for the frequencies of the circles.
    circleColor : str
        The color of the circles.
    dotColor : str
        The color of the dot.
    traceColor : str
        The color of the trace.
    '''

    if len(radii) != len(freqs):
        raise Exception("The number of radii and frequencies must be the same.")
    
    # Default Parameters
    run_time, freqScale = 5.0, 0.25
    graphArrDist= 0.5
    cameraOffset = 4
    circleColor, dotColor = BLACK, GREEN
    traceColor = BLACK

    # Settle other Keyword Arguments
    if kwaargs is not None:
        for key, value in kwaargs.items():
            if key == "run_time":
                if (not(isinstance(value, int))) and (not(isinstance(value, float))):
                    raise TypeError("run_time must be a float.")
                run_time = value
            
            elif key == "graphArrDist":
                if not(isinstance(value, float)) and not(isinstance(value, int)):
                    raise TypeError("graphArrDist must be a float.")
                graphArrDist = value
            
            elif key == "cameraOffset":
                if not(isinstance(value, float)) and not(isinstance(value, int)):
                    raise TypeError("cameraOffset must be a float.")
                cameraOffset = value
            
            elif key == "freqScale":
                if not(isinstance(value, float)) and not(isinstance(value, int)):
                    raise TypeError("freqScale must be a float.")
                freqScale = value
            
            elif key == "circleColor":
                if not(isinstance(value, str)):
                    raise TypeError("circleColor must be a string.")
                circleColor = value
            
            elif key == "dotColor":
                if not(isinstance(value, str)):
                    raise TypeError("dotColor must be a string.")
                dotColor = value
            
            elif key == "traceColor":
                if not(isinstance(value, str)):
                    raise TypeError("traceColor must be a string.")
                traceColor = value
            
            else:
                raise Exception(("Something's Wrong"))
    
    
    # Scale all the frequencies by the scaing factor
    freqs = list(map(lambda x: freqScale * x, freqs))
    
    # Create the circles for the Fourier Series
    Circles = [Circle(radius=r, stroke_width=1.5, color=circleColor) for r in radii]
    
    # The Main Circle
    C0 = Circles[0]

    # Move the circles to the initial positions (On the boundary of the previous circles)
    for i in range(1, len(Circles)):
        Circles[i].add_updater(lambda m, i=i: m.move_to(Circles[i-1].get_start()))

    # The dot that the arrow will follow along with the arrow
    D = Dot(C0.get_center() + sum(radii) * RIGHT, radius=0.01, color=dotColor)
    D.add_updater(lambda m: m.move_to(Circles[-1].get_start()))
    
    # The arrow that will trace the graph of the wave following the dot
    arrow = Arrow(D.get_center(), C0.get_center() + (sum(radii) + graphArrDist) * RIGHT,
        stroke_width=4, buff=0, max_tip_length_to_length_ratio=0.2, color=BLUE_E)
    
    # The animation for creating the circles, the dot and the arrows
    self.play(Create(VGroup(*Circles, D, arrow)), run_time=5)
    self.play(C0.animate.shift(cameraOffset * LEFT), arrow.animate.shift(cameraOffset * LEFT))
    self.wait(0.5)
    
    # The Traced Path
    trace = TracedPath(
        lambda : arrow.get_tip().get_critical_point(RIGHT), # Returns the coordinates of the tip of the arrow
        stroke_color=traceColor, dissipating_time=15
    )
    self.add(trace)

    # Ensure that the arrow is on the dot
    arrow.add_updater(
        lambda m: m.put_start_and_end_on(
            D.get_center(),
            # End Arrow Position: Same x-pos as the main circle's center, but y-position of the dot
            [C0.get_center()[0] + sum(radii) + graphArrDist, D.get_center()[1], 0] 
        )
    )

    # Ensure that the camera follows the main circle
    self.camera.frame.add_updater(lambda cam: cam.move_to(C0.get_center() + cameraOffset * RIGHT))
    self.add(self.camera.frame)

    # Rotate the circles according to their frequencies
    for i in range(len(freqs)):
        # ω = 2πf
        Circles[i].add_updater(lambda m, dt, i=i: m.rotate(2 * PI * freqs[i] * dt, about_point=Circles[i].get_center()))

    # The updater to translate the main circle to simulate time moving forward
    C0.add_updater(lambda m, dt: m.move_to(C0.get_center() + dt * LEFT))
    
    # Move everything else in the scene along with the circles
    ScnGrp = VGroup(*ScnMobjects)
    ScnGrp.add_updater(lambda m, dt: m.shift(dt * LEFT))
    self.add(ScnGrp)

    self.wait(run_time)