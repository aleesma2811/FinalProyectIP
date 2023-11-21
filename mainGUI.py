## All code functions and image transformations are in mainCode.py
### Author: Efren Flores

import pygame
import cv2
import sys
import numpy as np
from tkinter import Tk, filedialog
import matplotlib.pyplot as plt

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen_width = 900
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Animal Sight Visualization")

# Load images for reference and animal sight
default_image_path = "images/default.jpg"
animal_sight_images = {
    "Dog Sight": "images/dog_sight.jpg",
    "Cat Sight": "images/cat_sight.jpg",
    "Bird Sight": "images/bird_sight.jpg",
    "Bee Sight": "images/bee_sight.jpg",
    "Snake Sight": "images/snake_sight.jpg",
    "Crab Sight": "images/crab_sight.jpg",
}

# Load default image
current_image_path = default_image_path
reference_image = pygame.image.load(current_image_path)
reference_image = pygame.transform.scale(reference_image, (400, 400))
current_animal_sight = None
animal_sight_image = None

# Font settings
font = pygame.font.Font(None, 36)
selected_font = pygame.font.Font(None, 40)

# Initialize webcam capture
cap = cv2.VideoCapture(0)
webcam_active = False

def load_image(image_path, size=(400, 400)):
    image = cv2.imread(image_path)
    image = cv2.resize(image, size)
    return pygame.surfarray.make_surface(np.swapaxes(image, 0, 1))

def transform_to_animal_sight(frame, animal):
    # Implement your transformation logic here
    # This is a placeholder function; you need to replace it with your actual logic
    # For now, it just converts the frame to grayscale
    if animal is not None:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)
    else:
        return frame

def display_menu():
    screen.fill(WHITE)

    # Display menu options
    text_default_images = font.render("Default Images", True, BLACK)
    text_upload_images = font.render("Upload Image", True, BLACK)
    text_webcam = font.render("Webcam Image", True, BLACK)
    screen.blit(text_default_images, (50, 200))
    screen.blit(text_upload_images, (50, 300))
    screen.blit(text_webcam, (50, 400))

    pygame.display.flip()

# Function to display the original image
def display_original_image(image_path):
    original_image = pygame.image.load(image_path)
    original_image = pygame.transform.scale(original_image, (400, 400))
    screen.blit(original_image, (50, 50))
    pygame.display.flip()

def display_images():
    screen.fill(WHITE)

    # Display original image on the left only if a type of sight is selected
    if current_animal_sight:
        screen.blit(load_image(animal_sight_images[current_animal_sight]), (50, 50))

    # Display animal sight image on the right
    if current_animal_sight:
        screen.blit(animal_sight_image, (450, 50))

    # Display navigation bar
    for i, animal in enumerate(animal_sight_images.keys()):
        text = font.render(animal, True, BLACK)
        rect = pygame.Rect((i * (screen_width // len(animal_sight_images)), 0), (screen_width // len(animal_sight_images), 40))
        pygame.draw.rect(screen, WHITE, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        screen.blit(text, (i * (screen_width // len(animal_sight_images)) + 10, 5))

    # Highlight the selected animal in the navigation bar
    selected_text = selected_font.render(current_animal_sight or "Default", True, BLACK)
    screen.blit(selected_text, (screen_width // 2 - selected_text.get_width() // 2, 550))

    # Display return to menu button
    pygame.draw.rect(screen, WHITE, (600, 500, 150, 40))  # Return to Menu Button
    text_menu = font.render("Return to Menu", True, BLACK)
    screen.blit(text_menu, (610, 505))

    pygame.display.flip()


def display_webcam():
    ret, frame = cap.read()

    # Display original webcam footage on the left
    webcam_surface = pygame.surfarray.make_surface(np.swapaxes(frame, 0, 1))
    screen.blit(webcam_surface, (50, 50))

    # Transform frame to animal sight on the right
    if current_animal_sight:
        animal_sight_frame = transform_to_animal_sight(frame, current_animal_sight)
        animal_sight_surface = pygame.surfarray.make_surface(np.swapaxes(animal_sight_frame, 0, 1))
        screen.blit(animal_sight_surface, (550, 50))

    # Display return to menu button
    pygame.draw.rect(screen, WHITE, (800, 500, 150, 40))  # Return to Menu Button
    text_menu = font.render("Return to Menu", True, BLACK)
    screen.blit(text_menu, (810, 505))

    pygame.display.flip()

# Main loop
menu_active = True
webcam_section_active = False
while True:
    if menu_active:
        display_menu()
    elif webcam_section_active:
        display_webcam()
    else:
        display_images()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            if menu_active:
                if 50 <= x <= 200 and 200 <= y <= 240:  # Default Images
                    menu_active = False
                    current_image_path = default_image_path
                    reference_image = pygame.image.load(current_image_path)
                    reference_image = pygame.transform.scale(reference_image, (400, 400))
                    current_animal_sight = None
                    animal_sight_image = None
                elif 50 <= x <= 200 and 300 <= y <= 340:  # Upload Image
                    root = Tk()
                    root.withdraw()
                    file_path = filedialog.askopenfilename(title="Select Image File",
                                                            filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
                    root.destroy()
                    if file_path:
                        menu_active = False
                        current_image_path = file_path
                        reference_image = pygame.image.load(current_image_path)
                        reference_image = pygame.transform.scale(reference_image, (400, 400))
                        current_animal_sight = None
                        animal_sight_image = None
                elif 50 <= x <= 200 and 400 <= y <= 440:  # Webcam Image
                    menu_active = False
                    webcam_section_active = True

            elif not webcam_section_active:
                # Check if a navigation bar option is clicked
                for i, animal in enumerate(animal_sight_images.keys()):
                    if i * (screen_width // len(animal_sight_images)) <= x <= (i + 1) * (screen_width // len(animal_sight_images)) and 0 <= y <= 40:
                        current_animal_sight = animal
                        animal_sight_image = load_image(animal_sight_images[animal])
                        break
                # Check if the return to menu button is clicked
                if 600 <= x <= 750 and 500 <= y <= 540:
                    menu_active = True

            elif webcam_section_active:
                # Check if the return to menu button is clicked
                if 800 <= x <= 950 and 500 <= y <= 540:
                    webcam_section_active = False
                    menu_active = True

    # If using webcam, capture frame and transform to the selected animal sight
    if webcam_active:
        ret, frame = cap.read()
        if ret:
            animal_sight_frame = transform_to_animal_sight(frame, current_animal_sight)
            animal_sight_surface = pygame.surfarray.make_surface(np.swapaxes(animal_sight_frame, 0, 1))
            screen.blit(animal_sight_surface, (550, 50))

# Release webcam and close
if webcam_active:
    cap.release()
pygame.quit()
sys.exit()
