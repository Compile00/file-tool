# 相似度类, 用于计算两个字符串的相似度
import os
import shutil
import difflib
class Sim:
    # Levenshtein距离
    def levenshtein_distance(self, str1, str2):
        """计算两个字符串之间的 Levenshtein 距离。

        Args:
          str1: 第一个字符串。
          str2: 第二个字符串。

        Returns:
          两个字符串之间的 Levenshtein 距离。
        """

        # 初始化动态规划表。
        n = len(str1) + 1
        m = len(str2) + 1
        d = [[0] * m for i in range(n)]

        # 填充动态规划表。
        for i in range(n):
            d[i][0] = i
        for j in range(m):
            d[0][j] = j
        for i in range(1, n):
            for j in range(1, m):
                if str1[i - 1] == str2[j - 1]:
                    d[i][j] = d[i - 1][j - 1]
                else:
                    d[i][j] = min(d[i - 1][j], d[i][j - 1], d[i - 1][j - 1]) + 1

        # 返回 Levenshtein 距离。
        return d[n - 1][m - 1]

    #计算相似度的值
    def similarity_ratio(self, str1, str2):
        """计算两个字符串的相似度比率。

        Args:
          str1: 第一个字符串。
          str2: 第二个字符串。

        Returns:
          两个字符串的相似度比率。
        """

        # 计算 Levenshtein 距离。
        distance = self.levenshtein_distance(str1, str2)

        # 计算相似度比率。
        similarity_ratio = 1 - distance / max(len(str1), len(str2))

        return similarity_ratio


    # 先打印出结果, 再返回cutoff值
    def printmessage(self,str1, str2):
        precent = self.similarity_ratio(str1, str2)
        rounded_number = round(precent, 2)  # 保留小数点后两位
        print(precent)
        print("{}和{}字符串的相似度为:{}%".format(str1,str2,rounded_number*100))
        print("cutoff的值为:{}".format(rounded_number))

        return rounded_number

    #直接返回cutoff值
    def out_cutoff(self,str1, str2):
        cutoff = self.similarity_ratio(str1, str2)
        rounded_number = round(cutoff, 2)  # 保留小数点后两位
        return rounded_number



# 按相似度匹配并移动

def diff(source_folder, num, simi):
    # 设置源文件夹和目标文件夹的路径
    source_folder = "test5"

    num = 1

    files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    folders = [d for d in os.listdir(source_folder) if os.path.isdir(os.path.join(source_folder, d))]

    print(files)
    print(folders)

    file_base = []
    for f in files:
        file_base.append(os.path.splitext(f)[0])
    print(file_base)

    # 遍历所有的文件夹名, 找出最合适的文件, 并放入其中
    for dirname in folders:
        # 找到最相似的文件夹名，使用0.5作为相似度阈值, n=1表示匹配出最符合的一个
        closest_match = difflib.get_close_matches(dirname, file_base, n=num, cutoff=simi)
        print("{}匹配到的{}".format(dirname, closest_match))

    # # 遍历源文件夹中的所有文件
    # for filename in files:
    #     # 获取文件名中除了扩展名的部分
    #     file_base = os.path.splitext(filename)[0]
    #     # print(file_base)
    #     # 获取目标文件夹中的所有文件夹名
    #     dest_subfolders = folders
    #     # 找到最相似的文件夹名，使用0.5作为相似度阈值, n=1表示匹配出最符合的一个
    #     closest_match = difflib.get_close_matches(file_base, dest_subfolders, n=1, cutoff=0.5)
    #     # closest_match = difflib.get_close_matches(dest_subfolders, file_base, n=1, cutoff=0.5)
    #
    #     print(closest_match)

    # 如果找到了相似的文件夹名，就移动文件
    # if closest_match:
    #     # 获取文件的完整路径
    #     source_path = os.path.join(source_folder, filename)
    #     # 获取目标路径
    #     dest_path = os.path.join(dest_folder, closest_match[0], filename)
    #     # 移动文件
    #     shutil.move(source_path, dest_path)

    print("执行完毕!")