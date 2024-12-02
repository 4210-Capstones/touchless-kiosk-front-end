from pathlib import Path
import pygame
import sys
import time
import os
import datetime
import json

# Function to initialize the metadata file
def initialize_metadata_file(metadata_file):
    """
    Ensures the metadata file exists. If not, creates an empty JSON file.

    Args:
        metadata_file (str): Path to the metadata JSON file.
    """
    if not os.path.exists(metadata_file):
        # Create the metadata file if it doesn't exist
        with open(metadata_file, "w") as file:
            json.dump({}, file)  # Create an empty JSON object
        print(f"Metadata file created at {metadata_file}.")
    else:
        # If the file exists, just print a message
        print(f"Metadata file already exists at {metadata_file}.")

# Function to load flyers from the folder and metadata file
def load_flyers_from_folder(folder_path, metadata_file):
    """
    Loads flyers and their metadata from a designated folder. 
    Automatically adds new flyers to the metadata file with a placeholder date.

    Args:
        folder_path (str): Path to the folder containing flyer images.
        metadata_file (str): Path to a JSON file with metadata (expiration dates).

    Returns:
        list of dict: Flyers with 'image_path' and 'expiration_date'.
    """
    flyers = []  # List to hold valid flyers
    today = datetime.date.today()  # Get today's date

    # Load existing metadata from the JSON file
    with open(metadata_file, "r") as file:
        metadata = json.load(file)

    # Check all files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):  # Only process files (not subdirectories)
            # If the file isn't already in the metadata, add it
            if file_name not in metadata:
                # Add new flyer with a default expiration date (7 days from today)
                default_expiration = today + datetime.timedelta(days=7)
                metadata[file_name] = default_expiration.isoformat()  # Store the date in ISO format
                print(f"Added new flyer to metadata: {file_name} (expires {default_expiration})")

            # Only include flyers with valid expiration dates
            expiration_date = datetime.date.fromisoformat(metadata[file_name])
            if expiration_date >= today:  # Check if the flyer is still valid
                flyers.append({"image_path": file_path, "expiration_date": expiration_date})

    # Save updated metadata back to the JSON file
    with open(metadata_file, "w") as file:
        json.dump(metadata, file, indent=4)

    return flyers  # Return the list of valid flyers

# Function to display the slideshow of flyers
def display_slideshow(folder_path, metadata_file, display_time=3, refresh_interval=30):
    """
    Displays a looping slideshow of valid flyers, dynamically adding new ones.

    Args:
        folder_path (str): Path to the folder containing flyer images.
        metadata_file (str): Path to a JSON file with metadata (expiration dates).
        display_time (int): Duration to display each image (in seconds).
        refresh_interval (int): Interval to check for new flyers (in seconds).
    """
    pygame.init()  # Initialize Pygame
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Set up fullscreen display
    pygame.display.set_caption("Club Event Slideshow")  # Set the window title

    while True:
        # Load valid flyers dynamically from the folder and metadata file
        flyers = load_flyers_from_folder(folder_path, metadata_file)
        image_paths = [flyer["image_path"] for flyer in flyers]  # Get the paths of valid images

        for image_path in image_paths:
            try:
                # Load and display the image
                image = pygame.image.load(image_path)  # Load the image file
                screen_size = screen.get_size()  # Get the screen size
                image = pygame.transform.scale(image, screen_size)  # Scale the image to fit the screen
                screen.blit(image, (0, 0))  # Display the image on the screen
                pygame.display.flip()  # Update the display to show the new image

                # Wait for the display time before switching to the next image
                start_time = time.time()  # Get the current time
                while time.time() - start_time < display_time:  # Keep the image for the specified display time
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                            pygame.quit()  # Close the Pygame window on quit
                            sys.exit()  # Exit the program
            except pygame.error as e:
                # If an error occurs while loading the image, print the error
                print(f"Error loading image {image_path}: {e}")

        # Wait before refreshing the flyer list
        time.sleep(refresh_interval)

# Example usage of the script
if __name__ == "__main__":
    # Path to the folder containing the flyer images
    # THIS NEEDS TO BE CHANGED TO THE APPROPRIATE DIRECTORY FOR THE KIOSK
    folder_path = Path("../../images").resolve()
    
    # THIS NEEDS TO BE CHANGED TO THE APPROPRIATE DIRECTORY FOR THE KIOSK
    metadata_file = folder_path / "flyer_metadata.json"

    # Ensure the metadata file exists (create it if necessary)
    initialize_metadata_file(metadata_file)

    # Start the slideshow, displaying each image for 5 seconds and refreshing the flyer list every 30 seconds
    display_slideshow(folder_path, metadata_file, display_time=5, refresh_interval=30)
