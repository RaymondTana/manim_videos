from manim import *
import math
import numpy as np
import random
import re

##### SETTINGS #####

# Delays
TINY_DELAY = 0.1
SHORT_DELAY = 0.2
NORMAL_DELAY = 0.5
BIG_DELAY = 0.8
LONG_DELAY = 1
LARGE_DELAY = 1.4

# Colors
CORAL = ManimColor("#E78F8E")
SUNGLOW = ManimColor("#FFD166")
INDIGO = ManimColor("#9191E9")
STEEL = ManimColor("#457EAC")
LAPIS = ManimColor("#2D5D7B")

# Font
DEFAULT_FONT = 'serif'
FONT_COLOR = WHITE
FONT_ALIGN = 'center'

PARAGRAPH_SIZE = 45
SMALL_SIZE = 60
NORMAL_SIZE = 80
BIG_SIZE = 100
PROMINENT_SIZE = 140

# TeX template
TEX_TEMPLATE = TexTemplate()
TEX_TEMPLATE.add_to_preamble(r"\usepackage{mathrsfs}")
TEX_TEMPLATE.add_to_preamble(r"\usepackage{amsmath}")
TEX_TEMPLATE.add_to_preamble(r"\usepackage{amsthm}")
TEX_TEMPLATE.add_to_preamble(r"\usepackage{amssymb}")
TEX_TEMPLATE.add_to_preamble(r"\usepackage{amsfonts}")
TEX_TEMPLATE.add_to_preamble(r"\usepackage{mathtools}")

# Buffer
NORMAL_BUFFER = 0.5

####################

###### SCENE #######

# class TuringMachine(Scene):
#     def construct(self):
#         ##### METHODS ######

#         def float_tex(text):
#             T = Tex(
#                 rf'{text}',
#                 tex_template = TEX_TEMPLATE,
#                 color = FONT_COLOR,
#                 font_size = PARAGRAPH_SIZE,
#             )
#             self.play(Write(T))
#             self.wait(NORMAL_DELAY)
#             self.play(FadeOut(T))
            
#         def float_mathtex(*text):
#             T = MathTex(
#                 *text,
#                 color = FONT_COLOR,
#                 font_size = PARAGRAPH_SIZE,
#             ).arrange(DOWN, buff = NORMAL_BUFFER)
#             self.play(Write(T))
#             self.wait(NORMAL_DELAY)
#             self.play(FadeOut(T))
#         ####################

#         float_mathtex(r"\nabla \cdot \vec{E} = \frac{\rho}{\epsilon_0}",
#             r"\nabla \times \vec{B} = \mu_0 \vec{J} + \mu_0 \epsilon_0 \frac{\partial \vec{E}}{\partial t}")

#         float_tex('hello $e^x$')

class MengerSponge(ThreeDScene):
    def construct(self):
        # Set up 3D scene with camera and lighting
        self.set_camera_orientation(phi = 60 * DEGREES, theta = 45 * DEGREES)
        self.camera.light_source.move_to(3 * IN + 2 * LEFT + 2 * UP)
        
        # Title
        title = Text("Menger Sponge", font_size = 48)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        
        # Animate different iterations of the Menger Sponge
        for n in range(4): # Show iterations 0 through 3
            # Create iteration label
            iteration_text = Text(f"Iteration n = {n}", font_size = 36)
            iteration_text.next_to(title, DOWN)
            self.add_fixed_in_frame_mobjects(iteration_text)
            
            # Generate Menger Sponge for current iteration
            sponge = self.create_menger_sponge(n)
            sponge.set_color(BLUE)
            sponge.set_sheen(0.5, direction = IN)
            
            # Add the sponge to scene
            self.add(sponge)
            
            # Rotate the sponge
            self.play(
                Rotate(sponge, angle = 2 * PI, axis = UP, run_time = 3),
                rate_func = linear
            )
            
            # Brief pause before next iteration
            self.wait(0.5)
            
            # Remove current sponge and text for next iteration
            self.remove(sponge, iteration_text)
        
        # Final display of highest iteration with slow rotation
        final_sponge = self.create_menger_sponge(3)
        final_sponge.set_color_by_gradient(BLUE, PURPLE, GREEN)
        final_sponge.set_sheen(0.7, direction = IN)
        
        final_text = Text("Final Iteration n = 3", font_size = 36)
        final_text.next_to(title, DOWN)
        self.add_fixed_in_frame_mobjects(final_text)
        
        self.add(final_sponge)
        self.play(
            Rotate(final_sponge, angle = 4 * PI, axis = UP + 0.3 * RIGHT, run_time = 6),
            rate_func = linear
        )
        
        self.wait(2)
    
    def create_menger_sponge(self, n, size=2, center=ORIGIN):
        """
        Recursively create a Menger Sponge of iteration n.
        
        Args:
            n: Iteration level (0 = solid cube)
            size: Size of the current cube
            center: Center position of the current cube
        
        Returns:
            VGroup containing all the cubes that make up the sponge
        """
        if n == 0:
            # Base case: return a single cube
            cube = Cube(side_length=size, fill_opacity=0.8)
            cube.move_to(center)
            return VGroup(cube)
        
        # Recursive case: create 20 smaller cubes (27 - 7 removed)
        sponge_group = VGroup()
        new_size = size / 3
        
        # Generate all 27 possible positions in a 3x3x3 grid
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    # Skip the 7 positions that should be removed:
                    # - Center cube (1,1,1)
                    # - Face centers: cubes where exactly 2 coordinates are 1
                    skip_positions = [
                        (1, 1, 1),  # Center
                        (1, 1, 0), (1, 1, 2),  # Front/back face centers
                        (1, 0, 1), (1, 2, 1),  # Top/bottom face centers  
                        (0, 1, 1), (2, 1, 1),  # Left/right face centers
                    ]
                    
                    if (i, j, k) in skip_positions:
                        continue
                    
                    # Calculate position of this sub-cube
                    offset = np.array([
                        (i - 1) * new_size,
                        (j - 1) * new_size, 
                        (k - 1) * new_size
                    ])
                    new_center = center + offset
                    
                    # Recursively create sub-sponge
                    sub_sponge = self.create_menger_sponge(n - 1, new_size, new_center)
                    sponge_group.add(sub_sponge)
        
        return sponge_group

