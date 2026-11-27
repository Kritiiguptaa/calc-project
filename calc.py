"""Simple command-line calculator for UCS 745 Cloud and DevOps, Assignment Q1."""


# add: returns the sum of two numbers.
# How it works: takes the two values it is given and applies the + operator.
def add(a, b):
    return a + b


# subtract: returns the difference of two numbers (first minus second).
# How it works: applies the - operator to the two values, in the order given.
def subtract(a, b):
    return a - b


# multiply: returns the product of two numbers.
# How it works: applies the * operator to the two values.
def multiply(a, b):
    return a * b


# divide: returns the quotient of two numbers, guarding against division by zero.
# How it works: checks whether the divisor is zero first and returns an error
# message instead of crashing; otherwise it applies the / operator.
def divide(a, b):
    if b == 0:
        return "Error: cannot divide by zero"
    return a / b


# read_number: asks the user for one number and keeps asking until it gets one.
# How it works: loops on input(), tries to turn the text into a float, and on a
# ValueError prints a hint and loops again.
def read_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("That is not a number, please try again.")


# main: runs the interactive menu loop of the calculator.
# How it works: prints the five menu choices, reads one choice, collects the two
# operands when an operation was picked, calls the matching function and prints
# the result; choice 5 breaks out of the loop and ends the program.
def main():
    while True:
        print("\n--- Calculator ---")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "5":
            print("Goodbye!")
            break

        if choice not in ("1", "2", "3", "4"):
            print("Invalid option, please pick a number from 1 to 5.")
            continue

        a = read_number("Enter the first number: ")
        b = read_number("Enter the second number: ")

        if choice == "1":
            print("Result:", add(a, b))
        elif choice == "2":
            print("Result:", subtract(a, b))
        elif choice == "3":
            print("Result:", multiply(a, b))
        else:
            print("Result:", divide(a, b))


if __name__ == "__main__":
    main()
