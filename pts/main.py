from manim import *
import math
import numpy as np
import random
import re
from fractions import Fraction

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

# Some titles
class all_text(Scene):
    def construct(self):
        section_titles = ['Geometric Dimension', 'Compression', 'Dimension from Compression']
        formulas = [
            {
                'title': 'Point-to-Set Principle',
                'math': r'\operatorname{dim}_{\operatorname{fractal}}(S) = \max_{x \in S} \operatorname{dim}(x) = \max_{x \in S} \lim_{n \to \infty} \frac{C(x \upharpoonright n)}{n}',
            },
            {
                'title': 'Effective dimension',
                'math': r'\operatorname{dim}(x) = \lim_{n \to \infty} \frac{C(x \upharpoonright n)}{n}',
            }
        ]

        write_speed = 0.75
        self.wait(2)
        for s in section_titles:
            T = Tex(s, font_size = 64)
            self.play(Write(T), run_time = write_speed)
            self.wait(2)
            self.play(Unwrite(T), run_time = write_speed)
            self.wait(2)

        self.wait(2)
        for s in formulas:
            T = Tex(s['title'], font_size = 64).move_to(UP * 2)
            M = MathTex(s['math'], font_size = 45)
            self.play(Write(T), Write(M), run_time = write_speed)
            self.wait(5)
            self.play(Unwrite(T), Unwrite(M), run_time = write_speed)
            self.wait(2)

        write_speed = 0.75
        self.wait(2)
        T = Tex("Example: the Cantor Set", font_size = 64)
        self.play(Write(T), run_time = write_speed)
        self.wait(2)
        self.play(Unwrite(T), run_time = write_speed)
        self.wait(2)

###### INTRODUCITON + GEOMETRIC DIMENSION #######

# What's the fractal dimension of the Cantor set? 
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
        question = Tex(r"$1$D? ... $0$D?", font_size = 50)
        note = MathTex(r"\operatorname{dim}_{\operatorname{fractal}}(\text{Cantor}) = \frac{\log 2}{\log 3} \approx 0.6309", font_size = 50)
        G = VGroup(question, note).arrange(RIGHT, buff = 1.2).move_to(2 * DOWN)

        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(5)
        self.add_fixed_in_frame_mobjects(question)
        self.play(Write(question))
        self.wait(2)
        self.add_fixed_in_frame_mobjects(note)
        self.play(Write(note))
        self.wait(3)
        self.play(FadeOut(VGroup(*blocks), title, question, note), run_time = 1)

# Initial flatworld scene
class FlatWorld(ThreeDScene):
    def construct(self):
        plane = NumberPlane(
            x_range = [-7, 7, 1],
            y_range = [-4, 4, 1],
            background_line_style = {"stroke_opacity" : 0.20, "stroke_width" : 1.2},
        )
        plane.set_z_index(-5)
        self.add(plane)

        self.set_camera_orientation(phi = 0 * DEGREES, theta = -90 * DEGREES, zoom = 1.0)

        # Create the main square
        sq = Square(side_length = 1.6, color = BLUE, fill_opacity = 0.85)
        
        # Create facial features as cut-outs (negative space)
        # Two circular eyes
        left_eye = Circle(radius = 0.12, color = BLACK, fill_opacity = 1.0)
        left_eye.move_to(sq.get_center() + LEFT * 0.25 + UP * 0.15)
        
        right_eye = Circle(radius = 0.12, color = BLACK, fill_opacity = 1.0)
        right_eye.move_to(sq.get_center() + RIGHT * 0.25 + UP * 0.15)
        
        # D-shaped smile using an arc
        smile = Arc(
            radius = 0.3,
            angle = PI,
            start_angle = PI,
            color = BLACK,
            stroke_width = 8
        )
        smile.move_to(sq.get_center() + DOWN * 0.3)
        
        # Group the square with its facial features
        face = VGroup(sq, left_eye, right_eye, smile)
        
        self.play(FadeIn(face, scale = 0.7))
        
        # Define a wiggly parameterized loop path
        def wiggly_path(t):
            # t goes from 0 to 1 for a complete loop
            # Create a figure-8 like curve with some wiggliness
            x = 2.5 * np.sin(2 * PI * t) * np.cos(PI * t) + 0.3 * np.sin(8 * PI * t)
            y = 1.5 * np.sin(4 * PI * t) + 0.2 * np.cos(12 * PI * t) * t
            return np.array([x, y, 0])
        
        def rotation_func(t):
            # Rotate smoothly along the path with some extra wiggles
            return 1 * PI * t + 0.5 * np.sin(6 * PI * t)
        
        # Store initial position and rotation
        initial_pos = face.get_center()
        initial_angle = 0
        
        # Animate along the wiggly path
        def update_face(mob, alpha):
            # Get position along the curve
            new_pos = wiggly_path(alpha)
            # Get rotation at this point
            new_angle = rotation_func(alpha)
            
            # Reset to initial state, then apply transformations
            mob.move_to(initial_pos)
            mob.rotate(-face.angle)  # Reset rotation
            mob.rotate(new_angle)    # Apply new rotation
            mob.shift(new_pos)       # Apply position offset
            
            # Store current angle for next reset
            face.angle = new_angle
            
        # Initialize angle tracking
        face.angle = 0
        
        self.play(
            UpdateFromAlphaFunc(face, update_face),
            run_time = 4.0,
            rate_func = rate_functions.ease_in_out_quad
        )

        # show flatness
        self.move_camera(
            phi = 60 * DEGREES, theta = 90 * DEGREES, zoom = 0.95,
            run_time = 1.8, rate_func = rate_functions.ease_in_out_quad
        )
        self.move_camera(
            phi = 60 * DEGREES, theta = -90 * DEGREES, zoom = 0.95,
            run_time = 6, rate_func = rate_functions.ease_in_out_quad
        )

        self.wait(2)

# Part of the intro for geometric dimension
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
        S = 3.0 
        PHI0 = 60 * DEGREES 
        THETA0 = -90 * DEGREES 
        ROT_RATE = 0.12 
        COLOR = BLUE

        self.set_camera_orientation(phi = PHI0, theta = THETA0, zoom = 1.0)
        self.begin_ambient_camera_rotation(rate = ROT_RATE)

        LABEL_POS = 3.2 * UP 

        def make_label(t): # create a HUD label
            return MathTex(t, font_size = 64).move_to(LABEL_POS)

        label = make_label(r"0\text{D}") 
        self.add_fixed_in_frame_mobjects(label)

        def update_label(t): 
            new = make_label(t)
            self.play(Transform(label, new), run_time = 0.3)

        # 0D
        ring = Circle(radius = 0.3, color = COLOR, stroke_width = 14).set_fill(opacity = 0.0)
        self.play(FadeIn(ring))
        
        dot = Dot(radius = 0.08, color = COLOR)
        self.play(ReplacementTransform(ring, dot), run_time = 0.6)
        self.wait(2)

        # 1D
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

        # 2D
        H = ValueTracker(0.0)

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

        # 3D
        D = ValueTracker(1e-3)

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
        note = MathTex(r"\operatorname{dim}_{\operatorname{fractal}}(\text{Menger}) = \frac{\log 20}{\log 3} \approx 2.7268", font_size = 45).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(menger)
        sponge = self.create_menger_sponge(n = 3, size = S)
        sponge.set_color(BLUE)
        self.play(FadeIn(sponge), Write(menger))
        self.wait(5)
        self.add_fixed_in_frame_mobjects(note)
        self.play(Write(note))
        self.wait(3)
        self.play(FadeOut(sponge, menger, note), run_time = 0.5)

        self.stop_ambient_camera_rotation()

        cube_obj = Cube(side_length = S).set_fill(COLOR, opacity = 0.95).set_stroke(width = 0)
        self.play(FadeIn(cube_obj), run_time = 0.6)

        # Picking a point on the top face (z = S / 2) and slightly offset in x-y
        p = 0.6 * (S / 2) * LEFT + 0.25 * (S / 2) * UP + (S / 2 + 0.01) * OUT
        marker = Sphere(radius = 0.02).set_fill(RED, opacity = 1.0).set_stroke(width = 0).move_to(p)
        self.play(FadeIn(marker), run_time = 0.6)
        self.wait(0.5)

        # Pan the cube so the chosen point moves to the screen center and zoom in
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

