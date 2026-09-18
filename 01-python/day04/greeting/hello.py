def say_hi(name: str) -> str:
    return f'hi, {name}'


def say_bye(name: str) -> str:
    return f'bye, {name}'


if __name__ == '__main__':
    assert say_hi("tester") == "hi"
