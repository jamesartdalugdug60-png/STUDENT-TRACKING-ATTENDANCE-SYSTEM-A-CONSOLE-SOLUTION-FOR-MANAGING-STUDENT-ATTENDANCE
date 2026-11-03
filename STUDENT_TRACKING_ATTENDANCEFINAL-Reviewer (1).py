"""
=====================================================================
 STUDENT TRACKING ATTENDANCE SYSTEM (Teacher/Student roles)
 - Student ID: numbers only
 - Student name: letters only
 - Student portal shows: Status: Present / Status: Absent
=====================================================================
"""

# ---------------- DATA STRUCTURES ----------------
students = []                 # list of [student_id, name]
attendance_records = []       # list of [student_id, status]

VALID_STATUSES = ["Present", "Absent"]

TEACHER_PASSWORD = "Educ4"   # exact password required to enter the Teacher menu


# ---------------- STUDENT REGISTRATION ----------------
def register_student(student_id, name):
    """Registers a new student. Blocks duplicate IDs."""
    for record in students:
        if record[0] == student_id:
            print(f"\n[ERROR] Student ID {student_id} already exists. Registration blocked.")
            return False

    students.append([student_id, name])
    print(f"\n[SUCCESS] Student {name} (ID: {student_id}) registered.")
    return True


# ---------------- RECORD ATTENDANCE ----------------
def record_attendance(student_id, status):
    """Records attendance for a registered student.

    If the student already has a record, it updates the status instead.
    """
    if find_student(student_id) is None:
        print(f"\n[ERROR] Student ID {student_id} is not registered.")
        return False

    if status not in VALID_STATUSES:
        print(f"\n[ERROR] Invalid status. Use one of: {', '.join(VALID_STATUSES)}")
        return False

    for record in attendance_records:
        if record[0] == student_id:
            old_status = record[1]
            record[1] = status
            print(f"\n[SUCCESS] Attendance updated: {student_id} | {old_status} -> {status}")
            return True

    attendance_records.append([student_id, status])
    print(f"\n[SUCCESS] Attendance recorded: {student_id} | {status}")
    return True


# ---------------- FIND ----------------
def find_student(student_id):
    """Returns the student record matching the ID, or None."""
    for record in students:
        if record[0] == student_id:
            return record
    return None


# ---------------- STUDENT: VIEW OWN ATTENDANCE ----------------
def view_student_attendance(student_id):
    """Shows a student's ID, name, and their attendance status."""
    student = find_student(student_id)
    if student is None:
        print(f"\n[ERROR] Student ID {student_id} is not registered.")
        return

    print(f"\nSTUDENT ID : {student[0]}")
    print(f"NAME       : {student[1]}")
    print("-" * 40)

    found = False
    for record in attendance_records:
        if record[0] == student_id:
            print(f"Status: {record[1]}")
            found = True

    if not found:
        print("No attendance record yet.")


# ---------------- TEACHER: ATTENDANCE REPORT ----------------
def display_attendance_report():
    """Summary report of Present/Absent for every student."""
    print("\n" + "=" * 56)
    print("ATTENDANCE SUMMARY REPORT")
    print("=" * 56)
    print(f"{'STUDENT ID':<12}{'NAME':<22}{'STATUS':<10}")
    print("-" * 56)

    for student in students:
        sid, name = student[0], student[1]
        status_text = "-"
        for record in attendance_records:
            if record[0] == sid:
                status_text = record[1]
        print(f"{sid:<12}{name:<22}{status_text:<10}")

    print("-" * 56)


# ---------------- INPUT VALIDATION ----------------
def get_choice(prompt, valid_options):
    """Repeatedly asks for input until it matches a valid option."""
    while True:
        value = input(prompt).strip()
        for option in valid_options:
            if value.lower() == option.lower():
                return option
        print(f"[ERROR] Invalid choice. Please enter one of: {', '.join(valid_options)}")


def get_status(prompt):
    """Asks for an attendance status (Present or Absent only)."""
    return get_choice(prompt, VALID_STATUSES)


