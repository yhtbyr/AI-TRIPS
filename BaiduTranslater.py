import random
import hashlib
import urllib
import requests
from tkinter import *
from tkinter import ttk
import pyautogui

# 可用翻译语言,仅为展示未全部列出
LangList = {
    "自动检测":"auto",
    "中文":"zh",
    "英语":"en",
    "粤语":"yue",
    "文言文":"wyw",
    "日语":"jp",
    "韩语":"kor",
    "法语":"fra",
    "西班牙语":"spa",
    "泰语":"th",
    "阿拉伯语":"ara",
    "俄语":"ru",
    "葡萄牙语":"pt",
    "德语":"de",
    "意大利语":"it"
}

# 翻译
def tranlate(q, fromLang="auto", toLang="zh"):
    """
    q:
    --
        需要被翻译的词句\n
    
    fromLang:
    ---------
        被翻译词句语言,默认为自动\n
   
    toLang:
    -------
        需要被翻译成的语言,默认为zh(中文)\n
    """
    # api申请地址 https://fanyi-api.baidu.com/manage/developer
    appid = '你的appid'  # appid
    secretKey = '你的密钥'  # 密钥

    #'/api/trans/vip/translate'  #API地址
    salt = random.randint(32768, 65536)  # 随机数,API需要
    sign = hashlib.md5((appid + q + str(salt) + secretKey).encode()).hexdigest()  # md5标签
    # 完整访问地址,其中urllib.parse.quote函数将q转为ASCII码
    myurl = 'appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

    res = requests.request("get",'https://api.fanyi.baidu.com/api/trans/vip/translate?',params=myurl)  # 通过GET请求访问地址
    # ["trans_result"][0]["dst"]
    # 返回页面内容
    return res.json()

# 获取信息并进行翻译
def get_massage(fromLangList, toLangList, inputBox, outputBox):
    res = tranlate(inputBox.get("1.0","5.40").strip(), LangList[fromLangList.get()], LangList[toLangList.get()])  # 翻译
    outputBox.configure(state='normal')  # 恢复输出框读写功能
    outputBox.delete("1.0","5.40")  # 清空输入框
    outputBox.insert(END, res["trans_result"][0]["dst"])  # 将翻译结果写入
    outputBox.configure(state='disabled')  # 关闭输出框读写功能

# 创建视图
def GUI():
    tk = Tk()  # 创建窗口
    tk.resizable(width=False, height=False)  # 禁止更改窗口大小
    tk.title("百度翻译API")  # 窗口名称
    x,y = pyautogui.size()  # 获取屏幕分辨率
    tk.geometry("1200x500+{}+{}".format(x//2-600, y//2-250))  # 设置窗口大小和显示位置

    # 创建下拉框 (输入语言)
    Label(tk, text="输入语言:", width=15, font=('楷体', 20)).grid(row=1,column=1)  # 引导内容
    fromLangList = ttk.Combobox(tk,width=20, font=('楷体', 20))  # 创建下拉框对象
    fromLangList["value"] = tuple(tuple(LangList.keys()))  # 设置下拉框数值
    fromLangList["state"] = 'readonly'  # 设置下拉框状态为只读
    fromLangList.current(0)  # 设置下拉框默认值
    fromLangList.grid(row=1,column=2)  # 设置布局
    # 创建下拉框 (输出语言)
    Label(tk, text="输出语言:", width=15, font=('楷体', 20)).grid(row=2,column=1)  # 引导内容
    toLangList = ttk.Combobox(tk,width=20, font=('楷体', 20))  # 创建下拉框对象
    toLangList["value"] = tuple(tuple(LangList.keys())[1::])  # 设置下拉框数值
    toLangList["state"] = 'readonly'  # 设置下拉框状态为只读
    toLangList.current(0)  # 设置下拉框默认值
    toLangList.grid(row=2,column=2)  # 设置布局

    # 创建输入框
    Label(tk, text="输入框:", font=('楷体', 20)).grid(row=3, column=1)  # 引导内容
    inputBox = Text(tk, width=40, height=4, font=('楷体', 20))  # 设置多行文本框
    inputBox.grid(row=3, column=2)  # 设置布局
    # 创建输出框
    Label(tk, text="输出框:", font=('楷体', 20)).grid(row=4, column=1)  # 引导内容
    outputBox = Text(tk, width=40, height=4, font=('楷体', 20))  # 设置多行文本框
    outputBox.grid(row=4, column=2)  # 设置布局
    outputBox.configure(state='disabled')

    # 翻译按钮res["trans_result"][0]["dst"]
    f_b = Button(tk, text="翻译", bg="grey", font=('楷体', 20), command=lambda:get_massage(fromLangList, toLangList, inputBox, outputBox))  # 设置按钮
    f_b.grid(row=5, column=2, sticky="n")  # 设置布局
    

    tk.mainloop()  # 保持窗口开启

GUI()
    

