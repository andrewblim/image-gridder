
import argparse
import sys
from imagegridder import generateGrid

if __name__ == "__main__":
    
    help_text = \
    """Output size will default to the smallest image size unless otherwise specified.
    The rows R and columns C, if not specified, will be R = C = sqrt(# of images),
    and if # of images is not a perfect square an error is returned. 
    """
    
    parser = argparse.ArgumentParser(description="Generate a grid of images.",
                                     epilog=help_text)
    
    parser.add_argument("-i", "--input",  
                        metavar="filename", type=str, nargs="+", default=[],
                        help="a list of input image files")
    parser.add_argument("-o", "--output",
                        metavar="filename", type=str,
                        help="the filename to write the output to")
    parser.add_argument("-s", "--size", 
                        metavar=("W", "H"), type=int, nargs=2, default=(None, None),
                        help="the desired width W and height H of the image grid in pixels")
    parser.add_argument("-r", "--rows", 
                        metavar="R", type=int, default=None,
                        help="the number of rows in the grid")
    parser.add_argument("-c", "--cols", 
                        metavar="C", type=int, default=None,
                        help="the number of columns in the grid")
    parser.add_argument("-l", "--labels",
                        action="store_true",
                        help="generate row and column labels (will cause image to be bigger than specified in --size)")
    parser.add_argument("-p", "--permute",
                        action="store_true",
                        help="randomly shuffle the order of input image files")
    parser.add_argument("-b", "--border",
                        metavar="W", type=int, default=0,
                        help="add a whitespace border of width W around the image")
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="verbose mode")
    
    args = parser.parse_args()
    
    if (len(args.input) == 0):
        print "No images specified, nothing done (use the -i flag to specify them)."
        sys.exit(0)
    
    generateGrid(input_images=args.input, 
                 output_image=args.output,
                 width=args.size[0],
                 height=args.size[1],
                 rows=args.rows,
                 cols=args.cols,
                 border=args.border,
                 add_labels=args.labels,
                 permute=args.permute,
                 verbose=args.verbose)
    