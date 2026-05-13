# HIT137 Assignment 3

## Files
- `game_manager.py` = game manager module for integration.
- `demo_app.py` =  Tkinter demo showing how to use the manager.
- `requirements.txt` = required packages.

## Install
```bash
pip install -r requirements.txt
```

## Run demo
```bash
python demo_app.py
```

## How  can be  integrate

```python
from game_manager import GameManager

manager = GameManager()
manager.load_image("sample.jpg")

# In Tkinter click event on modified image:
result = manager.handle_click(event.x, event.y)

# For reveal button:
result = manager.reveal_unfound()

# For displaying images:
original_rgb = manager.get_original_rgb()
modified_rgb = manager.get_modified_rgb()

# For drawing circles:
original_marked = manager.draw_markers_for_display(original_rgb)
modified_marked = manager.draw_markers_for_display(modified_rgb)
```

## Assignment rule coverage
- OOP: uses multiple classes, constructor, methods, class interaction, inheritance and polymorphism.
- OpenCV: loads images and performs all image manipulation using OpenCV.
- Differences: generates exactly 5 random, non-overlapping difference regions.
- Alteration types: colour shift, local blur, brightness change.
- Click checking: validates clicks against known difference regions.
- Mistakes: maximum 3 mistakes per image.
- Reveal: reveals all unfound differences.
- Portable: `game_manager.py` can be copied directly into the group project.