# Need a scene to explain fractal dimension. Table + definition of fractal dimension as the "appropriate exponent" for a shape
class DimensionTable3D(ThreeDScene):
    def construct(self):

        BLUE_FILL = BLUE_D 
        BLUE_EDGE = BLUE_B 

        def stylize(m):
            m.set_fill(BLUE_FILL, opacity = 1)
            m.set_stroke(BLUE_EDGE, width = 2, opacity = 1)
            return m

        DOT = Tex("\vdots").set_opacity(0).set_stroke(width = 0)

        cells = [
            [Tex(r"Dimension"), Tex(r"0D"), Tex(r"1D"), Tex(r"2D"), Tex(r"3D")],
            [Tex(r"Shape"), DOT.copy(), DOT.copy(), DOT.copy(), DOT.copy()],
            [Tex(r"Size"), DOT.copy(), MathTex(r"\text{Length} = \ell^{{1}}"), MathTex(r"\text{Area} = \ell^{{2}}"), MathTex(r"\text{Volume} = \ell^{{3}}")],
            [Tex(r"Shape"), DOT.copy(), DOT.copy(), DOT.copy(), DOT.copy()],
            [Tex(r"Size"), DOT.copy(), MathTex(r"\text{Length} = 2r^{{1}}"), MathTex(r"\text{Area} = \pi r^{{2}}"), MathTex(r"\text{Volume} = \tfrac{4}{3}\,\pi r^{{3}}")]
        ]

        tbl = MobjectTable(
            cells,
            include_outer_lines = True,
            line_config = {"stroke_color": WHITE, "stroke_width": 2},
            v_buff = 0.35, h_buff = 0.6,
        ).scale(0.9)

        self.add_fixed_in_frame_mobjects(tbl)
        self.play(FadeIn(tbl))
        self.wait(0.2)

        # --- Helpers ---
        def place_in_cell(mobj: Mobject, row: int, col: int, scale=1.0, pad=0.75):
            target = tbl.get_cell((row, col))
            max_w = target.width * pad
            max_h = target.height * pad
            if mobj.width > max_w:
                mobj.scale(max_w / mobj.width)
            if mobj.height > max_h:
                mobj.scale(max_h / mobj.height)
            if scale != 1.0:
                mobj.scale(scale)
            mobj.move_to(target.get_center())
            return mobj

        def shade2d(m: Mobject):
            if hasattr(m, "set_shade_in_3d"):
                m.set_shade_in_3d(True)
            return m
        point_l = stylize(shade2d(Sphere(radius = 0.08, resolution = (16, 16))))
        line_l = Line3D(0.8 * LEFT, 0.8 * RIGHT, thickness = 0.06, color = BLUE_FILL)
        line_l.set_stroke(BLUE_EDGE, width = 1, opacity = 1)
        square = stylize(shade2d(Square(side_length = 1.35)))
        cube = stylize(Cube(side_length = 1.15))

        place_in_cell(point_l, 2, 2)
        place_in_cell(line_l, 2, 3)
        place_in_cell(square, 2, 4)
        place_in_cell(cube, 2, 5)

        self.play(GrowFromCenter(point_l))
        self.play(FadeIn(line_l))
        self.play(FadeIn(square))
        self.play(FadeIn(cube))
        self.wait(0.4)

        point_r = stylize(shade2d(Sphere(radius=0.08, resolution=(16, 16))))
        line_r = Line3D(0.8 * LEFT, 0.8 * RIGHT, thickness=0.06, color=BLUE_FILL)
        line_r.set_stroke(BLUE_EDGE, width=1, opacity=1)

        disk = stylize(Cylinder(radius=0.72, height=0.06, direction=OUT, resolution=28))
        ball = stylize(Sphere(radius=0.68, resolution=(32, 32)))

        place_in_cell(point_r, 4, 2)
        place_in_cell(line_r, 4, 3)
        place_in_cell(disk, 4, 4)
        place_in_cell(ball, 4, 5)

        self.play(GrowFromCenter(point_r))
        self.play(FadeIn(line_r))
        self.play(FadeIn(disk))
        self.play(FadeIn(ball))

        self.wait(4)

        table_group = VGroup(*[mob for mob in self.mobjects if isinstance(mob, VMobject)])

        self.play(table_group.animate.scale(0.8).shift(UP))

        self.wait(0.5)

        m = VGroup(
            Tex(r"Every shape has a corresponding \textit{exponent}.", font_size = 40),
            Tex(r"The exponent captures how its total size grows under scaling.", font_size = 40)
        ).arrange(DOWN, buff = 0.5).move_to(DOWN * 2)

        m.set_z_index(20)

        background = SurroundingRectangle(
            m,
            color = GOLD,
            fill_color = DARK_BLUE,
            fill_opacity = 0.3,
            buff = 0.4,
            stroke_width = 4,
            corner_radius = 0.1
        )

        self.play(AnimationGroup(Create(background), Write(m), lag_ratio = 0.3))

        self.wait(6)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

###### COMPRESSION #######

# Compressing a simple file
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

        # Remove everything... too many objects
        self.play(*[FadeOut(mob) for mob in self.mobjects])

# Compressing a random file
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

        # Remove everything... too many objects
        self.play(*[FadeOut(mob) for mob in self.mobjects])

# Taking C of a text file
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

        self.wait(2)

        # Remove everything... too many objects
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        T = MathTex(r"\underline{\text{Kolmogorov complexity}}", font_size = 64).move_to(UP * 2)
        M = MathTex(r'C(\text{data})', font_size = 64).next_to(T, DOWN, buff = 0.8)
        integer = MathTex(r'\in \mathbb{N}', font_size = 64).next_to(M, RIGHT)
        group = VGroup(M, integer)
        self.play(Write(T), Write(M), Write(integer), run_time = 0.75)
        self.wait(2)
        description = MarkupText('<i>"The minimal length the data may be compressed to."</i>', color = YELLOW).scale(0.6).next_to(group, DOWN, buff = 0.35)
        self.play(FadeIn(description, shift = 0.1 * UP), run_time = 0.6)
        self.wait(2)
        self.play(integer.animate.scale(1.12), run_time = 0.25)
        self.play(integer.animate.scale(1 / 1.12), run_time = 0.25)
        self.wait(5)
        self.play(Unwrite(T), Unwrite(M), Unwrite(integer), Unwrite(description), run_time = 0.75)
        self.wait(2)

# For making the chart for normalized kolmogorov complexity
class Slider_C_Chart(Scene):
    def construct(self):
        n_min, n_max = 0, 25 
        n_tracker = ValueTracker(n_min)

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
                dummy = Line(digits[0].get_left(), digits[0].get_left() + 0.01 * RIGHT).set_opacity(0)
                return Brace(dummy, DOWN, buff = 0.08).set_opacity(0)
            return Brace(grp, DOWN, buff = 0.08)

        brace = always_redraw(make_brace)
        brace_label = always_redraw(lambda:
            MathTex(r"x \upharpoonright {" + str(int(np.clip(n_tracker.get_value(), 0, n_max))) + r"}")
            .scale(0.9)
            .next_to(brace, DOWN, buff = 0.12)
        )

        middle = VGroup(mid_line, brace, brace_label)

        layout = VGroup(top, middle).arrange(DOWN, buff = 0.5).move_to(ORIGIN)

        self.play(FadeIn(title), FadeIn(axes), FadeIn(x_label), FadeIn(y_label), FadeIn(y0), FadeIn(y1))
        self.play(FadeIn(graph))
        self.play(FadeIn(mid_line))
        self.play(FadeIn(brace), FadeIn(brace_label))

        # PHASE A: step n from 1 to 25
        for k in range(0, 26):
            self.play(n_tracker.animate.set_value(k), run_time = 0.12, rate_func = linear)

        self.wait(3)

        full_brace = Brace(VGroup(*digits, dots), DOWN, buff = 0.08)
        sym_label = MathTex(r"x \upharpoonright n").scale(0.9).next_to(full_brace, DOWN, buff = 0.12)

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
        ylab2 = axes2.get_y_axis_label(MathTex(r"\frac{C(x \upharpoonright n)}{n}"), edge = LEFT, direction = LEFT, buff = 0.3)

        xs2 = np.arange(0, 301) 
        ratios2 = []
        random.seed(42)
        for i in range(0, 26):
            ratios2.append(ratios[i])
        for i in range(26, 301):
            ratios2.append(0.55 + (0.85 - 0.55) * (1 - math.exp(-(i + 300) / 300)) + random.gauss(0, 0.4 * math.exp(-(2 * i + 300) / 300)))
        ratio_vals = np.clip(ratios2, 0, 1)

        def graph2_fn():
            n = int(np.clip(n_tracker.get_value(), 1, 300))
            X = xs2[: n + 1]
            Y = ratio_vals[: n + 1]

            pts = [axes2.c2p(float(x), float(y)) for x, y in zip(X, Y)]
            # Ensure at least two points so the line is visible only when n >= 1
            if len(pts) < 2:
                return VGroup()

            line = VMobject()
            line.set_stroke(YELLOW, 3)
            line.set_points_smoothly(pts)
            return line

        graph2 = always_redraw(graph2_fn)

        new_top = VGroup(title2, axes2, xlab2, ylab2, graph2)
        new_top.move_to(top) 

        # cross-fade old to new
        self.play(
            FadeOut(VGroup(title, axes, x_label, y_label, graph)),
            FadeIn(new_top),
            run_time = 0.6
        )

        # n from 25 to 300
        self.play(n_tracker.animate.set_value(300), run_time = 4.0, rate_func = smooth)

        as_y = 0.8
        start_point = axes2.c2p(0, as_y)
        end_point = axes2.c2p(300, as_y)
        
        asymptote = DashedLine(
            start = start_point,
            end = end_point,
            color = WHITE,
            stroke_width = 7,
            dash_length = 0.2 
        )
        self.play(Create(asymptote), run_time = 1.5)
        self.wait()

        label = MathTex(rf"\operatorname{{dim}}(x) \approx {as_y}", color = WHITE)
        label.next_to(asymptote, DOWN, buff = 0.5)
        label.shift(RIGHT * 2.5) 
        
        self.play(Write(label))

        self.wait(3)

        self.play(*[FadeOut(mob) for mob in self.mobjects])

