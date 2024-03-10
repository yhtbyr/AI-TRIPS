import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.family'] = 'SimHei'  # 将字体设置为黑体'SimHei'
matplotlib.rcParams['font.sans-serif'] = ['SimHei']

labels = np.array(["语文", "数学", "英语", "化学", "物理", "生物", "信息"])
dataLenth = 7  # 数据长度
data = np.array([90, 80, 70, 60, 50, 40, 30])
angles = np.linspace(0, 2 * np.pi, dataLenth, endpoint=False)  # 根据数据长度平均分割圆周长

# 闭合
data = np.concatenate((data, [data[0]]))
angles = np.concatenate((angles, [angles[0]]))
labels = np.concatenate((labels, [labels[0]]))  # 对labels进行封闭

fig = plt.figure(facecolor="white")  # facecolor 设置框体的颜色
plt.subplot(111, polar=True)  # 将图分成1行1列，画出位置1的图；设置图形为极坐标图
plt.plot(angles, data, color='b', linewidth=2)
plt.fill(angles, data, facecolor='b', alpha=0.25)  # 填充两条线之间的色彩，alpha为透明度
plt.thetagrids(angles * 180 / np.pi, labels)  # 做标签
plt.grid(True)
plt.show()