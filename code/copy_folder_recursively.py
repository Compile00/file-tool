# 递归地复制文件夹

import shutil
import os

# source_folder = 'E:\保存python文件\停息日期登记\excel'   # 待复制的文件夹
# destination_folder = 'E:\保存python文件\停息日期登记\destination'  #目的文件夹


def folder_recursively(source, destination):
  # 统计总文件数量
  total_files = 0
  # 只需要root路径和files文件列表,不需要dirs子文件夹列表。所以使用_作为变量名占位,表示这个元素不会在循环中使用。
  # Python语言允许我们用_来作为不需要的变量名占位符,表示对这个变量不做处理。
  for root, _, files in os.walk(source_folder):
      total_files += len(files)

  # 打印总文件数
  print(f'总文件数量为: {total_files}')

  # 当前复制文件数量
  copied_files = 0

  try:
    # 递归遍历源文件夹
    for root, dirs, files in os.walk(source_folder):

      # 遍历所有文件
      for file in files:

        # 构造源文件的完整路径
        src_file = os.path.join(root, file)

        # 直接使用源文件名作为目标文件名
        dest_file = os.path.join(destination_folder, file)

        # 复制文件
        shutil.copy(src_file, dest_file)
        # 打印进度
        copied_files += 1
        print(f'已经复制 {copied_files}/{total_files} 文件', end='\r')

    print('\n完成!')
  except OSError as e:
    print(e)
    print("检查是否已经复制过文件到目标文件夹")



while True:
  try:
    source_folder = input("请输入要操作的文件夹, 将提取该文件夹下的所有文件(包括嵌套文件夹中的文件), 输入0退出\n")
    if source_folder == '0':
      break
    destination_folder = input("请输入要将提取到的文件复制到指定的文件夹\n")

    folder_recursively(source_folder, destination_folder)

  except Exception as e:
    print(e)
    print("发生了未知错误, 请重新输入, 注意可能是要搜索的文件不符合该系统的查找规则, 多次尝试无果后,请放弃使用!")