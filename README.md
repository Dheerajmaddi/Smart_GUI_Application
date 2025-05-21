# SMART ATTENDANCE GUI APPLICATION

## Execution Instructions

1. **Open** the `Smart_GUI_Application` folder in your IDE.
2. **Install MySQL** on your system.
3. **Install required Python modules** for the application:
   ```sh
   pip install -r requirements.txt
   ```
4. **Run the main file** `app.py` to start the application, or open the terminal and enter:
   ```sh
   python app.py
   ```

---

## Application Walkthrough

### Register a Student

- Enter the details on the home page and click the **Register** button.
- An image of the student will be captured automatically.
- The student receives a successful registration email.

---

### Attendance (Automatic and Manual)

- Enter the subject name and click the **Fill Attendance** button.
- For face-recognized attendance, details will be saved automatically.
- For manual attendance, details should be entered by the admin.
- Students will get notified via email regarding their attendance.