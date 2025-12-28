# 5 Defying Infinities: 5 Increasingly Difficult Hat Problems

[![IMAGE ALT TEXT HERE]()]()

[The video]() was animated using [Manim Community (v0.19.0)](https://docs.manim.community/en/stable/index.html). 

The primary Manim script is `main.py`.

## Description

### Problem Statement

## Sources

## How to Render Transparent Scenes
Both of the following options seem to work when within the `klein` directory with the `.venv` activated:
### Option A: 
- Pick a final file name like `A.mov`
- **Command**: `manim render -pqh --format=mov --transparent -o A.mov main.py UpdatingMatrixAnimation`
- **Note**: QuickTime Player can't preview it!
### Option B: 
- Pick an intermediate file name like `A.mov` and a final file name like `B.mov`:
- **Commands**: 
    ```
        manim render -pqh --format=mov --transparent -o A.mov main.py UpdatingMatrixAnimation
        
        ffmpeg -i media/videos/main/1080p60/A.mov -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le B.mov << EOF 
    y 
    EOF
    ```
- **Note**: QuickTime can preview this one!
