import basic3

while True:
    text = input('input > ')
    result, error = basic3.run('<stdin>', text)

    if error: print(error.as_string())
    else: print(result)