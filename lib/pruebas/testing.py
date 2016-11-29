_failure_count = 0

def print_exception(function, exception, mensaje, *args):
    try:
        function(*args)
    except exception:
        print_test(mensaje, True)
    else:
        print_test(mensaje, False)

def print_test(mensaje, ok):
    global _failure_count
    _failure_count += 0 if ok else 1
    print("{}... {}".format(mensaje, "OK" if ok else "ERROR"))

def failure_count():
    return _failure_count;
