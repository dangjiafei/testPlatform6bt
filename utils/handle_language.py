import locale


def handle_language():
    # 设置简体中文
    locale.setlocale(locale.LC_CTYPE, 'chinese')
