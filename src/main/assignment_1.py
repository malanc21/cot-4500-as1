from decimal import Decimal
import sympy
from sympy import sympify


def append_64_bit(binary_string):
    number_to_append = 64 - len(binary_string)
    new_binary = binary_string + ('0' * number_to_append)
    return new_binary


def double_precision(binary_string):
    sign = Decimal(binary_string[0])

    exponent = Decimal(0)
    for index in range(1, 12):
        exponent = Decimal(exponent) + (Decimal(binary_string[index]) * 2**(11 - index))

    mantisa = Decimal(0)
    for index in range(12, 64):
        mantisa = Decimal(mantisa) + (Decimal(binary_string[index])) * Decimal((1/2)**(index - 11))

    answer = Decimal(((-1)**sign)*(2**(exponent-1023))*(1+mantisa))

    return answer


def digit_chopping(number_to_chop, digit):
    # Remove unnecessary 0s before number
    number_to_chop = str(number_to_chop)
    for i in number_to_chop:
        if i == "0":
            number_to_chop = number_to_chop[1:]
        elif i != "0":
            break

    number_to_chop = Decimal(number_to_chop)

    # convert to scientific notation
        # multipy scientific notation by 10^-1 to get normalized decimal floating point
    scientific_notation = "{:e}".format(number_to_chop)
    e_index = int((scientific_notation.find('e')))

    # Find what power 10 is to for normalized answer
    power_of_10 = Decimal(scientific_notation[(e_index + 1):]) + Decimal(1)
    normalized_decimal_w_out_10_factor = Decimal(scientific_notation[: e_index]) * Decimal(10**(-1))

    normalized_decimal_w_out_10_factor = str(normalized_decimal_w_out_10_factor)
    if Decimal(normalized_decimal_w_out_10_factor) >= 0:
        chopped_decimal = normalized_decimal_w_out_10_factor[:digit + 2]
    elif Decimal(normalized_decimal_w_out_10_factor) < 0:
        chopped_decimal = normalized_decimal_w_out_10_factor[:digit + 3]
    chopped_decimal = Decimal(chopped_decimal)

    answer = chopped_decimal * 10**power_of_10
    answer = float(format(answer, '.1f'))

    return answer


def digit_rounding(number_to_round, digit):
    # Remove unnecessary 0s before number
    number_to_round = str(number_to_round)
    for i in number_to_round:
        if i == "0":
            number_to_round = number_to_round[1:]
        elif i != "0":
            break

    number_to_round = Decimal(number_to_round)

    # convert to scientific notation
        # multipy scientific notation by 10^-1 for normalized decimal floating point
    scientific_notation = "{:e}".format(number_to_round)
    e_index = int((scientific_notation.find('e')))

    # Find what power 10 is to for normalized answer
    power_of_10 = Decimal(scientific_notation[(e_index + 1):]) + Decimal(1)
    normalized_decimal_w_out_10_factor = Decimal(scientific_notation[: e_index]) * Decimal(10 ** (-1))

    format_spec = '.' + str(digit) + 'f'
    rounded_decimal = format(normalized_decimal_w_out_10_factor, format_spec)
    rounded_decimal = Decimal(rounded_decimal)

    answer = Decimal(rounded_decimal * 10 ** power_of_10)

    return answer


def absolute_error(exact, rounded):
    absolute_error = Decimal(abs(exact - rounded))
    return absolute_error


def relative_error(exact, rounded):
    relative_error = abs(exact - rounded) / abs(exact)
    return relative_error


def check_for_alternating(function_we_got):
    term_check = check_for_negative_1_exponent_term(function_we_got)
    return term_check


def check_for_negative_1_exponent_term(function_we_got) -> bool:
    if "-1**k" in function_we_got:
        return True
    return False


def check_for_decreasing(function_we_got, x):
    decreasing_check = True
    k = 1
    starting_val = abs(eval(function_we_got))
    for k in range(1, 75):
        result = abs(eval(function_we_got))

        if starting_val > result:
            decreasing_check = True

    return decreasing_check


