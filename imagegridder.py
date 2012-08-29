
import Image
import math
import random
import sys

ASPECT_TOLERANCE = 0
SCALEUP_LINEAR_TOLERANCE = 1.05

def generateGrid(input_images, output_image, height=None, width=None, 
                 rows=None, cols=None, border_width=0, 
                 add_labels=False, permute=False, verbose=False):
    
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
    
    # to do: inherit mode from child images? for now just RGB hard-coded
    output = Image.new("RGB", size=(width, height))
    box_size = (float(width)/cols, float(height)/rows)
    
    for r in range(rows):
        for c in range(cols):
            box = (int(box_size[0] * r), int(box_size[1] * c), 
                   int(box_size[0] * (r+1)), int(box_size[1] * (c+1)))
            print box
            i = cols * r + c
            images[i] = images[i].resize((width, height))
            images[i].save(str(i) + ".jpg")
            output.paste(images[i].crop(box), box)
    
    # if add_labels == True, add some labels on (increasing image size)
    
    
    
    output.save(output_image)