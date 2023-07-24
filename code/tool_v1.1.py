# 批量匹配文件名并移动文件到对应的文件夹
import os
import re
import shutil
import pandas as pd


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
    print("分割线".center(50, "="))
    print("已经匹配到的"+str(matches))
    print("分割线".center(50, "="))
    print("没有匹配到的" + str(no_matches))
    print("分割线".center(50, "="))

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

    for i in range(len(matches)):
        dir_paths.append(folder+"/"+matches[i])  #将匹配到的文件夹名拼接成路径

    for dir_path in dir_paths:
        shutil.copytree(dir_path, os.path.join(dst_dir, os.path.basename(dir_path)))  # 复制


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
    print("分割线".center(50, "="))
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
    print("分割线".center(50, "="))
    print("已经将匹配到的文件夹复制到该文件夹:{}".format(dst_dir))
    print("执行完毕".center(50, "*"))


def printname():
    cur = input('请输入要读取的文件夹或者路径:')
    cur_dir = r'{}'.format(cur)  # 如果不加 r,反斜杠会被转换,导致路径错误
    print("读取该路径或者文件夹: "+cur_dir)

    # 通过os.path.isfile()和os.path.isdir()对每个条目判断是否文件或文件夹,分别存到不同列表中
    filenames = [f for f in os.listdir(cur_dir) if os.path.isfile(os.path.join(cur_dir, f))]
    dirnames = [d for d in os.listdir(cur_dir) if os.path.isdir(os.path.join(cur_dir, d))]

    fileonlynames = [f.split('.')[0] for f in os.listdir(cur_dir) if os.path.isfile(os.path.join(cur_dir, f))]

    # 创建两个DataFrame分别存储文件名和文件夹名
    files_df = pd.DataFrame({'文件名': filenames})
    dirs_df = pd.DataFrame({'文件夹名': dirnames})
    files_only_df = pd.DataFrame({'纯文件名': fileonlynames})

    # 合并(concat)两个DataFrame
    result_df = pd.concat([files_df, dirs_df, files_only_df], axis=1)


    while True:
        excel_name = input("请输入要创建的excel表的文件名, 不输入直接回车即默认输出的文件名为: result.xlsx, 回车即可\n")
        if len(excel_name) == 0:
            print('使用默认文件名result.xlsx')
            excel_name = 'result.xlsx'
            break
        pattern = re.compile(r'^[\w\.-]+$')
        if pattern.match(excel_name):
            # print('合法文件名')
            excel_name = excel_name+".xlsx"  # 拼接成完整的文件名
            break
        else:
            print('非法文件名,请重新输入:')

    # 将concat后的DataFrame写入Excel
    result_df.to_excel(excel_name, index=False)
    print("写入表格成功, excel文件名为:{}".center(50, "*").format(excel_name))
    print("分割线".center(50, "="))

def list2find(path):

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
    print("分割线".center(50, "="))
    print("待匹配的名单为" + str(namelist))
    print("分割线".center(50, "="))
    print("总共要匹配的个数为:{}个".format(len(namelist)))
    print("分割线".center(50, "="))

    while True:
        select = input("请选择你接下来的操作:1. 按名单找文件, 2.按名单找文件夹 (仅需输入数字即可): ")

        if (select == "1"):
            filecopy(namelist)
            break
        elif (select == "2"):
            dircopy(namelist)
            break
        else:
            print("输入有误, 请重新输入!")

def file2dir(path):
    # 获取文件名称
    filenames = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    print(filenames)
    # 获取所有文件夹名称
    dirnames = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    print(dirnames)


    matchnamedict = {} #匹配到的文件夹名加入到字典中
    nomatchname = []  # 未匹配到的文件夹名
    # 先将所有文件夹名放到未匹配中, 若匹配到则移除
    for i in dirnames:
        nomatchname.append(i)

    while True:
    # 遍历所有文件夹
        matchname = []  # 匹配到的文件夹名
        for d in dirnames:
            found = False
            # 尝试匹配文件中的姓名
            for f in filenames:
                if d in f:
                    shutil.move(path + "/" + f, path + "/" + d)  # 都是根据路径进行移动
                    #移除已经移动的文件名
                    matchname.append(d)
                    # 将匹配到的加入字典中并计数
                    try:
                        filenames.remove(f)
                        nomatchname.remove(d)
                    except Exception:
                        pass
                    key = d
                    if key in matchnamedict:
                        matchnamedict[key] += 1
                    else:
                        matchnamedict[key] = 1
                    found = True
                    break
        if not matchname:
            print("匹配结束")
            break

    nomatchname = list(set(nomatchname))  # 列表去重
    # print(', '.join(f"{k}={v}" for k, v in dict.items()))
    # print("已经匹配到的" + str(matchname))
    print("分割线".center(50,"="))
    print("已经匹配到的: " + ', '.join(f"文件夹: ({k}):有{v}个文件" for k, v in matchnamedict.items()))
    print("分割线".center(50, "="))
    print("没有匹配到的" + str(nomatchname))
    print("执行完毕".center(50, "*"))

while(True):
    try:
        print("欢迎使用文件批量处理小工具! v1.1".center(50,"-"))
        choose = input(
            "请输入你的要进行的操作,1. 读出某个文件夹下的文件名, 2.根据名单进行查找文件或文件夹, 3.将文件复制到指定文件夹中, 输入0退出程序: ")
        if (choose == "1"):
            printname()
        elif (choose == "2"):
            while True:
                try:
                    file_name = os.listdir(r'./')  # 读取当前相对路径下的文件名, 以列表的形式保存
                    print('当前路径下的Excel文件名')
                    choice = []
                    for i in file_name:
                        if i[-4:] == ".xls" or i[-5:] == ".xlsx":
                            choice.append(i)
                    print(choice)

                    path = input("请输入要匹配的名单的Excel文件名: (输入0返回上一级)\n")
                    if path == '0':
                        break
                    list2find(path)
                except:
                    print(
                        "发生了未知错误, 请重新输入(可能是文件名错误), 注意可能是要搜索的文件不符合该系统的查找规则, 多次尝试无果后,请放弃使用!")

        elif (choose == "3"):
            print("将文件移动到指定文件夹中")
            while True:
                print("文件夹名是文件名的子集，比如：（文件夹名：张三， 文件名：张三123.pdf）")
                try:
                    path = input("请输入你要操作的文件夹或者文件夹路径(输入0返回上一级):")
                    if path == "0":
                        break
                    file2dir(path)
                except Exception as e:
                    print(e)
                    print("输入有误, 请重新输入")

        elif (choose == "0"):
            print("程序已退出!")
            break
        else:
            print("输入有误, 请重新输入!")
            continue
    except Exception as e:
        print(e)
        print("发生了未知错误, 重新开始")