class MengerSpongeInteractive(ThreeDScene):
    """
    Alternative version with interactive controls and better visualization
    """
    def construct(self):
        # Set up scene
        self.set_camera_orientation(phi = 75 * DEGREES, theta = 30 * DEGREES)
        self.camera.light_source.move_to(4 * OUT + 3 * LEFT + 2 * UP)
        
        # Create title and controls
        title = Text("Interactive Menger Sponge", font_size = 40)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        
        # Show each iteration with detailed animation
        iterations_to_show = [0, 1, 2, 3]
        
        for i, n in enumerate(iterations_to_show):
            # Create info text
            info_lines = [
                f"Iteration: {n}",
                f"Cubes: {20 ** n if n > 0 else 1}",
                f"Volume ratio: {(20 / 27) ** n:.3f}" if n > 0 else "Volume ratio: 1.000"
            ]
            
            info_text = VGroup(*[Text(line, font_size = 24) for line in info_lines])
            info_text.arrange(DOWN, aligned_edge = LEFT)
            info_text.to_corner(UL, buff = 1)
            info_text.shift(DOWN * 1.5)
            self.add_fixed_in_frame_mobjects(info_text)
            
            # Create the sponge
            sponge = self.create_menger_sponge_colored(n)
            
            # Animate appearance
            if n == 0:
                self.play(Create(sponge), run_time = 1)
            else:
                self.play(FadeIn(sponge, scale = 0.8), run_time = 1.5)
            
            # Rotate to show different angles
            self.play(
                Rotate(sponge, angle = PI, axis = UP + 0.2 * RIGHT, run_time = 2),
                rate_func=smooth
            )
            
            self.play(
                Rotate(sponge, angle = PI, axis = RIGHT + 0.2 * UP, run_time = 2),
                rate_func=smooth
            )
            
            # Clean up for next iteration
            if i < len(iterations_to_show) - 1:
                self.play(FadeOut(sponge), FadeOut(info_text), run_time = 1)
            else:
                # Final continuous rotation
                self.play(
                    Rotate(sponge, angle = 2 * PI, axis = UP, run_time = 4),
                    rate_func = linear
                )
        
        self.wait(2)
    
    def create_menger_sponge_colored(self, n, size = 2.5, center = ORIGIN, depth = 0):
        """
        Create Menger Sponge with color gradient based on recursion depth
        """
        if n == 0:
            cube = Cube(side_length=size, fill_opacity = 0.85)
            cube.move_to(center)
            
            # Color based on depth for visual interest
            colors = [BLUE, GREEN, YELLOW, RED, PURPLE, ORANGE]
            cube.set_color(colors[depth % len(colors)])
            cube.set_sheen(0.6, direction = IN)
            
            return cube
        
        sponge_group = VGroup()
        new_size = size / 3
        
        # Create the 20 remaining cubes
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    # Skip removed positions
                    skip_positions = [
                        (1, 1, 1),  # Center
                        (1, 1, 0), (1, 1, 2),  # Face centers
                        (1, 0, 1), (1, 2, 1),
                        (0, 1, 1), (2, 1, 1),
                    ]
                    
                    if (i, j, k) in skip_positions:
                        continue
                    
                    offset = np.array([
                        (i - 1) * new_size,
                        (j - 1) * new_size,
                        (k - 1) * new_size
                    ])
                    new_center = center + offset
                    
                    sub_sponge = self.create_menger_sponge_colored(
                        n - 1, new_size, new_center, depth + 1
                    )
                    sponge_group.add(sub_sponge)
        
        return sponge_group

class MengerSpongeInteractiveQuicker(ThreeDScene):
    """
    Fast version optimized for quick previews
    """
    def construct(self):
        # Set up scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.camera.light_source.move_to(4*OUT + 3*LEFT + 2*UP)
        
        # Create title and controls
        title = Text("Fast Menger Sponge Preview", font_size=40)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        
        # Show only lower iterations for speed
        iterations_to_show = [0, 1, 2]  # Skip level 3 for speed
        
        for i, n in enumerate(iterations_to_show):
            # Create info text
            info_lines = [
                f"Iteration: {n}",
                f"Cubes: {20**n if n > 0 else 1}",
                f"Volume ratio: {(20/27)**n:.3f}" if n > 0 else "Volume ratio: 1.000"
            ]
            
            info_text = VGroup(*[Text(line, font_size = 24) for line in info_lines])
            info_text.arrange(DOWN, aligned_edge = LEFT)
            info_text.to_corner(UL, buff=1)
            info_text.shift(DOWN * 1.5)
            self.add_fixed_in_frame_mobjects(info_text)
            
            # Create the sponge
            sponge = self.create_menger_sponge_colored(n)
            
            # Faster animations
            if n == 0:
                self.play(Create(sponge), run_time = 0.8)
            else:
                self.play(FadeIn(sponge, scale = 0.8), run_time=1)
            
            # Single rotation
            self.play(
                Rotate(sponge, angle = PI, axis = UP + 0.2 * RIGHT, run_time = 1.5),
                rate_func = smooth
            )
            
            # Clean up for next iteration
            if i < len(iterations_to_show) - 1:
                self.play(FadeOut(sponge), FadeOut(info_text), run_time = 0.5)
            else:
                # Final rotation
                self.play(
                    Rotate(sponge, angle = PI, axis = UP, run_time = 2),
                    rate_func = linear
                )
        
        self.wait(1)
    
    def create_menger_sponge_colored(self, n, size=2.5, center=ORIGIN, depth=0):
        """
        Create Menger Sponge with color gradient based on recursion depth
        """
        if n == 0:
            cube = Cube(side_length=size, fill_opacity = 0.85)
            cube.move_to(center)
            
            # Color based on depth for visual interest
            colors = [BLUE, GREEN, YELLOW, RED, PURPLE, ORANGE]
            cube.set_color(colors[depth % len(colors)])
            cube.set_sheen(0.6, direction = IN)
            
            return cube
        
        sponge_group = VGroup()
        new_size = size / 3
        
        # Create the 20 remaining cubes
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    # Skip removed positions
                    skip_positions = [
                        (1, 1, 1),  # Center
                        (1, 1, 0), (1, 1, 2),  # Face centers
                        (1, 0, 1), (1, 2, 1),
                        (0, 1, 1), (2, 1, 1),
                    ]
                    
                    if (i, j, k) in skip_positions:
                        continue
                    
                    offset = np.array([
                        (i - 1) * new_size,
                        (j - 1) * new_size,
                        (k - 1) * new_size
                    ])
                    new_center = center + offset
                    
                    sub_sponge = self.create_menger_sponge_colored(
                        n - 1, new_size, new_center, depth + 1
                    )
                    sponge_group.add(sub_sponge)
        
        return sponge_group

