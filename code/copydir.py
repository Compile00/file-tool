# 批量匹配文件名并移动文件到对应的文件夹
import os
import re
import shutil
import pandas as pd


# list1 = ['file1.txt', 'file2.csv', 'photo1.jpg']
#
# list2 = ['/home/user/folder/file1.txt', '/tmp/file2.csv', '/user/photos/photo1.jpg']


# 匹配文件名
def matchesname(namelist,filenames):
    # 匹配到文件路径
    matches = []
    # nomatches = set()
    no_matches = []
    # 将匹配出名单中的文件路径, 取子集, 即名单上的名为文件路径的子集
    for name in namelist:
        found = False
        for path in filenames:
            if name in path:
                matches.append(path)
                found = True
                break
        if not found:
            no_matches.append(name)
    print("已经匹配到的"+str(matches))
    print("没有匹配到的" + str(no_matches))

    return matches


# 移动文件
def filemove(matches,folder, target_folder):
    # 文件路径列表, 进行批量复制移动
    file_paths = []
    # file_paths = ['/home/user/file1.txt', '/tmp/logs/file2.log']
    # 将拼接好文件路径
    for i in range(len(matches)):
        file_paths.append(folder+"/"+matches[i])
    # file_paths = matches
    # target_folder = 'backup2'  # 目标文件夹
    # 进行复制
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        target_path = os.path.join(target_folder, file_name)
        shutil.copy(file_path, target_path)

# 移动文件夹
def dirmove(matches,folder, dst_dir):
    # 文件路径列表, 进行批量复制移动
    dir_paths = []
    # file_paths = ['/home/user/file1.txt', '/tmp/logs/file2.log']
    # 将拼接好文件路径

    # src_dir = 'source_dir'
    # dst_dir = 'dest_dir'


    for i in range(len(matches)):
        dir_paths.append(folder+"/"+matches[i])  #将匹配到的文件夹名拼接成路径
    # file_paths = matches
    # target_folder = 'backup2'  # 目标文件夹
    # 进行复制
    for dir_path in dir_paths:
        # shutil.copytree(file_path, dst_dir)  # 将src_dir文件夹复制到目标文件夹dst_dir中
        # if not os.path.exists(dst_dir):  # 如果目标文件夹不存在则创建一个文件夹
        #     os.makedirs(dst_dir)
        # 因为copytree不会复制源文件夹, 只会复制源文件夹内的东西, 注意dst_dir这个文件夹是新创建的, 必须确保原来的路径下无该文件夹才能复制成功
        # 在目标目录下创建同名文件夹os.path.join(dst_dir, os.path.basename(file_path))
        shutil.copytree(dir_path, os.path.join(dst_dir, os.path.basename(dir_path)))  # 先复制


# 输出当前路径下的所有文件
def findfilename(filedirpath):
    # 文件夹中的所有文件名
    folder = filedirpath  # 扫描文件夹路径
    filenames = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]  # 搜索该文件夹下所有的文件, 并以列表的形式输出文件名
    print("该文件夹下的所有文件名: "+str(filenames))  # 输出该文件夹下的所有文件名

    return filenames   # 返回文件名列表



def finddirname(dirpath):
    # 文件夹名称列表
    dirname = []
    # 遍历指定路径下的文件夹和文件
    for name in os.listdir(dirpath):
        # 拼接成完整路径
        path = os.path.join(dirpath, name)

        # 判断是否文件夹
        if os.path.isdir(path):
            dirname.append(name)

    print("该路径下的所有文件夹名: "+str(dirname))
    return dirname

# 按名单找文件
def filecopy(namelist):
    folders = []
    for dirpath, dirnames, filenames in os.walk('.'):
        folders += [os.path.join(dirpath, d) for d in dirnames]
    print("当前路径下的文件夹" + str(folders))

    filedirpath = input("请输入搜索的文件夹路径\n")

    filenames = findfilename(filedirpath)
    matches = matchesname(namelist, filenames)  # 匹配文件名

    pattern = re.compile(r'^[\w\.-]+$')
    while True:
        diy = input("请输入要复制到的文件夹名, 不输入默认输出的文件夹名为: backup, 回车即可\n")
        if len(diy) == 0:
            print('检测到空输入,使用默认文件夹名backup')
            diy = 'backup'

        if os.path.exists(diy):
            print("已经有重复的文件夹, 为了避免数据覆盖,请重新输入新的文件名")
            continue  # 直接跳过下面的判断, 继续重新开始输入

        if pattern.match(diy):
            # print('合法文件名')
            break
        else:
            print('非法文件名,请重新输入:')

    folder_name = diy

    if not os.path.exists(folder_name):  # 不存在该文件夹则创建一个文件夹
        os.makedirs(folder_name)

    filemove(matches, filedirpath, folder_name)  # 复制文件
    print("已经将匹配到的文件复制到该文件夹:{}".format(folder_name))

    print("执行完毕".center(50, "*"))


