class Person:
    """Person class"""

    def __init__(self, name, age):
        self.name = name
        self.age = age


# @classmethod # 类方法/静态类
class Student(Person):  # 继承Person类
    """Student class"""

    __slot__ = ('name', 'age')  # 限制属性，将无法动态为该类添加属性，只能使用已定义的属性

    @staticmethod  # 静态方法
    def print_info():
        print("Student class")

    @property  # 属性装饰器
    def student_info(self):
        return f"Student {self.name} is {self.age} years old"

    def study(self, course_name):
        """
        study a course
        :param course_name:  name
        :return:  None
        """
        print(f"{self.name}正在学习{course_name}")


Student.print_info()

stu = Student("xiaoming", 18)
stu.study("Python")
print(stu.student_info)