class QuickPreview(ThreeDScene):
    """
    Ultra-fast preview showing just one iteration with minimal animation
    """
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)
        
        title = Text("Quick Menger Sponge Preview", font_size=36)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        
        # Show just iteration 2 (good balance of detail vs speed)
        sponge = self.create_menger_sponge(2)
        sponge.set_color_by_gradient(BLUE, GREEN)
        sponge.set_sheen(0.5)
        
        self.add(sponge)
        self.play(Rotate(sponge, PI, axis = UP, run_time = 2))
        self.wait(0.5)
    
    def create_menger_sponge(self, n, size = 2, center = ORIGIN):
        """Optimized version with reduced recursion"""
        if n == 0:
            cube = Cube(side_length=size, fill_opacity = 0.8)
            cube.move_to(center)
            return cube
        
        sponge_group = VGroup()
        new_size = size / 3
        
        # Only create the 20 valid positions
        valid_positions = []
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if (i, j, k) not in [(1,1,1), (1,1,0), (1,1,2), (1,0,1), (1,2,1), (0,1,1), (2,1,1)]:
                        valid_positions.append((i, j, k))
        
        for i, j, k in valid_positions:
            offset = np.array([(i - 1) * new_size, (j - 1) * new_size, (k - 1) * new_size])
            new_center = center + offset
            sub_sponge = self.create_menger_sponge(n - 1, new_size, new_center)
            sponge_group.add(sub_sponge)
        
        return sponge_group

class Cantor(ThreeDScene):
    MAX_DEPTH = 5 # number of iterations
    UNIT = 12 # pixels that represent length 1
    BASE_H = 0.4 # height of the first block
    THICKNESS = 0.25 # y-depth of every prism
    BLOCK_COLOR = BLUE_E
    ZOOM_FACTOR = 1.6

    def make_block(self, a: float, b: float, level: int) -> Mobject:
        """
        Build a Prism spanning the sub-interval [a,b] in [0,1].
        It stores its own new endpoints and height for the next pass.
        """
        length = (b - a) * self.UNIT
        height = self.BASE_H * (0.9 ** level)

        block = Prism(
            dimensions = [length, self.THICKNESS, height],
            fill_opacity = 0.7,
            stroke_width = 0
        ).set_color(self.BLOCK_COLOR).set_sheen(0.3, direction = UP)

        # centre-x maps [0, 1] to [- UNIT / 2, + UNIT / 2]
        cx = (a + b) / 2 * self.UNIT - self.UNIT / 2
        block.move_to([cx, 0, height / 2]) # z = height/2 puts it on the floor

        # remember geometry for later
        block.bounds = (a, b) # endpoints in [0, 1]
        block.h = height # current height
        return block

    def construct(self):
        self.set_camera_orientation(phi = 65 * DEGREES, theta = 90 * DEGREES)
        self.camera.light_source.move_to(4 * OUT + 3 * LEFT + 2 * UP)
        phi, theta, focal_distance, gamma, zoom = self.camera.get_value_trackers()
        accumulated_zoom = 1

        # start with the whole interval
        blocks = [self.make_block(0, 1, 0)]
        self.play(FadeIn(VGroup(*blocks)))

        self.play(theta.animate.set_value(80 * DEGREES), run_time = 2)

        # iterate Cantor construction
        for depth in range(self.MAX_DEPTH):
            halves, split_anims = [], []

            # split every block into its two halves
            for blk in blocks:
                a, b = blk.bounds
                mid = (a + b) / 2
                left = self.make_block(a, mid, depth)
                right = self.make_block(mid, b, depth)
                halves += [left, right]
                split_anims.append(ReplacementTransform(blk, VGroup(left, right)))
            self.play(*split_anims, run_time=0.00001)

            # squash each half into a third of the parent, anchored at its outer edge
            squash_anims, thirds = [], []
            for L, R in zip(halves[::2], halves[1::2]):
                a, m = L.bounds
                m, b = R.bounds # m is the same mid-point
                h = L.h
                span = b - a
                third = span / 3
                scale = (third) / (span / 2)  # always 2/3

                # new target data
                left_bounds = (a, a + third)
                right_bounds = (b - third, b)
                new_h = h * 0.9
                dz = (new_h - L.h) / 2 # raise/lower so bottom stays on floor

                # left block: shrink about its LEFT-bottom-front corner
                L_anchor = L.get_corner(LEFT + DOWN + OUT)
                squash_anims.append(
                    L.animate.scale([scale, 1, new_h / L.h], about_point = L_anchor).shift([0, 0, dz])
                )
                L.bounds, L.h = left_bounds, new_h

                # right block: shrink about RIGHT-bottom-front corner
                R_anchor = R.get_corner(RIGHT + DOWN + OUT)
                squash_anims.append(
                    R.animate.scale([scale, 1, new_h / R.h], about_point = R_anchor).shift([0, 0, dz])
                )
                R.bounds, R.h = right_bounds, new_h

                thirds += [L, R]

            self.play(*squash_anims, run_time = 1.0)
            blocks = thirds # next iteration
            
            right_block = max(thirds, key = lambda m : m.get_center()[0])
            cx = right_block.get_center()[0]
            
            accumulated_zoom *= self.ZOOM_FACTOR
            self.move_camera(frame_center = [cx, 0, 0], zoom = accumulated_zoom)
            
        self.wait()
        self.move_camera(frame_center = [0, 0, 0], zoom = 1)

        title = MathTex(r"\text{Middle-$\frac{1}{3}$ Cantor set}", font_size = 64).to_edge(UP)
        question = MathTex(r"1D?... 0D?").move_to(2 * DOWN)
        note = MathTex(r"\operatorname{dim}_{\operatorname{fractal}} = \frac{\log 2}{\log 3} \approx 0.6309", font_size = 30).next_to(question, DOWN)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(5)
        self.add_fixed_in_frame_mobjects(question)
        self.play(Write(question))
        self.wait(2)
        self.add_fixed_in_frame_mobjects(note)
        self.play(Write(note))
        self.wait(3)
        self.play(FadeOut(VGroup(*blocks), title, question, note), run_time = 0.5)


