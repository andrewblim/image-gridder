
import Image

ASPECT_TOLERANCE = 0

def generateGrid(input_images, output_image, height=None, width=None, 
                 rows=None, cols=None, border_width=0, 
                 add_labels=False, verbose=False):
    
    if len(input_images) == 0:
        print "No images specified"
        exit()
    
    aspect_ratios = []
    if verbose: print "Aspect ratios:"
    for input_image in input_images:
        im = Image.open(input_image)
        aspect_ratios.append(im.size[0] / im.size[1])
        if verbose: print "%s %0.4f" % (input_image, im.size[0] / im.size[1])
    
    if max(aspect_ratios) - min(aspect_ratios) > ASPECT_TOLERANCE:
        print "Warning: max - min aspect ratio > %f, some images may be distorted." % ASPECT_TOLERANCE
    
    