# -*- coding: utf-8 -*-
"""
@author: Craddy
"""

import tkinter as tk
import random
import numpy as np
import pygame.mixer
from PIL import Image,ImageTk
from tkinter.messagebox import showinfo
from queue import LifoQueue

class Maze():
    def __init__(self,num_rows,num_cols):
        self.rows = num_rows         #行数
        self.cols = num_cols         #列数
        self.width =  850            #游戏界面宽度
        self.height =  700           #游戏界面高度
        self.gui_width = 400         #提示界面宽度
        self.gui_height = 300        #提示界面高度
        self.d = self.height/self.cols                             #每一个格边长
        self.trace = [0,0]           #用于跟踪行走轨迹
        self._des = [self.rows-1,self.cols-1]  #终点坐标
        self.bg = "#778899"   #颜色待定
        self.wall_color = '#F0FFF0'
        self.start_color = '#fff000000'
        self.des_color = '#000fff000'
        self.hint_color = '#FFC0CB'
        self.board = tk.Tk()          #迷宫根窗口
        self.board.iconbitmap('logo.ico')      #设置图标
        self.board.title("The Maze Runner")    #设置标题
        self._set_size()
        self.select_crazy = 0         #用于标记是否选择了crazy难度
        self.select_double = 0        #用于标记是否选择了双人对战模式
        
    #获取屏幕位置从而设置窗口位置居中
    def _set_size(self):
        screenwidth = self.board.winfo_screenwidth()
        screenheight = self.board.winfo_screenheight()
        #游戏界面的大小
        self.size = "%dx%d+%d+%d"%(self.width,self.height,(screenwidth-self.width)/2,(screenheight-self.height)/2)
        #一般窗口的大小
        self.size2 = "%dx%d+%d+%d"%(self.gui_width,self.gui_height,(screenwidth-self.gui_width)/2,(screenheight-self.gui_height)/2)
        self.board.geometry(self.size)
    #创建背景图标
    def _create_background(self):
        p1 = Image.open("背景3.png")
        p2 = Image.open("背景4.png")
        self.bg1 = ImageTk.PhotoImage(p1)
        self.bg2 = ImageTk.PhotoImage(p2)
    #创建画布用于画迷宫    
    def _create_canvas(self):
        self.canvas = tk.Canvas(self.board,width=self.width,height=self.height,background=self.bg)
        self.canvas.pack(side=tk.LEFT)
        #image = Image.open("雪迎.png")
        #im = ImageTk.PhotoImage(image)
        #self.canvas.create_image(300,300,im)

    def _create_walls(self):
        #先让迷宫全是墙
        for i in range(self.rows):
            for j in range(self.cols):
                #上横边
                self.canvas.create_line(i*self.d,j*self.d,(i+1)*self.d,j*self.d,fill=self.wall_color)
                #左竖边
                self.canvas.create_line(i*self.d,j*self.d,i*self.d,(j+1)*self.d,fill=self.wall_color)
    #生成迷宫类似于prim算法（但是只取了其中“生成树”的含义，但是没有也没必要体现“最小”的含义）
    #以已有通路优先，随机加边实现生成树
    def _break_walls(self):
        #第一维是行，第二位是列，第三维表示上下左右四个方向通路（1表示通，0表示不通）和是否被访问过
        #第三维的1是左，2是上
        #m = [[[0 for i in range(self.rows)] for j in range(self.cols)] for k in range(5)]
        self.m = np.zeros((self.rows,self.cols,5),dtype=np.int)
        #初始化起点和终点
        self.m[0,0,0] = 1
        self.m[self.rows-1,self.cols-1,2] = 1
        history = [(0,0)]   #以左上角为起始点
        while history: 
            #随机选取一个点，但是保证了生成树
            r,c = random.choice(history)
            self.m[r,c,4] = 1 
            history.remove((r,c))
            check = []
            if c > 0:
                if self.m[r,c-1,4] == 1:
                    check.append('L')
                elif self.m[r,c-1,4] == 0:
                    history.append((r,c-1))
                    self.m[r,c-1,4] = 2
            if r > 0:
                if self.m[r-1,c,4] == 1: 
                    check.append('U') 
                elif self.m[r-1,c,4] == 0:
                    history.append((r-1,c))
                    self.m[r-1,c,4] = 2
            if c < self.cols-1:
                if self.m[r,c+1,4] == 1: 
                    check.append('R')
                elif self.m[r,c+1,4] == 0:
                    history.append((r,c+1))
                    self.m[r,c+1,4] = 2 
            if r < self.rows-1:
                if self.m[r+1,c,4] == 1: 
                    check.append('D') 
                elif  self.m[r+1,c,4] == 0:
                    history.append((r+1,c))
                    self.m[r+1,c,4] = 2
         
            # 随机选一个边
            if len(check):
                move_direction = random.choice(check)
                #通左边
                if move_direction == 'L':
                    self.canvas.create_line(c*self.d,r*self.d,c*self.d,(r+1)*self.d,fill=self.bg)
                    self.m[r,c,0] = 1
                    c = c-1
                    self.m[r,c,2] = 1
                #通上边
                if move_direction == 'U':
                    self.canvas.create_line(c*self.d,r*self.d,(c+1)*self.d,r*self.d,fill=self.bg)
                    self.m[r,c,1] = 1
                    r = r-1
                    self.m[r,c,3] = 1
                #通右边
                if move_direction == 'R':
                    self.canvas.create_line((c+1)*self.d,r*self.d,(c+1)*self.d,(r+1)*self.d,fill=self.bg)
                    self.m[r,c,2] = 1
                    c = c+1
                    self.m[r,c,0] = 1
                #通下边
                if move_direction == 'D':
                    self.canvas.create_line(c*self.d,(r+1)*self.d,(c+1)*self.d,(r+1)*self.d,fill=self.bg)
                    self.m[r,c,3] = 1
                    r = r+1
                    self.m[r,c,1] = 1
    #建立起点和终点
    def _create_start_and_des(self):
        self.walker = self.canvas.create_oval(self.d/3,self.d/3,self.d/3*2,self.d/3*2,fill=self.start_color)
        self.canvas.create_oval((self.rows-1)*self.d+self.d/3,(self.cols-1)*self.d+self.d/3,
                                self.rows*self.d-self.d/3,self.cols*self.d-self.d/3,fill=self.des_color)
        if self.select_double:
            self.start2_color = "#E0FFFF"
            self.des2_color = "#F5FFFA"
            self._start2 = [0,self.cols-1]
            self.walker2 = self.canvas.create_oval(self._start2[1]*self.d+self.d/3,self.d/3
                                    ,self._start2[1]*self.d+self.d/3*2,self.d/3*2,fill=self.start2_color)
            self._des2 = [self.rows-1,0]
            self.canvas.create_oval(self.d/3,self._des2[0]*self.d+self.d/3
                                    ,self.d/3*2,self._des2[0]*self.d+self.d/3*2,fill=self.des2_color)
    
    
    #退出窗口的函数
    def _quit(self):
        pygame.mixer.music.stop()   #关闭背景音乐
        self.board.quit()                 #退出窗口
        self.board.destroy()
    #返回选择难度界面
    def _back(self):
        self._quit()
        from Craddy_GUI import GUI
        root = GUI()
        root.init()
    #判断是否胜利（单人）
    def _is_victory(self):
        return self.trace == self._des
    #判断是否胜利（双人）
    def _is_victory_double(self):
        if self._is_victory():
            return 1
        if self._start2 == self._des2:
            return 2
        else:
            return 0
    def _move_walker(self,event):  #根据绑定的事件进行移动
        if event.keysym == "Up" and self.m[self.trace[0]][self.trace[1]][1]==1 and self.trace[0]>0:
            self.canvas.move(self.walker,0,-self.d)
            self.trace[0] -= 1
        elif event.keysym == 'Down' and self.m[self.trace[0]][self.trace[1]][3]==1 and self.trace[0]<self.cols:
            self.canvas.move(self.walker,0,+self.d)
            self.trace[0] += 1
        elif event.keysym == 'Left' and self.m[self.trace[0]][self.trace[1]][0]==1 and self.trace[1]>0:
            self.canvas.move(self.walker,-self.d,0)
            self.trace[1] -= 1
        elif event.keysym == 'Right' and self.m[self.trace[0]][self.trace[1]][2]==1 and self.trace[1]<self.cols:
            self.canvas.move(self.walker,+self.d,0)
            self.trace[1] += 1
        if self.select_double:
            if event.keysym == "w" and self.m[self._start2[0]][self._start2[1]][1]==1 and self._start2[0]>0:
                self.canvas.move(self.walker2,0,-self.d)
                self._start2[0] -= 1
            elif event.keysym == 's' and self.m[self._start2[0]][self._start2[1]][3]==1 and self._start2[0]<self.cols:
                self.canvas.move(self.walker2,0,+self.d)
                self._start2[0] += 1
            elif event.keysym == 'a' and self.m[self._start2[0]][self._start2[1]][0]==1 and self._start2[1]>0:
                self.canvas.move(self.walker2,-self.d,0)
                self._start2[1] -= 1
            elif event.keysym == 'd' and self.m[self._start2[0]][self._start2[1]][2]==1 and self._start2[1]<self.cols:
                self.canvas.move(self.walker2,+self.d,0)
                self._start2[1] += 1
        if not self.select_double:
            if self._is_victory():   #获胜
                t = tk.Toplevel()
                t.title("Victory")
                t.geometry(self.size2)
                tk.Label(t,text="Congratulations!\nYou have escaped from the Maze!\nDO you want to try again?",
                         font=("Times New Roman",15),compound='center',image=self.bg2).pack()
                tk.Button(t,text="Yes",command=self._back).place(relx=0.4,rely=0.9)
                tk.Button(t,text="No",command=self._quit).place(relx=0.6,rely=0.9)
        else:
            if self._is_victory_double() == 1:
                t = tk.Toplevel()
                t.title("Victory")
                t.geometry(self.size2)
                tk.Label(t,text="Congratulations.Player 1!\nYou have escaped from the Maze!\nDO you want to try again?",
                         font=("Times New Roman",15),compound='center',image=self.bg2).pack()
                tk.Button(t,text="Yes",command=self._back).place(relx=0.4,rely=0.9)
                tk.Button(t,text="No",command=self._quit).place(relx=0.6,rely=0.9)
            elif self._is_victory_double() == 2:
                t = tk.Toplevel()
                t.title("Victory")
                t.geometry(self.size2)
                tk.Label(t,text="Congratulations.Player 2!\nYou have escaped from the Maze!\nDO you want to try again?",
                         font=("Times New Roman",15),compound='center',image=self.bg2).pack()
                tk.Button(t,text="Yes",command=self._back).place(relx=0.4,rely=0.9)
                tk.Button(t,text="No",command=self._quit).place(relx=0.6,rely=0.9)
            

    #键盘事件绑定（上下左右）
    def _bind_keypress(self):
        self.canvas.bind_all("<KeyPress-Up>",self._move_walker)
        self.canvas.bind_all("<KeyPress-Down>",self._move_walker)
        self.canvas.bind_all("<KeyPress-Left>",self._move_walker)
        self.canvas.bind_all("<KeyPress-Right>",self._move_walker)
        if self.select_double:
            self.canvas.bind_all("<KeyPress-w>",self._move_walker)
            self.canvas.bind_all("<KeyPress-s>",self._move_walker)
            self.canvas.bind_all("<KeyPress-a>",self._move_walker)
            self.canvas.bind_all("<KeyPress-d>",self._move_walker)


    #游戏界面的按钮
    def _create_button(self):
        tk.Button(master=self.board,text="Quit",command=self._quit).place(relx=0.9,rely=0.5)
        tk.Button(master=self.board,text="Back",command=self._back).place(relx=0.9,rely=0.65)
        tk.Button(master=self.board,text="Hint",command=self._show_path).place(relx=0.9,rely=0.8)
    
    #bfs（显式队列实现）找最短路径
    def _bfs(self):
        def clear():   #清除提示路线
            for each in t:
                self.canvas.delete(each)
        vis = [[0 for i in range(self.rows)] for j in range(self.cols)]  #避免重复访问
        #d = [[0 for i in range(self.rows)] for j in range(self.cols)]
        parent = [[0 for i in range(self.rows)] for j in range(self.cols)]  #记录父节点
        #方向数组：左上右下
        dx = [0,-1,0,1]
        dy = [-1,0,1,0]
        #初始化
        q = LifoQueue()
        now = self.trace
        vis[now[0]][now[1]] = 1
        q.put(now)
        t = []  #存储提示的画像
        while(q):
            x,y = q.get()  #返回并删除
            for i in range(4):
                nx = x+dx[i]
                ny = y+dy[i]
                #判断是否能走过去
                if (nx>=0 and nx<self.rows and ny>=0 and ny<self.cols and vis[nx][ny]==0 and self.m[x][y][i]):
                    q.put((nx,ny))
                    vis[nx][ny] = 1
                    parent[nx][ny] = (x,y)
                    #如果到了终点
                    if nx == self._des[0] and ny == self._des[1]:
                        u,v = self._des
                        while parent[u][v] != 0:
                            #print(u,v)
                            u,v = parent[u][v]
                            if parent[u][v] == 0:
                                break
                            t.append(self.canvas.create_oval(v*self.d+self.d/3,u*self.d+self.d/3
                                                    ,v*self.d+self.d/3*2,u*self.d+self.d/3*2,fill=self.hint_color))
                        self.canvas.after(5*1000,clear)  #5s后清除提示路线
                        return #直接将函数返回，不再进行无意义的搜素
    
    def _show_path(self):   #显示最短路径
        #如果选择crazy难度则不允许提示
        if self.select_crazy==1 or self.select_double==1:
            showinfo("ERRORS","The Crazy level or double player mode have no HINT!")
        else:
            print("提示")
            self._bfs() #广搜找最短路径
    
    def _load_music(self):
        #背景音乐
        pygame.init()
        pygame.mixer.music.load("William Joseph - Radioactive.mp3")          #load("Simon Curtis - Beat Drop.mp3")
        pygame.mixer.music.play(-1,0)  #循环播放

    #超时未完成迷宫，游戏结束
    def _time_limitted(self):
        #提示窗口
        def _time_out():
            t = tk.Toplevel()
            t.title("Defeated")
            t.geometry(self.size2)
            tk.Label(t,text="I'm sorry,But time is up.\nYou fail.\nDo you want to try again?",
                     font=("Times New Roman",15),compound='center',image=self.bg1,anchor='center').pack()
            tk.Button(t,text="Yes",command=self._back).place(relx=0.4,rely=0.9)
            tk.Button(t,text="No",command=self._quit).place(relx=0.6,rely=0.9)
        if self.select_double==0:
            self.board.after(1*60*1000,_time_out)
    
    #刷新迷宫（仅在选择crazy难度后开始）
    def _refresh_walls(self):
        if self.select_crazy==0:
            return
        #重新建墙
        def _refresh():
            self._create_walls()
            self._break_walls()
        #实现移动迷宫
        self.board.after(10*1000,_refresh)
        self.board.after(20*1000,_refresh)
        self.board.after(30*1000,_refresh)
        self.board.after(40*1000,_refresh)
        self.board.after(50*1000,_refresh)
        #self.board.after(120*1000,_refresh)
    #建墙
    def _build_walls(self):
        self._create_walls()
        self._break_walls()
        self._create_start_and_des()
    #主循环
    def mainloop(self):
        self._create_background()
        self._create_canvas()
        self._build_walls()
        self._bind_keypress()
        self._create_button()
        self._load_music()
        self._refresh_walls()
        self._time_limitted()

if __name__ == '__main__':
    maze = Maze(50,50)
    maze.mainloop()