# Need another scene that assures the audience that no matter the formalism for Turing machines, get same notion.
class Explain_Algorithms(Scene):
    def construct(self):
        code2 = Code(
            code_string = '''
print(s)
''',
            background = "window",
            paragraph_config = {"font_size": 30},
            add_line_numbers = False
        )

        prompt = Tex(r"Given a target string \texttt{s}:", font_size = 60, color = WHITE).move_to(2 * UP)
        
        self.play(Write(prompt, run_time = 0.7))
        self.wait(1)

        self.play(Create(code2))
        self.wait()
        self.play(code2.animate.shift(0.5 * UP))

        conclusion = MathTex(r"C(\texttt{s}) \leq \operatorname{length}(\texttt{s}) + \text{constant}", font_size = 60, color = WHITE).move_to(2 * DOWN)
        arrow = Arrow([0, code2.get_bottom()[1], 0], [0, conclusion.get_top()[1], 0], stroke_width = 5, color = WHITE)

        self.play(AnimationGroup(GrowArrow(arrow), Write(conclusion), lag_ratio = 1), run_time = 2)
        self.wait(2)

        G = VGroup(prompt, code2, arrow, conclusion)
        self.play(G.animate.shift(2 * UP), FadeOut(prompt, shift = 2 * UP))

        conclusion2 = VGroup(
                        Tex(r"Normalized complexity: ", font_size = 60, color = WHITE),   
                        MathTex(r"\frac{C(\texttt{s})}{\operatorname{length}(\texttt{s})}", font_size = 60, color = WHITE)
                      ).arrange(RIGHT, buff = 0.4).move_to(2.3 * DOWN)
        arrow2 = Arrow(conclusion.get_bottom(), conclusion2.get_top() + 0.5 * DOWN, stroke_width = 5, color = WHITE)
        
        self.play(AnimationGroup(GrowArrow(arrow2), Write(conclusion2), lag_ratio = 1), run_time = 2)
        self.wait(3)
        
        self.play(FadeOut(conclusion2[0]), conclusion2[1].animate.move_to([0, conclusion2[0].get_y() - 0.5, 0]))
        
        self.wait(4)

        self.play(*[FadeOut(mob) for mob in self.mobjects])

# What is an algorithm?
class Use_Python(Scene):
    def construct(self):

        label = Tex("What is an algorithm?", font_size = 64)
        self.play(Write(label), run_time = 0.7)
        self.wait(2)
        self.play(Unwrite(label), run_time = 0.7)

        self.wait(2)

        code = Code(
            code_string = '''
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
    
print(factorial(10))
''',
            background = "window",
            paragraph_config = {"font_size": 30},
            add_line_numbers = True
        )
        self.play(Create(code), run_time = 1.5)

        self.wait(2)
        
        self.play(AnimationGroup(ShrinkToCenter(code)))
        self.wait(1)

# View numbers as files
class Numbers_As_Files(Scene):
    def construct(self):
        title = Tex("Real numbers have infinite binary expansions:", font_size = 64).move_to(2 * UP)
        self.play(Write(title), run_time = 0.75)

        # --- Phase 1: a couple of example lines (π, e) ---
        examples = VGroup(
            MathTex(r"1", "=", r"1.00000\cdots", "=", r"(1.0000000000\cdots)_2", substrings_to_isolate=["="]),
            MathTex(r"\pi", "=", r"3.14159\cdots", "=", r"(11.0010010000\cdots)_2", substrings_to_isolate=["="]),
            MathTex(r"e", "=", r"2.71828\cdots", "=", r"(10.1011011111\cdots)_2", substrings_to_isolate=["="])
        ).arrange(DOWN, aligned_edge = LEFT, buff = 0.5)

        # Lightly tint the equals signs to emphasize alignment
        anchor_x = examples[0].get_parts_by_tex("=")[0].get_center()[0]
        for m in examples:
            for eq in m.get_parts_by_tex("="):
                eq.set_color(GREY_B)
            # align first "=" across lines
            dx = anchor_x - m.get_parts_by_tex("=")[0].get_center()[0]
            m.shift(RIGHT * dx)

        for m in examples:
            self.play(Write(m))
            self.wait(0.2)

        self.wait(0.6)

        self.play(
            FadeOut(examples, shift = DOWN, lag_ratio = 0.05),
            FadeOut(title, shift = UP),
        )
        self.wait(0.2)

        left_expr = MathTex(r"x \;=\; 0.011010010\cdots", font_size = 56)

        dbl_arrow = MathTex(r"\longleftrightarrow", font_size = 56)

        bitstring = "011010010..."
        left_rendered_code = Code(
            code_string = bitstring,
            background = "window",
            background_config = {"fill_color": BLACK, "stroke_color": WHITE},
            paragraph_config = {"font_size": 30},
            add_line_numbers = False,
            formatter_style = "bw",
        ).scale(0.9)

        # Layout
        group = VGroup(left_expr, dbl_arrow, left_rendered_code).arrange(RIGHT, buff = 0.8)
        group.shift(1.5 * UP)
        self.play(Write(left_expr))
        self.play(
            FadeIn(dbl_arrow, shift = UP * 0.2),
            FadeIn(left_rendered_code, shift = RIGHT * 0.2),
        )
        self.wait(0.5)

        self.play(dbl_arrow.animate.scale(1.12), run_time = 0.25)
        self.play(dbl_arrow.animate.scale(1 / 1.12), run_time = 0.25)
        self.wait(2)

        left_copy = left_expr.copy()
        self.add(left_copy)
        self.play(left_copy.animate.shift(DOWN * 2))
        self.wait(0.2)
        new_left = MathTex(r"x \upharpoonright n \;=\; 0.\underbrace{0110100}_{n}10\cdots", font_size = 56).move_to(left_copy).shift(0.4 * LEFT + 0.4 * DOWN)
        self.play(Transform(left_copy, new_left))
        self.wait()

        question = Tex(r"What's $\frac{C(x \upharpoonright n)}{n}$ as $n \to \infty$?", font_size = 50)
        question.next_to(left_copy, RIGHT, buff = 0.7).shift(0.3 * UP)
        self.play(Write(question))

        self.wait(3)

        # Remove everything... too many objects
        self.play(*[FadeOut(mob) for mob in self.mobjects])

###### EFFECTIVE DIMENSION + PTS #######

