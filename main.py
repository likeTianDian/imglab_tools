import os
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter.filedialog import askdirectory

# select_directory = ''   # 用户选择的文件夹路径
path_list = []  # xml文件路径
# xml_count = 0   # xml框数

def select_file():
    """选择按钮，功能是弹出窗口，让用户选择目录"""
    global select_directory # 用户选择的文件夹路径
    select_directory = askdirectory()
    get_path(select_directory, '.xml')

def get_path(path, suffix_name, *args):
    """遍历所选目录的所有xml文件，并添加到list"""
    # print(path)
    # 获取当前目录下的所有文件
    dir_list = os.listdir(path)
    # print(dir_list)
    for file in dir_list:
        # 遍历所有文件
        # print(os.path.abspath(path))
        # print(file)
        # 将文件绝对路径和文件名拼接
        file_path = os.path.join(os.path.abspath(path), file)
        # print(file_path)
        if os.path.isdir(file_path):
            # 若当前文件为文件夹，重新遍历当前文件夹
            # print("测试")
            get_path(file_path, suffix_name, *args)
        else:
            if file_path.endswith(suffix_name):
                # 若文件后缀名为suffix_name则存储文件绝对路径
                    path_list.append(file_path)

            if len(args):
                # 若查找多个后缀名的文件，遍历需要查询的文件后缀
                for arg in args:
                    if file_path.endswith(arg):
                        # 若找到文件后缀为arg的存储文件的绝对路径
                        path_list.append(file_path)

xml_count = 0   # xml框数
def xml_box_count():
    """计算xml文件中的box数量"""
    global xml_count
    for xml_path in path_list:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        box_element_list = root.iter(tag="box")
        for box_element in box_element_list:
            xml_count += 1
    label = tk.Label(window, text=('框数:', xml_count)).grid(row=1, column=1)

# UI界面
window = tk.Tk()
window.title('选择目录')
window.geometry('500x400')
selectButton = tk.Button(window, text='选择文件夹', command=select_file).grid(row=0)   # 选择目录按钮
# StartCountButton = tk.Button(window, text='按钮', command=lambda:get_path(select_directory, '.xml')).pack()
countXml = tk.Button(window, text='计算框数', command=xml_box_count).grid(row=1)
window.mainloop()
