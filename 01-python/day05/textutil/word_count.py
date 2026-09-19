from utils import expect_type_error


def word_count(text: str) -> int:
    """
    统计中英混合文本的词数：英文按空格分隔，中文按字符计。
    :param text: 待处理字符串
    :return: 包含的词数
    :raise TypeError: word_count() 只接受 str
    """
    if isinstance(text, str):
        num = 0
        for v in text.split():
            if v.encode('utf-8').isalpha():
                num += 1
            else:
                num += len(v)
        return num
    else:
        raise TypeError(
            f"word_count() 只接受 str，实际收到 "
            f"text={text!r} ({type(text).__name__})"
        )


if __name__ == "__main__":
    assert word_count("hello 世界 abc") == 4, "word_count()测试用例1：\"hello 世界 abc\"，预期结果：4，测试未通过"
    assert word_count("hello") == 1, "word_count()测试用例2：\"hello\"，预期结果：1，测试未通过"
    assert word_count("世界") == 2, "word_count()测试用例3：\"世界\"，预期结果：2，测试未通过"
    assert word_count("") == 0, "word_count()测试用例4：\"\"，预期结果：0，测试未通过"
    assert word_count("  多个  空格  ") == 4, "word_count()测试用例5：\"  多个  空格  \"，预期结果：4，测试未通过"
    expect_type_error(word_count, 123, error_type=TypeError, label="word_count()测试用例6")
    print("textutil 包全部通过")