# Might have to add some attributions to the PTS slide, as well as yellow text explaining in words
class PTS_Statement(Scene):
    def construct(self):

        m = VGroup(
            MathTex(r"\operatorname{dim}_{\operatorname{fractal}}(S)", font_size = 50, color = WHITE),
            MathTex(r"=", font_size = 50, color = WHITE),
            MathTex(r"\max_{x \in S} \operatorname{dim}(x)", font_size = 50, color = WHITE),
            MathTex(r"=", font_size = 50, color = WHITE),
            MathTex(r"\max_{x \in S} \lim_{n \to \infty} \frac{C(x \upharpoonright n)}{n}", font_size = 50, color = WHITE)
        ).arrange(RIGHT, buff = 0.5).move_to(2 * UP)
        m[2].shift(DOWN * 0.1)

        m.set_z_index(100)

        emphasize_list = [ 0, 2, 4 ]

        background = SurroundingRectangle(
            m,
            color = GOLD,
            fill_color = DARK_BLUE,
            fill_opacity = 0.3,
            buff = 0.4,
            stroke_width = 4,
            corner_radius = 0.1
        )

        label = Text("THE POINT-TO-SET PRINCIPLE", font_size = 24, color = GOLD, weight = BOLD)
        label.next_to(background, UP, buff = 0.2)

        bottom_label = Tex(r"\parbox{30cm}{J. Lutz and N. Lutz. \textit{Algorithmic information, plane Kakeya sets, and conditional dimension}. 2018.}", font_size = 14, color = WHITE)
        bottom_label2 = Tex(r"\parbox{30cm}{\textit{Notes}:", font_size = 14, color = WHITE)
        bottom_label3 = Tex(r"\parbox{30cm}{– We should really take the \textit{supremum} over $x \in S$,}", font_size = 14)
        bottom_label4 = Tex(r"\parbox{30cm}{– This statement only works for certain simple sets, $S$ which are $\Sigma^0_2$,}", font_size = 14)
        bottom_label5 = Tex(r"\parbox{30cm}{– The limit of the normalized Kolmogorov complexity may not exist.}", font_size = 14)

        bottom_label.scale(2).next_to(background, DOWN, aligned_edge = LEFT, buff = 0.3).shift(0.1 * RIGHT)
        bottom_label2.scale(2).next_to(bottom_label, DOWN, aligned_edge = LEFT, buff = 0.2)
        bottom_label3.scale(2).next_to(bottom_label2, DOWN, aligned_edge = LEFT, buff = 0.2).shift(RIGHT)
        bottom_label4.scale(2).next_to(bottom_label3, DOWN, aligned_edge = LEFT, buff = 0.2)
        bottom_label5.scale(2).next_to(bottom_label4, DOWN, aligned_edge = LEFT, buff = 0.2)

        self.play(Create(background), Write(m), FadeIn(label))
        self.play(AnimationGroup(Write(bottom_label), Write(bottom_label2), Write(bottom_label3), Write(bottom_label4), Write(bottom_label5), lag_ratio = 0.2))
        
        self.wait(2)

        for e in emphasize_list:
            self.play(m[e].animate.scale(1.1), run_time = 0.3)
            self.wait(0.2)
            self.play(m[e].animate.scale(1 / 1.1), run_time = 0.3)
            self.wait(2)

        explanation = Tex(r"\parbox{30cm}{A set's fractal dimension reflects the maximal effective dimension across its points.}", color = YELLOW, font_size = 35).move_to(2.5 * DOWN)
        explanation2 = Tex(r"\parbox{30cm}{That is, a set's dimension comes from its least compressible points.}", color = YELLOW, font_size = 35).next_to(explanation, DOWN, aligned_edge = LEFT)
        self.play(Write(explanation))
        self.wait()
        self.play(Write(explanation2))

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

# Why effective dimension is a dimension notion?
class EffectiveDimensionDyadic(Scene):
    LEFT_PANEL_WIDTH = 8.0
    GRID_HALF = 3.0
    MAX_LEVEL = 6

    def construct(self):
        left_group = VGroup()

        blob = self.make_blob().scale(1.1)
        blob.set_fill(color = BLUE_E, opacity = 0.35).set_stroke(BLUE_D, width = 6)
        blob_label = MathTex("S", font_size = 48).move_to(blob.get_center() + 0.6 * UP + 0.2 * RIGHT)

        blob_group = VGroup(blob, blob_label)
        left_group.add(blob_group)

        x_point = Dot(point=np.array([-0.78, -0.285, 0]), color = YELLOW, radius = 0.08)
        x_label = MathTex("x", font_size = 40).next_to(x_point, UP * 0.7 + RIGHT * 0.4)
        left_group.add(x_point, x_label)

        Q_label = MathTex("Q(x, n) = ")
        yellow_square = Square(0.2, fill_color = YELLOW, color = YELLOW).next_to(Q_label, RIGHT, buff = 0.2)
        Q_group = VGroup(Q_label, yellow_square).move_to(3.5 * DOWN)
        left_group.add(Q_group)

        frame_square = Square(side_length = 2 * self.GRID_HALF)
        frame_square.set_stroke(GREY_B, width = 1.5, opacity = 1.0)
        frame_square.move_to(blob.get_center())
        left_group.add(frame_square)

        ####### explanation
        fs = 36

        setup = Tex(r'Suppose $x \in S$ has largest $\operatorname{dim}(x)$.', font_size = fs)
        m = Tex(r'Notice $C(x \upharpoonright n) \approx C(Q(x, n))$.', font_size = fs)
        
        prompt = Tex(r'So, for any $n$, if $\frac{C(x \upharpoonright n)}{n} = d$,', font_size = fs)
        conclusion1 = Tex(r'$n$ bits of information determine $Q\left(x, \frac{n}{d}\right)$', font_size = fs)
        arrow1 = Arrow(conclusion1.get_top(), prompt.get_bottom(), stroke_width = 5)
        conclusion2 = Tex(r'$\therefore$ scaling $S$ by $2$ $\rightsquigarrow$ scaling $\operatorname{size}(S)$ by $2^d$.', font_size = fs)
        arrow2 = Arrow(conclusion2.get_top(), conclusion1.get_bottom(), stroke_width = 5)

        right_group = VGroup(setup, m, prompt, arrow1, conclusion1, arrow2, conclusion2).arrange(DOWN, aligned_edge = LEFT, buff = 0.4)
        arrow1.set_x(0)
        arrow2.set_x(0)
        right_group.to_edge(RIGHT, buff = 0.1)

        left_group.to_edge(LEFT, buff = 1)

        self.play(
            FadeIn(blob, shift = 0.2 * UP),
            FadeIn(blob_label),
            FadeIn(x_point, scale = 0.8),
            FadeIn(x_label),
            FadeIn(frame_square),
            FadeIn(Q_group), 
            Write(setup)
        )

        highlight = None
        for n in range(self.MAX_LEVEL + 1):
            # Build the grid for this level
            grid = self.make_dyadic_grid(n, frame_square)
            grid.set_stroke(GREY_D, width = 1.0, opacity = 0.8)

            # Compute and draw the highlighted square containing x
            cell = self.cell_containing_point(n, frame_square, x_point.get_center())
            cell.set_stroke(YELLOW, width = 6).set_fill(YELLOW, opacity = 0.18)

            # Update right-panel level indicator
            self.play(
                FadeIn(grid, lag_ratio = 0.02, run_time = 0.4)
            )

            # Replace previous highlight (if any) with the refined one
            if highlight is None:
                self.play(FadeIn(cell, run_time = 0.5))
            else:
                self.play(ReplacementTransform(highlight, cell, run_time = 0.3))

            # keep references for next loop
            highlight = cell

            self.wait(0.2)

            # If there is another level coming, fade this grid (but keep highlight until swapped)
            if n < self.MAX_LEVEL:
                self.play(FadeOut(grid, run_time = 0.3))

        self.wait(5)

        self.play(AnimationGroup(Write(m), Write(prompt), GrowArrow(arrow1), Write(conclusion1), GrowArrow(arrow2), Write(conclusion2), lag_ratio = 3), run_time = 20)
        
        self.wait(6)

        self.play(*[FadeOut(mob) for mob in self.mobjects])

    # HELPERS

    def make_blob(self) -> VMobject:
        pts = [
            [-2.9, -0.6, 0],
            [-2.1, -1.1, 0],
            [-1.0, -1.2, 0],
            [-0.2, -0.5, 0],
            [ 0.7, -1.3, 0],
            [ 1.6, -1.8, 0],
            [ 2.4, -0.4, 0],
            [ 1.7, 1.4, 0],
            [ 0.2, 1.9, 0],
            [-1.2, 1.0, 0],
            [-2.4, 0.2, 0],
            [-2.9, -0.2, 0],
        ]
        vm = VMobject()
        vm.set_points_smoothly([*map(np.array, pts), np.array(pts[0])])
        vm.close_path()
        return vm

    def make_dyadic_grid(self, n: int, frame_square: Square) -> VGroup:
        L = 2 * self.GRID_HALF
        step = L / (2 ** n)
        bl = frame_square.get_center() + np.array([-self.GRID_HALF, -self.GRID_HALF, 0])

        lines = VGroup()
        for i in range(2 ** n + 1):
            x = bl[0] + i * step
            lines.add(Line([x, bl[1], 0], [x, bl[1] + L, 0]))
        for j in range(2 ** n + 1):
            y = bl[1] + j * step
            lines.add(Line([bl[0], y, 0], [bl[0] + L, y, 0]))
        return lines

    def cell_containing_point(self, n: int, frame_square: Square, p: np.ndarray) -> Square:
        L = 2 * self.GRID_HALF
        step = L / (2 ** n)
        origin = frame_square.get_center() + np.array([-self.GRID_HALF, -self.GRID_HALF, 0])

        i = int(np.floor((p[0] - origin[0]) / step))
        j = int(np.floor((p[1] - origin[1]) / step))

        i = max(0, min((2 ** n) - 1, i))
        j = max(0, min((2 ** n) - 1, j))

        cx = origin[0] + (i + 0.5) * step
        cy = origin[1] + (j + 0.5) * step
        cell = Square(side_length=step).move_to([cx, cy, 0])
        return cell

