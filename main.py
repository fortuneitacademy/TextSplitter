from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.core.window import Window
import os
from plyer import filechooser
Window.size = (400,500)
KV = '''
MDScreen:
    MDFloatLayout:
        MDLabel:
            text:'TextSplitter'
            halign:'center'
            font_size:25
            pos_hint:{'center_x':0.5,'center_y':0.93}
        MDTextField:
            id:text_filed_input
            hint_text: "Enter the path of the txt files"
            size_hint_x:0.85
            icon_right: "alert"
            pos_hint:{'center_x':0.5,'center_y':0.8}
            on_text:
                if len(self.text) > 0: self.icon_right = 'check'
                if not len(self.text) > 0: self.icon_right = "alert"
        MDRoundFlatIconButton:
            icon: "file"
            text: "Select  '.txt ' files "
            pos_hint:{'center_x':0.5,'center_y':0.71}
            on_press:app.select_file()
        MDTextField:
            id:text_filed_output
            hint_text: "Enter the output folder path"
            size_hint_x:0.85
            icon_right: "alert"
            pos_hint:{'center_x':0.5,'center_y':0.58}
            on_text:
                if len(self.text) > 0: self.icon_right = 'check'
                if not len(self.text) > 0: self.icon_right = "alert"
        MDRoundFlatIconButton:
            icon: "folder"
            text: "Select output folder"
            pos_hint:{'center_x':0.5,'center_y':0.49}
            on_press:app.select_folder()
        
        MDTextField:
            id:key_input
            hint_text: "Enter the splitting key"
            size_hint_x:0.5
            icon_right: "alert"
            pos_hint:{'center_x':0.5,'center_y':0.36}
            on_text:
                if len(self.text) > 0: self.icon_right = 'check'
                if not len(self.text) > 0: self.icon_right = "alert"
        MDRoundFlatIconButton:
            icon: "book-edit-outline"
            text: "Start"
            pos_hint:{'center_x':0.5,'center_y':0.27}
            on_release:
                app.start_app()
        MDLabel:
            id:bar_text
            text:''
            halign:'center'
            font_size:25
            pos_hint:{'center_x':0.5,'center_y':0.15}
        MDProgressBar:
            id:bar
            value: 0
            size_hint_x:0.85
            pos_hint:{'center_x':0.5,'center_y':0.1}

'''

class TextSplitter(MDApp):
    def build(self):
        self.oyna = Builder.load_string(KV)
        self.files = None
        self.icon = 'logots.png'
        self.folder = None
        self.key = None
        return self.oyna
    def select_file(self):
        self.files = filechooser.open_file(filters=["*.txt"])
        path_list = ''
        for a in self.files:
            path_list = path_list + '"' + str(a) + '"'
        self.oyna.ids.text_filed_input.text = path_list
    def select_folder(self):
        self.folder = filechooser.choose_dir()
        path_list = ''
        for a in self.folder:
            path_list = path_list + '"' + str(a) + '"'
        self.oyna.ids.text_filed_output.text = path_list
    def start_app(self):
        if len(self.oyna.ids.key_input.text) > 0:
            self.key = self.oyna.ids.key_input.text
        lise_wid = [self.oyna.ids.text_filed_input,self.oyna.ids.text_filed_output,self.oyna.ids.key_input]
        work = None
        for wid in lise_wid:
            if len(wid.text) > 0:
                pass
            else:
                wid.focus = True
                work = False
                break
        if not work == False and not self.files == None and not self.folder == None:
            try:
                self.oyna.ids.bar_text.text = '%'
                self.oyna.ids.bar.opacity = 1
                self.oyna.ids.bar.max = len(self.files)
                for file  in self.files:
                    self.oyna.ids.bar.value = int(self.files.index(file) + 1)
                    self.oyna.ids.bar_text.text = str(int(float(len(self.files) / int(self.files.index(file) + 1)) * 100)) + '%'
                    text = open(file,'r')
                    str_text = str(text.read())
                    text.close()
                    str_text_list = str_text.split(self.key)
                    for text in str_text_list:
                        name = str(os.path.basename(file))
                        name = name.replace('.txt','-') + str(str_text_list.index(text) + 1) + '.txt'
                        create_file = open(os.path.join(self.folder[0],name),'w')
                        create_file.write(text)
                self.files = None
                self.folder = None
            except Exception as e:
                self.oyna.ids.bar_text.text = str(e)
                self.oyna.ids.bar.opacity = 0
        elif not work == False:
            try:

                if self.files == None:
                    self.files = str(self.oyna.ids.text_filed_input.text).split(',')
                if self.folder == None:
                    self.folder = [str(self.oyna.ids.text_filed_output.text)]
                print(f'File: {self.files}\n',f'Folder: {self.folder}')
                self.oyna.ids.bar_text.text = '%'
                self.oyna.ids.bar.opacity = 1
                self.oyna.ids.bar.max = len(self.files)
                for file  in self.files:
                    self.oyna.ids.bar.value = int(self.files.index(file) + 1)
                    self.oyna.ids.bar_text.text = str(int(float(len(self.files) / int(self.files.index(file) + 1)) * 100)) + '%'
                    text = open(file,'r')
                    str_text = str(text.read())
                    text.close()
                    str_text_list = str_text.split(self.key)
                    for text in str_text_list:
                        name = str(os.path.basename(file))
                        name = name.replace('.txt','-') + str(str_text_list.index(text) + 1) + '.txt'
                        create_file = open(os.path.join(self.folder[0],name),'w')
                        create_file.write(text)
            except Exception as e:
                self.oyna.ids.bar_text.text = str(e)
                self.oyna.ids.bar.opacity = 0
                print(f'File: {self.files}\n', f'Folder: {self.folder}')

TextSplitter().run()