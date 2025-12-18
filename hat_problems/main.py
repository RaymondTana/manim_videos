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

####################

LEVELS = [
    {
        'title': 'Level 1',
        'label': r'\mathbb{N}',
        'number': 2,
        'guesses': 'finite',
        'number_type': 'natural'
    },
    {
        'title': 'Level 2',
        'label': r'\mathbb{Q}',
        'number': 2,
        'guesses': 'finite',
        'number_type': 'rational'
    },
    {
        'title': 'Level 3',
        'label': r'\mathbb{R}',
        'number': 2,
        'guesses': 'countable',
        'number_type': 'real'
    },
    {
        'title': 'Level 4',
        'label': r'\mathbb{R}',
        'number': 3,
        'guesses': 'finite',
        'number_type': 'real'
    },
    {
        'title': 'Level 5',
        'label': r'\aleph_{n}',
        'underbrace': r'{n + 2}',
        'guesses': 'finite',
        'number_type': 'real'
    }
]

####################

def generate_number(number_type):
    """Generate a single random number based on the number_type."""
    if number_type == 'natural':
        # Small integer between [-3, 3] or power of ten
        if random.random() < 0.5:
            return str(random.randint(-3, 3))
        else:
            return str(random.randint(-3, 3) * 10 ** random.randint(2, 3))
    elif number_type == 'rational':
        # Rational with integers between [-10, 10]
        num = random.randint(-10, 10)
        den = random.randint(1, 10)
        frac = Fraction(num, den)
        return f"{frac.numerator}/{frac.denominator}" if frac.denominator != 1 else str(frac.numerator)
    elif number_type == 'real':
        # Real number with exactly 3 decimal places
        return f"{random.uniform(-5, 5):.3f}"
    return "0"

def arrange_hats(level, hat_numbers=None, number_type = ""):
    """
    Arrange hats for a given level.

    Args:
        level: Level dictionary with configuration
        hat_numbers: Optional list of specific numbers to display on each hat.
                     If None, uses the level's label for all hats.
    """
    if 'underbrace' in level.keys():
        if hat_numbers is None:
            arranged_hats = VGroup([
                get_hat(ORIGIN, label = level['label']),
                get_hat(ORIGIN, label = level['label']),
                MathTex(r'\cdots'),
                get_hat(ORIGIN, label = level['label'])
            ])
        else:
            arranged_hats = VGroup([
                get_hat(ORIGIN, label = hat_numbers[0]),
                get_hat(ORIGIN, label = hat_numbers[1]),
                MathTex(r'\cdots'),
                get_hat(ORIGIN, label = hat_numbers[2])
            ])
        arranged_hats.arrange(RIGHT, buff = 0.5)
        underbrace = Brace(arranged_hats, DOWN)
        label = underbrace.get_tex(level['underbrace'])
        arranged_hats.add(underbrace, label)
    else:
        if hat_numbers is None:
            arranged_hats = VGroup(*[get_hat(ORIGIN, label = level['label']) for i in range(level['number'])])
        else:
            arranged_hats = VGroup(*[get_hat(ORIGIN, label = hat_numbers[i] + ("..." if number_type == 'real' else "")) for i in range(level['number'])])
        arranged_hats.arrange(RIGHT, buff = 0.5)
    return arranged_hats