###### EXAMPLE: CANTOR SET #######

# To apply the PTS principle to, say, the Cantor set, we'll need a couple slides. 
class CantorSetConstructionRed(Scene):
    DEPTH = 4
    BAR_HEIGHT = 2 
    LINE_Y = -3.0
    TERNARY_DIGITS = 5 
    DOT_SIZE = 0.1 
    TOTAL_WIDTH = 11.0
    X_BAR_LEN = 1.6
    INCLUDE_RED = True

    def construct(self):
        nl = NumberLine(
            x_range = [0, 1, 1 / 27],
            include_ticks = False, include_numbers = False,
            length = self.TOTAL_WIDTH,
        )
        nl.set_z_index(100) 

        ticks, labels = self.make_custom_ticks(nl)
        ticks.set_z_index(100)
        labels.set_z_index(100)
        self.add(nl, ticks, labels)

        y_bar = 0
        current_bars = VGroup(self.interval_rect(nl, 0.0, 1.0, y = y_bar))
        current_bars[0].set_z_index(20)
        self.play(GrowFromCenter(current_bars[0]))

        x_tracker = ValueTracker(0.5)
        x_bar = always_redraw(lambda:
            Line(
                nl.number_to_point(x_tracker.get_value()),
                nl.number_to_point(x_tracker.get_value()) + UP * self.X_BAR_LEN,
                stroke_width = 4, color = YELLOW
            )
        )

        x_eq = always_redraw(lambda:
            self.ternary_equation_tex(x_tracker.get_value(), self.TERNARY_DIGITS)
                .scale(0.8)
                .next_to(
                    VectorizedPoint(nl.number_to_point(x_tracker.get_value()) + UP * self.X_BAR_LEN),
                    UP + 0.6 * RIGHT, buff = 0.12
                )
        )

        x_bar.set_z_index(105)
        x_eq.set_z_index(105)

        for depth in range(self.DEPTH):
            split_anims = []
            new_bars = VGroup()
            stage_halves = [] 

            # Phase 1: split each bar into two half-width bars centered at ± w/4
            for bar in current_bars:
                cx, cy, _ = bar.get_center()
                w = bar.get_width()

                left_half = self.make_bar_at_width(w / 2, height = self.BAR_HEIGHT, center=[cx - w / 4, cy, 0])
                right_half = self.make_bar_at_width(w / 2, height = self.BAR_HEIGHT, center=[cx + w / 4, cy, 0],
                                                    color = bar.get_fill_color(), stroke = bar.get_stroke_color())

                left_half.set_z_index(20)
                right_half.set_z_index(20)

                split_anims.append(Transform(bar, left_half))
                split_anims.append(TransformFromCopy(bar, right_half))

                stage_halves.append((bar, right_half))  # references after the split

            self.play(AnimationGroup(*split_anims, lag_ratio = 0.06), run_time = 0.9)

            # Phase 2: shrink each half to third-width and slide to ± w/3 centers
            slide_anims = []
            red_anims = []
            red_labels = [r'.1', r'.\_1', r'.\_\_1', r'.\_\_\_1', r'.\_\_\_\_1']
            for left_bar, right_bar in stage_halves:
                cx, cy, _ = (left_bar.get_center() + right_bar.get_center())/2
                w_current = left_bar.get_width() * 2  # since each is half of previous

                left_third  = self.make_bar_at_width(w_current / 3, self.BAR_HEIGHT, [cx - w_current / 3, cy, 0],
                                                     color = left_bar.get_fill_color(), stroke = left_bar.get_stroke_color())
                right_third = self.make_bar_at_width(w_current / 3, self.BAR_HEIGHT, [cx + w_current / 3, cy, 0],
                                                     color = right_bar.get_fill_color(), stroke = right_bar.get_stroke_color())

                left_third.set_z_index(20)
                right_third.set_z_index(20)

                slide_anims += [Transform(left_bar, left_third), Transform(right_bar, right_third)]
                new_bars.add(left_bar, right_bar)

                if self.INCLUDE_RED:
                    red_third = self.make_bar_at_width(w_current / 3, self.BAR_HEIGHT, [cx, cy, 0],
                                                        color = RED_D, stroke = RED_E)
                    red_third.set_z_index(20)
                    x = cx / self.TOTAL_WIDTH + 0.5
                    vertical_spread = 0.45
                    red_line = Line(
                        nl.number_to_point(x) + DOWN * self.BAR_HEIGHT / 2,
                        nl.number_to_point(x) + DOWN * (self.X_BAR_LEN + depth * vertical_spread),
                        stroke_width = 4, color = WHITE
                    )
                    red_text = MathTex(red_labels[depth]).scale(0.8).move_to(
                        [cx, - 0.25 - self.X_BAR_LEN - depth * vertical_spread, 0]
                    )
                    red_label = VGroup(red_line, red_text)
                    red_label.set_z_index(100)
                    red_anims += [FadeIn(red_third), FadeIn(red_label)]

            self.play(AnimationGroup(*slide_anims, lag_ratio = 0.06), run_time = 0.9)
            if self.INCLUDE_RED:
                self.play(AnimationGroup(*red_anims, lag_ratio = 0.06), run_time = 1)
                self.wait(1)
            current_bars = new_bars

        if self.INCLUDE_RED:
            construction_group = VGroup(*[mob for mob in self.mobjects if isinstance(mob, VMobject)])
            self.play(FadeOut(construction_group))

            m = MathTex(
                r'x \in \text{Cantor} \longleftrightarrow \operatorname{ternary}(x) \text{ has no 1s}',
                font_size = 65,
                color = WHITE
            ).move_to(2 * UP)
            background = SurroundingRectangle(
                m,
                color = GOLD,
                fill_color=DARK_BLUE,
                fill_opacity = 0.3,
                buff = 0.4,
                stroke_width = 4,
                corner_radius = 0.1
            )

            label = Text("MAIN OBSERVATION", font_size = 24, color = GOLD, weight = BOLD)
            label.next_to(background, UP, buff = 0.2)
            self.play(Write(m), Create(background), FadeIn(label))

            x_label = MathTex(
                r'x = (0.220020020220222020\cdots)_3',
                font_size = 55,
                color = WHITE
            ).move_to(2 * DOWN)
            arrow = Arrow(
                background.get_bottom(), 
                x_label.get_top(),
                buff = 0.2,
                stroke_width = 4,
                color = GRAY_A
            )
            implication_anims = [GrowArrow(arrow), Write(x_label)]
            self.play(AnimationGroup(*implication_anims, lag_ratio = 0.3))

        else:
            self.play(FadeIn(VGroup(x_bar, x_eq), shift = UP * 0.1), run_time = 0.5)
            self.wait(0.5)
            self.play(x_tracker.animate.set_value(1 / 9 - 0.01), run_time = 1.0)
            self.wait(0.6)
            self.play(x_tracker.animate.set_value(5 / 9 + 0.013), run_time = 1.2)
            self.wait(0.6)
            self.play(x_tracker.animate.set_value(8 / 9 + 0.001), run_time = 0.9)
            self.wait(0.6)
            self.play(x_tracker.animate.set_value(19.5 / 27), run_time = 1.0)
            self.wait(0.6)
            self.play(x_tracker.animate.set_value(1 / 27 - 0.001), run_time = 1.0)
            self.wait(0.6)
            self.play(x_tracker.animate.set_value(4 / 9), run_time = 1.0)

        self.wait(4)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    # ---------- helpers ----------

    def interval_rect(self, nl: NumberLine, a: float, b: float, y: float) -> Rectangle:
        xa = nl.number_to_point(a)[0]; xb = nl.number_to_point(b)[0]
        w = abs(xb - xa); cx = 0.5 * (xa + xb)
        return self.make_bar_at_width(w, self.BAR_HEIGHT, [cx, y, 0])

    def make_bar_at_width(self, width, height, center, color = BLUE_D, stroke = BLUE_E) -> Rectangle:
        r = Rectangle(width = width, height = height,
                      fill_color = color, stroke_color = stroke, stroke_width = 2)
        r.set_fill(color, opacity = 1.0).move_to(center)
        return r

    def make_custom_ticks(self, nl: NumberLine):
        ticks = VGroup(); labels = VGroup()
        def tick_at(x, h = 0.18, sw = 2):
            p = nl.number_to_point(x)
            return Line(p + DOWN * h / 2, p + UP * h / 2, stroke_width = sw, color = WHITE)
        # 0 and 1
        for x, s in [(0, "0"), (1, "1")]:
            t = tick_at(x, h = 0.28, sw = 3.2)
            lbl = MathTex(s).scale(0.8).next_to(t, DOWN, buff = 0.12)
            ticks.add(t); labels.add(lbl)
        # thirds
        for k in [1, 2]:
            x = k/3
            t = tick_at(x, h = 0.24, sw = 2.4)
            lbl = MathTex(rf"\tfrac{{{k}}}{{3}}").scale(0.8).next_to(t, DOWN, buff = 0.12)
            ticks.add(t); labels.add(lbl)
        # ninths
        for k in range(1, 9):
            x = k / 9
            if x in {1 / 3, 2 / 3}: continue
            t = tick_at(x, h = 0.20, sw = 2.0)
            lbl = MathTex(rf"\tfrac{{{k}}}{{9}}").scale(0.7).next_to(t, DOWN, buff = 0.10)
            ticks.add(t); labels.add(lbl)
        # 27ths (unlabeled)
        ninths = {k / 9 for k in range(1, 9)}
        for k in range(1, 27):
            x = k/27
            if x in {0, 1, 1 / 3, 2/3} or x in ninths: continue
            ticks.add(tick_at(x, h = 0.14, sw = 1.6))
        return ticks, labels

    def ternary_equation_tex(self, x: float, k: int) -> MathTex:
        digs = self.ternary_digits(x, k)
        s = r"x \,=\, 0." + "".join(str(d) for d in digs) + r"\,{}_3"
        tex = MathTex(s, substrings_to_isolate = ["x"])
        tex.set_color_by_tex("x", YELLOW)
        return tex

    def ternary_digits(self, x: float, k: int):
        x = min(max(x, 0.0), 1.0)
        f = Fraction(x).limit_denominator(3**(k + 3))
        out = []
        for _ in range(k):
            f *= 3
            d = int(f); out.append(d); f -= d
        return out