class MacOSTextEditorWithCode(Scene):
    def construct(self):
        code = '''from manim import Scene, Square

class FadeInSquare(Scene):
    def construct(self):
        s = Square()
        self.play(FadeIn(s))
        self.play(s.animate.scale(2))
        self.wait()'''

        rendered_code = Code(
            code_string=code,
            language="python",
            background="window",
            background_config={"stroke_color": "maroon"},
            add_line_numbers = False,

        )
        self.play(Create(rendered_code))

from manim import *

class SideBySideCode(Scene):
    def construct(self):

        # Create left code object
        left_rendered_code = Code(
            code_string = '''00000000000000000000000000000000000
00000000000000000000000000000000000
00000000000000000000000000000000000
00000000000000000000000000000000000
00000000000000000000000000000000000
00000000000000000000000000000000000
                 
                ...

00000000000000000000000000000000000
00000000000000000000000000000000000
00000000000000000000000000000000000
00000000000000000000000000000000000
''',
            background = "window",
            background_config = {"fill_color": "black", "stroke_color": "white"}, 
            paragraph_config = {"font_size": 30},
            add_line_numbers = False,
            formatter_style = 'bw',
        ).scale(0.7).to_edge(LEFT, buff=0.5)

        # Create right code object
        right_rendered_code = Code(
            code_string = '''print('0' * 1000000)''',
            language='python',
            background = "window",
            background_config = {"fill_color": "black", "stroke_color": "white"},
            paragraph_config = {"font_size": 35},
            add_line_numbers = False,
            formatter_style = 'github-dark'
        ).scale(0.7).to_edge(RIGHT, buff = 0.5)

        # Create arrow pointing from left to right
        arrow = Arrow(
            start = left_rendered_code.get_right(),
            end = right_rendered_code.get_left(),
            buff = 0.2,
            stroke_width = 4,
            color = GRAY_A
        )

        # Reverse direction arrow
        back_arrow = CurvedArrow(
            start_point = right_rendered_code.get_top() + 0.2 * UP,
            end_point = left_rendered_code.get_corner(UR) + 0.2 / (2 ** 0.5) * (UP + RIGHT),
            stroke_width = 4,
            color = YELLOW,
        )

        # Show left code
        self.play(Create(left_rendered_code), run_time = 4)
        self.wait(1)
        # Show arrow
        self.play(GrowArrow(arrow))
        # Show right code
        self.play(Create(right_rendered_code))
        self.wait(2)
        # Reverse arrow
        self.play(Create(back_arrow))
        self.wait(2)

class SideBySideCode_Random(Scene):
    def construct(self):

        # Create left code object
        left_rendered_code = Code(
            code_string = '''11001001011011101010101101010000010
10000010111101111000111101011101011
01111001000001101101100101000001110
10110001101001100101101000000011010
01111000001101101111000000110100110
11101011000110111101001001101111101
                 
                ...

10000010100001010000001111001000101
10100011100100100001000111000010111
00101000111100100001100001100000000
11111010110010100101001101101001011
''',
            background = "window",
            background_config = {"fill_color": "black", "stroke_color": "white"}, 
            paragraph_config = {"font_size": 30},
            add_line_numbers = False,
            formatter_style = 'bw',
        ).scale(0.7).to_edge(LEFT, buff=0.5)

        # Create right code object
        right_rendered_code = Code(
            code_string = '''verbatim?''',
            language='python',
            background = "window",
            background_config = {"fill_color": "black", "stroke_color": "white"},
            paragraph_config = {"font_size": 35},
            add_line_numbers = False,
            formatter_style = 'github-dark'
        ).scale(0.7).to_edge(RIGHT, buff = 2)

        # Create arrow pointing from left to right
        arrow = Arrow(
            start = left_rendered_code.get_right(),
            end = right_rendered_code.get_left(),
            buff = 0.2,
            stroke_width = 4,
            color = GRAY_A
        )

        # Reverse direction arrow
        back_arrow = CurvedArrow(
            start_point = right_rendered_code.get_top() + 0.2 * UP,
            end_point = left_rendered_code.get_corner(UR) + 0.2 / (2 ** 0.5) * (UP + RIGHT),
            stroke_width = 4,
            color = YELLOW,
        )

        # Animation sequence
        # Show left code
        self.play(Create(left_rendered_code), run_time = 2)
        self.wait(2)
        # Show arrow
        self.play(GrowArrow(arrow))
        # Show right code
        self.play(Create(right_rendered_code))
        self.wait(2)
        # Reverse arrow
        self.play(Create(back_arrow))
        self.wait(2)


