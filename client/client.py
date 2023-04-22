import threading
import tkinter
import tkinter as tk
import loginCanvas
from PIL import Image,ImageTk
from CanvasToWidget import MyButton
from loginCanvas import Login
from register1Canvas import Register1
from register2Canvas import Register2
from register3Canvas import Register3
from register4Canvas import Register4
from register5Canvas import Register5
import sys,os
import cv2
import numpy as np

class App(tk.Tk):
    def __init__(self):
        super(App, self).__init__()
        self.geometry("915x540+250+100")
        self.overrideredirect(True)
        self.resizable(False, False)
        self.title("test modern app")

        self.wm_attributes('-transparentcolor', '#ab23ff')

        self.login=Login()
        self.r1=Register1()
        self.r2=Register2()
        self.r3=Register3()
        self.r4=Register4()
        self.r5=Register5()

        #adding the background image to canvas
        self.backImage = tk.PhotoImage(file=r"C:\Users\ID 1\tkinterTest\E-student\client\assest\general\loginBackgroundImg.png")
        self.Background = tk.Canvas(self, width=915, height=540, highlightthickness=0, background="#ab23ff")
        self.Background.create_image(0, 0, image=self.backImage, anchor=tk.NW)
        self.Background.place(x=0,y=0)

        #adding the top header Bar
        self.headerBarImg = tk.PhotoImage(file=r"C:\Users\ID 1\tkinterTest\E-student\client\assest\general\headerBar.png")
        self.headerBarObject=self.Background.create_image(55, 42, image=self.headerBarImg, anchor=tk.NW)

        #adding the moving option to the header bar
        self.Background.tag_bind(self.headerBarObject,"<ButtonPress-1>", self.start_move)
        self.Background.tag_bind(self.headerBarObject,"<ButtonRelease-1>", self.stop_move)
        self.Background.tag_bind(self.headerBarObject,"<B1-Motion>", self.on_move)

        # adding the close button
        self.closeStandardImg = Image.open(r"C:\Users\ID 1\tkinterTest\E-student\client\assest\general\closeStandardImg.png").resize((46,46))
        self.closeHoverImg = Image.open(r"C:\Users\ID 1\tkinterTest\E-student\client\assest\general\closeHoverImg.png").resize((46,46))
        self.closeButton = MyButton(self.Background,standardImg=self.closeStandardImg,hoverImg=self.closeHoverImg,x=812,y=43,behavior=self.quit)

        self.logoImg = ImageTk.PhotoImage(Image.open(r"C:\Users\ID 1\tkinterTest\E-student\client\assest\general\EstudentLogo.png"))
        self.loginObject = self.Background.create_image(79, 51, image=self.logoImg, anchor=tk.NW)

        # create a Toplevel window
        self.loginWidgetsFrame1=self.login.createLogin(self)

        # loginWidgetsImg = tk.PhotoImage(
        #     file=r"C:\Users\ID 1\tkinterTest\E-student\client\assest\loginPage\loginFrame.png")
        # loginWidgetsFrame = self.Background.create_image(55, 136, image=loginWidgetsImg, anchor=tk.NW)

        # loginWidgetsImg =r"C:\Users\ID 1\tkinterTest\E-student\client\assest\loginPage\loginFrame.png"
        # base=tk.Canvas(base,width=915,height=540)
        # loginWidgetsFrame = self.Background.create_image(55, 136, image=tk.PhotoImage(file=loginWidgetsImg), anchor=tk.NW)

        # self.loginWidgetsImg = tk.PhotoImage(
        #     file=r"C:\Users\ID 1\tkinterTest\E-student\client\assest\loginPage\loginFrame.png")
        # self.loginWidgetsFrame = self.Background.create_image(55, 136, image=self.loginWidgetsImg, anchor=tk.NW)

    def start_move(self, event):
        self._dragging = True
        self._x = event.x
        self._y = event.y

    def stop_move(self, event):
        self._dragging = False

    def on_move(self, event):
        if self._dragging:
            x = self.winfo_x() + event.x - self._x
            y = self.winfo_y() + event.y - self._y        # self.config(cursor="arrow")

            self.geometry(f"+{x}+{y}")

    def resourcePath(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def detectFaces(self,photo):
        # Load the Haar Cascade classifier for face detection
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # photo=Image.open('humanface2.jpg')
        # Load the image
        img = np.array(photo)
        print(img.shape)

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return faces

    def drawFace(self,img,faces,color=(187,134,252),width=1):
        (x, y, w, h) = faces[0]
        cv2.rectangle(img, (x, y), (x + w, y + h), color, width)

    def cropFace(self,photo, faces,size=100):
        # If a face is detected, crop the image to the region containing the face
        img = np.array(photo)
        (x, y, w, h) = faces[0]
        pading = min(int(w / 5), int(h / 5))
        cropped_img = img[y - pading:y + h + pading, x - pading:x + w + pading]

        # Resize the cropped image to a square with the specified dimensions
        resized_img = cv2.resize(cropped_img, (size, size), interpolation=cv2.INTER_AREA)
        return resized_img

    def numpyToStr(self,npImage):
        photo = tk.PhotoImage(width=npImage.shape[1], height=npImage.shape[0])
        photo.put("{" + " ".join(str(x) for x in np.ravel(npImage)) + "}", to=(0, 0))
        return photo
    def loginToRegister1(self):
        self.config(cursor="arrow")
        self.Background.signup.place_forget()
        self.loginGroup.removeGroup()
        self.submitLoginButton.place_forget()
        self.r1.createRegister1(self)


    def register1ToLogin(self):
        self.register1Group.removeGroup()
        self.submitRegister1Button.place_forget()
        self.login.createLogin(self)

    def register1ToRegister2(self):
        # print(self.register1Form.get())
        if self.register1Form.validate():
            self.r1.dayVar=self.dayRegisterList.get()
            self.r1.monthVar=self.monthRegisterList.get()
            self.r1.yearVar=self.yearRegisterList.get()
            self.r1.genderVar=self.genderRegisterOptionList.get()
            print(self.r1.genderVar)
            # print(self.r1.genderVar.getValue())
            self.register1Group.removeGroup()
            self.r2.createRegister2(self)

    # def register2ToRegister2(self):
    #     self.register1Group.removeGroup()
    #     self.r2.createRegister2(self)

    def register2ToRegister1(self):
        self.register2Group.removeGroup()
        self.nextRegister2Button.place_forget()
        self.backRegister2Button.place_forget()
        self.r1.createRegister1(self)

    def register2ToRegister3(self):
        if self.register2Form.validate():
            self.register2Group.removeGroup()
            self.nextRegister2Button.place_forget()
            self.backRegister2Button.place_forget()
            self.r3.createRegister3(self)

    def register3ToRegister2(self):
        self.register3Group.removeGroup()
        self.nextRegister3Button.place_forget()
        self.backRegister3Button.place_forget()
        self.r2.createRegister2(self)

    # def register3ToRegister2(self):
    #     self.r3.bacCityVar=self.bacCityRegister3List.get()
    #     self.r3.bacSectorVar=self.bacSectorRegister3List.get()
    #     self.r3.bacLanguageVar=self.bacLanguageRegister3List.get()
    #     self.r3.schoolTypeVar = self.hTypeRegisterOptionList.get()
    #
    #     self.register3Group.removeGroup()
    #     self.r2.createRegister1(self)

    def register3ToRegister4(self):
        if self.register3Form.validate():
            self.r3.bacCityVar=self.bacCityRegister3List.get()
            self.r3.bacSectorVar=self.bacSectorRegister3List.get()
            self.r3.bacLanguageVar=self.bacLanguageRegister3List.get()
            self.r3.schoolTypeVar=self.hTypeRegisterOptionList.get()

            self.register3Group.removeGroup()
            self.nextRegister3Button.place_forget()
            self.backRegister3Button.place_forget()
            self.r4.createRegister4(self)

    def register4ToRegister3(self):
        self.register4Group.removeGroup()
        self.nextRegister4Button.place_forget()
        self.backRegister4Button.place_forget()
        self.r3.createRegister3(self)

    def register4ToRegister5(self):
        if self.register4Form.validate():
            self.r4.cityVar=self.cityRegister4List.get()
            self.r4.countryVar=self.countryRegister4List.get()


            self.register4Group.removeGroup()
            self.nextRegister4Button.place_forget()
            self.backRegister4Button.place_forget()
            self.r5.createRegister5(self)

    def register5ToRegister4(self):
        self.register5Group.removeGroup()
        self.nextRegister5Button.place_forget()
        self.backRegister5Button.place_forget()
        self.r4.createRegister4(self)







window=App()
window.mainloop()