def make_notes(guesses, number_type, correct_number=None, include_correct=True, exclude_numbers=None, show_numbers=True):
    """
    Create a note object with a list of numbers or just descriptive text.

    Args:
        guesses: 'finite' or 'countable'
        number_type: 'natural', 'rational', or 'real'
        correct_number: The correct number to potentially include
        include_correct: If True and correct_number is provided, include it in the list.
                        If False, ensure it's NOT in the list.
        exclude_numbers: List of numbers to exclude (e.g., other players' hat numbers)
        show_numbers: If True, show numbers in the list. If False, only show the text description.

    Returns:
        tuple: (note VGroup, list of numbers used in this note)
    """
    text = "finitely many" if guesses == 'finite' else "countably many"

    if exclude_numbers is None:
        exclude_numbers = []

    # Generate two random numbers for display
    use_numbers = []

    if show_numbers:
        if include_correct and correct_number is not None:
            # Include the correct number as the first element
            use_numbers.append(correct_number)
            # Generate one more random number that's different and not excluded
            while True:
                num = generate_number(number_type)
                if num != correct_number and num not in exclude_numbers and num not in use_numbers:
                    use_numbers.append(num)
                    break
        else:
            # Generate two random numbers, ensuring they don't match correct_number or excluded numbers
            for _ in range(2):
                while True:
                    num = generate_number(number_type)
                    if (num != correct_number and
                        num not in exclude_numbers and
                        num not in use_numbers):
                        use_numbers.append(num)
                        break

    # Draw a note object that looks like a page with a folded corner
    note_width = 1.5
    note_height = 2.0
    fold_size = 0.3

    # Main rectangle body
    main_rect = Polygon(
        np.array([-note_width/2, note_height/2, 0]),
        np.array([note_width/2, note_height/2, 0]),
        np.array([note_width/2, -note_height/2 + fold_size, 0]),
        np.array([note_width/2 - fold_size, -note_height/2, 0]),
        np.array([-note_width/2, -note_height/2, 0]),
        color=WHITE,
        fill_color=WHITE,
        fill_opacity=0.9,
        stroke_width=2
    )

    # Folded corner triangle
    fold = Polygon(
        np.array([note_width/2 - fold_size, -note_height/2, 0]),
        np.array([note_width/2, -note_height/2 + fold_size, 0]),
        np.array([note_width/2 - fold_size, -note_height/2 + fold_size, 0]),
        color=GRAY,
        fill_color=GRAY,
        fill_opacity=0.6,
        stroke_width=2
    )

    # Create text content
    numbers_text = VGroup()

    if show_numbers:
        # Show numbers list with count text
        start_y = note_height/2 - 0.4
        line_spacing = 0.35

        # First number
        num1 = MathTex(use_numbers[0] + ("..." if number_type == 'real' else ""), color=BLACK, font_size=28)
        num1.move_to(np.array([0, start_y, 0]))
        numbers_text.add(num1)

        # Second number
        num2 = MathTex(use_numbers[1] + ("..." if number_type == 'real' else ""), color=BLACK, font_size=28)
        num2.move_to(np.array([0, start_y - line_spacing, 0]))
        numbers_text.add(num2)

        # Ellipses
        dots = MathTex(r"\vdots", color=BLACK, font_size=28)
        dots.move_to(np.array([0, start_y - 2.25*line_spacing, 0]))
        numbers_text.add(dots)

        # Count text with newline 
        text_parts = text.split()
        count_text = Tex(f"{text_parts[0]}\\\\{text_parts[1]}", color=BLACK, font_size=20)
        count_text.move_to(np.array([0, start_y - 3.5*line_spacing, 0]))
        numbers_text.add(count_text)
    else:
        # Show only the descriptive text, centered with newline
        text_parts = text.split()
        centered_text = Tex(f"{text_parts[0]}\\\\{text_parts[1]}", color=BLACK, font_size=28)
        centered_text.move_to(ORIGIN)
        numbers_text.add(centered_text)

    # Group everything together
    note = VGroup(main_rect, fold, numbers_text)

    return note, use_numbers