class ComplexityOfTextFiles(Scene):
    def construct(self):

        # Create left code object
        code = Code(
            code_string = '''00000000000000000000000000000000000
00000000000000000000000000000000000
00000000000000000000000000000000000
00000000000000000000000000000000000
00000000000000000000000000000000000
00000000000000000000000000000000000
                 
                ...

00000000000000000000000000000000000
00000000000000000000000000000000000
00000000000000000000000000000000000
00000000000000000000000000000000000
''',
            background = "window",
            background_config = {"fill_color": "black", "stroke_color": "white"}, 
            paragraph_config = {"font_size": 30},
            add_line_numbers = False,
            formatter_style = 'bw',
        ).scale(0.7).move_to(ORIGIN)

        self.play(Create(code), run_time = 0.5)
        self.wait(1)

        # Prepare formula pieces, positioned around the code's target
        code.generate_target()
        code.target.scale(0.4)
        final_center = ORIGIN + UP * 0.5
        code.target.move_to(final_center)

        C_tex = MathTex(r"C")
        open_tex = MathTex(r"(")
        close_tex = MathTex(r")")
        h = code.target.height
        open_tex.stretch_to_fit_height(h * 1.04)
        close_tex.stretch_to_fit_height(h * 1.04)
        open_tex.next_to(code.target, LEFT, buff = 0.08).match_y(code.target)
        C_tex.next_to(open_tex, LEFT, buff = 0.2)
        close_tex.next_to(code.target, RIGHT, buff = 0.08).match_y(code.target)

        self.play(
            MoveToTarget(code),
            FadeIn(C_tex, shift = 0.1 * DOWN),
            FadeIn(open_tex, shift = 0.1 * DOWN),
            FadeIn(close_tex, shift = 0.1 * DOWN),
            run_time = 0.9,
        )
        self.wait(2)

        # Reveal RHS 
        rhs = MathTex(r"\approx \log(\mathrm{length}(\text{file}))")
        # rhs = MathTex(r"\approx \mathrm{length}(\text{file})")
        rhs.next_to(close_tex, RIGHT, buff = 0.18).match_y(code)
        
        self.play(FadeIn(rhs, shift = 0.1 * DOWN))

        self.wait()

        equation = VGroup(C_tex, open_tex, code, close_tex, rhs)
        self.play(equation.animate.scale(1.15).move_to(ORIGIN + UP * 0.2))

        self.wait()

        yellow_text = MarkupText('<i>"Perfectly compressible"</i>', color = YELLOW).scale(0.6).next_to(rhs, DOWN, buff = 0.15).align_to(rhs, LEFT)
        self.play(FadeIn(yellow_text, shift = 0.1 * UP), run_time = 0.6)

        top_group = VGroup(equation, yellow_text)
        self.play(top_group.animate.to_edge(UP, buff = 1), run_time = 0.8)

        # -------

        bottom_code = Code(
            code_string = '''11001001011011101010101101010000010
10000010111101111000111101011101011
01111001000001101101100101000001110
10110001101001100101101000000011010
01111000001101101111000000110100110
11101011000110111101001001101111101
                 
                ...

10000010100001010000001111001000101
10100011100100100001000111000010111
00101000111100100001100001100000000
11111010110010100101001101101001011
''',
            background = "window",
            background_config = {"fill_color": "black", "stroke_color": "white"}, 
            paragraph_config = {"font_size": 30},
            add_line_numbers = False,
            formatter_style = 'bw',
        ).scale(0.5).move_to(2 * DOWN)

        self.play(Create(bottom_code), run_time = 0.5)

        # Prepare formula pieces, positioned around the code's target
        bottom_code.generate_target()
        bottom_code.target.scale(0.4 * 0.7 / 0.5)

        bottom_C_tex = MathTex(r"C")
        bottom_open_tex = MathTex(r"(")
        bottom_close_tex = MathTex(r")")
        bottom_open_tex.stretch_to_fit_height(h * 1.04)
        bottom_close_tex.stretch_to_fit_height(h * 1.04)
        bottom_open_tex.next_to(bottom_code.target, LEFT, buff = 0.08).match_y(bottom_code.target)
        bottom_C_tex.next_to(bottom_open_tex, LEFT, buff = 0.2)
        bottom_close_tex.next_to(bottom_code.target, RIGHT, buff = 0.08).match_y(bottom_code.target)

        self.play(
            MoveToTarget(bottom_code),
            FadeIn(bottom_C_tex, shift = 0.1 * DOWN),
            FadeIn(bottom_open_tex, shift = 0.1 * DOWN),
            FadeIn(bottom_close_tex, shift = 0.1 * DOWN),
            run_time = 0.9,
        )

        # Reveal RHS 
        bottom_rhs = MathTex(r"\approx \mathrm{length}(\text{file})")
        bottom_rhs.next_to(bottom_close_tex, RIGHT, buff = 0.18).match_y(bottom_code)
        
        self.play(FadeIn(bottom_rhs, shift = 0.1 * DOWN))

        bottom_equation = VGroup(bottom_C_tex, bottom_open_tex, bottom_code, bottom_close_tex, bottom_rhs)
        self.play(bottom_equation.animate.scale(1.15).align_to(top_group, LEFT).to_edge(DOWN, buff = 1), run_time = 0.8)

        bottom_yellow_text = MarkupText('<i>"Perfectly incompressible"</i>', color = YELLOW).scale(0.6).next_to(bottom_rhs, DOWN, buff = 0.15).align_to(bottom_rhs, LEFT)
        self.play(FadeIn(bottom_yellow_text, shift = 0.1 * UP), run_time = 0.6)

