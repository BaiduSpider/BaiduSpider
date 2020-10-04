from unittest import TestLoader, TextTestRunner

def run_tests():
    """运行所有单元测试
    
    此函数将会自动运行所有位于`tests`文件夹内的单元测试
    """
    # 检测所有测试
    tests = TestLoader().discover('./tests')
    # 运行测试
    TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    run_tests()
