# mainGUI.py

import pygame
import sys
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

# Variables 
animal_sight_type = None
text_default_images = font.render("1. Default Images", True, BLACK)
text_upload_images = font.render("2. Upload Image", True, BLACK)
text_webcam = font.render("3. Webcam Image", True, BLACK)
text_exit = font.render("0. Exit", True, BLACK)

# Function to display the images
def display_images(original_image, transformed_image):
    # Display original image
    screen.blit(original_image, (50, 50))

    # Display transformed image
    screen.blit(transformed_image, (550, 50))

    # Display navigation bar
    animals = ["Dog", "Cat", "Bird", "Bee", "Bat", "Crab", "Snake"]
    for i, animal in enumerate(animals):
        if animal == animal_sight_type:
            text_animal = selected_font.render(animal, True, BLACK)
        else:
            text_animal = font.render(animal, True, BLACK)
        screen.blit(text_animal, (i * (screen_width // len(animals)), 0))

    # Display return to menu button
    text_return = font.render("Return to Menu", True, BLACK)
    pygame.draw.rect(screen, WHITE, (600, 500, 150, 40))
    screen.blit(text_return, (600, 500))

    pygame.display.flip()

# Function to display the default images section
def display_default_images():
    screen.fill(WHITE)
    
    # Display default images
    original_image, transformed_image = transform_image("images/dog.jpg")
    display_images(original_image, transformed_image)

# Function to display the upload image section
def display_upload_image():
    screen.fill(WHITE)
    
    # Open file dialog to get image path
    root = Tk()
    root.withdraw()
    image_path = filedialog.askopenfilename()
    root.destroy()  # Close the Tkinter window

    if image_path:
        original_image, transformed_image = transform_image(image_path)
        display_images(original_image, transformed_image)

# Function to display the webcam section
def display_webcam():
    screen.fill(WHITE)
    transformed_image = pygame.Surface((400, 400))
    cap = cv2.VideoCapture(0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()

            # Handling mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_click(event.pos)

        _, frame = cap.read()
        cv2.imshow("Webcam", frame)

        # Add transformation to the webcam frame
        transformed_frame = transform_webcam_image(frame, animal_sight_type)

        # Display the transformed frame
        pygame.surfarray.blit_array(transformed_image, np.swapaxes(transformed_frame, 0, 1))
        pygame.display.flip()

        # Break the loop if 'q' key is pressed or menu is not active
        if cv2.waitKey(1) & 0xFF == ord('q') or not menu_active:
            break

    cap.release()
    cv2.destroyAllWindows()

# Flag to track whether to display the main menu
menu_active = True

# Function to handle mouse clicks
def handle_mouse_click(position):
    global menu_active
    if not menu_active:
        # If not in the menu, check for the "Return to Menu" button
        if 600 <= position[0] <= 750 and 500 <= position[1] <= 540:
            menu_active = True  # Set back to True when returning to the menu
    else:
        # If in the menu, check for other options
        if 50 <= position[0] <= 50 + text_default_images.get_width() and 200 <= position[1] <= 200 + text_default_images.get_height():
            display_default_images()
            menu_active = False
        elif 50 <= position[0] <= 50 + text_upload_images.get_width() and 300 <= position[1] <= 300 + text_upload_images.get_height():
            display_upload_image()
            menu_active = False
        elif 50 <= position[0] <= 50 + text_webcam.get_width() and 400 <= position[1] <= 400 + text_webcam.get_height():
            display_webcam()
            menu_active = False
        elif 600 <= position[0] <= 750 and 500 <= position[1] <= 540:
            # "Return to Menu" button is clicked, set menu_active to True
            menu_active = True

# Function to display the menu
def display_menu():
    screen.fill(WHITE)
    text_welcome = font.render("MENÚ", True, BLACK)
    screen.blit(text_welcome, (screen_width // 2 - text_welcome.get_width() // 2, 150))
    pygame.display.flip()

    menu_options = [text_default_images, text_upload_images, text_webcam, text_exit]

    for i, option in enumerate(menu_options):
        screen.blit(option, (50, 200 + i * 100))

    pygame.display.flip()

def transform_image(image_path):
    original_image = pygame.image.load(image_path)
    original_image = pygame.transform.scale(original_image, (400, 400))

    # Convert the image to a NumPy array
    original_array = pygame.surfarray.array3d(original_image)

    if animal_sight_type == "Dog":
        transformed_image = pygame.surfarray.make_surface(np.swapaxes(transform_to_dog_sight(original_array), 0, 1))
    elif animal_sight_type == "Cat":
        transformed_image = pygame.surfarray.make_surface(np.swapaxes(transform_to_cat_sight(original_array), 0, 1))
    elif animal_sight_type == "Bird":
        transformed_image = pygame.surfarray.make_surface(np.swapaxes(transform_to_bird_sight(original_array), 0, 1))
    elif animal_sight_type == "Bee":
        transformed_image = pygame.surfarray.make_surface(np.swapaxes(transform_to_bee_sight(original_array), 0, 1))
    elif animal_sight_type == "Bat":
        transformed_image = pygame.surfarray.make_surface(np.swapaxes(transform_to_bat_sight(original_array), 0, 1))
    elif animal_sight_type == "Crab":
        transformed_image = pygame.surfarray.make_surface(np.swapaxes(transform_to_crab_sight(original_array), 0, 1))
    elif animal_sight_type == "Snake":
        transformed_image = pygame.surfarray.make_surface(np.swapaxes(transform_to_snake_sight(original_array), 0, 1))
    else:
        transformed_image = pygame.surfarray.make_surface(np.swapaxes(original_array, 0, 1))

    return original_image, transformed_image


# Display welcome message
screen.fill(WHITE)
text_welcome = font.render("Welcome to the Animal Sight Visualization Program!", True, BLACK)
text_welcome2 = font.render("Press any key to continue...", True, BLACK)
screen.blit(text_welcome, (50, 50))
screen.blit(text_welcome2, (50, 100))
pygame.display.flip()

# Wait for a key press to continue
waiting_for_key = True
while waiting_for_key:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            waiting_for_key = False

# Display menu
menu_active = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if menu_active:
            display_menu()

            # Handling mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_click(event.pos)

            # Handling key presses
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0 or event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    if event.key == pygame.K_1:
                        display_default_images()
                    elif event.key == pygame.K_2:
                        display_upload_image()
                    elif event.key == pygame.K_3:
                        display_webcam()
                    menu_active = False

    pygame.display.flip()
    pygame.time.delay(30)