from manim import *
import numpy as np
import random
class Slider_C_Chart(Scene):
    def construct(self):
        # controls
        n_min, n_max = 0, 25 
        n_tracker = ValueTracker(n_min)

        # C(x↾n)/n vs n (0...25), y in [0,1] with 0% and 100% labels
        axes = Axes(
            x_range = [0, 25, 5],
            y_range = [0, 1, 0.25],
            x_length = 8.5, 
            y_length = 3.0,
            tips = False,
            axis_config = dict(stroke_width = 2),
        )

        title = MathTex(r"\underline{\text{Incompressibility along $x$}}", color = WHITE).next_to(axes, UP, buff = 0.5)

        # Axis labels
        x_label = axes.get_x_axis_label(MathTex("n"), edge = DOWN, direction = DOWN, buff = 0.25)
        y_label = axes.get_y_axis_label(
            MathTex(r"\frac{C(x \upharpoonright n)}{n}"),
            edge = LEFT, direction = LEFT, buff = 0.3
        )
        # y-axis labels
        y0 = MathTex(r"0\%").scale(0.6)
        y1 = MathTex(r"100\%").scale(0.6)
        y0.add_updater(lambda m: m.move_to(axes.c2p(0, 0))
                                .align_to(axes.y_axis, LEFT)
                                .shift(0.35 * LEFT))
        y1.add_updater(lambda m: m.move_to(axes.c2p(0, 1))
                                .align_to(axes.y_axis, LEFT)
                                .shift(0.72 * LEFT))

        self.add(y0, y1)

        # Heights during first pass
        xs = np.arange(0, 26) 
        ratios = [  1, 
                    1,
                    0.93,
                    0.87,
                    0.89,
                    0.96,
                    0.85,
                    0.86,
                    0.78,
                    0.83,
                    0.79,
                    0.7,
                    0.62,
                    0.58,
                    0.52,
                    0.49,
                    0.44,
                    0.41,
                    0.39,
                    0.37,
                    0.46,
                    0.49,
                    0.5,
                    0.55,
                    0.56,
                    0.55
                ]

        def graph_up_to_n():
            n = int(np.clip(n_tracker.get_value(), n_min, n_max))
            if n < 1:
                return VGroup() # draw nothing until n >= 1
            else:
                X = xs[ : n + 1] # draw exactly up to n
                Y = ratios[ : n + 1]
                return axes.plot_line_graph(X, Y, add_vertex_dots = False).set_stroke(YELLOW, 3)
            
        graph = always_redraw(graph_up_to_n)

        top = VGroup(title, axes, x_label, y_label, y0, y1, graph).to_edge(UP, buff = 0.6)

        # MIDDLE: x in TeX, with underbrace over first n bits
        bit_string = "01101011100000000000110010"
        lhs = MathTex("x = 0.")
        digits = VGroup(*[MathTex(ch) for ch in bit_string]).arrange(RIGHT, buff = 0.03)
        dots = MathTex(r"\ldots")
        mid_line = VGroup(lhs, digits, dots).arrange(RIGHT, buff = 0.12).next_to(top, DOWN, buff = 0.4)

        def first_n_group():
            # get n
            n = int(np.clip(n_tracker.get_value(), 0, len(digits)))
            # return all the digits' Mobjects to be wrapped in the underbrace
            return VGroup(*digits[:n])

        def make_brace():
            grp = first_n_group()
            if len(grp) == 0:
                dummy = Line(digits[0].get_left(), digits[0].get_left()+0.01*RIGHT).set_opacity(0)
                return Brace(dummy, DOWN, buff = 0.08).set_opacity(0)
            return Brace(grp, DOWN, buff = 0.08)

        brace = always_redraw(make_brace)
        brace_label = always_redraw(lambda:
            MathTex(r"x \upharpoonright {" + str(int(np.clip(n_tracker.get_value(), 0, n_max))) + r"}")
            .scale(0.9)
            .next_to(brace, DOWN, buff = 0.12)
        )

        middle = VGroup(mid_line, brace, brace_label)

        # layout & build
        layout = VGroup(top, middle).arrange(DOWN, buff = 0.5).move_to(ORIGIN)

        self.play(FadeIn(title), FadeIn(axes), FadeIn(x_label), FadeIn(y_label), FadeIn(y0), FadeIn(y1))
        self.play(FadeIn(graph))
        self.play(FadeIn(mid_line))
        self.play(FadeIn(brace), FadeIn(brace_label))

        # PHASE A: step n from 1 to 25
        for k in range(0, 26):
            self.play(n_tracker.animate.set_value(k), run_time = 0.12, rate_func = linear)

        self.wait(3)

        # Switch the brace to cover all bits with ellipses, having symbolic label x↾n
        full_brace = Brace(VGroup(*digits, dots), DOWN, buff = 0.08)
        sym_label = MathTex(r"x \upharpoonright n").scale(0.9).next_to(full_brace, DOWN, buff = 0.12)

        # brace & bracelabel previously set to always_redraw
        # replace them with static versions
        self.play(
            ReplacementTransform(brace, full_brace),
            ReplacementTransform(brace_label, sym_label)
        )

        # PHASE B axes: widen x-range to 0...300, cross-fade the plotting layer
        axes2 = Axes(
            x_range = [0, 300, 50],
            y_range = [0, 1, 0.25],
            x_length = axes.x_length,
            y_length = axes.y_length,
            tips = False,
            axis_config = dict(stroke_width = 2),
        )

        title2 = MathTex(r"\underline{\text{Incompressibility along $x$}}").next_to(axes2, UP, buff = 0.5)

        xlab2 = axes2.get_x_axis_label(MathTex("n"), edge = DOWN, direction = DOWN, buff = 0.25)
        ylab2 = axes2.get_y_axis_label(MathTex(r"\frac{C(x \upharpoonright n)}{n}"),
                                    edge = LEFT, direction = LEFT, buff = 0.3)

        # make the new graph driven by the same n_tracker
        xs2 = np.arange(0, 301) 
        ratios2 = []
        for i in range(0, 26):
            ratios2.append(ratios[i])
        for i in range(26, 301):
            ratios2.append(0.55 + (0.85 - 0.55) * (1 - math.exp(-(i + 300) / 300)) + random.gauss(0, 0.4 * math.exp(-(2 * i + 300) / 300)))

        ratio_vals = np.clip(ratios2, 0, 1)

        def graph2_fn():
            n = int(np.clip(n_tracker.get_value(), 1, 300))
            X = xs2[:n+1]
            Y = ratio_vals[:n+1]

            pts = [axes2.c2p(float(x), float(y)) for x, y in zip(X, Y)]
            # Ensure at least two points so the line is visible only when n >= 1
            if len(pts) < 2:
                return VGroup()

            line = VMobject()
            line.set_stroke(YELLOW, 3)
            line.set_points_smoothly(pts)
            return line

        graph2 = always_redraw(graph2_fn)

        # n_tracker.set_value(25)

        # keep the new stack where the old one was
        new_top = VGroup(title2, axes2, xlab2, ylab2, graph2)
        new_top.move_to(top) # top was the original top group position

        # cross-fade old to new
        self.play(
            FadeOut(VGroup(title, axes, x_label, y_label, graph)),
            FadeIn(new_top),
            run_time = 0.6
        )

        # y0 & y1 track the current axes
        # have to rebind their updaters
        for lab in (y0, y1):
            lab.clear_updaters()
        y0.add_updater(lambda m: m.move_to(axes2.c2p(0, 0))
                                .align_to(axes2.y_axis, LEFT).shift(0.35 * LEFT))
        y1.add_updater(lambda m: m.move_to(axes2.c2p(0, 1))
                                .align_to(axes2.y_axis, LEFT).shift(0.75 * LEFT))

        # Drive n from 25 to 300 (only the plot changes now)
        self.play(n_tracker.animate.set_value(300), run_time = 4.0, rate_func = smooth)

        self.wait()