def get_hat(position, size=1.0, label="", color=WHITE, use_number=None):
    """
    Draw a top hat outline at the specified position with 3D curved appearance.
    
    Args:
        position: numpy array or list [x, y, z] for hat position
        size: float scale factor for the hat size
        label: string for TeX label to place inside the hat
        color: color of the hat outline
    
    Returns:
        VGroup containing the hat and label
    """
    # Define hat proportions
    brim_width = 2.0 * size
    brim_depth = 0.6 * size 
    crown_width = 1.3 * size
    crown_height = 1.1 * size
    brim_front_y = 0.12 * size
    brim_inner_front_y = 0.28 * size
    brim_start_angle = -PI * 1.28
    brim_angle = PI * 1.56
    label_size = 0.8 * size
    
    # BRIM PARTS (only visible front portions)
    # Front arc of brim (bottom outer edge)
    brim_front = Arc(
        radius=brim_width/2,
        start_angle=brim_start_angle,
        angle=brim_angle,
        color=color,
        stroke_width=2.5
    ).stretch(brim_depth/brim_width, 1).shift(brim_front_y * UP)
    
    # Front arc of brim inner edge (where crown meets brim) - only the front half
    brim_inner_front = Arc(
        radius=crown_width/2,
        start_angle=-PI,
        angle=PI,
        color=color,
        stroke_width=2.5
    ).stretch((brim_depth/brim_width) * 0.6, 1).shift(brim_inner_front_y * UP)
    
    # Inner brim arc endpoints
    inner_left = LEFT * crown_width/2
    inner_right = RIGHT * crown_width/2
    
    # CROWN PARTS
    # Left side of crown (starts from inner brim)
    crown_left = Line(
        start=inner_left,
        end=LEFT * crown_width/2 + UP * crown_height,
        color=color,
        stroke_width=2.5
    )
    
    # Right side of crown
    crown_right = Line(
        start=inner_right,
        end=RIGHT * crown_width/2 + UP * crown_height,
        color=color,
        stroke_width=2.5
    )
    
    # Top of crown - full ellipse is visible
    crown_top = Ellipse(
        width=crown_width,
        height=crown_width * 0.25,
        color=color,
        stroke_width=2.5
    ).shift(UP * crown_height)
    
    # Group all hat parts (in back-to-front order for proper visual layering)
    hat = VGroup(
        brim_inner_front,
        crown_left,
        crown_right,
        crown_top,
        brim_front
    )
    
    # Move to specified position
    hat.move_to(position)
    
    # Add label inside the hat if provided
    if label:
        label_text = MathTex(label, color=color)
        label_text.scale(label_size)

        # Check if label is too wide for the crown and shrink if necessary
        max_width = crown_width * 0.85  # Use 85% of crown width for some padding
        if label_text.width > max_width:
            # Shrink the label to fit within the crown width
            scale_factor = max_width / label_text.width
            label_text.scale(scale_factor)

        # Position label in the center of the crown
        label_text.move_to(hat.get_center())
        hat.add(label_text)

    return hat
        
class levels(Scene):
    def construct(self):
        write_speed = 0.75
        self.wait(2)
        for level in LEVELS:
            T = Tex(level['title'], font_size = 64).move_to(UP * 2)
            self.play(Write(T), run_time = write_speed)
            self.wait(1)
            arranged_hats = arrange_hats(level)
            self.play(LaggedStart(*[Create(hat) for hat in arranged_hats], lag_ratio = 0.2))
            self.wait(2)
            self.play(FadeOut(*self.mobjects))
            self.wait(1)

