from PIL import Image
from easygui import fileopenbox, msgbox
import turtle, random, os

# TODO - maybe merge similar colors using PIL?

max_size = 256 # max Height or Width of resized image
threshold = 10 # The higher this is the closer to white a pixel has to be for the turtles pen to be up.
               # 0 for best quality. 765 for worst quality.
pensize = [1, 1] # [min, max]

# Filetypes
image_file_types = ["bmp", "eps", "gif", "icns", "ico", "im", "jpg", "jpeg", "msp", "pcx", "png", "ppm", "sgi", "spider", "tiff", "webp", "xbm", "blp", "cur", "dcx", "dds", "fli", "flc", "fpx", "ftex", "gbr", "gd", "imt", "iptc", "nna", "mcidas", "mic", "mpo", "pcd", "pixar", "psd", "tga", "wal", "xpm"]

#Get file name
this_name = os.path.basename(__file__)

def load_image_array(image_name, max_size):
    # Load the image
    im = Image.open(image_name)

    # Convert the image into RGB
    im = im.convert('RGB')

    # Make the image a new size
    im.thumbnail((max_size, max_size), Image.ANTIALIAS)

    # Get image new size
    width, height = im.size

    # Create image_array = array of rows
    # Row = array of (r, g, b, distance_in_pixils_of_this_color)
    image_array = []
    for h in range(height):
        row = []
        pix = [(-1, -1, -1), -1] 
        for w in range(width):
            rgb = im.getpixel((w,h))
            if pix[0] != rgb:
                if(pix[1] > 0):
                    row.append(pix)
                pix = [rgb, 1]
            else:
                pix[1] += 1
                
        row.append(pix)
        image_array.append(row)

    # Return size, image array
    return (width, height), image_array
            
def setup_turtle(image_name, size):
    # Create and name the window, and set it's color to RGB
    window = turtle.Screen()
    window.title(image_name)
    window.colormode(255)

    # Create turtle
    turt = turtle.Turtle()
    turt.speed(0)

    # Move up and left half the image size to center the drawing
    turt.penup()
    turt.backward(int(size[0]/2))
    turt.left(90)
    turt.forward(int(size[1]/2))
    turt.right(90)

    return window, turt

def get_image_name():
    # Get files types
    file_types = []
    for ft in image_file_types:
        file_types.append("*." + ft)

    # Get file
    name = fileopenbox(msg="Please select an image",
                       title=this_name,
                       default="*",
                       filetypes=file_types,
                       multiple=False)

    # Check for valid extension
    x, ext = os.path.splitext(name)
    if ext[1:] not in image_file_types:
        msgbox("Error - '" + ext[1:] + "' is not a supported image file.", this_name)
        return ""
    
    return name
        

def main():
    # Get image
    image_name = get_image_name()
    if image_name == "": return
    
    # Setup
    size, ia = load_image_array(image_name, max_size)
    w, george = setup_turtle(image_name, size)

    # Drawing
    for row in ia:
        george.pendown()
        for pix in row:
            #print(pix)
            # For each pixil in the image, move forward 1 with that pen color
            r, g, b = pix[0]
            if(765-(r+g+b) < threshold):
                george.penup()
            else:
                george.pensize(random.randint(pensize[0], pensize[1]))
                george.pencolor(r, g, b)
                george.pendown()
            
            george.forward(pix[1])
        # At the end of each line move to the start of the next
        george.penup()
        george.left(90)
        george.backward(1)
        george.right(90)
        george.backward(size[0])

    # Finishing up
    george.hideturtle()
    msgbox("Done.", this_name)


# Run the main function
if __name__ == "__main__":
    main()