class ChatBubble(VGroup):
    """Rounded rectangle + small triangular tail (no SpeechBubble dependency)."""
    def __init__(self, text, direction=RIGHT, width=3.8, height=1.2, font_size=26, **kwargs):
        super().__init__(**kwargs)
        box = RoundedRectangle(corner_radius=0.2, width=width, height=height)
        tail = Polygon(ORIGIN, 0.35*UP, 0.35*DOWN)
        if direction is RIGHT:
            tail.next_to(box, LEFT, buff=0).shift(0.15*DOWN)
        elif direction is LEFT:
            tail.next_to(box, RIGHT, buff=0).shift(0.15*UP)
        elif direction is UP:
            tail.next_to(box, DOWN, buff=0).rotate(PI/2)
        else:  # DOWN
            tail.next_to(box, UP, buff=0).rotate(-PI/2)

        tail.match_style(box)
        tail.set_fill(opacity=1.0)
        label = Text(text, font_size=font_size).move_to(box.get_center())
        self.add(box, tail, label)

class FlatWorld(ThreeDScene):
    def construct(self):
        plane = NumberPlane(
            x_range = [-7, 7, 1],
            y_range = [-4, 4, 1],
            background_line_style = {"stroke_opacity" : 0.20, "stroke_width" : 1.2},
        )
        plane.set_z_index(-5)
        self.add(plane)

        self.set_camera_orientation(phi = 0 * DEGREES, theta = 0 * DEGREES, zoom = 1.0)

        sq = Square(side_length = 1.6, color = BLUE, fill_opacity = 0.85)
        self.play(FadeIn(sq, scale = 0.7))
        self.play(
            sq.animate.move_to(2.5 * RIGHT + 1.2 * UP),
            Rotate(sq, angle = TAU * 2, about_point = ORIGIN),
            run_time = 2.2,
            rate_func = rate_functions.ease_in_out_sine,
        )
        self.play(
            sq.animate.move_to(ORIGIN),
            Rotate(sq, angle = TAU * 1.5, about_point = sq.get_center()),
            run_time = 2.0,
            rate_func = rate_functions.ease_in_out_sine,
        )
        self.wait(0.3)

        # show flatness
        self.move_camera(
            phi = 60 * DEGREES, theta = 90 * DEGREES, zoom = 0.95,
            run_time = 1.8, rate_func=rate_functions.ease_in_out_quad
        )
        self.move_camera(
            phi = 60 * DEGREES, theta = 70 * DEGREES, zoom = 0.95,
            run_time = 1.6, rate_func = rate_functions.ease_in_out_quad
        )
        self.wait(0.4)

