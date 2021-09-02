# !usr/bin/env python
# -*- coding:utf-8 _*-
import os
import re
import xml.etree.ElementTree as ET
import tkinter as tk
import datetime
# import win32api
from tkinter.filedialog import askdirectory, askopenfilename

# select_directory = ''   # 用户选择的文件夹路径
path_list = []  # xml文件路径
path_list_img = []  # img图片路径
# xml_count = 0   # xml框数

def select_directory():
    """选择按钮，功能是弹出窗口，让用户选择目录"""
    global select_directory, path_list
    path_list = []
    select_directory = askdirectory()
    tk.Label(window, text=('当前选择：',select_directory)).grid_forget()
    get_xml_path(select_directory, '.xml')

def select_file():
    '''选择文件按钮'''
    global path_list, xml_path
    path_list = []
    xml_path = askopenfilename()
    # print(xml_path)
    path_list.append(os.path.abspath(xml_path))
    tk.Label(window, text=('当前选择：', xml_path)).grid(row=1, column=0, columnspan=4)
    # print(xml_path.rsplit('/', 1)[-2])
    # path_list = path_list.replace("\\", "\\\\")
    # print(path_list)

def get_xml_path(path, suffix_name, *args):
    """遍历所选目录的所有xml文件，并添加到list"""
    # print(path)
    # 获取当前目录下的所有文件
    global path_list
    # path_list = []
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
            get_xml_path(file_path, suffix_name, *args)
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
    # print(path_list)

def get_img_path(path, suffix_name, *args):
    """遍历所选目录的所有xml文件，并添加到list"""
    # print(path)
    # 获取当前目录下的所有文件
    global path_list_img
    # path_list_img = []
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
            get_img_path(file_path, suffix_name, *args)
        else:
            if file_path.endswith(suffix_name):
                # 若文件后缀名为suffix_name则存储文件绝对路径
                    path_list_img.append(file_path)

            if len(args):
                # 若查找多个后缀名的文件，遍历需要查询的文件后缀
                for arg in args:
                    if file_path.endswith(arg):
                        # 若找到文件后缀为arg的存储文件的绝对路径
                        path_list_img.append(file_path)
    # print(path_list)

def creat_xml():
    '''创建xml文件'''
    global xml_file_count
    xml_file_count = 0
    skip_count = 0
    img_dir = []
    xml_dir = []
    xml_creat_path = []
    skip_file = []
    get_img_path(select_directory, '.jpg', '.png', '.xml')
    # print(path_list_img)
    for file_path in path_list_img:
        '''获取所有图片目录'''
        # print(img_path)
        if ('.xml') in file_path:
            '''获得xml的路径'''
            # print(img_path)
            xml_dir.append(file_path.rsplit('.', 1)[-2])
        else:
            # print('false')
            img_dir.append(file_path.rsplit('\\', 1)[-2])
        # xml_dir = list(set(xml_dir))

    img_dir = list(set(img_dir))    # 去除重复的路径
    xml_dir = list(set(xml_dir))
    # print(img_dir)
    # print(xml_dir)

    '''删除已有xml的路径'''
    for a in img_dir:
        if a not in xml_dir:
            xml_creat_path.append(a)
        else:
            skip_file.append(a)
            skip_count += 1
    print(xml_creat_path)

    '''创建xml: imglab.exe -c 0.xml 0'''
    for file_path in xml_creat_path:
        os.system('.\\imglab.exe -c ' + file_path + '.xml ' + file_path)
        xml_file_count += 1

    '''显示一些状态'''
    tk.Label(window, text=('已创建：', xml_file_count, ',已跳过：', skip_count)).grid(row=3, column=1)
    skip_file_list = tk.Text(window, width=30, height=2)
    for item in skip_file:
        skip_file_list.insert(tk.END,item)
    skip_file_list.grid(row=3, column=2)

xml_count = 0  # xml框数
def xml_box_count():
    """计算xml文件中的box数量"""
    # global xml_count
    xml_count = 0
    for xml_path in path_list:
        # print(xml_path)
        tree = ET.parse(xml_path)
        root = tree.getroot()
        box_element_list = root.iter(tag="box")
        for box_element in box_element_list:
            xml_count += 1
            # print(xml_count)
        # print(xml_count)
    tk.Label(window, text=('框数:', xml_count)).grid(row=2, column=1)

