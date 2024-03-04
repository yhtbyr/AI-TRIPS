from threading import Thread
from pynput import mouse, keyboard
from tkinter import *
import pyautogui
import pyscreeze
import datetime
import os
    
# 设计异步操作
def async_call(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper
    

# 封装截图功能
@async_call
class screen:
    def __init__(self) -> None:
        self.joints = [] # 节点列表
        self.p = True # 控制鼠标监听的开关
        self.listener() # 开始监听

        self.win_x, self.win_y = pyautogui.size()  # 获取屏幕分辨率
        self.tk = Tk() # 创建窗口
        self.tk.resizable(width=False, height=False)  # 禁止更改窗口大小
        self.tk.geometry("{}x{}".format(self.win_x,self.win_y)) # 设置窗口大小和显示位置
        self.tk.configure(bg="#808080") # 设置窗口背景颜色
        self.tk.attributes("-alpha", 0.5) # 设置窗口透明度
        self.tk.attributes('-topmost', 'true') # 置顶窗口
        self.tk.overrideredirect(True) # 关闭窗口标题栏
        
        self.canvas = Canvas(self.tk, width=self.win_x, height=self.win_y) # 创建画布
        self.canvas.pack() # 封装画布
        self.tk.bind('<KeyPress-Escape>', self.quit) # 结束截图
        self.tk.bind('<KeyPress-Return>', self.save) # 保存截图
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag) # 绘制矩形选个框
        self.tk.mainloop() # 保持窗口开启

    def quit(self, event):
        self.p = False
        self.tk.destroy() # 退出窗口
    def save(self, event):
        self.p = False
        self.tk.destroy() # 退出窗口
        path = "screen"  # 相对路径
        if path not in os.listdir("C:/Users/Public/Downloads"):  # 判断相对路径文件夹是否存在
            os.mkdir("C:/Users/Public/Downloads/"+path) # 创建文件夹
        nowDatatime = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d-%H%M%S")  # 获取当前时间
        
        # 调整节点
        if self.joints[1][0]<self.joints[0][0]:self.joints[1][0],self.joints[0][0]=self.joints[0][0],self.joints[1][0]
        if self.joints[1][1]<self.joints[0][1]:self.joints[1][1],self.joints[0][1]=self.joints[0][1],self.joints[1][1]
        # 截图
        pyscreeze.screenshot("C:/Users/Public/Downloads/screen/{}.png".format(nowDatatime), 
                                    region=(self.joints[0][0],
                                    self.joints[0][1],
                                    self.joints[1][0]-self.joints[0][0],
                                    self.joints[1][1]-self.joints[0][1],
                                    ))   
    def on_mouse_drag(self, event):
        self.canvas.delete("crop_rectangle") # 删除上一步绘画
        self.current_x = event.x # 临时变量,鼠标横轴
        self.current_y = event.y # 临时变量,鼠标纵轴
        self.canvas.create_rectangle(self.joints[0][0], self.joints[0][1], self.current_x, self.current_y, fill="gray", outline="red", tags="crop_rectangle") # 绘制矩形所选框
    
    # 设置按下或放下鼠标时操作
    def on_click(self, x, y, button, pressed):
        if not self.p:
            return self.p # self.p为false是停止监听
        if len(self.joints) == 2:self.joints=[] # 节点数为2时重置
        self.joints.append([x,y]) # 向节点列表添加节点
        # print(self.joints) # 输出节点数值
        
    # 设计鼠标监听
    @async_call # 异步操作防止监听事件影响画布加载
    def listener(self):
        listenerMouse = mouse.Listener(on_click=self.on_click)  # 监听鼠标
        listenerMouse.start()  # 开始
        listenerMouse.join()  # 添加监听器
        listenerMouse.stop()  # 结束

# 使用说明
print("使用说明:\n程序启动后按<ctrl>+<alt>+s进行截图,enter为保存,esc为退出截图\n截图会被保存在C:\\Users\\Public\\Downloads\\screen中")
# 绑定热键监听键盘事件
with keyboard.GlobalHotKeys({
    "<ctrl>+<alt>+s":lambda:screen()
}) as l:
    l.join()


