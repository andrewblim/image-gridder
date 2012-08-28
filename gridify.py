
import argparse
from imagegridder import generateGrid

if __name__ == "__main__":
    
    help_text = \
    """Output size will default to the smallest image size unless otherwise specified.
    The rows R and columns C, if not specified, will be R = C = sqrt(# of images),
    and if # of images is not a perfect square an error is returned. 
    """
    
    parser = argparse.ArgumentParser(description="Generate a grid of images.",
                                     epilog=help_text)
    
    parser.add_argument("output", 
                        metavar="output", type=str, nargs=1,
                        help="the filename to write the output to")
    parser.add_argument("-i", "--image",  
                        metavar="file", type=str, nargs="+",
                        help="a list of input image files")
    parser.add_argument("-s", "--size", 
                        metavar=("W", "H"), type=int, nargs=2, default=(None, None),
                        help="the desired width W and height H of the image grid")
    parser.add_argument("-r", "--rows", 
                        metavar="R", type=int, nargs=1, default=None,
                        help="the number of rows in the grid")
    parser.add_argument("-c", "--cols", 
                        metavar="C", type=int, nargs=1, default=None,
                        help="the number of columns in the grid")
    parser.add_argument("-b", "--border", 
                        metavar="W", type=int, nargs=1, default=0,
                        help="the width W of the gridlines (default 0)")
    parser.add_argument("-l", "--labels",
                        action="store_true",
                        help="generate row and column labels (will cause image to be bigger than specified size)")
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="verbose mode")
    
    args = parser.parse_args()
    
    generateGrid(input_images=args.image, 
                 output_image=args.output,
                 width=args.size[0],
                 height=args.size[1],
                 rows=args.rows,
                 cols=args.cols,
                 border_width=args.border,
                 add_labels=args.labels,
                 verbose=args.verbose)
    
    