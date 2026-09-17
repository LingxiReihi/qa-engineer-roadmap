from dataclasses import dataclass


@dataclass
class Options:
    bigger: str = "大了"
    smaller: str = "小了"
    correct: str = "恭喜你，猜对了！"
    error: str = "输入非法"


def compare(guess: int, target: int) -> str:
    if isinstance(guess, int) and isinstance(target, int):
        if guess > target:
            return Options.bigger
        elif guess < target:
            return Options.smaller
        else:
            return Options.correct
    return Options.error


assert compare(1, 2) == Options.smaller, f"compare测试用例1：(1, 2)，预期返回{Options.smaller}"
assert compare(100, 100) == Options.correct, f"compare测试用例2：(100, 100)，预期返回{Options.correct}"
assert compare("1", 1) == Options.error, f"compare测试用例3：(\"1\",1)，预期返回{Options.error}"


def guess_number(target: int, max_attempts: int = 5) -> bool:
    """让用户猜数字，返回是否在 max_attempts 次内猜中。"""
    while max_attempts > 0:
        guess = input(f"剩余{max_attempts}回合，请输入您猜的数字：")
        if guess.isdigit():
            guess = int(guess)
            res = compare(guess, target)
            if res == Options.correct:
                print(Options.correct)
                return True
            else:
                if res == Options.smaller:
                    print(Options.smaller)
                elif res == Options.bigger:
                    print(res)
                max_attempts -= 1
        else:
            print(Options.error)
    return False