# Just like above, except slides around an x value, no red rectangles
class CantorSetConstruction(Scene):
    DEPTH = 5
    BAR_HEIGHT = 2 
    LINE_Y = -3.0
    TERNARY_DIGITS = 5 
    DOT_SIZE = 0.1 
    TOTAL_WIDTH = 11.0
    X_BAR_LEN = 1.6
    INCLUDE_RED = False

    def construct(self):
        nl = NumberLine(
            x_range = [0, 1, 1 / 27],
            include_ticks = False, include_numbers = False,
            length = self.TOTAL_WIDTH,
        )
        nl.set_z_index(100) 

        ticks, labels = self.make_custom_ticks(nl)
        ticks.set_z_index(100)
        labels.set_z_index(100)
        self.add(nl, ticks, labels)

        y_bar = 0
        current_bars = VGroup(self.interval_rect(nl, 0.0, 1.0, y = y_bar))
        current_bars[0].set_z_index(20)
        self.play(GrowFromCenter(current_bars[0]))

        x_tracker = ValueTracker(0.5)
        x_bar = always_redraw(lambda:
            Line(
                nl.number_to_point(x_tracker.get_value()),
                nl.number_to_point(x_tracker.get_value()) + UP * self.X_BAR_LEN,
                stroke_width = 4, color = YELLOW
            )
        )

        x_eq = always_redraw(lambda:
            self.ternary_equation_tex(x_tracker.get_value(), self.TERNARY_DIGITS)
                .scale(0.8)
                .next_to(
                    VectorizedPoint(nl.number_to_point(x_tracker.get_value()) + UP * self.X_BAR_LEN),
                    UP + 0.6 * RIGHT, buff = 0.12
                )
        )

        x_bar.set_z_index(105)
        x_eq.set_z_index(105)

        for depth in range(self.DEPTH):
            split_anims = []
            new_bars = VGroup()
            stage_halves = [] 

            # Phase 1: split each bar into two half-width bars centered at ± w/4
            for bar in current_bars:
                cx, cy, _ = bar.get_center()
                w = bar.get_width()

                left_half = self.make_bar_at_width(w / 2, height = self.BAR_HEIGHT, center=[cx - w / 4, cy, 0])
                right_half = self.make_bar_at_width(w / 2, height = self.BAR_HEIGHT, center=[cx + w / 4, cy, 0],
                                                    color = bar.get_fill_color(), stroke = bar.get_stroke_color())

                left_half.set_z_index(20)
                right_half.set_z_index(20)

                split_anims.append(Transform(bar, left_half))
                split_anims.append(TransformFromCopy(bar, right_half))

                stage_halves.append((bar, right_half))  # references after the split

            self.play(AnimationGroup(*split_anims, lag_ratio = 0.06), run_time = 0.9)

            # Phase 2: shrink each half to third-width and slide to ± w/3 centers
            slide_anims = []
            red_anims = []
            red_labels = [r'.1', r'.\_1', r'.\_\_1', r'.\_\_\_1', r'.\_\_\_\_1']
            for left_bar, right_bar in stage_halves:
                cx, cy, _ = (left_bar.get_center() + right_bar.get_center())/2
                w_current = left_bar.get_width() * 2  # since each is half of previous

                left_third  = self.make_bar_at_width(w_current / 3, self.BAR_HEIGHT, [cx - w_current / 3, cy, 0],
                                                     color = left_bar.get_fill_color(), stroke = left_bar.get_stroke_color())
                right_third = self.make_bar_at_width(w_current / 3, self.BAR_HEIGHT, [cx + w_current / 3, cy, 0],
                                                     color = right_bar.get_fill_color(), stroke = right_bar.get_stroke_color())

                left_third.set_z_index(20)
                right_third.set_z_index(20)

                slide_anims += [Transform(left_bar, left_third), Transform(right_bar, right_third)]
                new_bars.add(left_bar, right_bar)

                if self.INCLUDE_RED:
                    red_third = self.make_bar_at_width(w_current / 3, self.BAR_HEIGHT, [cx, cy, 0],
                                                        color = RED_D, stroke = RED_E)
                    red_third.set_z_index(20)
                    x = cx / self.TOTAL_WIDTH + 0.5
                    vertical_spread = 0.45
                    red_line = Line(
                        nl.number_to_point(x) + DOWN * self.BAR_HEIGHT / 2,
                        nl.number_to_point(x) + DOWN * (self.X_BAR_LEN + depth * vertical_spread),
                        stroke_width = 4, color = WHITE
                    )
                    red_text = MathTex(red_labels[depth]).scale(0.8).move_to(
                        [cx, - 0.25 - self.X_BAR_LEN - depth * vertical_spread, 0]
                    )
                    red_label = VGroup(red_line, red_text)
                    red_label.set_z_index(100)
                    red_anims += [FadeIn(red_third), FadeIn(red_label)]

            self.play(AnimationGroup(*slide_anims, lag_ratio = 0.06), run_time = 0.9)
            if self.INCLUDE_RED:
                self.play(AnimationGroup(*red_anims, lag_ratio = 0.06), run_time = 1)
                self.wait(1)
            current_bars = new_bars

        if self.INCLUDE_RED:
            construction_group = VGroup(*[mob for mob in self.mobjects if isinstance(mob, VMobject)])
            self.play(FadeOut(construction_group))

            m = MathTex(
                r'x \in \text{Cantor} \longleftrightarrow \operatorname{ternary}(x) \text{ has no 1s}',
                font_size = 65,
                color = WHITE
            ).move_to(2 * UP)
            background = SurroundingRectangle(
                m,
                color = GOLD,
                fill_color=DARK_BLUE,
                fill_opacity = 0.3,
                buff = 0.4,
                stroke_width = 4,
                corner_radius = 0.1
            )

            label = Text("MAIN OBSERVATION", font_size = 24, color = GOLD, weight = BOLD)
            label.next_to(background, UP, buff = 0.2)
            self.play(Write(m), Create(background), FadeIn(label))

            x_label = MathTex(
                r'x = (0.220020020220222020\cdots)_3',
                font_size = 55,
                color = WHITE
            ).move_to(2 * DOWN)
            arrow = Arrow(
                background.get_bottom(), 
                x_label.get_top(),
                buff = 0.2,
                stroke_width = 4,
                color = GRAY_A
            )
            implication_anims = [GrowArrow(arrow), Write(x_label)]
            self.play(AnimationGroup(*implication_anims, lag_ratio = 0.3))

        else:
            self.play(FadeIn(VGroup(x_bar, x_eq), shift = UP * 0.1), run_time = 0.5)
            self.wait(0.5)
            self.play(x_tracker.animate.set_value(1 / 9 - 0.01), run_time = 1.0)
            self.wait(0.6)
            self.play(x_tracker.animate.set_value(5 / 9 + 0.013), run_time = 1.2)
            self.wait(0.6)
            self.play(x_tracker.animate.set_value(8 / 9 + 0.001), run_time = 0.9)
            self.wait(0.6)
            self.play(x_tracker.animate.set_value(19.5 / 27), run_time = 1.0)
            self.wait(0.6)
            self.play(x_tracker.animate.set_value(1 / 27 - 0.001), run_time = 1.0)
            self.wait(0.6)
            self.play(x_tracker.animate.set_value(4 / 9), run_time = 1.0)

        self.wait(4)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    # ---------- helpers ----------

    def interval_rect(self, nl: NumberLine, a: float, b: float, y: float) -> Rectangle:
        xa = nl.number_to_point(a)[0]; xb = nl.number_to_point(b)[0]
        w = abs(xb - xa); cx = 0.5 * (xa + xb)
        return self.make_bar_at_width(w, self.BAR_HEIGHT, [cx, y, 0])

    def make_bar_at_width(self, width, height, center, color = BLUE_D, stroke = BLUE_E) -> Rectangle:
        r = Rectangle(width = width, height = height,
                      fill_color = color, stroke_color = stroke, stroke_width = 2)
        r.set_fill(color, opacity = 1.0).move_to(center)
        return r

    def make_custom_ticks(self, nl: NumberLine):
        ticks = VGroup(); labels = VGroup()
        def tick_at(x, h = 0.18, sw = 2):
            p = nl.number_to_point(x)
            return Line(p + DOWN * h / 2, p + UP * h / 2, stroke_width = sw, color = WHITE)
        # 0 and 1
        for x, s in [(0, "0"), (1, "1")]:
            t = tick_at(x, h = 0.28, sw = 3.2)
            lbl = MathTex(s).scale(0.8).next_to(t, DOWN, buff = 0.12)
            ticks.add(t); labels.add(lbl)
        # thirds
        for k in [1, 2]:
            x = k/3
            t = tick_at(x, h = 0.24, sw = 2.4)
            lbl = MathTex(rf"\tfrac{{{k}}}{{3}}").scale(0.8).next_to(t, DOWN, buff = 0.12)
            ticks.add(t); labels.add(lbl)
        # ninths
        for k in range(1, 9):
            x = k / 9
            if x in {1 / 3, 2 / 3}: continue
            t = tick_at(x, h = 0.20, sw = 2.0)
            lbl = MathTex(rf"\tfrac{{{k}}}{{9}}").scale(0.7).next_to(t, DOWN, buff = 0.10)
            ticks.add(t); labels.add(lbl)
        # 27ths (unlabeled)
        ninths = {k / 9 for k in range(1, 9)}
        for k in range(1, 27):
            x = k/27
            if x in {0, 1, 1 / 3, 2/3} or x in ninths: continue
            ticks.add(tick_at(x, h = 0.14, sw = 1.6))
        return ticks, labels

    def ternary_equation_tex(self, x: float, k: int) -> MathTex:
        digs = self.ternary_digits(x, k)
        s = r"x \,=\, 0." + "".join(str(d) for d in digs) + r"\,{}_3"
        tex = MathTex(s, substrings_to_isolate = ["x"])
        tex.set_color_by_tex("x", YELLOW)
        return tex

    def ternary_digits(self, x: float, k: int):
        x = min(max(x, 0.0), 1.0)
        f = Fraction(x).limit_denominator(3**(k + 3))
        out = []
        for _ in range(k):
            f *= 3
            d = int(f); out.append(d); f -= d
        return out

