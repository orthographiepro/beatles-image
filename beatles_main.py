from beatles_lib import *

dotarray = [
    lego_dot([10, 10, 10], "black", 698),
    lego_dot([90, 90, 90], "dark grey", 141),
    lego_dot([160, 160, 160], "light grey", 51),
    lego_dot([255, 255, 255], "white", 149),
    lego_dot([20, 41, 97], "dark blue", 121),
    lego_dot([112, 141, 161], "grey blue", 52),
    lego_dot([180, 207, 227], "baby blue", 57),
    lego_dot([255, 111, 0], "orange", 74),
    lego_dot([250, 188, 32], "yellow", 65),
    lego_dot([252, 234, 172], "sand", 283),
    lego_dot([189, 172, 115], "beige", 137),    
    lego_dot([186, 122, 45], "light brown", 29),
    lego_dot([217, 107, 56], "orange brown", 85),
    lego_dot([138, 64, 32], "brown", 250),
    lego_dot([74, 34, 17], "dark brown", 554)
]


my_image = lego_image()
my_image.set_original_image("./origin_images/bowie.jpeg")

for dot in dotarray:
    my_image.add_dot(dot)

my_image.shrink()
my_image.quantize_greedy()
my_image.show_spaced()