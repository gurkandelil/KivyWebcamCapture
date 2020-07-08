from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import time
import PIL.Image
import cv2
import numpy as np

global photo
Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)

    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
''')


class CameraClick(BoxLayout):
    def capture(self):

        camera = self.ids['camera']
        img2 = cv2.imread('frame.png')

        pixels_data = camera.texture.get_region(x=camera.x, y=camera.y, width=camera.resolution[0],
                                                height=camera.resolution[1]).pixels
        image = PIL.Image.frombytes(mode="RGBA", size=(int(camera.resolution[0]), int(camera.resolution[1])),
                                    data=pixels_data)

        pil_image = image.convert('RGB')
        open_cv_image = np.array(pil_image)
        # Convert RGB to BGR
        img1 = open_cv_image[:, :, ::-1].copy()

        #Image processing
        CameraClick.image_processing(img1,img2)



    def image_processing(img1,img2):

        rows, cols, channels = img2.shape
        roi = img1[0:rows, 0:cols]

        img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 200, 255, cv2.THRESH_BINARY_INV)
        mask_inv = cv2.bitwise_not(mask)

        img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        img2_fg = cv2.bitwise_and(img2, img2, mask=mask)

        out_img = cv2.add(img1_bg, img2_fg)
        img1[0:rows, 0:cols] = out_img

        # Write Function
        CameraClick.file_write(img1)


    def file_write(image):
        timestr = time.strftime("%Y%m%d_%H%M%S")
        cv2.imwrite("IMG_{}.png".format(timestr), image)
        print("Captured")

class TestCamera(App):

    def build(self):
        return CameraClick()


TestCamera().run()
