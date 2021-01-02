import re 
import os 
import cv2
import pickle
import _pickle
import tkinter as tk
import pkg_resources
import face_recognition
from statistics import mode
from numpy import where
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import simpledialog

class recognizer:
	def __init__(self):
		win = False
		self.root = tk.Tk()
		self.root.title("Face Recognizer")
		self.root.protocol("WM_DELETE_WINDOW", self.ending)
		self.lmain          = tk.Label(self.root,width=640,height=480)
		#self.lmain.grid(column=1,rowspan=3)
		button_frame   = tk.LabelFrame(self.root, text="Controls" )
		#button_frame.grid(columnspan=3,column=2,row=1)
		self.snap_button    = tk.Button(button_frame, text='Recognize',    width=25, state = tk.DISABLED, command=self.snapshot_callback)
		#self.snap_button.grid(column=2,row=1,rowspan=1)
		self.pause_button   = tk.Button(button_frame, text='Start',       width=25, command=self.pause_callback)
		#self.pause_button.grid(column=3,row=1,rowspan=1)
		self.reset_button   = tk.Button(button_frame, text='Reset', fg="red",       width=25, command=self.reset_callback)
		#self.reset_button.grid(column=4,row=1,rowspan=1)
		self.export_button   = tk.Button(button_frame, text='Export data', fg="blue",       width=25, command=self.export_callback)
		#self.reset_button.grid(column=4,row=1,rowspan=1)
		
		self.people = pickle.loads(open('.faces_encodings', "rb").read())
		self.info_dict = pickle.loads(open('.names_dict', "rb").read())
		
		self.option_list = self.people['names']
		if len(self.option_list) == 0: self.option_list = [' ']

		edit_frame         = tk.LabelFrame(button_frame, text="Edit info")
		self.option_var = tk.StringVar(self.root)
		self.options        = tk.OptionMenu(edit_frame,self.option_var,*self.option_list)
		self.edit_button   = tk.Button(edit_frame, text='edit', width=25, command=self.edit_callback)
		
		label_frame         = tk.LabelFrame(self.root, text="Bio")
		#label_frame.grid(column=2,row=2,columnspan=3,rowspan=2)
		self.bio_label      = tk.Label(label_frame, text="Information about the recognized person.")

		self.lmain.pack(fill="both",side="left", expand="yes")
		label_frame.pack(fill="both",side="right", expand="yes")
		self.bio_label.pack()
		button_frame.pack(fill="both",side="right", expand="yes")
		self.pause_button.pack(side="top",ipady=20)
		self.snap_button.pack(ipady=20)
		edit_frame.pack()
		self.options.pack()
		self.edit_button.pack()
		self.export_button.pack(side="bottom",ipady=20)
		self.reset_button.pack(side="bottom",ipady=20)

		haar_xml = pkg_resources.resource_filename('cv2', 'data/haarcascade_frontalface_default.xml')
		self.faceCascade = cv2.CascadeClassifier(haar_xml)

		Cam_dev_path = '/dev/v4l/by-id/usb-Sonix_Technology_Co.__Ltd._REDRAGON_Live_Camera_SN0001-video-index0'
		try:
			if not os.path.exists(Cam_dev_path): raise runtimeerror()
			real_path = os.path.realpath(Cam_dev_path)
			device_re = re.compile("\/dev\/video(\d+)")
			info = device_re.match(real_path)
			if info:
			    device_num = int(info.group(1))
			    print("Using default video capture device on /dev/video" + str(device_num))
		except:
			print("Please make sure the camera is connected!")
			print("Using cam0....")
			device_num = 0

		if not win: self.cap = cv2.VideoCapture("/dev/video" + str(device_num))
		else:  self.cap = cv2.VideoCapture(str(device_num))
		self.cap.set(16,640) # set Width
		self.cap.set(9,480) # set Height

		haar_xml = pkg_resources.resource_filename('cv2', 'data/haarcascade_frontalface_default.xml')
		self.faceCascade = cv2.CascadeClassifier(haar_xml)

		self.paused = True

		self.start_logo()


	def show_frame(self):
		if not self.paused:
			_, img = self.cap.read()
			img = cv2.flip(img, 1)
			self.frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
			self.faces_marking()
			img = Image.fromarray(self.frame)
			imgtk = ImageTk.PhotoImage(image=img)
			self.lmain.imgtk = imgtk
			self.lmain.configure(image=imgtk)
		self.lmain.after(20, self.show_frame)

	def faces_marking(self):
		gray = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
		faces = self.faceCascade.detectMultiScale(gray,scaleFactor=1.2,minNeighbors=3,minSize=(20, 20))		
		for (x, y, w, h) in faces:
				cv2.rectangle(self.frame,(x,y),(x+w,y+h),(0,0,255),2)
		
	def update_option_menu(self):
		menu = self.options["menu"]
		menu.delete(0, "end")
		for string in self.option_list:
				menu.add_command(label=string, 
                             command=lambda value=string: self.option_var.set(value))
            
	def start_logo(self):
		img = Image.open(r"Logo.png")  
		imgtk = ImageTk.PhotoImage(image=img)
		self.lmain.imgtk = imgtk
		self.lmain.configure(image=imgtk)
		
        
	def pause_callback(self):
		self.snap_button.config(state=tk.NORMAL if self.paused else tk.DISABLED)
		self.pause_button.config(text="Pause" if self.paused else "Start")
		self.paused = False if self.paused else True
		self.bio_label.config(text="")

	def export_callback(self):
          with open('Data Report.txt', 'w') as f:
        				 for (name, bio) in self.info_dict.items():
        				     print(name+'\t'+bio+'\n',file=f)
          messagebox.showinfo(title="Report succeeded ", message="Data is reported successfully!")     

	def edit_callback(self):
		old_name = self.option_var.get()
		try: index = self.people['names'].index(old_name)
		except: 
				messagebox.showerror(title="Edit failed", message="No name "+old_name+" found!")
				return 			
		_ = self.info_dict.pop(old_name)
		answer = simpledialog.askstring("Name and Bio", "Please enter a name followed by an *, then a simple bio.",parent=self.root)
		if type(answer)!=type(None):
			name, bio = answer.split('*')
			if bio[0]==' ': bio = bio[1:]
			self.people['names'][index] = name
			self.info_dict[name] = bio
			messagebox.showinfo(title="Edit succeeded ", message="edited "+name+"'s face successfully!")
		self.option_list = self.people['names']
		self.update_option_menu()
		self.option_var.set(self.option_list[0])
          


	def snapshot_callback(self):
		self.pause_button.config(text="Pause" if self.paused else "Start")
		self.paused = not(self.paused)
		self.snap_button.config(state=tk.DISABLED)

		displayed_names=[]
		bios=""
        
		gray = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
		faces = self.faceCascade.detectMultiScale(gray,scaleFactor=1.2,minNeighbors=3,minSize=(20, 20))
		boxes = [(y,x+w,y+h,x) for (x,y,w,h) in faces]
		if len(faces)==0:
			messagebox.showerror(title="Detection failed", message="No face detected!")
			return 			

		try: encodings = face_recognition.face_encodings(self.frame,boxes)
		except: 
			print("Error in face recognition!")
			encodings = []

		for encoding in encodings:
  	     		matches = face_recognition.compare_faces(self.people["encodings"],encoding)
  	     		name = mode(list(map(self.people['names'].__getitem__,where(matches)[0]))) if True in matches else "Unknown"                      
  	     		displayed_names.append(name)

		if "Unknown" in displayed_names and displayed_names.count("Unknown")>1:
			messagebox.showerror(title="Detection failed", message="Sorry, we can only support one unknown face at a time!")
			return 			

            
		for ((x, y, w, h), name) in zip(faces, displayed_names):
			if name=="Unknown":
  	     		  cv2.rectangle(self.frame,(x,y),(x+w,y+h),(255,0,0),2)
  	     		  imgtk = ImageTk.PhotoImage(image=Image.fromarray(self.frame))
  	     		  self.lmain.imgtk = imgtk
  	     		  self.lmain.configure(image=imgtk)
  	     		  answer = simpledialog.askstring("Name and Bio", "Please enter a name followed by an *, then a simple bio.",parent=self.root)
  	     		  if type(answer)!=type(None):
        				 name, bio = answer.split('*')
        				 if bio[0]==' ': bio = bio[1:]
        				 self.people['encodings'].append(encoding)
        				 self.people['names'].append(name)
        				 self.info_dict[name] = bio
        				 messagebox.showinfo(title="Detection succeeded ", message="recorded "+name+"'s face successfully!")
			cv2.rectangle(self.frame,(x,y),(x+w,y+h),(0,0,255),2)
			cv2.putText(self.frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)	
			if name == "Unknown": continue
			bios+= "\n"+name+":\t"+self.info_dict[name]+"\n"
            
		self.option_list = self.people['names']
		self.update_option_menu()
		self.option_var.set(self.option_list[0])
		self.bio_label.config(text=bios)
		imgtk = ImageTk.PhotoImage(image=Image.fromarray(self.frame))
		self.lmain.imgtk = imgtk
		self.lmain.configure(image=imgtk)


	def reset_callback(self):
		if messagebox.askyesno("ERASE ALL DATA?!", "Do you really wish to erase all recorded faces?"):    
		    self.people = {"names":[],"encodings":[]}	
		    self.info_dict = {"":""}	

	def ending(self):
		if messagebox.askyesno("Quit", "Do you really wish to quit?"):    
		    self.paused = True
		    f = open(".faces_encodings", "wb")
		    f.write(pickle.dumps(self.people))
		    f.close()
		    f = open(".names_dict", "wb")
		    f.write(pickle.dumps(self.info_dict))
		    f.close()
		    self.cap.release()
		    self.root.quit()
				

def main():
	recog = recognizer()
	recog.show_frame()
	recog.root.mainloop()

if __name__ == '__main__':
	main()	


