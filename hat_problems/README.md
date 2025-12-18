# 5 Defying Infinities: 5 Increasingly Difficult Hat Problems

[![IMAGE ALT TEXT HERE]()]()

This video increments through five increasingly complex problems involving guessing numbers written on hats. Along the way, we encounter and develop facts about cardinal and ordinal numbers, opening up the wild zoo of infinities. [The video]() was animated using [Manim Community (v0.19.0)](https://docs.manim.community/en/stable/index.html). 

The primary Manim script is `main.py`.

## Description

### Problem Statement

There are some players each donned with a hat bearing a number. Each player may only see the numbers on all others' hats. Each player submits a *finite* (unless otherwise specified) list of numbers which might be on their own hat: this submission is made once and simultaneously with all other players. So long as *at least one* player's list contains their own number, everyone wins. Players may confer on a strategy; but once numbers are assigned, no communication may be had. Each of the following variants specifies the quantity of players and the type of numbers worn on their hats.

### The 5 Levels of Difficulty

1. **Level 1 [Two with $\mathbb{N}$]**: Two players are assigned a *natural* number on each of their hats.
2. **Level 2 [Two with $\mathbb{Q}$]**: Two players are assigned a *rational* number on each of their hats.
3. **Level 3 [Two with $\mathbb{R}$]**: Two players are assigned a *real* number on each of their hats, and may submit *countably infinitely* many guesses.
4. **Level 4 [Three with $\mathbb{R}$]**: Three players are assigned a *real* number on each of their hats.
    1. Prove it is impossible to guarantee a win if there were only two players assigned real numbers and submitting only finitely many guesses.  
5. **Level 5 [$n + 2$ with $\aleph_n$]**: $n + 2$ players are assigned an element from a set of cardinality $\aleph_n$ on each of their hats.

### Required Background

1. Natural numbers, rational numbers, and real numbers.
2. Differently sized infinities: countability vs uncountability, Cantor’s diagonalization argument.
3. Cardinality of sets and bijections.
4. Ordinals and cardinals!
5. Continuum Hypothesis.

## Sources

- [Popular article](https://www.nytimes.com/2001/04/10/science/why-mathematicians-now-care-about-their-hat-color.html) about Hat Problems by Sara Robinson, 2001: 
    - Robinson, Sara. “Why Mathematicians Now Care About Their Hat Color.” *The New York Times*, April 10, 2001. https://www.nytimes.com/2001/04/10/science/why-mathematicians-now-care-about-their-hat-color.html.
- [Book](https://doi.org/10.1007/978-3-319-01333-6): *The Mathematics of Coordinated Inference* by Christopher S. Hardin and Alan D. Taylor, 2013:
    - Hardin, Christopher S., and Alan D. Taylor. *The Mathematics of Coordinated Inference: A Study of Generalized Hat Problems*. Developments in Mathematics, vol. 32. Springer, Cham, 2013. https://doi.org/10.1007/978-3-319-01333-6.
- [Reddit post](https://www.reddit.com/r/math/comments/pimd8c/unreasonably_difficult_hatprisoner_puzzles/):
    - `u/redstonerodent` (original post) and `u/jfb1337` (comment). *Unreasonably difficult hat/prisoner puzzles.* Reddit, `r/math`. Posted 2021. Available at: https://www.reddit.com/r/math/comments/pimd8c/unreasonably_difficult_hatprisoner_puzzles/.
- [StackExchange thread](https://math.stackexchange.com/questions/4595594/riddle-finite-set-that-contains-one-of-the-three-numbers):
    - Antoine, *Riddle: finite set that contains one of the three numbers*, Math StackExchange, https://math.stackexchange.com/questions/4595594/riddle-finite-set-that-contains-one-of-the-three-numbers. Question posted Dec. 10, 2022; answer by David Clyde, comment/edits by Asaf Karagila.