def xml_id_order_increase():
    '''对按照顺序的text进行运算后替换原来的'''
    global separator, id_column
    if not separator:
        separator = '_'
    if not id_column:
        id_column = 1
    for xml_path in path_list:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        for label in root.iter('label'):
            # print(label.text)
            original_label = str(label.text)
            # print(label_text)
            label_id = original_label.split(separator)[id_column]
            # print(label_id)
            if int(label_id) > int(is_greater_than_id):
                # new_label = int(label.text) + 1
                # print('原来的ID：', label_id)
                new_id = int(label_id) + 1
                # print('新的ID:', new_id)
                # new_label = re.sub(r'(\d+_)(\d+)', '\1' + str(new_id), original_label)
                new_label = original_label.split('_')[0] + '_' + str(new_id)
                # print('原始label:', original_label)
                # print('新的label:', new_label)
                label.text = str(new_label)
        datetime_now = datetime.datetime.now().strftime('%d%H%M%S')
        # print(datetime_now)
        tree.write(xml_path.rsplit('\\', 1)[-2] +'\\' + os.path.basename(xml_path).split('.')[-2] + '_' + datetime_now + '.xml')
        # print(xml_path.rsplit('\\', 1)[-2])
        # print(os.path.basename(xml_path).split('.')[-2])
        # print(datetime_now)

def set_id_is_greater_than_the():
    '''从窗口获得用户输入的数字(ID)'''
    global is_greater_than_id
    is_greater_than_id = input_ID.get()
    # print(is_greater_than_id)

def set_input_separator():
    global separator
    separator = input_separator.get()

def set_input_id_column():
    global id_column
    id_column = input_id_column.get()

# UI界面
window = tk.Tk()
button_width = 22
window.title('选择目录')
window.geometry('500x300')
tk.Button(window, text='选择文件', command=select_file, width=button_width).grid(row=0, column=0)   # 选择文件按钮
tk.Button(window, text='选择文件夹', command=select_directory, width=button_width).grid(row=0, column=1)   # 选择目录按钮
# tk.Label(window, text='当前选择: ').grid(row=0, column=2)
# tk.Entry(window, textvariable = path_list).grid(row=0, column=3)
# StartCountButton = tk.Button(window, text='按钮', command=lambda:get_path(select_directory, '.xml')).pack()

countXml = tk.Button(window, text='计算框数', command=xml_box_count, width=button_width).grid(row=2, column=0)

tk.Button(window, text='创建xml', command=creat_xml, width=button_width).grid(row=3, column=0)

tk.Button(window, text='ID递增', command=xml_id_order_increase, width=button_width).grid(row=4, column=0)
tk.Button(window, text='设置ID大于(不包括)某个数:', command=set_id_is_greater_than_the, width=button_width).grid(row=4, column=1)
input_ID = tk.Entry(window)
input_ID.grid(row=4, column=2)

tk.Label(window, text='输入分隔符,默认:"_"').grid(row=5, column=0)
tk.Label(window, text='输入列数,默认:1').grid(row=5, column=1)

input_separator = tk.Entry(window)
input_separator.grid(row=6, column=0)
input_id_column = tk.Entry(window)
input_id_column.grid(row=6, column=1)

tk.Button(window, text='点击设置分隔符', command=set_input_separator).grid(row=7, column=0)
tk.Button(window, text='点击设置id列', command=set_input_id_column).grid(row=7, column=1)

# 创建一个菜单项，类似于导航栏
menubar=tk.Menu(window)

# 创建菜单项
# fmenu1=tk.Menu(window)
# for item in ['新建','打开','保存','另存为']:
#   # 如果该菜单时顶层菜单的一个菜单项，则它添加的是下拉菜单的菜单项。
#   fmenu1.add_command(label=item)

# fmenu2=tk.Menu(window)
# for item in ['复制','粘贴','剪切']:
#   fmenu2.add_command(label=item)

# fmenu3=tk.Menu(window)
# for item in ['默认视图','新式视图']:
#   fmenu3.add_command(label=item)

fmenu4=tk.Menu(window)
for item in ["Github:","liketiandian/imglab_tools"]:
    fmenu4.add_command(label=item)

# add_cascade 的一个很重要的属性就是 menu 属性，它指明了要把那个菜单级联到该菜单项上，
# 当然，还必不可少的就是 label 属性，用于指定该菜单项的名称
# menubar.add_cascade(label="文件",menu=fmenu1)
# menubar.add_cascade(label="编辑",menu=fmenu2)
# menubar.add_cascade(label="视图",menu=fmenu3)
menubar.add_cascade(label="关于",menu=fmenu4)

# 最后可以用窗口的 menu 属性指定我们使用哪一个作为它的顶层菜单
window['menu']=menubar
window.mainloop()

# print("数量：", xml_count)