# Show the two codes for a ternary real    
class MapTwosToOnes(Scene):
    def construct(self):        
        # Create left code object
        left_rendered_code = Code(
            code_string = '''220020020220222020202022020
200000202222022220002222020
                 
            ...
''',
            background = "window",
            background_config = {"fill_color": "black", "stroke_color": "white"}, 
            paragraph_config = {"font_size": 30},
            add_line_numbers = False,
            formatter_style = 'bw',
        ).scale(0.7)

        left_label = MathTex(r'\operatorname{ternary}(x)').next_to(left_rendered_code, UP, buff = 0.2)
        top_left = VGroup(left_rendered_code, left_label).to_edge(LEFT, buff = 0.5)

        # Create right code object
        right_rendered_code = Code(
            code_string = '''1100100101101110101010110101
1000001011110111100011110101
                 
            ...
''',
            language='python',
            background = "window",
            background_config = {"fill_color": "black", "stroke_color": "white"},
            paragraph_config = {"font_size": 30},
            add_line_numbers = False,
            formatter_style = 'bw'
        ).scale(0.7)
        right_label = Tex(r'short code for $x$').next_to(right_rendered_code, UP, buff = 0.2)
        top_right = VGroup(right_rendered_code, right_label).to_edge(RIGHT, buff = 0.5).to_edge(DOWN, buff = 1)

        # Create arrow pointing from left to right
        arrow = Arrow(
            start = left_rendered_code.get_right(),
            end = right_rendered_code.get_left(),
            buff = 0.2,
            stroke_width = 4,
            color = GRAY_A
        )
        arrow_label = MathTex(r'2 \mapsto 1').next_to(arrow, DOWN, buff = 0.05)
        arrow_group = VGroup(arrow, arrow_label)

        # Create left code object
        bottom_rendered_code = Code(
            code_string = '''111001011100000010101011100
011010100101011010010011010
                 
            ...
''',
            background = "window",
            background_config = {"fill_color": "black", "stroke_color": "white"}, 
            paragraph_config = {"font_size": 30},
            add_line_numbers = False,
            formatter_style = 'bw',
        ).scale(0.7)

        bottom_label = MathTex(r'\operatorname{binary}(x)').next_to(bottom_rendered_code, UP, buff = 0.2)
        bottom_group = VGroup(bottom_rendered_code, bottom_label)
        bottom_group.to_edge(RIGHT, buff = 0.5).to_edge(UP, buff = 1)

        down_arrow = Arrow(
            start = left_rendered_code.get_right(),
            end = bottom_rendered_code.get_left(),
            buff = 0.2,
            stroke_width = 4,
            color = GRAY_A
        )

        # Show left code
        self.play(Create(left_rendered_code), Write(left_label), run_time = 1.5)
        self.wait(2)
        # Show binary
        binary_anims = [GrowArrow(down_arrow), Write(bottom_label), Create(bottom_rendered_code)]
        self.play(AnimationGroup(*binary_anims, lag_ratio = 0.3), run_time = 2)
        # Show code
        code_anims = [GrowArrow(arrow), Write(arrow_label), Write(right_label), Create(right_rendered_code)]
        self.play(AnimationGroup(*code_anims, lag_ratio = 0.3), run_time = 2)
        self.wait(2)
        
        self.wait(4)
        # Remove everything... too many objects
        self.play(*[FadeOut(mob) for mob in self.mobjects])

