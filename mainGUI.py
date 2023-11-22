# mainGUI.py

import pygame
from tkinter import Tk, filedialog
import cv2
import numpy as np
from mainCode import *

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

# Font settings
font = pygame.font.Font(None, 36)
selected_font = pygame.font.Font(None, 40)

# Display welcome message
screen.fill(WHITE)
text_welcome = font.render("Welcome to the Animal Sight Visualization Program!", True, BLACK)
screen.blit(text_welcome, (50, 50))
pygame.display.flip()

# Display menu
menu_active = True
while menu_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                menu_active = False
            elif event.key == pygame.K_1:
                menu_active = False
                animal_sight_type = "Dog"
            elif event.key == pygame.K_2:
                menu_active = False
                animal_sight_type = "Cat"
            elif event.key == pygame.K_3:
                menu_active = False
                animal_sight_type = "Bird"

# Function to display the menu
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

# Function to display the original and transformed images
def display_images(original_image, transformed_image):
    screen.fill(WHITE)

    # Display original image on the left
    screen.blit(original_image, (50, 50))

    # Display transformed image on the right
    screen.blit(transformed_image, (550, 50))

    # Display navigation bar
    animals = ["Dog", "Cat", "Bird", "Bee", "Bat", "Crab", "Snake"]
    for i, animal in enumerate(animals):
        text = font.render(animal, True, BLACK)
        rect = pygame.Rect((i * (screen_width // len(animals)), 0), (screen_width // len(animals), 40))
        pygame.draw.rect(screen, WHITE, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        screen.blit(text, (i * (screen_width // len(animals)) + 10, 5))

    # Highlight the selected animal in the navigation bar
    selected_text = selected_font.render(animal_sight_type or "Default", True, BLACK)
    screen.blit(selected_text, (screen_width // 2 - selected_text.get_width() // 2, 550))

    # Display return to menu button
    pygame.draw.rect(screen, WHITE, (600, 500, 150, 40))  # Return to Menu Button
    text_menu = font.render("Return to Menu", True, BLACK)
    screen.blit(text_menu, (610, 505))

    pygame.display.flip()

# Function to handle image transformation
def transform_image(image_path):
    original_image = pygame.image.load(image_path)
    original_image = pygame.transform.scale(original_image, (400, 400))
    
    if animal_sight_type == "Dog":
        transformed_image = pygame.surfarray.make_surface(np.swapaxes(transform_to_dog_sight(pygame.surfarray.array3d(original_image)), 0, 1))
    elif animal_sight_type == "Cat":
        transformed_image = pygame.surfarray.make_surface(np.swapaxes(transform_to_cat_sight(pygame.surfarray.array3d(original_image)), 0, 1))
    elif animal_sight_type == "Bird":
        transformed_image = pygame.surfarray.make_surface(np.swapaxes(transform_to_bird_sight(pygame.surfarray.array3d(original_image)), 0, 1))
    # Add more cases for other animals

    return original_image, transformed_image

# Main loop
while True:
    if menu_active:
        display_menu()
    else:
        original_image, transformed_image = transform_image("images/dog.jpg")  # Change the image path accordingly
        display_images(original_image, transformed_image)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            if menu_active:
                if 50 <= x <= 200 and 200 <= y <= 240:  # Default Images
                    menu_active = False
                elif 50 <= x <= 200 and 300 <= y <= 340:  # Upload Image
                    root = Tk()
                    root.withdraw()
                    file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
                    root.destroy()
                    if file_path:
                        menu_active = False
                        original_image, transformed_image = transform_image(file_path)
                elif 50 <= x <= 200 and 400 <= y <= 440:  # Webcam Image
                    menu_active = False

            elif not menu_active:
                # Check if a navigation bar option is clicked
                animals = ["Dog", "Cat", "Bird", "Bee", "Bat", "Crab", "Snake"]
                for i, animal in enumerate(animals):
                    if i * (screen_width // len(animals)) <= x <= (i + 1) * (screen_width // len(animals)) and 0 <= y <= 40:
                        animal_sight_type = animal
                        original_image, transformed_image = transform_image("images/dog.jpg")  # Change the image path accordingly
                        break
                # Check if the return to menu button is clicked
                if 600 <= x <= 750 and 500 <= y <= 540:
                    menu_active = True

    pygame.time.delay(30)
