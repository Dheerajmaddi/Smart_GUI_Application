import smtplib

my_email = "planningmanagement4@gmail.com"
paswrd = "sjcr jrjf rklj fwnx"


def registration_succesful(to_address):
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=my_email, password=paswrd)
    connection.sendmail(
        from_addr=my_email,
        to_addrs=to_address,
        msg="Subject: Registratin Succesfull!!!\n\nThank you registering Smart GUI Application.")
    connection.close()


def attendance_confirmation(to_address):
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=my_email, password=paswrd)
    connection.sendmail(
        from_addr=my_email,
        to_addrs=to_address,
        msg="Subject: Attendance Succesfull!!!\n\nAttendance captured. Happy learning!!!.")
    connection.close()
