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