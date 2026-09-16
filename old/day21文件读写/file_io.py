# file = open('致橡树.txt', 'r', encoding='utf-8')  # 打开文件
# print(file.read())  # 读取文件内容
# file.close()  # 关闭文件访问
#
# file = open('致橡树.txt', 'r', encoding='utf-8')  # 打开文件
# # 逐行读取文件内容
# for line in file:
#     print(line, end='')  # 取消末尾换行（原文件已换行，再次换行会导致输出多余空行）
# file.close()
#
# file = open('致橡树.txt', 'r', encoding='utf-8')  # 打开文件
# # 读取所有行并存储在列表中
# lines = file.readlines()
# for line in lines:
#     print(line, end='')
# file.close()
#
# file = open('致橡树.txt', 'a', encoding='utf-8')  # 打开文件
# file.write('\n标题：《致橡树》')  # 写入文件内容
# file.write('\n作者：舒婷')
# file.write('\n时间：1977年3月')
# file.close()

# file = None  # 初始化文件对象为None，表示文件未打开
# try:
#     file = open('致橡树.txt', 'r', encoding='utf-8')  # 打开文件
#     print(file.read())  # 读取文件内容
# except FileNotFoundError:  # 捕获文件未找到错误
#     print('无法打开指定的文件!')  # 输出错误信息
# except LookupError:  # 捕获编码错误
#     print('指定了未知的编码!')  # 输出错误信息
# except UnicodeDecodeError:  # 捕获解码错误
#     print('读取文件时解码错误!')  # 输出错误信息
# finally:
#     if file:
#         file.close()

try:
    with open('guido.jpg', 'rb') as file1, open('吉多.jpg', 'wb') as file2:  # 使用完成后自动关闭文件
        data = file1.read(512)  # 读取512字节数据
        # 循环读取数据并写入文件
        while data:  # 循环读取数据并写入文件
            file2.write(data)
            data = file1.read()  # 读取512字节数据
except FileNotFoundError:
    print('指定的文件无法打开.')
except IOError:
    print('读写文件时出现错误.')
print('程序执行结束.')