class DimensionLadderExtrude(ThreeDScene):
    def create_menger_sponge(self, n, size = 2, center = ORIGIN):
        if n == 0:
            # Base case: return a single cube
            cube = Cube(side_length = size, fill_opacity = 0.8)
            cube.move_to(center)
            return VGroup(cube)
        
        # Recursive case: create 20 smaller cubes
        sponge_group = VGroup()
        new_size = size / 3
        
        # Generate all 27 possible positions in a 3 x 3 x 3 grid
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    # Skip the 7 positions that should be removed:
                    skip_positions = [
                        (1, 1, 1), # Center
                        (1, 1, 0), (1, 1, 2), # Front/back face centers
                        (1, 0, 1), (1, 2, 1), # Top/bottom face centers  
                        (0, 1, 1), (2, 1, 1), # Left/right face centers
                    ]
                    if (i, j, k) in skip_positions:
                        continue
                    
                    # Calculate position of this sub-cube
                    offset = np.array([
                        (i - 1) * new_size,
                        (j - 1) * new_size, 
                        (k - 1) * new_size
                    ])
                    new_center = center + offset
                    
                    # Recursively create sub-sponge
                    sub_sponge = self.create_menger_sponge(n - 1, new_size, new_center)
                    sponge_group.add(sub_sponge)
        
        return sponge_group
    
    def construct(self):
        S = 3.0 # final side length
        PHI0 = 60 * DEGREES # slight overhead
        THETA0 = -90 * DEGREES # your preferred azimuth
        ROT_RATE = 0.12 # slow ambient spin
        COLOR = BLUE # unified color

        self.set_camera_orientation(phi = PHI0, theta = THETA0, zoom = 1.0)
        self.begin_ambient_camera_rotation(rate = ROT_RATE)

        LABEL_POS = 3.2 * UP 

        def make_label(t): # create a HUD label (not in 3D space)
            return MathTex(t, font_size = 64).move_to(LABEL_POS)

        label = make_label(r"0\text{D}") # initial label
        self.add_fixed_in_frame_mobjects(label) # fix label to screen

        def update_label(t): 
            new = make_label(t)
            self.play(Transform(label, new), run_time = 0.3)

        # 0D: large hollow circle to dot
        ring = Circle(radius = 0.3, color = COLOR, stroke_width = 14).set_fill(opacity = 0.0)
        self.play(FadeIn(ring))
        
        dot = Dot(radius = 0.08, color = COLOR)
        self.play(ReplacementTransform(ring, dot), run_time = 0.6)
        self.wait(2)

        # 1D: sweep point to line segment
        L = ValueTracker(0.0) # length

        line = always_redraw(
            lambda: Line(
                start = LEFT * (L.get_value() / 2),
                end = RIGHT * (L.get_value() / 2),
                color = COLOR,
                stroke_width = 10,
            )
        )

        self.add(line)
        self.play(
            L.animate.set_value(S),
            FadeOut(dot, scale = 0.5),
            run_time = 1.8,
            rate_func = rate_functions.ease_in_out_sine,
        )
        update_label(r"1\text{D}")
        self.wait(0.3)

        # 2D: sweep line to square
        H = ValueTracker(0.0) # height

        square_fill = always_redraw(
            lambda: Rectangle(
                width = S,
                height = max(H.get_value(), 1e-3),
                stroke_width = 0,
                fill_opacity = 0.95,
                color = COLOR,
                fill_color = COLOR,
            )
        )

        self.add(square_fill)
        self.play(
            H.animate.set_value(S),
            line.animate.set_opacity(0.0),
            run_time = 1.8,
            rate_func = smooth,
        )
        self.remove(line)
        update_label(r"2\text{D}")
        self.wait(0.4)

        # 3D: sweep square to cube
        D = ValueTracker(1e-3) # depth

        prism = always_redraw(
            lambda: Prism(
                dimensions = (S, S, max(D.get_value(), 1e-3))
            ).set_fill(COLOR, opacity = 0.95).set_stroke(width = 0)
        )

        self.add(prism)
        self.remove(square_fill)
        self.play(
            D.animate.set_value(S),
            run_time = 2.0,
            rate_func = rate_functions.ease_in_out_sine,
        )
        update_label(r"3\text{D}")

        self.wait(2)

        footer = MathTex(r"\text{geometric dimension}", font_size = 64).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(footer)
        self.play(Write(footer), run_time = 1)
        self.wait(3)
        self.play(FadeOut(label, footer, prism), run_time = 0.5)

        # Menger Sponge
        menger = MathTex(r"\text{Menger sponge}", font_size = 64).to_edge(UP)
        # footer2 = MathTex(r"\text{fractal dimension}", font_size = 64).to_edge(DOWN)
        note = MathTex(r"\operatorname{dim}_{\operatorname{fractal}} = \frac{\log 20}{\log 3} \approx 2.7268", font_size = 50).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(menger)
        sponge = self.create_menger_sponge(n = 3, size = S)
        sponge.set_color(BLUE)
        self.play(FadeIn(sponge), Write(menger))
        self.wait(5)
        # self.add_fixed_in_frame_mobjects(footer2)
        # self.play(Write(footer2))
        # self.wait(2)
        self.add_fixed_in_frame_mobjects(note)
        self.play(Write(note))
        self.wait(3)
        self.play(FadeOut(sponge, menger, note), run_time = 0.5)

        # Start the zooming in and question
        self.stop_ambient_camera_rotation()

        cube_obj = Cube(side_length = S).set_fill(COLOR, opacity = 0.95).set_stroke(width = 0)
        self.play(FadeIn(cube_obj), run_time = 0.6)

        # Picking a point on the top face (z = S / 2) and slightly offset in x-y
        p = 0.6 * (S / 2) * LEFT + 0.25 * (S / 2) * UP + (S / 2 + 0.01) * OUT
        marker = Sphere(radius = 0.02).set_fill(RED, opacity = 1.0).set_stroke(width = 0).move_to(p)
        self.play(FadeIn(marker), run_time = 0.6)
        self.wait(0.5)

        # Pan the cube so the chosen point moves to the screen center and zoom in
        # focus = VGroup(cube_obj, marker)
        self.play(
            cube_obj.animate.shift(-p),
            marker.animate.shift(-p),
            run_time = 0.5,
            rate_func = rate_functions.ease_in_out_sine,
        )
        self.move_camera(zoom = 11, run_time = 1.2, rate_func = rate_functions.ease_in_out_quad)
        self.wait(4)

        # Go back
        self.move_camera(zoom = 1.0, run_time = 1.2, rate_func = rate_functions.ease_in_out_quad)
        self.play(
            cube_obj.animate.shift(p),
            marker.animate.shift(p),
            run_time = 0.5,
            rate_func = rate_functions.ease_in_out_sine,
        )
        self.play(FadeOut(marker), run_time = 0.5)
        self.wait(0.5)

        question = MathTex(r"\text{Is dimension only a \textit{macroscopic} property?}", font_size = 50).to_edge(UP)
        self.add_fixed_in_frame_mobjects(question)
        self.play(Write(question), run_time = 1)
        self.wait(3)
        self.play(FadeOut(question), run_time = 0.5)

def PTS_statement(Scene):
    def construct(self): 
        formula = MathTex(r"\operatorname{dim}_{\operatorname{fractal}}(S) = \max_{x \in S} \operatorname{dim}(x) = \max_{x \in S} \lim_{n \to \infty} \frac{C(x \upharpoonright n)}{n}", font_size = 50).to_edge(UP)
        asterisk = MathTex(r" ^*")
        self.play(Write(formula), run_time = 1)

        self.wait(3)
        self.play(FadeOut(formula), run_time = 0.5)
        self.wait(1)
