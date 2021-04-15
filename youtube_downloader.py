from pytube import YouTube
from tkinter import filedialog
from tkinter import ttk 
from tkinter import *
import re
import threading


class Application:

	def __init__(self,root):
		self.root = root
		self.root.grid_rowconfigure(0,weight=2)
		self.root.grid_columnconfigure(0,weight=1)
		self.root.config(bg='#696969')

		top_label = Label(self.root,text='Video Downloader',fg='#40E0D0',font=('Duru Sans',30))
		top_label.grid(pady=(10,10))
		link_label = Label(self.root,text='URL',font=('Open Sans',10))
		link_label.grid(pady=(0,5))

		self.link_var = StringVar()

		self.link_entry = Entry(self.root,width=50,textvariable=self.link_var)
		self.link_entry.grid(pady=(0,10),ipady=1)

		self.link_entry_error = Label(self.root,text='')
		self.link_entry_error.grid()


		self.file_to_dir_button = Button(self.root,text='Choose Directory',font=('Bell MT',15),command=self.open_dir)
		self.file_to_dir_button.grid(pady=(10,5))

		
		

		self.youtube_choose_label = Label(self.root,text='Choose Download type')
		self.youtube_choose_label.grid(pady=(5,5))

		self.download_choices = [('Audio MP3',1),('Video MP4',2)]

		self.choice_var = StringVar()
		self.choice_var.set(1)

		for text,mode in self.download_choices:
			self.youtube_choices = Radiobutton(self.root,text=text,variable=self.choice_var,value=mode)
			self.youtube_choices.grid()

		self.download_button = Button(self.root,text='Download',font=('Roboto',10),command=self.check_youtube_link)

		self.download_button.grid()

		self.file_location_label = Label(self.root,text='',font=('Freestyle Script',25))
		self.file_location_label.grid()


	def open_dir(self):
		
		self.folder_name = filedialog.askdirectory()

		if len(self.folder_name) > 0:
			self.file_location_label.config(text=self.folder_name,fg='green')
			return True
		else:
			self.file_location_label.config(text='Select location',fg='red')

	def check_youtube_link(self):
		self.matchyoutubelink = re.match('^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$',self.link_var.get())
                                          
		print(self.link_var.get())
		print(self.matchyoutubelink)

		if not self.matchyoutubelink:
			self.link_entry_error.config(text='Invalid link')
		elif not self.open_dir:
			self.file_location_label.config(text='Select location')
		elif self.matchyoutubelink and self.open_dir:
			self.download_window()

	def download_window(self):

		self.new_window = Toplevel(self.root)
		self.root.withdraw()
		self.new_window.grid_rowconfigure(0,weight=0)
		self.new_window.grid_columnconfigure(0,weight=1)


		self.app = SecondApp(self.new_window,self.link_var.get(),self.folder_name,self.choice_var.get())



class SecondApp:

	def __init__(self,downloadwindow,downloadlink,folder_name,filetype):

		self.downloadwindow = downloadwindow
		self.downloadlink = downloadlink
		self.folder_name = folder_name
		self.filetype = filetype

		self.yt = YouTube(self.downloadlink)

		if filetype == '1':
			self.video_type = self.yt.streams.filter(only_audio=True).first()
			self.max_filesize = self.video_type.filesize

		if filetype == '2':
			self.video_type = self.yt.streams.first()
			self.max_filesize = self.video_type.filesize

		self.loading_label = Label(self.downloadwindow,text='Downloading....')
		self.loading_label.grid()

		self.downloaded_percent = Label(self.downloadwindow,text='0')
		self.downloaded_percent.grid()

		self.progressbar = ttk.Progressbar(self.downloadwindow,length=400,orient='horizontal',mode='indeterminate')
		self.progressbar.grid()
		self.progressbar.start()

		threading.Thread(target=self.downloadfile).start()

		threading.Thread(target=self.yt.register_on_progress_callback(self.show_progress)).start()

		

	def downloadfile(self):

		if self.filetype == '1':
			self.yt.streams.filter(only_audio=True).first().download(self.folder_name)
		if self.filetype == '2':
			self.yt.streams.first().download(self.folder_name)

	def show_progress(self,streams,Chunks,bytes_remaining):

		self.percent_count = float('%0.2f'% (100-(100*(bytes_remaining/self.max_filesize))))

		if self.percent_count < 100:
			self.downloaded_percent.config(text=self.percent_count)

		else:
			self.progressbar.stop()
			self.loading_label.grid_forget()
			self.progressbar.grid_forget()

			self.download_finished = Label(self.downloadwindow,text='Download finished')
			self.download_finished.grid()

			self.downloaded_file = Label(self.downloadwindow,text=self.yt.title)
			self.downloaded_file.grid()

			MB = float('%0.2f'% (self.max_filesize/(10**6)))
			self.download_filesize = Label(self.downloadwindow,text=str(MB))
			self.download_filesize.grid()

        	
if __name__=="__main__":

    window = Tk()
    window.title('YouTube-Download-Manager')

    app = Application(window)

    mainloop()        	

        	
        	
        	
        	

        	

        	
        	

           

        
        	
       
        	
        	








