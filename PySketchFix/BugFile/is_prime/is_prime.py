def is_prime(number):
    if number == 0 or number == 1:
        return True
    for element in range(2, number):
        if number / element == 0:  # Fix number % element == 0
            return False
    return True
