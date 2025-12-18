from manim import *
import math
import numpy as np
import random
import re
from fractions import Fraction

# TeX template
TEX_TEMPLATE = TexTemplate()
TEX_TEMPLATE.add_to_preamble(r"\usepackage{mathrsfs}")
TEX_TEMPLATE.add_to_preamble(r"\usepackage{amsmath}")
TEX_TEMPLATE.add_to_preamble(r"\usepackage{amsthm}")
TEX_TEMPLATE.add_to_preamble(r"\usepackage{amssymb}")
TEX_TEMPLATE.add_to_preamble(r"\usepackage{amsfonts}")
TEX_TEMPLATE.add_to_preamble(r"\usepackage{mathtools}")

# 1-Parameter Family
def f(t: float, i: int, j: int):
    if i == 0:
        if j == 0:
            return math.cos(2 * t)
        if j == 1:
            return math.sin(2 * t)
        if j == 2:
            return math.sin(t)
    if i == 1:
        if j == 0:
            return math.sin(2 * t)
        if j == 1:
            return math.cos(2 * t)
        if j == 2:
            return -math.sin(t)
    if i == 2:
        if j == 0:
            return -math.sin(t)
        if j == 1:
            return math.sin(t)
        if j == 2:
            return math.cos(t)

class UpdatingMatrix(VGroup):    
    def __init__(
        self,
        matrix_func,            # (t, i, j) -> float
        rows : int,
        cols : int, 
        decimal_places=2,       # Number of decimal places to display
        element_buff=0.8,       # Horizontal buffer between elements
        row_buff=0.6,           # Vertical buffer between rows
        bracket_buff=0.2,       # Buffer between brackets and matrix content
        min_width=0.8,          # Minimum width reserved for each number (prevents shifting)
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.matrix_func = matrix_func
        self.rows = rows
        self.cols = cols
        self.decimal_places = decimal_places
        self.element_buff = element_buff
        self.row_buff = row_buff
        self.bracket_buff = bracket_buff
        self.min_width = min_width
        
        self.elements = [[
            DecimalNumber(0, num_decimal_places=decimal_places, include_sign=True) 
            for j in range(cols) ] 
        for i in range(rows) ]
        
        # Position all elements in a grid
        self._position_elements()
        
        # Add all elements to the VGroup
        for row in self.elements:
            for elem in row:
                self.add(elem)
        
        # Create brackets
        self._create_brackets()
    
    def _position_elements(self):
        for i in range(self.rows):
            for j in range(self.cols):
                elem = self.elements[i][j]
                # Fixed position in grid
                x_pos = j * (self.min_width + self.element_buff)
                y_pos = -i * self.row_buff
                elem.move_to([x_pos, y_pos, 0])
    
    def _create_brackets(self):
        # Calculate matrix bounds
        matrix_elements = VGroup(*[elem for row in self.elements for elem in row])
        
        # Get the bounding box
        left = matrix_elements.get_left()[0] - self.bracket_buff
        right = matrix_elements.get_right()[0] + self.bracket_buff
        top = matrix_elements.get_top()[1] + 0.1
        bottom = matrix_elements.get_bottom()[1] - 0.1
        
        # Create brackets using lines
        height = top - bottom
        bracket_tip = 0.15
        
        # Left bracket
        left_bracket = VGroup(
            Line([left, top, 0], [left - bracket_tip, top, 0]),
            Line([left - bracket_tip, top, 0], [left - bracket_tip, bottom, 0]),
            Line([left - bracket_tip, bottom, 0], [left, bottom, 0])
        )
        
        # Right bracket
        right_bracket = VGroup(
            Line([right, top, 0], [right + bracket_tip, top, 0]),
            Line([right + bracket_tip, top, 0], [right + bracket_tip, bottom, 0]),
            Line([right + bracket_tip, bottom, 0], [right, bottom, 0])
        )
        
        self.add(left_bracket, right_bracket)
        self.left_bracket = left_bracket
        self.right_bracket = right_bracket
    
    def update_values(self, t):
        for i in range(self.rows):
            for j in range(self.cols):
                value = self.matrix_func(t, i, j)
                self.elements[i][j].set_value(value)
        return self
    
    def create_updater(self, value_tracker):
        return lambda mob : mob.update_values(value_tracker.get_value())

class UpdatingMatrixAnimation(Scene):
    def construct(self):
        N = 3
        
        # Sliding time parameter
        t = ValueTracker(0)
        
        # Time label
        t_label = DecimalNumber(
            t.get_value(),
            num_decimal_places=2,
            include_sign=False
        )
        t_label.add_updater(lambda m: m.set_value(t.get_value()))
        t_text = MathTex(r't = ')
        t_group = VGroup(t_text, t_label).arrange(RIGHT, buff=0.2)
        t_group.to_edge(UP, buff=1)
        
        # Create the stable matrix
        matrix = UpdatingMatrix(
            matrix_func=f,
            rows=N,
            cols=N,
            decimal_places=2,
            element_buff=1.0,
            row_buff=0.7,
            min_width=1.0
        )
        
        # Add matrix label
        f_label = MathTex(r'f(t) = ')
        matrix_group = VGroup(f_label, matrix).arrange(RIGHT, buff=0.3)
        matrix_group.next_to(t_group, DOWN, buff=0.8)
        
        # Link matrix to t parameter
        matrix.add_updater(matrix.create_updater(t))
        
        # Add to scene
        self.add(t_group, matrix_group)
        
        # Animate the parameter
        self.wait()
        self.play(t.animate.set_value(5.0), run_time=3, rate_func=smooth)
        self.play(t.animate.set_value(-2.5), run_time=2, rate_func=linear)
        self.wait()
        self.play(t.animate.set_value(0), run_time=2, rate_func=smooth)
        self.wait()
        
        self.play(FadeOut(*self.mobjects))
        self.wait(1)