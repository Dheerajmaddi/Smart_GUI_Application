import csv
import os


def has_data(filename):
    """Returns True if the file has data, False otherwise."""

    file_size = os.path.getsize(filename)
    if file_size == 0:
        return False

    with open(filename, "r") as f:
        first_line = f.readline()
        if first_line == "":
            return False

    return True


def is_student_registered(enrollment, name):
    # Check if the student is already registered in the CSV file
    with open('StudentDetails\StudentDetails.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # print(enrollment)
            if row and row[0] == enrollment and row[1] == name:
                return True
    return False


def save_to_csv(student_data):
    """Saves the user's details to CSV."""

    with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        writer.writerow(student_data)
