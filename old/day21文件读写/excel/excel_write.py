import random
import xlwt

student_name = ["小明", "小红", "张三", "李四", "王五"]
scores = [[random.randint(50, 101) for _ in range(3)] for _ in range(len(student_name))]

# 创建工作簿对象(Workbook)
wb = xlwt.Workbook()

# 创建工作表对象(sheet)
sheet = wb.add_sheet('三年级五班')

# 创建表头
titles = ('姓名', '语文', '数学', '英语')
# 写入表头
for index, titles in enumerate(titles):
    sheet.write(0, index, titles)

# 写入数据
# 写入学生姓名
for row in range(len(scores)):
    sheet.write(row + 1, 0, student_name[row])
    # 写入学生成绩
    for col in range(len(scores[row])):
        sheet.write(row + 1, col + 1, scores[row][col])

# 保存工作簿
wb.save('成绩表.xls')
