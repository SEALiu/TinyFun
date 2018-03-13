import os

# 批量修改文件后缀
if __name__ == '__main__':
    path = "."
    for file in os.listdir(path):
        if file[-6:] != "BZDmp4":
        	continue

        os.rename(file, file[:-6]+"mp4")
