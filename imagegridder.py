
import Image, ImageFont, ImageDraw
import math
import random
import string

ASPECT_TOLERANCE = 0
SCALEUP_LINEAR_TOLERANCE = 1.05
LABEL_SIZE_FACTOR = 0.15
FONT_PATH = "/Library/Fonts/"

def generateGrid(input_images, output_image, height=None, width=None, 
                 rows=None, cols=None, border=0, add_labels=False, 
                 permute=False, verbose=False):
    
    """
    Generates the image grid with indicated height and width and indicated rows
    and columns (tries to make some smart assumptions if these are not
    provided). Optionally adds a border and labels if these are specified. 
    """
    
    if permute: random.shuffle(input_images)
    
    images = []
    for input_image in input_images:
        image = Image.open(input_image)
        images.append(image)
        if verbose:
            print "%s %s %s (aspect %0.3f)" % \
                  (input_image, image.size, image.mode, image.size[0]/image.size[1])
    
    # check aspect ratios for similarity
    
    aspect_ratios = [image.size[0] / image.size[1] for image in images]
    if max(aspect_ratios) - min(aspect_ratios) > ASPECT_TOLERANCE:
        print "Warning: max - min aspect ratio > %f, some images may be distorted." % ASPECT_TOLERANCE
    
    # default values/error checks on the number of rows and cols
    
    n = float(len(input_images))
    if rows == None and cols == None:
        if int(math.sqrt(n)) != math.sqrt(n):
            raise Exception("Rows/columns unspecified, square grid presumed but # of images %d is not a perfect square" % n)
        else:
            rows = int(math.sqrt(n))
            cols = rows
    elif rows == None:
        if int(n/rows) != (n/rows):
            raise Exception("Rows unspecified, columns %d do not divide # of images %d" % (cols, n))
        else:
            rows = int(n/cols)
    elif cols == None:
        if int(n/rows) != n/rows:
            raise Exception("Columns unspecified, rows %d do not divide # of images %d" % (rows, n))
        else:
            cols = int(n/rows)
    if rows * cols != n:
        raise Exception("Rows %d * columns %d do not add up to # of images %d" % (rows, cols, n))
    
    # default values/error checks on the image size
    
    if height == None or width == None:
        sizes = [image.size[0] * image.size[1] for image in images]
        smallest_image = images[sizes.index(min(sizes))]
        (width, height) = smallest_image.size
    
    for image in images:
        if width > image.size[0] * SCALEUP_LINEAR_TOLERANCE:
            print "Warning: image width will be scaled beyond tolerance max %f" % SCALEUP_LINEAR_TOLERANCE
        if height > image.size[1] * SCALEUP_LINEAR_TOLERANCE:
            print "Warning: image height will be scaled beyond tolerance max %f" % SCALEUP_LINEAR_TOLERANCE
    
    if rows > height:
        raise Exception("Number of rows %d greater than height of image %d" % (rows, height))
    if cols > width:
        raise Exception("Number of columns %d greater than width of image %d" % (cols, width))
    
    # generate new image
    
    grid_width = width
    grid_height = height
    width += 2 * border
    height += 2 * border
    if add_labels == True:
        label_width = int(LABEL_SIZE_FACTOR * min(width, height))
        width += label_width
        height += label_width
    else:
        label_width = 0
        
    # to do: inherit mode from child images? for now just RGB hard-coded
    output = Image.new("RGB", size=(width, height), color="white")
    offset = border + label_width
    box_size = (float(grid_width)/cols, float(grid_height)/rows)
    
    for r in range(rows):
        for c in range(cols):
            box = (int(box_size[0] * c), int(box_size[1] * r), 
                   int(box_size[0] * (c+1)), int(box_size[1] * (r+1)))
            offset_box = tuple([x + offset for x in box])
            i = cols * r + c
            images[i] = images[i].resize((grid_width, grid_height))
            output.paste(images[i].crop(box), offset_box)
    
    # if add_labels == True, add some labels on (increasing image size)
    
    if add_labels == True:
        
        font_size = int(min(box_size[0], box_size[1])/3)
        font = ImageFont.truetype(FONT_PATH + "Arial.ttf", font_size, encoding="unic")
        draw = ImageDraw.Draw(output)
        font_offset = int(box_size[1]/3)
        for r in range(rows):
            draw_point = (border, offset + font_offset + int(box_size[1] * r))
            draw.text(draw_point, str(r+1), font=font, fill="black")
        font_offset = int(box_size[0]/3)
        for c in range(cols):
            draw_point = (offset + font_offset + int(box_size[0] * c), border)
            draw.text(draw_point, int2colstring(c+1), font=font, fill="black")

    output.save(output_image)
    

def int2colstring(x):
    """
    Converts an int to a column string (base 26 where the digits are A-Z). 
    Adapted from Alex Martelli's int2base code from the thread 
    http://stackoverflow.com/questions/2267362/convert-integer-to-a-string-in-a-given-numeric-base-in-python
    """
    if x < 0: sign = -1
    elif x==0: return '0'
    else: sign = 1
    x *= sign
    digits = []
    while x:
        digits.append(string.uppercase[x % 26 - 1])
        x /= 26
    if sign < 0:
        digits.append('-')
    digits.reverse()
    return ''.join(digits)