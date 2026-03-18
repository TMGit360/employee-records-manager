def format_name(lastname, firstname):
    return f"{lastname.title()}, {firstname.title()}"


def normalize_name(name_text):
    return name_text.strip().title()


def format_salary(amount):
    return f"${amount:,.2f}"


def parse_salary(salary_text):
    cleaned = salary_text.strip().replace("$", "").replace(",", "")

    try:
        salary = float(cleaned)
        if salary < 0:
            return None
        return salary
    except ValueError:
        return None


def display_error(message):
    print(f"❌ {message}\n")


def confirm_choice(prompt):
    while True:
        choice = input(prompt).strip().lower()
        if choice in ("y", "yes"):
            return True
        elif choice in ("n", "no"):
            return False
        else:
            display_error("Please enter Y or N. Example: Y")


def display_menu():
    print("EMPLOYEE MANAGEMENT SYSTEM")
    print("--------------------------\n")

    print(
        "V - View All Employees      "
        "A - Add Employee           "
        "U - Update Salary"
    )

    print(
        "S - View Single Employee    "
        "D - Delete Employee        "
        "Q - Quit"
    )

    print()


def get_menu_choice():
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip().lower()
        print()

        if choice in ("v", "s", "a", "d", "u", "q"):
            return choice
        else:
            display_error("Invalid choice. Please enter V, S, A, D, U, or Q. Example: V")


def get_name_input(action_text):
    while True:
        lastname = input(f"Enter the employee's last name for {action_text}: ").strip()
        firstname = input(f"Enter the employee's first name for {action_text}: ").strip()

        if lastname == "" or firstname == "":
            display_error("Please enter both a first and last name.")
            continue

        print()
        return normalize_name(lastname), normalize_name(firstname)


def get_salary_input():
    while True:
        salary_text = input(
            "Enter the employee salary (example: 85000, 85000.50, or $85,000.50): "
        ).strip()

        salary = parse_salary(salary_text)

        if salary is None:
            display_error(
                "Invalid salary format. Please enter a valid number. Example: $85,000.50"
            )
            continue

        return salary


def load_dict(filename):
    employee_dict = {}

    with open(filename, "r") as infile:
        for line in infile:
            line = line.rstrip("\n")

            if line == "":
                continue

            employee_list = line.split("*")

            if len(employee_list) != 3:
                continue

            lastname = normalize_name(employee_list[0])
            firstname = normalize_name(employee_list[1])
            salary = parse_salary(employee_list[2])

            if salary is None:
                continue

            fullname = lastname + " " + firstname
            employee_dict[fullname] = salary

    return employee_dict


def save_dict(filename, employee_dict):
    sorted_items = sorted(
        employee_dict.items(),
        key=lambda item: (
            item[0].split()[0].lower(),
            item[0].split()[1].lower(),
            item[1]
        )
    )

    with open(filename, "w") as outfile:
        for fullname, salary in sorted_items:
            lastname, firstname = fullname.split(" ", 1)
            outfile.write(f"{lastname}*{firstname}*{salary:.1f}\n")


def show_all_employees(employee_dict):
    if not employee_dict:
        print("No employees found.\n")
        return

    sorted_items = sorted(
        employee_dict.items(),
        key=lambda item: (
            item[0].split()[0].lower(),
            item[0].split()[1].lower(),
            item[1]
        )
    )

    count = 1
    for fullname, salary in sorted_items:
        lastname, firstname = fullname.split(" ", 1)
        print(f"{count}. {format_name(lastname, firstname)} {format_salary(salary)}")
        count += 1
    print()


def show_single_employee(employee_dict):
    lastname, firstname = get_name_input("search")
    fullname = lastname + " " + firstname

    if fullname in employee_dict:
        salary = employee_dict[fullname]
        print(
            "Last: " + lastname +
            "\n" + "First: " + firstname +
            "\n" + "Salary: " + format_salary(salary) + "\n"
        )
    else:
        display_error("Employee not found. Example: Smith and John")


def add_employee(employee_dict):
    lastname, firstname = get_name_input("adding")
    fullname = lastname + " " + firstname

    if fullname in employee_dict:
        display_error("That employee already exists. Use Update Salary instead.")
        return

    salary = get_salary_input()

    print(f"\nNew employee: {format_name(lastname, firstname)} {format_salary(salary)}")
    if confirm_choice("Add this employee? (Y/N): "):
        employee_dict[fullname] = salary
        print("Employee added successfully.\n")
    else:
        print("Add cancelled.\n")


def delete_employee(employee_dict):
    lastname, firstname = get_name_input("deletion")
    fullname = lastname + " " + firstname

    if fullname not in employee_dict:
        display_error("Employee not found. Example: Smith and John")
        return

    print(f"Employee found: {format_name(lastname, firstname)} {format_salary(employee_dict[fullname])}")
    if confirm_choice("Delete this employee? (Y/N): "):
        del employee_dict[fullname]
        print("Employee deleted successfully.\n")
    else:
        print("Delete cancelled.\n")


def update_employee_salary(employee_dict):
    lastname, firstname = get_name_input("salary update")
    fullname = lastname + " " + firstname

    if fullname not in employee_dict:
        display_error("Employee not found. Example: Smith and John")
        return

    print(
        f"Current salary for {format_name(lastname, firstname)} is "
        f"{format_salary(employee_dict[fullname])}\n"
    )

    new_salary = get_salary_input()

    print(
        f"\nUpdate salary for {format_name(lastname, firstname)} "
        f"to {format_salary(new_salary)}?"
    )
    if confirm_choice("(Y/N): "):
        employee_dict[fullname] = new_salary
        print("Employee salary updated successfully.\n")
    else:
        print("Update cancelled.\n")


def view_dict(employee_dict, filename):
    while True:
        check_view = get_menu_choice()

        if check_view == "v":
            show_all_employees(employee_dict)

        elif check_view == "s":
            show_single_employee(employee_dict)

        elif check_view == "a":
            add_employee(employee_dict)
            save_dict(filename, employee_dict)

        elif check_view == "d":
            delete_employee(employee_dict)
            save_dict(filename, employee_dict)

        elif check_view == "u":
            update_employee_salary(employee_dict)
            save_dict(filename, employee_dict)

        elif check_view == "q":
            print("End of Program")
            break


def main():


    while True:
        filename = "employee.txt"

        try:
            response_dict = load_dict(filename)
            view_dict(response_dict, filename)
            break

        except FileNotFoundError:
            display_error("File could not be found. Example: employee.txt")
            break


if __name__ == "__main__":
    main()