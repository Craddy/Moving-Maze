# -*- coding: utf-8 -*-
"""
@author: Craddy
"""

import tkinter as tk
from PIL import ImageTk,Image
from Maze_logic import Maze
class GUI():
    def __init__(self):
        self.width = 400
        self.height = 300
        self.num_rows = 0
        self.num_cols = 0
        self.select_crazy=0
        self.select_double=0
    def _start(self):
        self.top1.destroy()
        self.load_choose_box()
    def load_welcome_window(self):
        self.top1 = tk.Tk()
        #logo_s = Image.open("迷宫图标.ico")
        #logo = ImageTk.PhotoImage(logo_s)
        self.top1.iconbitmap('logo.ico')
        self.top1.title("Moving Maze")
        screenwidth = self.top1.winfo_screenwidth()
        screenheight = self.top1.winfo_screenheight()
        #设置窗口居中
        self.size1 = "%dx%d+%d+%d"%(self.width,self.height,(screenwidth-self.width)/2,(screenheight-self.height)/2) 
        self.top1.geometry(self.size1)
        #设置背景图片
        bg_image = Image.open(r"背景.png")
        background = ImageTk.PhotoImage(bg_image)
        #设置开始按钮
        tk.Button(self.top1,text="Start",command=self._start).pack()
        #问候语
        tk.Label(self.top1,text="Welcome to The Moving Maze~\nI hope you will enjoy the adventure here",
                 font=("Times New Roman",15),compound="center",image=background).pack(expand=tk.YES)

        self.top1.mainloop()
    
    def load_choose_box(self):
        #选择难度界面
        def verify_difficulty():
            x = v.get()
            #normal难度
            if x==1:
                self.num_rows = 10
                self.num_cols = 10
            #advanced难度
            elif x==2:
                self.num_rows = 20
                self.num_cols = 20
            #expert难度
            elif x==3:
                self.num_rows = 30
                self.num_cols = 30
            #crazy难度
            elif x==4:
                self.num_rows = 45
                self.num_cols = 45
                self.select_crazy = 1
            #双人模式
            elif x==5:
                self.num_rows = 45
                self.num_cols = 45
                self.select_double = 1
            self.top2.destroy()
            self.create_maze()
        self.top2 = tk.Tk()
        self.top2.iconbitmap('logo.ico')
        self.top2.title("Moving Maze")
        self.top2.geometry(self.size1)
        #设置背景图片
        bg2_image = Image.open(r'背景2.png')
        background2 = ImageTk.PhotoImage(bg2_image)
        #单选按钮变量
        v = tk.IntVar()
        #info_label
        tk.Label(self.top2,text="Select the difficulty level",font=("Times New Roman",12),anchor="se",compound="center"
                              ,image=background2).pack(expand=tk.YES)
        #select_normal_button
        tk.Radiobutton(self.top2,text = "Normal",value=1,variable=v,bg="#FFF8DC").place(relx=0.45,rely=0.3)
        #select_advanced_button
        tk.Radiobutton(self.top2,text = "Advanced",value=2,variable=v,bg="#FFF8DC").place(relx=0.45,rely=0.4)
        #select_expert_button
        tk.Radiobutton(self.top2,text = "Expert",value=3,variable=v,bg="#FFF8DC").place(relx=0.45,rely=0.5)
        #select_crazy_button
        tk.Radiobutton(self.top2,text = "Crazy",value=4,variable=v,bg="#FFF8DC").place(relx=0.45,rely=0.6)
        #双人模式
        tk.Radiobutton(self.top2,text = "Double Player",value=5,variable=v,bg="#FFF8DC").place(relx=0.45,rely=0.7)
        #verify_button
        tk.Button(self.top2,text="Start",command = verify_difficulty,bg="#FFF8DC").place(relx=0.45,rely=0.8)
    
        self.top2.mainloop()
    def create_maze(self):
        maze = Maze(self.num_rows,self.num_cols)
        maze.select_crazy = self.select_crazy
        maze.select_double = self.select_double
        maze.mainloop()
    #初始化
    def init(self):
        self.load_welcome_window()

if __name__ == "__main__":      
   root = GUI()
   root.init()
