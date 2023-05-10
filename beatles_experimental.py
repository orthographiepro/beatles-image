from beatles_lib import lego_image
import numpy as np
import random as rd
import time


def median_cut(farbraum, it, lim, results: list, q: list):

    if len(results) >= lim or farbraum.size == 0:
        return
    
    min_values = np.amin(farbraum, axis=0)
    max_values = np.amax(farbraum, axis=0)
    ranges = max_values - min_values
    longest_axis = np.argmax(ranges)

    if ranges[longest_axis] <= 5:
        return

    med_element = np.median(farbraum, axis=0)
    med = med_element[longest_axis]
    results.append(med_element)

    smaller_condition = np.repeat((farbraum[:, longest_axis] <= med), 3)
    smaller_elements = np.extract(smaller_condition, farbraum)
    smaller_elements = smaller_elements.reshape((smaller_elements.shape[0] // 3, 3))

    q.append( (smaller_elements, it+1, lim, results, q) )
    
    larger_condition = np.repeat((farbraum[:, longest_axis] > med), 3)
    larger_elements = np.extract(larger_condition, farbraum)
    larger_elements = larger_elements.reshape((larger_elements.shape[0] // 3, 3))
    q.append( (larger_elements, it+1, lim, results) )

    param = q[0]
    q = q[1:]
    median_cut(param[0], param[1], param[2], param[3], q=q)



class experimental_lego_image(lego_image):

    def __init__(self) -> None:
        super().__init__()

    def quantize_dither2(self):
        self.lego_image = self.lego_image.astype(np.float64)

        accumulated_error = np.array([0, 0, 0])

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
                accumulated_error = self.lego_dot_list[min_dot_index].color - self.lego_image[i, j, :]
                self.lego_image[i, j, :] = self.lego_dot_list[min_dot_index].color
                
                if j+1 < lego_image.side:
                    self.lego_image[i, j+1, :] += (7/16 * accumulated_error)
                                    
                if i+1 < lego_image.side:
                    self.lego_image[i+1, j, :] += (5/16 * accumulated_error)
                    if j+1 < lego_image.side:
                        self.lego_image[i+1, j+1, :] += (3/16 * accumulated_error)
                    if j-1 >= 0:
                        self.lego_image[i+1, j-1, :] += (1/16 * accumulated_error)  

                if self.lego_dot_list[min_dot_index].empty():
                    self.lego_dot_list.remove(self.lego_dot_list[min_dot_index])

        self.lego_image = self.lego_image.astype(np.uint8)
        self.lego_image[1, 1, 1] = 255
    

    def quantize_dither(self):
        accumulated_error = np.array([0, 0, 0])

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
                accumulated_error = self.lego_dot_list[min_dot_index].color - self.lego_image[i, j, :]
                self.lego_image[i, j, :] = self.lego_dot_list[min_dot_index].color
                
                # error diffusion

                weights = {(0, 1): 7/16, (1, -1): 3/16, (1, 0):5/16, (1, 1):1/16}
                if j+1 >= lego_image.side:
                    weights[(0, 1)] = 0
                    weights[(1, 1)] = 0
                    weights[(1, -1)] += 0.25
                    weights[(1, 0)] += 0.25
                if i+1 >= lego_image.side:
                    weights[(0, 1)] = 1
                    if j+1 >= lego_image.side:
                       weights[(0, 1)] = 0 
                    weights[(1, 1)] = 0
                    weights[(1, -1)] = 0
                    weights[(1, 0)] = 0
                else:
                    if j-1 < 0:
                        weights[(1, 0)] = 0.5 
                        weights[(1, -1)] = 0              
                
                for w in weights:
                    u, v =  w
                    u += i
                    v += j
                    if weights[w] > 0:
                        self.lego_image[u, v, :] += (weights[w] * accumulated_error).astype(np.uint8)

                if self.lego_dot_list[min_dot_index].empty():
                    self.lego_dot_list.remove(self.lego_dot_list[min_dot_index])


def quantize_med_cut_rand(self):
        farbraum = np.reshape(self.lego_image, (lego_image.side**2, 3))
        quantized_colors = []
        l = len(self.lego_dot_list)
        median_cut(farbraum, 0, lim=l, results=quantized_colors, q=[])

        rd.seed(time.time())
        # generate mapping (random)
        map_list = []
        for i in range(50):
            mapping = []
            rd.shuffle(quantized_colors)
            dist = 0
            for j in range(l):
                mapping.append(self.lego_dot_list[j])
                for z in [0, 1, 2]:
                    dist += (quantized_colors[j][z] - self.lego_dot_list[j].color[z])**2

            map_list.append((mapping, dist))
        
        map_list.sort(key=(lambda x: x[1]))
        mapping = map_list[0][0]
        print(map_list.index(min(map_list, key=lambda x : x[1])))
        
        for i in range(self.lego_image.shape[0]):
            for j in range(self.lego_image.shape[1]):
                
                color_here = self.lego_image[i, j, :]

                min_dist = 255 * 255 * 3
                min_color = 0
                z = 0
                for color in quantized_colors:
                    euklid_dist = 0
                    for v in [1, 2, 0]:
                        euklid_dist += (color_here[v] - color[v])**2
                    if euklid_dist < min_dist:
                        min_color = mapping[z]
                        min_dist = euklid_dist
                    z += 1

                self.lego_image[i, j, :] = min_color.color

                if min_color.empty():
                    self.lego_dot_list.remove(min_color)