def minimum_terms(error):
    counter = 0
    # new_function = 1 / (counter + 1)**3
    while (1 / (counter + 1)**3) >= error:
        counter = counter + 1

    print(str(counter) + "\n")


def eval_function(given_function, eval_at):
    given_function = sympify(given_function, evaluate=False)
    x = sympy.Symbol('x')
    expression_eval = given_function.subs(x, eval_at)
    return expression_eval


def bisection_method(left, right, given_function, tolerance):
    initial_left = eval_function(given_function, left)
    initial_right = eval_function(given_function, right)

    # Verify bounds are on opposite sides of function
    if initial_left * initial_right >= 0:
        print("Invalid inputs. Not on opposite sides of the function")
        return

    iteration_counter = 0
    while right - left >= tolerance:

        # Find the midpoint
        midpoint = (left + right) / 2

        # Check if the midpoint is a root
        if eval_function(given_function, midpoint) == 0.0:
            break

        # Repeat steps adjusting ends if midpoint is not a root
        if eval_function(given_function, midpoint) * eval_function(given_function, left) < 0:
            right = midpoint
        else:
            left = midpoint
        iteration_counter = iteration_counter + 1

    print(str(iteration_counter) + "\n")


def evaluate_f(expression, initial_approximation):
    x = sympy.Symbol('x')
    expression_eval = expression.subs(x, initial_approximation)
    return expression_eval


def evaluate_derivative(expression, initial_approximation):
    x = sympy.Symbol('x')
    f_prime_eval = sympy.diff(expression, x, 1).evalf(subs={x: initial_approximation})
    return f_prime_eval


def newton_raphson(initial_approximation, tolerance, given_factor):
    iteration_counter = 0

    # finds f
    string_as_expression = sympify(given_factor, evaluate=False)
    f = evaluate_f(string_as_expression, initial_approximation)

    # finds f'
    f_prime = evaluate_derivative(string_as_expression, initial_approximation)

    approximation: float = f / f_prime
    while abs(approximation) >= tolerance:
        # finds f
        f = evaluate_f(string_as_expression, initial_approximation)

        # finds f'
        f_prime = evaluate_derivative(string_as_expression, initial_approximation)

        approximation = f / f_prime
        initial_approximation -= approximation
        iteration_counter += 1

    print(str(iteration_counter) + "\n")


def main():
    # QUESTION 1
    binary_string = "010000000111111010111001"
    new_binary = append_64_bit(binary_string)
    decimal_places = 4
    answer = double_precision(new_binary)
    format_spec = '.' + str(decimal_places) + 'f'
    print(format(answer, format_spec) + "\n")

    # QUESTION 2
    chopped_digit = digit_chopping(answer, 3)
    print(str(chopped_digit) + "\n")

    # QUESTION 3
    rounded_digit = digit_rounding(answer, 3)
    print(format(rounded_digit, '.1f') + "\n")
    rounded_digit = Decimal(rounded_digit)

    # QUESTION 4
    answer = Decimal(answer)
    absolute = absolute_error(answer, rounded_digit)
    print(format(absolute, '.4f'))

    relative = relative_error(answer, rounded_digit)
    print(str(relative) + "\n")

    # QUESTION 5
    # Pre reqs
    function = "(-1**k) * (x**k) / (k**3)"
    x: int = 1
    check1: bool = check_for_alternating(function)
    check2: bool = check_for_decreasing(function, x)

    error = 10**(-4)
    if check1 and check2:
        minimum_terms(error)

    # QUESTION 6
    # PART A BISECTION METHOD
    left = -4
    right = 7
    function_string = "x**3 + (4*(x**2)) - 10"
    accuracy = .0001
    bisection_method(left, right, function_string, accuracy)

    # PART B NEWTON RAPHSON METHOD
    initial_approximation = -4
    newton_raphson(initial_approximation, accuracy, function_string)


if __name__ == '__main__':
    main()