class level_statements(Scene):
    def construct(self):
        self.wait(2)
        for level in LEVELS:
            # Generate random DISTINCT numbers for each hat
            num_hats = level['number'] if 'underbrace' not in level.keys() else 3
            hat_numbers = []
            while len(hat_numbers) < num_hats:
                num = generate_number(level['number_type'])
                if num not in hat_numbers:
                    hat_numbers.append(num)

            # 1. There are some players each donned with a hat bearing a number.
            arranged_hats = arrange_hats(level, hat_numbers=hat_numbers, number_type=level['number_type'])
            arranged_hats.move_to(UP * 1.5)
            self.play(LaggedStart(*[Create(hat) for hat in arranged_hats], lag_ratio = 0.2))
            self.wait(2)

            # 2. Each player may only see the numbers on all others' hats.
            # Draw edges between hats as permitted, but edges from hat to self as X'd out

            # Get actual hat positions (not the ellipsis or underbrace)
            hat_positions = []
            for i, hat in enumerate(arranged_hats):
                if isinstance(hat, VGroup) and not isinstance(hat, MathTex):
                    hat_positions.append(hat.get_center())
                    if len(hat_positions) >= num_hats:
                        break

            # Create visibility edges
            edges = VGroup()
            self_loops = VGroup()

            for i in range(len(hat_positions)):
                for j in range(i, len(hat_positions)):
                    if i != j:
                        # Draw rainbow-like curved arc above the hats
                        start_point = hat_positions[j] + UP * 0.9
                        end_point = hat_positions[i] + UP * 0.9

                        # Calculate arc parameters for rainbow-like curve
                        horizontal_dist = abs(hat_positions[j][0] - hat_positions[i][0])
                        arc_height = 1.2 + horizontal_dist * 0.5 # Height scales with distance
                        
                        # Create a smooth curved path using a quadratic bezier-like arc
                        midpoint = (start_point + end_point) / 2 + UP * arc_height

                        # Use ArcBetweenPoints for a nice smooth arc
                        arc = ArcBetweenPoints(
                            start_point + RIGHT * 0.1,
                            end_point + LEFT * 0.1,
                            angle=TAU/4, # Creates a nice rainbow-like curve
                            color=GREEN,
                            stroke_width=3
                        )

                        edges.add(arc)
                    else:
                        # Draw self-loop as a teardrop tethered to the bottom-center of the hat

                        # Start point: bottom-center of the hat
                        anchor_point = hat_positions[i] + DOWN * 0.9

                        # Create a teardrop shape using a custom path
                        # The teardrop will extend downward and curve back up
                        loop_width = 0.5
                        loop_height = 1.0

                        # Define control points for a teardrop bezier curve
                        # Start at anchor (top of teardrop, tethered to hat)
                        start = anchor_point

                        # Left side curves down and out
                        left_control1 = anchor_point + LEFT * 0.1 + DOWN * 0.3
                        left_control2 = anchor_point + LEFT * loop_width + DOWN * 0.6
                        left_bottom = anchor_point + LEFT * (loop_width * 0.4) + DOWN * loop_height

                        # Bottom curves around
                        bottom_control = anchor_point + DOWN * (loop_height + 0.1)

                        # Right side curves back up
                        right_bottom = anchor_point + RIGHT * (loop_width * 0.4) + DOWN * loop_height
                        right_control2 = anchor_point + RIGHT * loop_width + DOWN * 0.6
                        right_control1 = anchor_point + RIGHT * 0.1 + DOWN * 0.3

                        # Create the teardrop path using CubicBezier curves
                        left_curve = CubicBezier(
                            start,
                            left_control1,
                            left_control2,
                            left_bottom,
                            color=RED,
                            stroke_width=2.5
                        )

                        bottom_curve = CubicBezier(
                            left_bottom,
                            bottom_control,
                            bottom_control,
                            right_bottom,
                            color=RED,
                            stroke_width=2.5
                        )

                        right_curve = CubicBezier(
                            right_bottom,
                            right_control2,
                            right_control1,
                            start,
                            color=RED,
                            stroke_width=2.5
                        )

                        self_loop = VGroup(left_curve, bottom_curve, right_curve)

                        # Add arrow tip at the top right, pointing back at the anchor point
                        arrow_tip = Triangle(color=RED, fill_opacity=1, stroke_width=0)
                        arrow_tip.scale(0.12)
                        arrow_tip.rotate(-PI * 0.6) # Point leftward/downward toward anchor
                        arrow_tip.move_to(start + RIGHT * 0.05 + DOWN * 0.05)

                        # Small X mark underneath the loop
                        x_size = 0.12
                        x_position = anchor_point + DOWN * (loop_height + 0.3)
                        x_mark = VGroup(
                            Line(x_position + UL * x_size, x_position + DR * x_size, color=RED, stroke_width=2.5),
                            Line(x_position + UR * x_size, x_position + DL * x_size, color=RED, stroke_width=2.5)
                        )
                        self_loops.add(VGroup(self_loop, arrow_tip, x_mark))

            connection_animations = [Create(edge) for edge in edges] + [Create(loop) for loop in self_loops]
            connections_group = AnimationGroup(*connection_animations)
            self.play(connections_group, run_time = 1.2)
            self.wait(3)

            # 3. Each player submits a finite (unless otherwise specified) list of numbers which might be on their own hat
            # Render notes object aligned beneath each hat
            # For the winning scenario, one note will contain the correct number
            winning_note_index = random.randint(0, len(hat_positions) - 1)

            notes_winning = VGroup()
            all_used_numbers = set(hat_numbers)  # Track all numbers used across all notes
            for i in range(len(hat_positions)):
                # The winning note gets the correct number
                include_correct = (i == winning_note_index)
                # Exclude all hat numbers AND numbers already used in other notes
                exclude_numbers = list(all_used_numbers)
                note, used_nums = make_notes(
                    guesses=level['guesses'],
                    number_type=level['number_type'],
                    correct_number=hat_numbers[i],
                    include_correct=include_correct,
                    exclude_numbers=exclude_numbers
                )
                # Add the numbers used in this note to the global tracker
                all_used_numbers.update(used_nums)

                note.scale(0.9)
                note.move_to(hat_positions[i] + DOWN * (2.5 + 1 * ('underbrace' in level.keys())))
                notes_winning.add(note)

            self.play(FadeOut(edges, self_loops))
            self.play(LaggedStart(*[FadeIn(note) for note in notes_winning], lag_ratio=0.15))
            self.wait(NORMAL_DELAY)

            # 4. This submission is made once and simultaneously with all other players.
            self.wait(SHORT_DELAY)

            # 5. So long as at least one player's list contains their own number, everyone wins.
            winning_note = notes_winning[winning_note_index]

            # Highlight the winning note
            highlight = SurroundingRectangle(winning_note, color=GREEN, buff=0.1, stroke_width=4)
            checkmark = MathTex(r"\checkmark", color=GREEN, font_size=100)
            checkmark.next_to(winning_note, RIGHT, buff=0.3)

            self.play(Create(highlight))
            self.play(Write(checkmark))

            # Show winning text
            win_text = Tex("Everyone wins!", color=GREEN, font_size=50)
            win_text.to_edge(UP)
            self.play(Write(win_text))
            self.wait(BIG_DELAY)

            # Clear winning scenario
            self.play(FadeOut(highlight, checkmark, win_text, notes_winning))
            self.wait(SHORT_DELAY)

            # 6. But if all the players miss writing down their own number, everyone loses.
            # Create new notes where NONE contain the correct number
            notes_losing = VGroup()
            all_used_numbers = set(hat_numbers)  # Track all numbers used across all notes
            for i in range(len(hat_positions)):
                # Exclude all hat numbers AND numbers already used in other notes
                exclude_numbers = list(all_used_numbers)
                note, used_nums = make_notes(
                    guesses=level['guesses'],
                    number_type=level['number_type'],
                    correct_number=hat_numbers[i],
                    include_correct=False,  # Ensure the correct number is NOT included
                    exclude_numbers=exclude_numbers
                )
                # Add the numbers used in this note to the global tracker
                all_used_numbers.update(used_nums)

                note.scale(0.9)  # Increased from 0.4 to 0.9 (2.25x bigger)
                note.move_to(hat_positions[i] + DOWN * (2.5 + 1 * ('underbrace' in level.keys())))
                notes_losing.add(note)

            self.play(LaggedStart(*[FadeIn(note) for note in notes_losing], lag_ratio=0.15))
            self.wait(SHORT_DELAY)

            # Show all notes with X marks
            x_mark_size = 0.5
            x_marks = VGroup()
            for note in notes_losing:
                x_mark = VGroup(
                    Line(UL * x_mark_size, DR * x_mark_size, color=RED, stroke_width=4),
                    Line(UR * x_mark_size, DL * x_mark_size, color=RED, stroke_width=4)
                )
                x_mark.move_to(note.get_center())
                x_marks.add(x_mark)

            self.play(LaggedStart(*[Create(x) for x in x_marks], lag_ratio=0.1))

            # Show losing text
            lose_text = Tex("Everyone loses", color=RED, font_size=50)
            lose_text.to_edge(UP)
            self.play(Write(lose_text))
            self.wait(BIG_DELAY)

            self.play(FadeOut(x_marks, lose_text, notes_losing))
            self.wait(SHORT_DELAY)

            # 8. So, how do you guarantee the players always win?
            # Show the same hats with generic symbols (as in the levels Scene),
            # with notes underneath showing only the text description

            # First fade out the specific number hats
            self.play(FadeOut(arranged_hats))
            self.wait(SHORT_DELAY)

            # Show generic hats with just the level label (no specific numbers)
            generic_hats = arrange_hats(level, number_type=level['number_type'])
            generic_hats.move_to(UP * 1.5)
            self.play(LaggedStart(*[Create(hat) for hat in generic_hats], lag_ratio=0.2))
            self.wait(NORMAL_DELAY)

            # Create notes with only text (no specific numbers)
            # Get positions for notes based on the number of actual hats
            notes_text_only = VGroup()
            for i in range(len(hat_positions)):
                note, _ = make_notes(
                    guesses=level['guesses'],
                    number_type=level['number_type'],
                    show_numbers=False  # Only show text description
                )
                note.scale(0.9)
                note.move_to(hat_positions[i] + DOWN * (2.5 + 1 * ('underbrace' in level.keys())))
                notes_text_only.add(note)

            self.play(LaggedStart(*[FadeIn(note) for note in notes_text_only], lag_ratio=0.15))
            self.wait(BIG_DELAY)

            # Optional: Show a question or prompt
            question_text = Tex("How do you guarantee the players always win?", font_size=44)
            question_text.to_edge(UP)
            self.play(Write(question_text), run_time = 0.6)
            self.wait(2)

            # Flush this level
            self.play(FadeOut(*self.mobjects))
            self.wait(2)

