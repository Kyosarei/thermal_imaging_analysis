from PIL import Image
import os

def load_image(image_path):
    """
    Receives an image file and returns a second image in grayscale.
    image -> image
    """
    img = Image.open(image_path).convert('L')
    return img

def min_max_bright(img):
    """Establishes a numeric value based on brightness by iterating through each pixel, regardless of size,
    and returns the maximum and minimum brightness of the image.
    load_image, int, int -> tuple"""
    width, height = img.size
    bright_min = 255
    bright_max = 0

    # Iterating through the image's pixel matrix
    # Analyzes each pixel and updates the minimum and maximum values during each iteration
    for y in range(height):
        for x in range(width):
            bright = img.getpixel((x, y))
            if bright > bright_max:
                bright_max = bright
            if bright < bright_min:
                bright_min = bright

    return bright_min, bright_max

def bright_to_temperature(bright, bright_min, bright_max):
    """
    Parameterizes the brightness values based on the maximum and minimum values for the 0 to 255 intensity scale
    and assigns a pseudo-temperature from 0 to 100 for better pattern comprehension.
    bright -> float
    bright_min -> int
    bright_max -> int
    Returns -> float
    """
    if bright_max == bright_min:
        return 0  # Prevents invalid division by zero
    parametrization = (bright - bright_min) / (bright_max - bright_min)
    temperature = parametrization * 100  # Converts to the 0 to 100 scale
    return temperature

def analyze_image(img, bright_min, bright_max, min_temp_threshold=80, min_bright_threshold=180):  # temp 0 to 100, bright 0 to 255
    """
    Establishes brightness and pseudo-temperature thresholds for pixel analysis, removing occurrences of 
    non-critical areas. Even if the pseudo-scale is high, the image may still be dark and not visually alarming.
    Uses pillow.getpixel to create a new image highlighting pixels that exceed both thresholds with red pixels.

    img -> Image
    bright_min -> int
    bright_max -> int
    min_temp_threshold -> int
    min_bright_threshold -> int
    Returns -> tuple (coordinates, Image)
    """
    width, height = img.size
    risk_coordinates_list = []  # Stores the coordinates of every pixel that exceeds both thresholds
    highlighted_image = img.convert('RGB')  # Converts image back to RGB to create a new image with red pixels

    # Iterate through the image matrix for each coordinate to analyze based on the established parameters
    for y in range(height):
        for x in range(width):
            bright = img.getpixel((x, y))
            temperature = bright_to_temperature(bright, bright_min, bright_max)

            if temperature >= min_temp_threshold and bright >= min_bright_threshold:
                # Append the list with the coordinates and temperature if conditions are met
                risk_coordinates_list.append((x, y, temperature))
                highlighted_image.putpixel((x, y), (255, 10, 0))  # Colors the pixel red

    return risk_coordinates_list, highlighted_image

def save_coordinates(risk_coordinates_list, image_num):
    """Saves the list of coordinates and temperatures to a .txt file in the current directory."""
    file_name = f"coordinates_temperature_image{image_num}.txt"

    # Opens the file for writing ('w' mode overwrites or creates the file)
    with open(file_name, 'w') as file:
        # Iterates over the list of coordinates and temperatures
        for coord in risk_coordinates_list:
            # Formats the coordinates and temperature as a string and writes to the file
            file.write(f"Coordinate: ({coord[0]}, {coord[1]}) - Temperature: {coord[2]:.2f}\n")

    # Message indicating successful file save
    print(f"Coordinates and temperatures saved in '{file_name}'.")
    if os.name == 'nt':
        os.startfile(file_name)
    else:
        print(f"The file '{file_name}' would be automatically opened, but it cannot be because your system is not Windows.")

def save_image(img, image_num):
    """Saves the final image in the project folder with a dynamic name."""
    img.save(f"highlighted_image{image_num}.png")

def choose_image():
    """
    Displays a list of available images (image1 to image10) and allows the user to choose one.
    Returns the path of the selected image.
    """
    print("Choose an image from the options below:")
    for i in range(1, 11):
        print(f"{i}. image{i}.png")

    # Receives the user's choice
    choice = int(input("Enter the number of the image you want to analyze (1 to 10): "))

    # Checks if the choice is within the valid range
    if choice < 1 or choice > 10:
        print("Invalid choice! Choose a number between 1 and 10.")
        return choose_image()  # Recursively calls the function if the choice is invalid

    # Returns the chosen image number
    return choice

def main():
    """
    Main function that manages the entire image analysis process:
    - Load the selected image
    - Obtain the minimum and maximum brightness values
    - Analyze regions of high temperature in the image
    - Save the highlighted image and print the coordinates of high-temperature regions.
    """
    while True:  # Establishes a loop
        # Step 1: Choose the image
        image_num = choose_image()

        # Step 2: Load and convert the image to grayscale
        image_path = f"imagem{image_num}.png"
        img = load_image(image_path)

        # Step 3: Determine the minimum and maximum brightness of the image
        bright_min, bright_max = min_max_bright(img)

        # Step 4: Analyze the image for high-temperature regions
        risk_coordinates_list, highlighted_image = analyze_image(img, bright_min, bright_max)

        # Step 5: Save files
        save_coordinates(risk_coordinates_list, image_num)

        # Step 6: Display the results and save the new image with highlights
        print(f"Coordinates of regions exceeding the temperature limit are in 'coordinates_temperature_image{image_num}.txt'.")
        print(f"The darkest pixel has a brightness of {bright_min}, and the brightest pixel has {bright_max}.")

        save_image(highlighted_image, image_num)
        print(f"Highlighted image saved as 'highlighted_image{image_num}.png'.")

        # Display the new image
        highlighted_image.show()

        # Continue or exit the loop
        continue_analysis = input("Analyze another image? (y/n): ").strip().lower()
        if continue_analysis != 'y':
            print("Thank you for using the program. See you next time!")
            break

        else:
            print("Sure, please choose another image:")

main()
