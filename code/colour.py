from imageio import imread

#Calculate the overall server statistics
def findAvgRGB(url,samples):
    img = imread(url)
    width = len(img[0])
    height = len(img)
    rgb = [0,0,0]
    for i in range(1,samples+1):
        for j in range(1,samples+1):
            c_array = img[int((j/(samples+1))*height)][int((i/(samples+1))*width)]
            for k in range(3):
                rgb[k] += c_array[k]
    rgb = [int(c/((samples+1)*(samples+1))) for c in rgb]
    return rgb