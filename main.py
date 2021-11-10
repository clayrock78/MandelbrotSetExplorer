"""
* Clayton Jones * 11-9-2021 *

Mandelbrot explorer front-end
"""

# Import statements
import pygame as pg
#from pygame.locals import K_r
import calculate_bounds
import os

from numpy.lib.type_check import real

global cwd, rendered
cwd = os.path.dirname(os.path.realpath(__file__))
rendered = False

global max_iterations
max_iterations = 500

# Function Definitions

def show_iters(screen, font):
    global max_iterations

    # Show the user the iterations
    iteration_text = font.render(f"Iterations = {max_iterations}", True, (0,255,0))
    iteration_rect = iteration_text.get_rect()
    iteration_rect.center = (90,22)
    iteration_rect.left = 10
    screen.blit(iteration_text, iteration_rect)

def make_image(real_bounds, pixel_bounds):
    global max_iterations
    scale = pixel_bounds[0][1]

    with open(cwd + "\\backend\\bounds.txt", "w") as file:
        # Unpack  bounds
        x_bounds, y_bounds = real_bounds
        lower_x, upper_x = x_bounds
        lower_y, upper_y = y_bounds
        
        # Write information to file 
        file.write(f"{lower_x},{upper_x},{lower_y},{upper_y},{max_iterations},{scale}")

    # Call the backend to generate image
    os.system(f'"{cwd}"' + "\\backend\\target\\release\\my-project.exe")

def main():
    global max_iterations, rendered

    width = 500
    height = 500
    real_bounds = (-2,1), (-1.5,1.5)
    pixel_bounds = (0,width), (0,height)

    # Intialize PyGame for our window and click listening
    pg.init()
    
    # Create a screen
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("MBS Explorer v1")

    # Generate the set
    make_image(real_bounds, pixel_bounds)

    # Display the image
    image = pg.image.load(cwd + "\\backend\\mandel.png")
    screen.blit(image, (0,0))
    pg.display.flip()

    font = pg.font.Font("freesansbold.ttf", 50)
    medium_font = pg.font.Font("freesansbold.ttf", 30)
    small_font = pg.font.Font("freesansbold.ttf", 20)

    running = True

    # Main loop : listens for clicks
    while running:

        # Event Handling
        for event in pg.event.get():

            # Mouse click event
            if event.type == pg.MOUSEBUTTONUP:
                rendered = False
                # Get click position
                pos = pg.mouse.get_pos()
                
                # Calculate new bounds
                res = calculate_bounds.calculate(pos, real_bounds, pixel_bounds, 25)
                real_bounds, unused = res

                max_iterations += 100

                # Call backend to make image
                make_image(real_bounds, pixel_bounds)
                
            # Close the program
            if event.type == pg.QUIT:
                running = False
        
        if pg.key.get_focused():
            if pg.key.get_pressed()[ord("=")]:
                rendered = False
                max_iterations = int(max_iterations * 1.5)

            if pg.key.get_pressed()[ord("]")]:
                rendered = False
                max_iterations //= 1.5

            if pg.key.get_pressed()[ord("r")]:
                rendered = False
                real_bounds = (-2,1), (-1.5,1.5)

            # Creating High-Res Render
            if pg.key.get_pressed()[ord("x")]:

                # Tell the user a high-res render is being made
                text = medium_font.render("Generating high-res render", True, (0,255,0), None)
                textrect = text.get_rect()
                textrect.center = (250,250)
                screen.blit(text, textrect)
                pg.display.flip()

                # Begin render
                make_image(real_bounds, ((0,2000), (0,2000)))

                # Reblit old image
                image = pg.image.load(cwd + "\\backend\\mandel.png")
                screen.blit(image, (0,0))

                # Show max iterations        
                show_iters(screen, small_font)

                # Update the screen
                pg.display.flip()

        if not rendered:
            # Display text to indicate the image is being generated
            text = font.render("Generating Image...", True, (0,255,0), None)
            textrect = text.get_rect()
            textrect.center = (250,250)
            screen.blit(text, textrect)
            pg.display.flip()

            # Call backend to make image
            make_image(real_bounds, pixel_bounds)

            # Display the image
            image = pg.image.load(cwd + "\\backend\\mandel.png")
            screen.blit(image, (0,0))

            # Display the iterations
            show_iters(screen, small_font)

            # Refresh the display
            pg.display.flip()

            rendered = True


# Function calls
if __name__ == "__main__":
    main()
