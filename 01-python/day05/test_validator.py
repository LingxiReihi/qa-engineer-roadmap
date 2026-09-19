from utils import expect_type_error, un_require_type, require_type
from validator import *

if __name__ == '__main__':
    # region normalize_phone测试块

    normalize_phone_tc = {
        'case1': {
            'input': '13812345678',
            'output': '13812345678'
        },
        'case2': {
            'input': '138 1234 5678',
            'output': '13812345678'
        },
        'case3': {
            'input': '+8613812345678',
            'output': '13812345678'
        },
        'case4': {
            'input': '0086-138-1234-5678',
            'output': '13812345678'
        },
        'case5': {
            'input': '8613812345678',
            'output': '13812345678'
        },
        'case6': {
            'input': '23812345678',
            'output': ValueError
        },
        'case7': {
            'input': '12345',
            'output': ValueError
        },
        'case8': {
            'input': '',
            'output': ValueError
        },
        'case9': {
            'input': 13012345678,
            'output': TypeError
        }
    }
    assert normalize_phone(normalize_phone_tc['case1']['input']) == normalize_phone_tc['case1'][
        'output'], f"normalize_phone()测试用例1：'13812345678'，预期结果'13812345678'，测试不通过"
    assert normalize_phone(normalize_phone_tc['case2']['input']) == normalize_phone_tc['case2'][
        'output'], f"normalize_phone()测试用例2：'138 1234 5678'，预期结果'13812345678'，测试不通过"
    assert normalize_phone(normalize_phone_tc['case3']['input']) == normalize_phone_tc['case3'][
        'output'], f"normalize_phone()测试用例3：'+8613812345678'，预期结果'13812345678'，测试不通过"
    assert normalize_phone(normalize_phone_tc['case4']['input']) == normalize_phone_tc['case4'][
        'output'], f"normalize_phone()测试用例4：'0086-138-1234-5678'，预期结果'13812345678'，测试不通过"
    assert normalize_phone(normalize_phone_tc['case5']['input']) == normalize_phone_tc['case5'][
        'output'], f"normalize_phone()测试用例5：'8613812345678'，预期结果'13812345678'，测试不通过"
    expect_type_error(
        normalize_phone, normalize_phone_tc['case6']['input'],
        error_type=normalize_phone_tc['case6']['output'],
        label="normalize_phone测试用例6"
    )
    expect_type_error(
        normalize_phone, normalize_phone_tc['case7']['input'],
        error_type=normalize_phone_tc['case7']['output'],
        label="normalize_phone测试用例7"
    )
    expect_type_error(
        normalize_phone, normalize_phone_tc['case8']['input'],
        error_type=normalize_phone_tc['case8']['output'],
        label="normalize_phone测试用例8"
    )
    expect_type_error(
        normalize_phone, normalize_phone_tc['case9']['input'],
        error_type=normalize_phone_tc['case9']['output'],
        label="normalize_phone测试用例9"
    )
    assert normalize_phone(normalize_phone("+86-130-5555-6666")) == normalize_phone(
        "+86-130-5555-6666"), "normalize_phone()测试用例10：'+86-130-5555-6666'，测试不通过"

    # endregion

    # region mask_phone测试块

    mask_phone_tc = {
        'case1': {
            'input': '13812345678',
            'output': '138****5678'
        },
        'case2': {
            'input': '138 1234 5678',
            'output': '138****5678'
        },
        'case3': {
            'input': 'abc',
            'output': ValueError
        },
        'case4': {
            'input': '238 1234 5678',
            'output': ValueError
        },
        'case5': {
            'input': 123456,
            'output': TypeError
        },
        'case6': {
            'input': '1234567891',
            'output': ValueError
        }
    }
    assert mask_phone(mask_phone_tc['case1']['input']) == mask_phone_tc['case1'][
        'output'], f"mask_phone()测试用例1：'13812345678'，预期结果'138****5678'，测试不通过"
    assert mask_phone(mask_phone_tc['case2']['input']) == mask_phone_tc['case2'][
        'output'], f"mask_phone()测试用例2：'138 1234 5678'，预期结果'138****5678'，测试不通过"
    expect_type_error(
        mask_phone, mask_phone_tc['case3']['input'],
        error_type=mask_phone_tc['case3']['output'],
        label="mask_phone测试用例3"
    )
    expect_type_error(
        mask_phone, mask_phone_tc['case4']['input'],
        error_type=mask_phone_tc['case4']['output'],
        label="mask_phone测试用例4"
    )
    expect_type_error(
        mask_phone, mask_phone_tc['case5']['input'],
        error_type=mask_phone_tc['case5']['output'],
        label="mask_phone测试用例5"
    )
    expect_type_error(
        mask_phone, mask_phone_tc['case6']['input'],
        error_type=mask_phone_tc['case6']['output'],
        label="mask_phone测试用例6"
    )
    # endregion

    # region validate_password测试块
    assert validate_password("Abc12345-") == [], 'validate_password()测试用例1："Abc12345-"，测试不通过'
    assert validate_password("abcdefgh") == ['需要包含至少一个大写字母', '需要包含至少一个数字',
                                             '需要包含至少一种非字母数字符号'], 'validate_password()测试用例2："abcdefgh"，测试不通过'
    assert validate_password("A1") == ['长度需要大于等于8',
                                       '需要包含至少一种非字母数字符号'], 'validate_password()测试用例3："A1"，测试不通过'
    assert validate_password("abcdefghi1.") == [
        '需要包含至少一个大写字母'], 'validate_password()测试用例4："abcdefghi1."，测试不通过'
    assert validate_password("A") == ['长度需要大于等于8', '需要包含至少一个数字',
                                      '需要包含至少一种非字母数字符号'], 'validate_password()测试用例5："A"，测试不通过'
    expect_type_error(validate_password, 123, error_type=TypeError, label="validate_password()测试用例6")
    assert validate_password("Abc12345_") == [], 'validate_password()测试用例7："Abc12345_"，测试不通过'
    assert validate_password("Abc123_") == ['长度需要大于等于8'], 'validate_password()测试用例8："Abc123_"，测试不通过'
    # endregion

    # region parse_score测试块

    assert parse_score("95") == 95, 'parse_score()测试用例1："95"，测试不通过'
    assert parse_score("95分") == 95, 'parse_score()测试用例2："95分"，测试不通过'
    assert parse_score("95/100") == 95, 'parse_score()测试用例3："95/100"，测试不通过'
    assert parse_score("0") == 0, 'parse_score()测试用例4："0"，测试不通过'
    assert parse_score("100") == 100, 'parse_score()测试用例5："100"，测试不通过'
    expect_type_error(parse_score, "101", error_type=ValueError, label="parse_score()测试用例6")
    expect_type_error(parse_score, "-1", error_type=ValueError, label="parse_score()测试用例7")
    expect_type_error(parse_score, "95/90", error_type=ValueError, label="parse_score()测试用例8")
    expect_type_error(parse_score, 100, error_type=TypeError, label="parse_score()测试用例9")
    expect_type_error(parse_score, "95/", error_type=ValueError, label="parse_score()测试用例10")
    expect_type_error(parse_score, "/", error_type=ValueError, label="parse_score()测试用例11")
    expect_type_error(parse_score, "分", error_type=ValueError, label="parse_score()测试用例12")
    expect_type_error(parse_score, "95分/100", error_type=ValueError, label="parse_score()测试用例13")
    expect_type_error(parse_score, "95//100", error_type=ValueError, label="parse_score()测试用例14")

    # endregion

    # region un_require_type, require_type 测试
    assert un_require_type("123", "321", match_type=str, not_match_type=int) == False, "un_require_type测试用例1，测试失败"
    assert un_require_type("123", 321, match_type=str) == True, "un_require_type测试用例2，测试失败"

    assert require_type("123", "321", match_type=str, not_match_type=int) == True, "require_type测试用例1，测试失败"
    assert require_type("123", 321, match_type=str) == False, "require_type测试用例2，测试失败"
    # endregion

    print("validator 包全部通过")
# mask_phone 的返回值可以看作哨兵值，当他出问题时，如果函数直接报错，能够直接定位到问题所在，
# 而如果返回的是失败的空串，则需要调用方进行bug防御编程，将会很难定位到问题所在
