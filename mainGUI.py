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

# Variables 
animal_sight_type = None

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
            elif event.key == pygame.K_4:
                menu_active = False
                animal_sight_type = "Bee"
            elif event.key == pygame.K_5:
                menu_active = False
                animal_sight_type = "Bat"
            elif event.key == pygame.K_6:
                menu_active = False
                animal_sight_type = "Crab"
            elif event.key == pygame.K_7:
                menu_active = False
                animal_sight_type = "Snake"

# Function to display the menu
def display_menu():
    screen.fill(WHITE)

    # Display welcome message
    screen.fill(WHITE)
    text_welcome = font.render("MENÚ", True, BLACK)
    screen.blit(text_welcome, (screen_width // 2 - text_welcome.get_width() // 2, 150))
    pygame.display.flip()

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
    elif animal_sight_type == "Bee":
        transformed_image = pygame.surfarray.make_surface(np.swapaxes(transform_to_bee_sight(pygame.surfarray.array3d(original_image)), 0, 1))
    elif animal_sight_type == "Bat":
        transformed_image = pygame.surfarray.make_surface(np.swapaxes(transform_to_bat_sight(pygame.surfarray.array3d(original_image)), 0, 1))
    elif animal_sight_type == "Crab":
        transformed_image = pygame.surfarray.make_surface(np.swapaxes(transform_to_crab_sight(pygame.surfarray.array3d(original_image)), 0, 1))
    elif animal_sight_type == "Snake":
        transformed_image = pygame.surfarray.make_surface(np.swapaxes(transform_to_snake_sight(pygame.surfarray.array3d(original_image)), 0, 1))
    else:
        transformed_image = pygame.surfarray.make_surface(np.swapaxes(original_image, 0, 1))

    return original_image, transformed_image

# Main loop
menu_active = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if menu_active:
            display_menu()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    pygame.quit()
                elif pygame.K_1 <= event.key <= pygame.K_7:
                    menu_active = False
                    animal_sight_type = ["Dog", "Cat", "Bird", "Bee", "Bat", "Crab", "Snake"][event.key - pygame.K_1]

        else:
            # Handling mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                # Check if the return to menu button is clicked
                if 600 <= x <= 750 and 500 <= y <= 540:
                    menu_active = True

                # Check if the navigation bar is clicked
                elif 0 <= y <= 40:
                    animals = ["Dog", "Cat", "Bird", "Bee", "Bat", "Crab", "Snake"]
                    for i, animal in enumerate(animals):
                        if i * (screen_width // len(animals)) <= x <= (i + 1) * (screen_width // len(animals)):
                            animal_sight_type = animal
                            break

                # Check if the default images button is clicked
                elif 50 <= y <= 90:
                    if 50 <= x <= 450:
                        original_image, transformed_image = transform_image("images/dog.jpg")
                    elif 550 <= x <= 950:
                        original_image, transformed_image = transform_image("images/cat.jpg")
                    



                # Check if the upload image button is clicked
                elif 150 <= y <= 190:
                    root = Tk()
                    root.withdraw()
                    image_path = filedialog.askopenfilename()
                    if image_path:
                        original_image, transformed_image = transform_image(image_path)

                # Check if the webcam image button is clicked
                elif 250 <= y <= 290:
                    cap = cv2.VideoCapture(0)
                    while True:
                        _, frame = cap.read()
                        cv2.imshow("Webcam", frame)

                        # Add transformation to the webcam frame
                        transformed_frame = transform_webcam_image(frame, animal_sight_type)

                        # Display the transformed frame
                        pygame.surfarray.blit_array(transformed_image, np.swapaxes(transformed_frame, 0, 1))
                        pygame.display.flip()

                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break

                    cap.release()
                    cv2.destroyAllWindows()

    pygame.time.delay(30)