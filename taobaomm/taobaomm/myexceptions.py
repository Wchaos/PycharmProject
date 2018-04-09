"""
user-defined Exception
自定义异常
"""
class ExtractError(Exception):
    """提取页面元素时的异常"""

    def __init__(self, reason='can not find element'):
        super(ExtractError, self).__init__()
        self.reason = reason