def get_valid_id(prompt):
    """Asks for a Student ID that contains numbers only."""
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return value
        print("[ERROR] Student ID must contain numbers only. No letters or symbols.")


def get_valid_name(prompt):
    """Asks for a Student Name that contains letters only (spaces and periods allowed for initials)."""
    while True:
        value = input(prompt).strip()
        cleaned = value.replace(" ", "").replace(".", "").replace("-", "")
        if value and cleaned.isalpha():
            return value
        print("[ERROR] Student name must contain letters only. No numbers or symbols.")


def check_teacher_password():
    """Asks for the teacher password.

    Returns True only if the password matches EXACTLY (case-sensitive).
    The user gets 3 attempts before being sent back to the main menu.
    """
    for attempt in range(3):
        password = input("Enter Teacher Password: ").strip()
        if password == TEACHER_PASSWORD:
            print("\n[SUCCESS] Access granted. Welcome, Teacher!")
            return True
        remaining = 2 - attempt
        if remaining > 0:
            print(f"[ERROR] Wrong password. Attempts left: {remaining}")
        else:
            print("[ERROR] Too many failed attempts. Returning to main menu.")
    return False


# ---------------- MENUS ----------------
def display_role_menu():
    print("\n" + "=" * 50)
    print(" STUDENT TRACKING ATTENDANCE SYSTEM")
    print("=" * 50)
    print(" Are you a Teacher or a Student?")
    print(" [1] Teacher")
    print(" [2] Student")
    print(" [3] Exit")
    print("=" * 50)


def teacher_menu():
    while True:
        print("\n" + "-" * 50)
        print(" TEACHER MENU")
        print("-" * 50)
        print(" [1] Register Student")
        print(" [2] Record Attendance")
        print(" [3] Attendance Report")
        print(" [4] Back to Main Menu")
        print("-" * 50)
        choice = get_choice("Select an option [1-4]: ", ["1", "2", "3", "4"])

        if choice == "1":
            while True:
                student_id = get_valid_id("Enter Student ID: ")
                if find_student(student_id) is None:
                    break
                print(f"\n[ERROR] Student ID {student_id} already exists. Please enter a different ID.")
            name = get_valid_name("Enter Student Name: ")
            register_student(student_id, name)

        elif choice == "2":
            student_id = get_valid_id("Enter Student ID: ")
            status = get_status("Enter Status (Present/Absent): ")
            record_attendance(student_id, status)

        elif choice == "3":
            display_attendance_report()

        elif choice == "4":
            return


def student_menu():
    """Students can ONLY view their own attendance by entering their ID."""
    print("\n" + "-" * 50)
    print(" STUDENT PORTAL")
    print("-" * 50)
    student_id = get_valid_id("Enter your Student ID: ")
    view_student_attendance(student_id)


def main():
    """Main program: role selection first, then role-specific menus."""
    while True:
        display_role_menu()
        choice = get_choice("Select an option [1-3]: ", ["1", "2", "3"])

        if choice == "1":
            if check_teacher_password():
                teacher_menu()

        elif choice == "2":
            student_menu()

        elif choice == "3":
            print("\nThank you for using the Student Tracking Attendance System. Goodbye!")
            break


# ---------------- SAMPLE DATA ----------------
def load_sample_data():
    students.append(["1001", "Ali Racman"])
    students.append(["1002", "K-mark Priela"])
    students.append(["1003", "Benjie Albesa"])
    students.append(["1004", "James Art Dalugdug"])
    students.append(["1005", "Troy John Molato"])
    students.append(["1006", "Jomel Pitre"])
    students.append(["1007", "El Jhon Seguis"])
    attendance_records.append(["1001", "Present"])
    attendance_records.append(["1002", "Absent"])
    attendance_records.append(["1003", "Present"])
    attendance_records.append(["1004", "Present"])
    attendance_records.append(["1005", "Absent"])
    attendance_records.append(["1006", "Present"])
    attendance_records.append(["1007", "Present"])


# ---------------- ENTRY POINT ----------------
if __name__ == "__main__":
    load_sample_data()
    main()