from manim import *
import math
import numpy as np
import random

class ClickGrid():
    def __init__(self, n = 1, init_state = None):
        self.n = n
        self.grid = []
        for i in range(n):
            self.grid.append([])
            for j in range(n):
                self.grid[i].append(
                    init_state[i][j] if init_state is not None else 1
                )
    def parity_game_click(self, i, j):
        for j_ in range(self.n):
            self.grid[i][j_] = 1 - self.grid[i][j_]
        for i_ in range(self.n):
            if i_ != i:
                self.grid[i_][j] = 1 - self.grid[i_][j]

    def get_solution(self):
        solution_array = []
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j] == 0:
                    solution_array.append((i, j))
        random.shuffle(solution_array)
        return solution_array
    
    def reset_grid(self, value = 1):
        for i in range(self.n):
            for j in range(self.n):
                self.grid[i][j] = value

class ParityBlock(Scene):
    def construct(self):

        # Setup
        n = 7
        table_size = 6
        side_length = table_size / n
        G = ClickGrid(n = n)
        delay = 0.5
        short_delay = 0.2

        self.add(Paragraph("by Raymond Tana", font_size = 25, font = "sans-serif", color = GRAY).to_corner(DR))

        def position(i, j):
            return RIGHT * side_length * (i - (n - 1) / 2) + DOWN * side_length * (j - (n - 1) / 2)

        squares = []

        for i in range(n):
            squares.append([])
            for j in range(n):
                s = Square(side_length = side_length)
                s.move_to(position(i, j))
                squares[i].append(s)
        
        self.add(*tuple([square for row in squares for square in row]))

        def assign_color(state):
            return RED if state == 1 else WHITE
        
        def reset_fills():
            for i in range(n):
                for j in range(n):
                    squares[i][j].set_stroke(color = WHITE).set_fill(color = assign_color(G.grid[i][j]), opacity = 1)

        def float_text(text):
            T = Paragraph(text, alignment = "center", font="sans-serif")
            textbox = Rectangle(width = T.width + 0.6, height = T.height + 0.5).set_fill(BLACK, opacity = 0.8).set_stroke(None)
            # textbox.surround(T)
            self.play(FadeIn(textbox), Write(T))
            self.wait(delay)
            self.play(FadeOut(textbox, T))

        # Show the board
        reset_fills()
        self.wait(1)

        # Show the rules of the board
        
        float_text("We have a grid that acts\nsorta like a Rubik's cube...")

        float_text("Every time you click it...")

        cursor = Circle(radius=0.1, color=YELLOW, fill_opacity=1)
        self.play(FadeIn(cursor))
        self.wait(short_delay)
        
        def click(i, j, speed = 0.4):
            # return
            self.play(cursor.animate.move_to(position(i, j)), run_time = speed, rate_func = smooth)
            cursor_copy = cursor.copy()
            square_copy = squares[i][j].copy()
            self.play(square_copy.animate.set_fill(color = BLUE_A), cursor_copy.animate.scale(1.5), run_time = speed)
            G.parity_game_click(i, j)
            reset_fills()
            self.play(FadeOut(square_copy, cursor_copy), run_time = speed)

        click(math.floor(n / 2), math.floor(n / 2))

        float_text("It flips the color of each cell\nin the same row and column!")

        float_text("It can be undone:")

        click(math.floor(n / 2), math.floor(n / 2))

        float_text("And it can get messy...")

        click(0, 2)
        click(n - 1, n - 2)
        click(math.floor(n / 2), math.floor(n / 2) - 1)
        click(math.floor(n / 2) + 1, math.floor(n / 2))
        click(n - 1, n - 1)

        self.wait()

        # Reset

        float_text("Now, let's reset.")
        G.reset_grid(1)
        reset_fills()

        # Start perturbing the board
        float_text("And randomly perturb the board.")

        for count in range(10):
            random_row = math.floor(np.random.random() * n)
            random_col = math.floor(np.random.random() * n)
            click(random_row, random_col, speed = 0.05)
            self.wait(short_delay)

        float_text("How do we get back to where we started?")

        solution = G.get_solution()
        self.wait(delay)
        float_text("Here's one way:")
        
        for step in solution:
            click(*step, speed = 0.08)
            self.wait(short_delay)

        float_text("Solved :)")

        float_text("Try to come up with a\ngeneral strategy yourself!")
        self.wait(0.5)