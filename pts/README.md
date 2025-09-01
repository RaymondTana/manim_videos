## Dimension is Not (Just) a Global Property!

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/Xo9yF5MV5JQ/0.jpg)](https://youtu.be/Xo9yF5MV5JQ)

Otherwise known as **How Compression relates to Fractals**, this video covers the application of incompressibility to fractal geometry. Namely, we introduce *fractal dimension*, *Kolmgorov complexity*, *effective dimension*, and the *Point-to-Set Principle*. [The video](https://youtu.be/Xo9yF5MV5JQ) was animated using [Manim Community (v0.19.0)](https://docs.manim.community/en/stable/index.html). 

This video was submitted as part of the 2025 Summer of Math Exposition (SoME4).

The primary Manim script is `main.py`.

## Description

Geometry class has convinced us that dimension is inherently a macroscopic property; i.e., that you can't understand the dimension of a shape without "zooming out" and seeing how much space it takes up. It has also convinced us that all points are created equal: that is, that all points are zero-dimensional. Yet, surprisingly, there is a meaningful way to describe the (possibly nonzero) "space" taken up by a point from the perspective of algorithms. More precisely, every point has an effective dimension related to how hard it is to produce approximations to that point -- or, equivalently, how hard it is to compress its digits. And the geometric/fractal dimension of any shape is computed as the maximal effective dimension across all the points in that shape. So, the dimension of a set comes from its least compressible elements. 

In this video, I discuss all these concepts, state the main theorem (The Point-to-Set Principle) which relates effective dimension of points to the fractal dimension of sets, and show how one may use this theorem to calculate the fractal dimension of a standard fractal known as the Middle-1/3 Cantor Set. 

