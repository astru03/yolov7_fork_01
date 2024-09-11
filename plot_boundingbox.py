import cv2
import matplotlib.pyplot as plt



def plot_bbox_to_image(image_path,label_path):
    
    img = cv2.imread(image_path)
    dh, dw, _ = img.shape

    fl = open(label_path, 'r')
    data = fl.readlines()
    fl.close()

    for dt in data:

        # Split string to float
        _, x, y, w, h = map(float, dt.split(' '))

        # Taken from https://github.com/pjreddie/darknet/blob/810d7f797bdb2f021dbe65d2524c2ff6b8ab5c8b/src/image.c#L283-L291
        # via https://stackoverflow.com/questions/44544471/how-to-get-the-coordinates-of-the-bounding-box-in-yolo-object-detection#comment102178409_44592380
        l = int((x - w / 2) * dw)
        r = int((x + w / 2) * dw)
        t = int((y - h / 2) * dh)
        b = int((y + h / 2) * dh)
        
        if l < 0:
            l = 0
        if r > dw - 1:
            r = dw - 1
        if t < 0:
            t = 0
        if b > dh - 1:
            b = dh - 1

        cv2.rectangle(img, (l, t), (r, b), (0, 0, 255), 1)

    plt.imshow(img)
    plt.show()
    
    
image_path =r"D:\ML_INSec\test_daten\test_daten\2023-10-15_13-28-13.077287350\video_03155.png"
label_txt = r"D:\ML_INSec\test_daten\test_daten\2023-10-15_13-28-13.077287350\video_03155.txt"
plot_bbox_to_image(image_path,label_txt)