def dircopy(namelist):
    print("dircopy")
    folders = []
    for dirpath, dirnames, filenames in os.walk('.'):
        folders += [os.path.join(dirpath, d) for d in dirnames]
    print("当前路径下的文件夹" + str(folders))

    filedirpath = input("请输入搜索的文件夹路径\n")

    dirnames = finddirname(filedirpath)
    matches = matchesname(namelist, dirnames)  # 匹配文件名

    pattern = re.compile(r'^[\w\.-]+$')
    while True:
        diy = input("请输入要复制到的文件夹名, 不输入默认输出的文件夹名为: backup2, 回车即可\n")
        if len(diy) == 0:
            print('检测到空输入,使用默认文件夹名backup2')
            diy = 'backup2'

        if os.path.exists(diy):
            print("已经有重复的文件夹, 为了避免数据覆盖,请重新输入新的文件名")
            continue  # 直接跳过下面的判断, 继续重新开始输入

        if pattern.match(diy):
            # print('合法文件名')
            break
        else:
            print('非法文件名,请重新输入:')

    dst_dir = diy

    if not os.path.exists(dst_dir):  # 不存在该文件夹则创建一个文件夹
        os.makedirs(dst_dir)

    dirmove(matches, filedirpath, dst_dir)  # 复制文件
    print("已经将匹配到的文件夹复制到该文件夹:{}".format(dst_dir))

    print("执行完毕".center(50, "*"))

while(True):
    # try:
    #     file_name = os.listdir(r'./')  # 读取当前相对路径下的文件名, 以列表的形式保存
    #     print('当前路径下的Excel文件名')
    #     choice = []
    #     for i in file_name:
    #         if i[-4:] == ".xls" or i[-5:] == ".xlsx":
    #             choice.append(i)
    #     print(choice)
    #
    #
    #     path = input("请输入要匹配的名单的Excel文件名: (输入0退出程序)\n")
    #     if path == '0':
    #         break
    #     # df = pd.read_excel(path, usecols=[lie])
    #     df = pd.read_excel(path)
    #     # print(df)
    #     print("该excel表有"+str(len(df.columns))+"列")  # 列数
    #
    #     print("仅按匹配列的数据匹配")
    #
    #     while True:
    #         lie = input("请输入你要匹配该表的哪一列?\n")
    #         lie = int(lie)-1
    #         if (lie<len(df.columns)):
    #             break
    #         print("输入错误, 请重新输入, 只能输入范围内的数, 该表格有{}列".format(len(df.columns)))
    #
    #     # 输出excel中的名单
    #     namelist = []
    #     for index, row in df.iterrows():
    #         if pd.isna(row[lie]):  # 如果有空值则跳过
    #             continue
    #         # print(row[lie])
    #         if isinstance(row[lie], float):
    #             row[lie] = int(row[lie])
    #         # namelist.append(str(int(row[0]))+ row[1])
    #         namelist.append(str(row[lie]))
    #     print("待匹配的名单为"+str(namelist))
    #     print("总共要匹配的个数为:{}个".format(len(namelist)))
    #
    #
    #     while True:
    #         select = input("请选择你接下来的操作:1. 按名单找文件, 2.按名单找文件夹 (仅需输入数字即可)")
    #
    #         if (select == "1"):
    #             filecopy(namelist)
    #             break
    #         elif (select == "2"):
    #             dircopy(namelist)
    #             break
    #         else:
    #             print("输入有误, 请重新输入!")
    # except:
    #     print("发生了未知错误, 请重新输入, 注意可能是要搜索的文件不符合该系统的查找规则, 多次尝试无果后,请放弃使用!")
    file_name = os.listdir(r'./')  # 读取当前相对路径下的文件名, 以列表的形式保存
    print('当前路径下的Excel文件名')
    choice = []
    for i in file_name:
        if i[-4:] == ".xls" or i[-5:] == ".xlsx":
            choice.append(i)
    print(choice)

    path = input("请输入要匹配的名单的Excel文件名: (输入0退出程序)\n")
    if path == '0':
        break
    # df = pd.read_excel(path, usecols=[lie])
    df = pd.read_excel(path)
    # print(df)
    print("该excel表有" + str(len(df.columns)) + "列")  # 列数

    print("仅按匹配列的数据匹配")

    while True:
        lie = input("请输入你要匹配该表的哪一列?\n")
        lie = int(lie) - 1
        if (lie < len(df.columns)):
            break
        print("输入错误, 请重新输入, 只能输入范围内的数, 该表格有{}列".format(len(df.columns)))

    # 输出excel中的名单
    namelist = []
    for index, row in df.iterrows():
        if pd.isna(row[lie]):  # 如果有空值则跳过
            continue
        # print(row[lie])
        if isinstance(row[lie], float):
            row[lie] = int(row[lie])
        # namelist.append(str(int(row[0]))+ row[1])
        namelist.append(str(row[lie]))
    print("待匹配的名单为" + str(namelist))
    print("总共要匹配的个数为:{}个".format(len(namelist)))

    while True:
        select = input("请选择你接下来的操作:1. 按名单找文件, 2.按名单找文件夹 (仅需输入数字即可)")

        if (select == "1"):
            filecopy(namelist)
            break
        elif (select == "2"):
            dircopy(namelist)
            break
        else:
            print("输入有误, 请重新输入!")


