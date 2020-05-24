import tkinter
import easytello
import cv2
import time
import PIL.Image, PIL.ImageTk

class TelloUserInterface:

    def __init__(self, window, window_title, video_source = 0):
        self.window = window
        self.window.title = window_title
        self.video_source = video_source

        # open video source (by default, tries to open webcam)
        self.video_source = MyVideoCapture(self.video_source)

        # create canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.video_source.width, height = self.video_source.height)
        self.canvas.grid(row = 10, column = 10)

        # button to take snapshot
        #self.button_snapshot = tkinter.Button(window, text = "Snapshot", width = 50, command = self.snapshot)
        #self.button_snapshot.grid(row = 2, column = 2)

        # Control Buttons & Labels
        self.forwardLabel = tkinter.Label(window, text='Forward')
        self.forwardButton = tkinter.Button(window, text='W')
        self.forwardLabel.grid(row=0, column=1)
        self.forwardButton.grid(row=1, column=1)

        self.backwardLabel = tkinter.Label(window, text='Backward')
        self.backwardButton = tkinter.Button(window, text='S')
        self.backwardLabel.grid(row=2, column=1)
        self.backwardButton.grid(row=3, column=1)

        self.leftRotateLabel = tkinter.Label(window, text='Left')
        self.leftRotateButton = tkinter.Button(window, text='A')
        self.leftRotateLabel.grid(row = 2, column = 0)
        self.leftRotateButton.grid(row = 3, column = 0)

        self.rightRotateLabel = tkinter.Label(window, text='Right')
        self.rightRotateButton = tkinter.Button(window, text='D')
        self.rightRotateLabel.grid(row=2, column=2)
        self.rightRotateButton.grid(row=3, column=2)

        self.ascendLabel = tkinter.Label(window, text='Up')
        self.ascendButton = tkinter.Button(window, text='^')
        self.ascendLabel.grid(row=5, column=1)
        self.ascendButton.grid(row=6, column=1)

        self.descendLabel = tkinter.Label(window, text='Down')
        self.descendButton = tkinter.Button(window, text='^')
        self.descendLabel.grid(row=7, column=1)
        self.descendButton.grid(row=8, column=1)

        # Launch and Land Labels and Display
        self.launchLabel = tkinter.Label(window, text='Launch')
        self.launchButton = tkinter.Button(window, text='Start')
        self.launchLabel.grid(row=5, column=4)
        self.launchButton.grid(row=6, column=4)

        self.landLabel = tkinter.Label(window, text='Land')
        self.landButton = tkinter.Button(window, text='Stop')
        self.landLabel.grid(row=7, column=5)
        self.landButton.grid(row=8, column=5)

        # Telemetry Labels and Display
        self.countdownLabel = tkinter.Label(window, text='Countdown')

        self.batteryLabel = tkinter.Label(window, text='Battery')
        self.batteryDisplay = tkinter.Message(window, text=':')
        self.batteryLabel.grid(row=3, column=6)
        self.batteryDisplay.grid(row=4, column=6)

        self.tempLabel = tkinter.Label(window, text='Temp')
        self.tempDisplay = tkinter.Message(window, text=':')
        self.tempLabel.grid(row=5, column=6)
        self.tempDisplay.grid(row=6, column=6)

        self.wifiLabel = tkinter.Label(window, text='Network')
        self.wifiDisplay = tkinter.Message(window, text=':')
        self.wifiLabel.grid(row=7, column=6)
        self.wifiDisplay.grid(row=8, column=6)

        self.speedLabel = tkinter.Label(window, text='Speed')
        self.speedDisplay = tkinter.Message(window, text=':')
        self.speedLabel.grid(row=9, column=6)
        self.speedDisplay.grid(row=10, column=6)


        # after it is called once, the update method will be automatically called
        self.delay = 15
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.video_source.get_frame()

        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        # Get a frame from the video source
        ret, frame = self.video_source.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        self.window.after(self.delay, self.update)

class MyVideoCapture:
    def __init__(self, video_source = 0):
        #Open Video Soruce
        self.video_source = cv2.VideoCapture(video_source)
        if not self.video_source.isOpened():
            raise ValueError("Unable to open video source", video_source)

        #Get video soruce width and height
        self.width = self.video_source.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.video_source.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.video_source.isOpened():
            ret, frame = self.video_source.read()
            if ret:
                # return a boolean success flag and the current frame converted to Gray
                return(ret, cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
            else:
                return(ret, None)
        else:
            return(ret, None)

    # release the video source when the object is destroyed
    def __del__(self):
        if self.video_source.isOpened():
            self.video_source.release()


# Create a window and pass it to the application object
TelloUserInterface(tkinter.Tk(), "Tello Interface")

