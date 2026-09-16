def ptp(data):
    """
    计算极差（全距）
    :param data:  数据
    :return:  极差
    """
    """极差（全距）"""
    return max(data) - min(data)


def mean(data):
    """
    计算算术平均
    :param data:  数据
    :return:  算术平均
    """
    return sum(data) / len(data)


def median(data):
    """
    计算中位数
    :param data:  数据
    :return:  中位数
    """
    temp, size = sorted(data), len(data)
    if size % 2 != 0:
        return temp[size // 2]
    else:
        return mean(temp[size // 2 - 1:size // 2 + 1])


def var(data, ddof=1):
    """
    计算方差
    :param data:  数据
    :param ddof:  自由度
    :return:  方差
    """
    x_bar = mean(data)
    temp = [(num - x_bar) ** 2 for num in data]
    return sum(temp) / (len(temp) - ddof)


def std(data, ddof=1):
    """
    计算标准差
    :param data:  数据
    :param ddof:  自由度
    :return:  标准差
    """
    return var(data, ddof) ** 0.5


def cv(data, ddof=1):
    """
    计算变异系数
    :param data:  数据
    :param ddof:  自由度
    :return:  变异系数
    """
    return std(data, ddof) / mean(data)


def describe(data):
    """
    输出描述性统计信息
    :param data:  数据
    :return:  描述性统计信息
    """
    print(f'均值: {mean(data)}')
    print(f'中位数: {median(data)}')
    print(f'极差: {ptp(data)}')
    print(f'方差: {var(data)}')
    print(f'标准差: {std(data)}')
    print(f'变异系数: {cv(data)}')
