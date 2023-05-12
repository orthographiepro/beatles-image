import numpy as np
from PIL import Image


def cartesian_product(*arrays):
    la = len(arrays)
    dtype = np.result_type(*arrays)
    arr = np.empty([len(a) for a in arrays] + [la], dtype=dtype)
    for i, a in enumerate(np.ix_(*arrays)):
        arr[...,i] = a
    return arr.reshape(-1, la)



class lego_dot:
    def __init__(self, color: list, name: str, count: int) -> None:
        
        if not len(color) == 3:
            raise TypeError("invalid color") 

        if count <= 0:
            raise ValueError("too few pieces")
        
        self.color = np.array(color)
        self.name = name
        self.number_left = count

    
    def __sub__(self, num: int):

        if num > self.number_left:
            raise ValueError("num bigger than pieces left")
        
        self.number_left = self.number_left - num


    def empty(self) -> bool:
        return self.number_left <= 0


class lego_image:
    side = 48 

    def __init__(self) -> None:
        self.raw_image = None
        self.sidelength = 0
        self.lego_dot_list = []
        self.lego_image = None


    def set_original_image(self, path):
        try:
            self.raw_image = np.array(Image.open(path).convert("RGB"))
        except FileNotFoundError as e:
            print("file not found", e.filename)
            return
            
        lengths = self.raw_image.shape
        if not lengths[0] == lengths[1]:
            raise ValueError("not a square image")
        if lengths[0] < lego_image.side:
            raise ValueError("resolution too low")
        self.sidelength = lengths[0]


    def add_dot(self, new_dot: lego_dot):
        self.lego_dot_list.append(new_dot)
    

    def shrink(self):
        ratio = (self.sidelength // lego_image.side)
        self.lego_image = np.zeros([lego_image.side, lego_image.side, 3]).astype(np.uint8)

        for i in range(lego_image.side):
            for j in range(lego_image.side):

                avg = np.array([0, 0, 0])
                counter = 0
                for u in range(ratio):
                    for v in range(ratio):
                        x = i * ratio + u
                        y = j * ratio + v
                        if x >= self.sidelength or y >= self.sidelength:
                            continue 
                        avg = avg + self.raw_image[x, y, :]
                        counter += 1

                self.lego_image[i, j, :] = (avg / counter).astype(np.uint8)

                    
    def quantize_greedy(self):
        for i in range(lego_image.side):
            for j in range(lego_image.side):

                color_here = self.lego_image[i, j, :]

                min_dist = 255 * 255 * 3
                min_dot_index = 0
                for u in range(len(self.lego_dot_list)):
                    dot = self.lego_dot_list[u]
                    euklid_dist = 0
                    for v in [1, 2, 0]:
                        euklid_dist += (color_here[v] - dot.color[v])**2
                    if euklid_dist < min_dist:

                        min_dist = euklid_dist
                        min_dot_index = u

                self.lego_dot_list[min_dot_index] - 1
                self.lego_image[i, j, :] = self.lego_dot_list[min_dot_index].color

                if self.lego_dot_list[min_dot_index].empty():
                    self.lego_dot_list.remove(self.lego_dot_list[min_dot_index])


    def quantize_greedy_randomized(self):
        # np.random.seed(time.time())
        translation_table_x = np.arange(lego_image.side)
        random_order = cartesian_product(translation_table_x, translation_table_x.copy())
        np.random.shuffle(random_order)
        # print(random_order)

        for coordinates in random_order:    
            i, j = coordinates            
            color_here = self.lego_image[i, j, :]

            min_dist = 255 * 255 * 3
            min_dot_index = 0
            for u in range(len(self.lego_dot_list)):
                dot = self.lego_dot_list[u]
                euklid_dist = 0
                for v in [1, 2, 0]:
                    euklid_dist += (color_here[v] - dot.color[v])**2
                if euklid_dist < min_dist:

                    min_dist = euklid_dist
                    min_dot_index = u

            self.lego_dot_list[min_dot_index] - 1
            self.lego_image[i, j, :] = self.lego_dot_list[min_dot_index].color

            if self.lego_dot_list[min_dot_index].empty():
                self.lego_dot_list.remove(self.lego_dot_list[min_dot_index])


    def show(self):
        Image.fromarray(self.lego_image).show()
                

    def make_spaced(self, input_img, shiny = 50):
        print_array = np.zeros([input_img.shape[0] * 6 - 1, input_img.shape[1] * 6 - 1, 3], dtype=np.uint8)

        for i in range(input_img.shape[0]):
            for j in range(input_img.shape[1]):
                self.draw_dot(print_array, i*6, j*6, color=input_img[i, j, :])
                
        return print_array


    def draw_dot(self, print_array, i: int, j: int, color, shiny = 50):
        """draws a 5*5 dot in the print_array, so that the upper left circle-corner is located at (i,j)"""
        
        for u in range(5):
            for v in range(5):

                if (u,v) in [(0,0), (0, 4), (4, 0), (4, 4)]:
                    continue

                if (u, v) in [(2, 1), (1, 2)]:
                    print_array[i+u, j+v, 0] = min(color[0] + shiny, 255)
                    print_array[i+u, j+v, 1] = min(color[1] + shiny, 255)
                    print_array[i+u, j+v, 2] = min(color[2] + shiny, 255)
                    continue

                print_array[i+u, j+v, :] = color

    
    def show_spaced(self, shiny = 50):
        print_array = self.make_spaced(self.lego_image, shiny)
        Image.fromarray(print_array).show()
    

    def make_slice(self, segment_index, start_with_zero = True):    # is more of a static method
        if start_with_zero == False:
            segment_index -= 1
        
        if segment_index < 0 or segment_index > 8:
            raise ValueError("segment index " + segment_index + " out of bounds")
        
        x_index = segment_index // 3 
        y_index = segment_index % 3

        print_array = self.lego_image[  lego_image.side*x_index // 3 : lego_image.side*(x_index+1) // 3,
                                        lego_image.side*y_index // 3 : lego_image.side*(y_index+1) // 3, 
                                        :
                                     ]
        
        # print_array[0, 0, :] = np.array([(x_index / 2) * 255, 0, (y_index / 2) * 255]).astype(np.uint8)
        # above should ease the location of the slice, but you end up losing one pixel. it should happen after make spaced
        return print_array

    
    def show_slice(self, slice_index, start_with_zero = True):
        print_slice = self.make_slice(slice_index, start_with_zero)
        print_slice = self.make_spaced(print_slice)
        Image.fromarray(print_slice).show()


    def show_slice_all(self):
        for i in range(9):
            self.show_slice(i)


    def build_image(self, image_path: str, dotlist):
        self.set_original_image(image_path)
        for dot in dotlist:
            self.add_dot(dot)

        self.shrink()
        self.quantize_greedy_randomized()
        self.show_spaced()
                