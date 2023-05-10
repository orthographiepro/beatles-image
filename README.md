# beatles-image
Create your own image configuration for the dot art Lego Beatles set!

## beatles_main
...holds the code invoked in order to create the actual lego-ified image. The source image needs to be a square! 
You might want to change the list of bricks since there are many different dot-art sets. 
Currently it is configured to match the numbers and colors of the Beatles set (duh).

## beatles_lib
...holds the necessary class definitions and algorithms to transform the images.
Experienced best results using the greedy randomized quantization algorithm.
You might want to customize build_image() to fit your needs:

### quantization
* quantize_greedy() - self explanatory, images contain fragments due to the linear iteration when using up all the bricks of one color
* quantize_greedy_randomized() - no more fragments (yay!), yet you might still have some issues in the image since small details such as pupils are improbable to hit at the beginning and thus might not get a strong color such as black to emphasize the contrast.
* also look at the experimental methods

### displaying the image
* show() - simple popup
* show_spaced() - more lego-ish
* show_slice_all() - opens nine popups, one for each 16x16 base plate



## beatles_experimental
...surprisingly holds experimental features such as error diffusion (which produced really ugly results, since the colors tend to clump due to the accummulated error).
Expected better results from Floyd and Steinberg :(
There also is an implementation of the median cut algorithm which quantizes the image really nicely. The problem here is that i still need a proper matching algorithm
to map the quantized colors to Lego brick types of a sufficiently large number and approximate color.

