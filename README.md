# 🔍 Spot the Difference Game

A desktop image-processing game developed with Python, Tkinter and OpenCV.  
The program accepts BMP, JPG and PNG images, automatically creates five visual differences and challenges the player to identify them.

<img width="2051" height="1058" alt="image" src="https://github.com/user-attachments/assets/a21be5ef-551a-470a-93b5-3a4567dd777b" />


## ✨ Features

- Loads BMP, JPG, JPEG and PNG images
- Displays the original and modified images side by side
- Generates five random, non-overlapping differences
- Applies colour shifts, blurring, brightness changes and rectangles
- Detects correct and incorrect clicks
- Allows a maximum of three mistakes
- Tracks found differences and total mistakes
- Reveals remaining differences when the game ends
- Includes victory and game-over states

## 🛠️ Technologies Used

- Python
- Tkinter
- OpenCV
- NumPy
- Pillow
- Object-oriented programming

## 📁 Project Structure

```text
image-difference-game/
├── spot_the_difference.py
├── README.md
├── sample_images/
├── screenshots/
```

## 🚀 Installation

1. Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/python-spot-the-difference-game.git
```

2. Open the project folder:

```bash
cd python-spot-the-difference-game
```

3. Install the required libraries:

```bash
pip install -r requirements.txt
```

4. Run the game:

```bash
python spot_the_difference.py
```

## 🎮 How to Play

1. Select **Load Image**.
2. Choose a BMP, JPG, JPEG or PNG image.
3. Compare the original and modified images.
4. Click differences in the modified image.
5. Find all five differences before making three mistakes.
6. Select **Reveal all** if you want to display the remaining differences.

Sample images are available in the `sample_images` folder.

## 🧠 What I Learned

Through this project, I developed experience in:

- Designing a Python application using multiple classes
- Applying object-oriented programming principles
- Processing images using OpenCV and NumPy
- Building a desktop interface using Tkinter
- Handling mouse events and application states
- Generating random, non-overlapping image regions
- Integrating independently developed components in a team project
- Testing and debugging a complete interactive application

## 👥 Team and Contributions

This project was developed by four team members. The application was divided into four main classes so that each member had primary responsibility for one component.

| Team member                  | Main responsibility                     | Contribution                                                                                                                                                 |
| ---------------------------- | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Duc Nghia Nguyen**         | `ImageProcessor` class and group leader | Developed image loading, resizing and conversion; generated non-overlapping differences; and applied colour shifts, blur, brightness changes and rectangles. |
| **Md Tamim Mahmud Hawlader** | `GameManager` class                     | Managed the game state, player clicks, found differences, remaining differences, mistakes, victory conditions and game-over conditions.                      |
| **Phuong Vy Ho**             | `Difference` class                      | Represented each generated difference and implemented point detection, overlap checking, centre calculation and marker radius calculation.                   |
| **That Quoc Thien Ton**      | GUI class (`SpotTheDifferenceApp`)      | Developed the Tkinter interface, image canvases, buttons, status displays, event handling and visual markers.                                                |

### My Role as Group Leader

In addition to developing the `ImageProcessor` class, I coordinated the team’s work and integrated the four independently developed classes into the final application. This involved ensuring that the classes exchanged data correctly, resolving compatibility issues between components and adjusting the combined code so that the complete game operated reliably.

I also improved the image-loading process so the application could accept multiple common image formats, including **BMP, JPG, JPEG and PNG**. Images are converted into a consistent RGB format before being processed, allowing the rest of the application to work with different source formats without requiring separate processing logic.

Through this role, I gained practical experience in team coordination, component integration, debugging, image processing and maintaining consistency across a multi-class Python application.


**My contribution:** As the group leader, I helped coordinate the project and integrate the final application. My main technical responsibility was developing the image-processing component, including image loading, difference generation, overlap detection and visual alterations.

## 📌 Academic Project Notice

This repository is a portfolio version of a university group project. Team members are credited for their contributions. The repository is intended to demonstrate programming, teamwork and image-processing skills.
