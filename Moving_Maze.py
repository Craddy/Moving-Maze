# -*- coding: utf-8 -*-
"""
@author: Craddy
"""

"""
通过打包成两个库（其中包含了GUI类和Maze类），实现整个程序
其中GUI类实现的主要是界面的布局，而Maze类主要实现迷宫游戏
其中迷宫主要有以下功能：
1、*最基本的迷宫布局，保证是个生成树（这就保证了迷宫有解）
2、** 路径提示 在玩家遇到困难时提供当前位置到终点的最短路径
3、*** 移动迷宫 在crazy难度中每10s刷新一次迷宫布局，这在很大程度上提升了游戏的难度（尤其是对于那些逆推迷宫解的玩家）
"""

from GUI import GUI
from Maze_logic import Maze

if __name__ == "__main__":
    root = GUI()
    root.init()
