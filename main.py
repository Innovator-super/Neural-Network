import tkinter as tk
from PIL import Image
from params import width, height, pixel, file
from function import array1D, array2D, rgb, lrelu, dlrelu
import json


window = tk.Tk()
window.geometry(f'{width * pixel * 2}x{height * pixel}')
window.title('picters')


canvas = tk.Canvas(window, width = width * pixel * 2, height = height * pixel, bg = 'white', highlightthickness = 0)
canvas.pack()


def create_pixels2D(w, h, fill = 'white', shift_x = 0, shift_y = 0):
    temp = array2D(w, h)


    for i in range(w):
        for j in range(h):
            start_x = i * pixel + shift_x * pixel
            start_y = j * pixel + shift_y * pixel
            end_x = start_x + pixel
            end_y = start_y + pixel


            temp[i][j] = canvas.create_rectangle(start_x, start_y, end_x, end_y, fill = fill, width = 0)
    
    
    return temp


def feed(x, y):
    global inputs_layer, hidden1_layer, hidden2_layer, outputs_layer
    inputs_layer[0] = x
    inputs_layer[1] = y


    inputs_layer[-1] = neiron
    hidden1_layer[-1] = neiron
    hidden2_layer[-1] = neiron


    for i in range(len(hidden1_layer)):
        sum = 0
        for j in range(len(inputs_layer)):
            sum += inputs_layer[j] * weight_inputs_hidden1_layers[j][i]
        hidden1_layer[i] = lrelu(sum)
    
    



    for i in range(len(hidden2_layer)):
        sum = 0
        for j in range(len(hidden1_layer)):
            sum += hidden1_layer[j] * weight_hidden1_hidden2_layers[j][i]
        hidden2_layer[i] = lrelu(sum)
    


    

    for i in range(len(outputs_layer)):
        sum = 0
        for j in range(len(hidden2_layer)):
            sum += hidden2_layer[j] * weight_hidden2_outputs_layers[j][i]
        outputs_layer[i] = lrelu(sum)
    

    return outputs_layer


def back(predicted, real):
    global weight_inputs_hidden1_layers, weight_hidden1_hidden2_layers, weight_hidden2_outputs_layers
    output_errors = [predicted[i] - real[i] for i in range(3)]


    output_deltas = [output_errors[i] * dlrelu(predicted[i]) for i in range(3)]


    hidden2_errors = array1D(len(hidden2_layer))
    for i in range(3):
        for j in range(len(hidden2_layer)):
            hidden2_errors[j] += output_deltas[i] * weight_hidden2_outputs_layers[j][i]
    

    hidden2_deltas = [hidden2_errors[i] * dlrelu(hidden2_layer[i]) for i in range(len(hidden2_layer))]

    
    hidden1_errors = array1D(len(hidden1_layer))
    for i in range(len(hidden2_layer)):
        for j in range(len(hidden1_layer)):
            hidden1_errors[j] += hidden2_errors[i] * weight_hidden1_hidden2_layers[j][i]
    

    hidden1_deltas = [hidden1_errors[i] * dlrelu(hidden1_layer[i]) for i in range(len(hidden1_layer))]


    for i in range(len(outputs_layer)):
        for j in range(len(hidden2_layer)):
            weight_hidden2_outputs_layers[j][i] -= output_deltas[i] * hidden2_layer[j] * lr


    for i in range(len(hidden2_layer)):
        for j in range(len(hidden1_layer)):
            weight_hidden1_hidden2_layers[j][i] -= hidden2_deltas[i] * hidden1_layer[j] * lr


    for i in range(len(hidden1_layer)):
        for j in range(len(inputs_layer)):
            weight_inputs_hidden1_layers[j][i] -= hidden1_deltas[i] * inputs_layer[j] * lr


def main():
    for i in range(width):
        for j in range(height):
            x = i / (width / 2) - 1
            y = j / (height / 2) - 1
            out = feed(x, y)

            color = rgb(out[0] * 255, out[1] * 255, out[2] * 255)
            canvas.itemconfig(nn_image[i][j], fill = color)

    for i in range(width):
        for j in range(height):
            x = i / (width / 2) - 1
            y = j / (height / 2) - 1
            out = feed(x, y)


            pixel = image.getpixel((i, j))
            real = [pixel[0] / 255, pixel[1] / 255, pixel[2] / 255]


            back(out, real)
    

    window.after(10, main)


image = Image.open(file).resize((width, height))
#print(image.format, image.size, image.mode)
#image.show()


original_image = create_pixels2D(width, height, 'blue')
nn_image = create_pixels2D(width, height, 'red', width)


for i in range(width):
    for j in range(height):
        value = image.getpixel((i, j))
        color = rgb(value[0], value[1], value[2])
        canvas.itemconfig(original_image[i][j], fill = color)


#супер архитектура кода
neiron = 1
inputs_layer = array1D(2) + [neiron]
hidden1_layer = array1D(16) + [neiron]
hidden2_layer = array1D(16) + [neiron]
outputs_layer = array1D(3)
lr = 0.03


#веса, ребра архетектуры
weight_inputs_hidden1_layers = array2D(len(inputs_layer), len(hidden1_layer), random = True)
weight_hidden1_hidden2_layers = array2D(len(hidden1_layer), len(hidden2_layer), random = True)
weight_hidden2_outputs_layers = array2D(len(hidden2_layer), len(outputs_layer), random = True)


main()


canvas.update()
window.mainloop()