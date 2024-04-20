class MyLog:
    @staticmethod
    def cout(debug_window, out):
        debug_window.append(str(out))
        print(out)

    @staticmethod
    def print_function_name(func):
        def wrapper(*args, **kwargs):
            #print(f"============The function name is {func.__name__}============")
            #print(*args)
            #print(**kwargs)
            return func(*args, **kwargs)
        return wrapper