class ordinal_transitions(Scene):
    # Since transition from one oracle to the next involves swapping around many natural numbers, I've decided to implement this using a technique of keeping track of which indices go where across each scene. I'll encode this using three fields:
    # 1. Ordinal: TeX for labeling the ordinal being illustrated
    # 2. Indices: how to build this ordinal by populating with mobjects from the previous, referenced by their indices
    # 3. Labels: TeX for labeling the elements used in displaying this ordinal

    # having index -1 means the character is new and that a new mobject should be created
    # if ever an index is unused, the mobject should be faded out
    # the ordinal part is written as a list because sometimes we want to show equivalent labels for the same ordinal... just animate chronologically through all those labels until you've reached the end, and then do the swapping
    ordinal_pictures = [
        {
            'ordinal': [r'0'],
            'indices': [],
            'labels': []
        },
        {
            'ordinal': [r'1'],
            'indices': [-1],
            'labels': [r'0']
        },
        {
            'ordinal': [r'2'],
            'indices': [0, -1],
            'labels': [r'0', r'1']
        },
        {
            'ordinal': [r'3'],
            'indices': [0, 1, -1],
            'labels': [r'0', r'1', r'2']
        },
        {
            'ordinal': [r'\omega'],
            'indices': [0, 1, 2, -1, -1],
            'labels': [r'0', r'1', r'2', r'3', r'\cdots']
        },
        {
            'ordinal': [r'\omega + 1'],
            'indices': [1, 2, 3, 4, -1, 0],
            'labels': [r'0', r'1', r'2', r'\cdots', r'|', r'\omega']
        },
        {
            'ordinal': [r'\omega + 2'],
            'indices': [1, 2, 3, 4, 5, 0],
            'labels': [r'0', r'1', r'\cdots', r'|', r'\omega', r'\omega + 1']
        },
        {
            'ordinal': [r'\omega + 3'],
            'indices': [1, 2, 3, 4, 5, 0],
            'labels': [r'0', r'\cdots', r'|', r'\omega', r'\omega + 1', r'\omega + 2']
        },
        {
            'ordinal': [r'\omega'],
            'indices': [3, 4, 5, 0, 1, -1, -1],
            'labels': [r'0', r'1', r'2', r'3', r'4', r'5', r'\cdots']
        },
        {
            'ordinal': [r'\omega + \omega', r'\omega \cdot 2'],
            'indices': [0, 2, 4, -1, -1, 1, 3, 5, 6],
            'labels': [r'0', r'1', r'2', r'\cdots', r'|', r'\omega', r'\omega + 1', r'\omega + 2', r'\cdots']
        },
        {
            'ordinal': r'\omega \cdot 2 + 1',
            'indices': [1, 2, 3, 4, 5, 6, 7, 8, -1, 0],
            'labels': [r'0', r'1', r'\cdots', r'|', r'\omega', r'\omega + 1', r'\omega + 2', r'\cdots', r'|', r'\omega \cdot 2']
        },
    ]