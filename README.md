# FaceRec-Tkinter

This is a quick python project for face recognition done in two days. It was made for a company for registeration purposes in an expo. The project uses OpenCV for the face detection and recognition tasks. Tkinter is also used for the GUI.

<p align="center">
<img src="https://github.com/MarkNaeem/FaceRec-Tkinter/blob/main/GUI.png" width="500">
 </p>
 
## Install and Dependencies

To install, just clone the project using `git clone https://github.com/MarkNaeem/FaceRec-Tkinter.git`.

**You need the following ni order to work properly:**
- Tkinter:          `sudo apt-get install python3-tk`
- face recognition: `pip3 install face-recognition`
- opencv:           `pip3 install opencv-python` <- *there are lother ways to install opencv with GPU support and some more features, Please refer to opencv documemntation for this*.
- ImageTK:          `sudo apt-get install python3-pil python3-pil.imagetk` 
- Pillow:           `pip3 install pillow`

 
## How it works

The project runs on python3 by running the command `python3 FR.py` in the project folder. You can replace the logo *Logo.png* with your own logo but just keep its name as "Logo.png". The *Data report.txt* is generated from the entered data for the recognized faces, it will only be generated once you click *report Export* data button in the program.

Please note that the application was made and run on Ubuntu using a redragon camera. So, in order to change to your camera, change the `cam_dev_path` to the path of your camera in Ubuntu.

If you use Windows os, change variable `win` to True and just try to change the *device_num* to match the number of your device.
New features will be added to make the change from Ubuntu to Windows and make changing the used camera accessible from the GUI.


## What is expected?

  - When the program is launched, your logo will show until you click start to open the camera. The video stream will appear in the place where the logo was.
  - The camera will detect faces immediatly in real-time and plot a blue box around each of them.
  - Once you started the camera stream, you can recognize, pause, edit, export data, or reset.
  - Pause will stop the recognition, so you can't recognize while the streaming is paused. You can resume by clicking on the same button now named "resume".
  - Recognize will pause the stream at the frame you clicked, take all the detected faces in the image, and start recognizing the faces. If a face is unkown, a messagebox will ask you to enter the name and the bio. The name should be followed by an * then the bio. This will be modified so that two seperate boxes will show up for the name and the bio separately. But if the face was recognized from the saved faces, the name will be written on the box and bio box will show the person's recorded bio.
  - After recording data about a certain person, you can edit them by selecting the name from a drop-down menu and click edit. A messagebox will show asking for the new name and bio to be entered the same way as before.
  - Export data will make a text file that contains all the recorded data. Each person will be mentined in a separate line with their name and bio.
  - Reset will erase all of the recorded data. This will be helpful if you have lots of recorded faces that will be no longer used, or you just need a new start of the program. It is not recommended to erase all the data if you have only one wrong input (just use the edit tool).
 