# Algebra giving log 2 / log 3
class FractionSimplification(Scene):
    def construct(self):

        T = Tex(r'\underline{Compression factor under the map $2 \mapsto 1$}', font_size = 50).move_to(UP * 2)
        self.play(Write(T), run_time = 0.75)
        self.wait(2)

        # Step 1: Initial descriptive text
        step1_num = MathTex(r'\# \text{ bits in codeword for } x \text{ at precision } 3^{-n}')
        step1_den = MathTex(r'\# \text{ bits to express reals to precision } 3^{-n}')
        step1_line = Line(LEFT * 4.5, RIGHT * 4.5)
        step1_fraction = VGroup(step1_num, step1_line, step1_den).arrange(DOWN, buff = 0.3)
        
        self.play(Write(step1_fraction))
        self.wait(1)
        
        # Step 2: Transform to logarithmic form with structured parts
        # Numerator parts
        log_part_num = MathTex(r'\log_2')
        paren_open_num = MathTex(r'(')
        base_num = MathTex(r'2')
        exponent_num = MathTex(r'^n')
        paren_close_num = MathTex(r')')
        step2_num = VGroup(log_part_num, paren_open_num, base_num, exponent_num, paren_close_num)
        step2_num.arrange(RIGHT, buff=0.05)
        
        # Denominator parts
        log_part_den = MathTex(r'\log_2')
        paren_open_den = MathTex(r'(')
        base_den = MathTex(r'3')
        exponent_den = MathTex(r'^n')
        paren_close_den = MathTex(r')')
        step2_den = VGroup(log_part_den, paren_open_den, base_den, exponent_den, paren_close_den)
        step2_den.arrange(RIGHT, buff=0.05)
        
        step2_line = Line(LEFT * 1.5, RIGHT * 1.5)
        step2_fraction = VGroup(step2_num, step2_line, step2_den).arrange(DOWN, buff = 0.3)
        
        self.play(ReplacementTransform(step1_fraction, step2_fraction))
        self.wait(1)
        
        # Step 3: Apply logarithm power rule with structured transformation
        # Create target expressions for numerator
        n_coeff_num = MathTex(r'n')
        log_part_new_num = MathTex(r'\log_2')
        base_new_num = MathTex(r'2')
        target_num = VGroup(n_coeff_num, log_part_new_num, base_new_num)
        target_num.arrange(RIGHT, buff = 0.2)
        
        # Create target expressions for denominator
        n_coeff_den = MathTex(r'n')
        log_part_new_den = MathTex(r'\log_2')
        base_new_den = MathTex(r'3')
        target_den = VGroup(n_coeff_den, log_part_new_den, base_new_den)
        target_den.arrange(RIGHT, buff = 0.2)
        
        step3_line = Line(LEFT, RIGHT)
        step3_fraction = VGroup(target_num, step3_line, target_den).arrange(DOWN, buff = 0.3)
        
        # Animate the transformation
        self.play(
            # Numerator transformation
            ReplacementTransform(exponent_num, n_coeff_num),
            ReplacementTransform(log_part_num, log_part_new_num),
            ReplacementTransform(base_num, base_new_num),
            FadeOut(paren_open_num),
            FadeOut(paren_close_num),
            # Denominator transformation
            ReplacementTransform(exponent_den, n_coeff_den),
            ReplacementTransform(log_part_den, log_part_new_den),
            ReplacementTransform(base_den, base_new_den),
            FadeOut(paren_open_den),
            FadeOut(paren_close_den),
            # Line transformation
            Transform(step2_line, step3_line)
        )
        self.wait(1)
        
        # Step 4: Smoothly cancel the n terms without repositioning
        # First fade out the n terms while keeping everything else in place
        self.play(
            FadeOut(n_coeff_num),
            FadeOut(n_coeff_den)
        )
        self.wait(0.5)
        
        # Then smoothly reposition the remaining logarithm terms and line
        # Calculate final positions manually to avoid VGroup arrangement issues
        current_center = step3_fraction.get_center()
        
        # Create final line first to get its position
        final_line = Line(LEFT * 0.7, RIGHT * 0.5)
        final_line.move_to(current_center)
        
        # Calculate positions for numerator and denominator
        num_target_y = final_line.get_center()[1] + 0.5
        den_target_y = final_line.get_center()[1] - 0.5
        
        # Calculate centered x positions for the log terms
        log_spacing = 0.7
        num_center_x = 0.2
        den_center_x = 0.2
        
        self.play(
            # Move numerator terms to center above the line
            log_part_new_num.animate.move_to([num_center_x - log_spacing/2, num_target_y, 0]),
            base_new_num.animate.move_to([num_center_x + log_spacing/2, num_target_y, 0]),
            # Move denominator terms to center below the line  
            log_part_new_den.animate.move_to([den_center_x - log_spacing/2, den_target_y, 0]),
            base_new_den.animate.move_to([den_center_x + log_spacing/2, den_target_y, 0]),
            # Transform the line
            Transform(step3_line, final_line)
        )
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])

# Application of PTS
class ApplicationOfPTS(Scene):
    def construct(self):
        expressions = [
            [
                r'1. Since we can shrink codes by a factor of $\frac{\log 2}{\log 3}$,',
                r'For each $x \in \operatorname{Cantor}$, we have $\operatorname{dim}(x) \leq \frac{\log 2}{\log 3}$.',
            
            ],
            [
                r'2. Since \textit{any} combination of 0s and 2s is possible,',
                r'There exists $x \in \operatorname{Cantor}$ where $\frac{C(x \upharpoonright n)}{n}$ is \textit{maximal} for all $n$.',
            ],
            [
                r'3. By the Point-to-Set Principle,',
                r'$\operatorname{dim}_{\operatorname{fractal}}(\operatorname{Cantor}) = \frac{\log 2}{\log 3}$.'
            ]
        ]

        t = []
        m = []
        for i in range(len(expressions)):
            t0 = Tex(expressions[i][0], font_size = 35, color = WHITE)
            t1 = Tex(expressions[i][1], font_size = 40, color = WHITE).next_to(t0, DOWN, buff = 0.5, aligned_edge = LEFT).shift(0.3 * RIGHT)
            t.append(VGroup(t0, t1))

        T = VGroup(*t).arrange(DOWN, aligned_edge = LEFT, buff = 1).shift(0.1 * UP)
        T.set_z_index(100)
        
        m = [
            SurroundingRectangle(
                _t[1], 
                color = GOLD,
                fill_color = DARK_BLUE,
                fill_opacity = 0.3,
                buff = 0.4,
                stroke_width = 4,
                corner_radius = 0.1
            ) for _t in t
        ]

        for i in range(len(t)):
            self.play(Write(t[i]), Create(m[i]))
            self.wait(5)

        self.play(*[FadeOut(mob) for mob in self.mobjects])

###### ENDING #######

# Ending screen
class EndingScreen(Scene):
    def construct(self):
        thank_you = Tex("Thanks for watching!", font_size = 80).to_edge(UP, buff = 2)
        line = Line(2 * LEFT, 2 * RIGHT, stroke_width = 3).next_to(thank_you, DOWN, buff = 0.7)
        
        logo = SVGMobject("symbol.svg")
        for m in logo.family_members_with_points():
            m.set_stroke(opacity = 1, width = 8)
        SoME = Tex("SoME", font_size = 90)
        SoME_logo = VGroup(logo, SoME).scale(0.8).to_edge(DOWN, buff = 0.6).to_edge(RIGHT, buff = 0.6)

        fs = 36
        info_table = MobjectTable([
                [Tex(r'\textbf{Created by}', font_size = fs), Tex('Raymond Tana', font_size = fs)], 
                [Tex(r'\textbf{Channel}', font_size = fs), Tex('PreterMathematics', font_size = fs)], 
                [Tex(r'\textbf{Date of Publication}', font_size = fs), Tex('August 31, 2025', font_size = fs)]
            ],
            include_outer_lines = False,
            line_config = {'stroke_opacity': 0},
            v_buff = 0.35, h_buff = 0.6,
        ).move_to(1.2 * DOWN)

        # Right-aligned left col, left-aligned right col
        for i, row in enumerate(info_table.get_rows()):
            for content in row[0]:
                content.align_to(info_table.get_columns()[0], RIGHT)
            for content in row[1]:
                content.align_to(info_table.get_columns()[1], LEFT)

        self.play(Write(thank_you), FadeIn(logo, shift = 0.5 * DOWN), Write(SoME), GrowFromCenter(line), Create(info_table))

        self.wait(4)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time = 3)