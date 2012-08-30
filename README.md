
image-gridder
=============

About
-----

image-gridder takes a bunch of input image files (presumably all of roughly equal dimensions) and generates an output file consisting of a grid where each square corresponds to a square on an input image. Why would I write such a program? To generate [Sporcle](http://www.sporcle.com/) quizzes, of course. Here's [one I created](http://www.sporcle.com/games/andrew_lim/album-cover-remix) with this program. Inspiration from a very old [GameFAQs competition](http://www.gamefaqs.com/features/c0003.html), the picture isn't even there any more, I randomly remembered it the other day and thought it would make a good Sporcle quiz. 

License: MIT, included in `license.txt`. 

Requirements
------------

- [PIL](http://www.pythonware.com/products/pil/); as with other Python packages I suggest installing with `pip`
- [freetype](http://www.freetype.org/), though some other library to handle TrueType may also work
- You may need image libraries; for example if you want to manipulate JPEGs you'll need a library such as [libjpeg](http://libjpeg.sourceforge.net/). 

Usage
-----

Use the `-h` or `--help` flag to get command-line help. 

In general you will run it as `python gridify.py -i [image files] -o [output image filename]`. You can specify the image files one by one, or you can use Unix-style wildcards; for example, if you have a directory `images` consisting solely of the images you want, use `-i images/*`. Use the `-s` or `--size` flags to control the size of the output image; the program will warn you if this involves scaling up an image beyond the built-in threshold of 1.05x. 

If you don't specify rows and/or columns with the `-r` and/or `-c` flags, it will assume you want a square, and will expect a perfect-square number of input images. If you specify only rows or columns, it will expect that this number will cleanly divide the number of input images and will generate a grid accordingly. 

The output grid populates left to right along each row and then moves down the rows. So the first image appears in the upper left corner, the second image is to its right, and so on until the row is filled, and then the next row is filled left to right, etc. If you specify a wildcard I believe `argparse` expands this to the same order that your system would, presumably alphabetical, and so if you want a specific order you either have to write out the image files one by one or rename the image files. Use the `-p` flag to randomly shuffle the order. 

Add a white border with `-b`, `--border` and labels with `-l`, `--labels` if so desired. 

FAQ
---

**I'm having some issues with JPGs/I'm having some issues with fonts.**

If you're getting error messages such as `IOError: decoder jpeg not available` or `ImportError: The _imagingft C module is not installed`, then that means you are lacking libraries to handle JPEGs or font rendering, respectively. You'll need to install libraries like libjpeg and freetype. 

When you install PIL (I've only tried with pip but I'd be surprised if you didn't get this when installing via other methods) you should get a summary that will say something like

    --------------------------------------------------------------------
    --- TKINTER support available
    --- JPEG support available
    --- ZLIB (PNG/ZIP) support available
    --- FREETYPE2 support available
    --- LITTLECMS support available
    --------------------------------------------------------------------

indicating some optional features that are and are not available. If you see "support not available" for JPEG/FREETYPE2 then this is the problem. 

On OS X, which is what I personally use: I used Homebrew to install the `libjpeg` and `freetype` packages. You'll need to reinstall PIL afterwards. 

To-do
-----

Selection of font size for labels is not all that intelligent. It won't stop you from making tiny font labels. If you include many images, the labels will get big and may overflow into each other and/or the grid. 
