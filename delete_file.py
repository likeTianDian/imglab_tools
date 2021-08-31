import os
def get_path(path, suffix_name, *args):
    """遍历所选目录的所有文件，并添加到list"""
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
