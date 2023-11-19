import csv
import openpyxl


class Course:
    all_course = [] #To keep track of all the Course objects

    def __init__(self, name, exam_date):
        
        self.name = name
        self.exam_date = exam_date
        self.sections = []  # It will contain all Section objects of the respective course
        Course.all_course.append(self)

    def get_all_sections(self, lect = 0, tut = 0, lab = 0):
        

        for section in self.sections: #Print all sections of the course
            if lect == 0:
                if isinstance(section, Lecture):
                    print(f"Section Name: {section.name}, Days: {section.days}, Time: {section.time}, Instructor: {section.instructor}") 
            if tut == 0:
                if isinstance(section, Tutorial):
                    print(f"Section Name: {section.name}, Days: {section.days}, Time: {section.time}, Instructor: {section.instructor}")
            if lab == 0:
                if isinstance(section, Lab):
                    print(f"Section Name: {section.name}, Days: {section.days}, Time: {section.time}, Instructor: {section.instructor}")

    def __str__(self):
        print(f"Course Name: {self.name}, Exam Date: {self.exam_date}") # Basic Info
    
    def delete_course(self):
        Course.all_course.remove(self)

    def delete_section(self, section):
        self.sections.remove(section)

    def populate_section(self):
        section_name = input("\nEnter section name: ")
        days = input("Enter days: ").split()
        time = input("Enter time: ")
        ins = input("Enter instructor: ")
        section = Section(section_name, days, time, ins, self) # Create a new section object 

class Section:

    def __new__(cls, name, days, time, instructor, course):
        if name[0] == 'L':
            return super(Section, cls).__new__(Lecture)
        elif name[0] == 'T':
            return super(Section, cls).__new__(Tutorial)
        elif name[0] == 'P':
            return super(Section, cls).__new__(Lab)
        else:
            return super(Section, cls).__new__(cls)
        
    def __init__(self, name, days, time, instructor, course):
        self.name = name
        self.days = days
        self.time = time
        self.instructor = instructor
        self.course = course
        course.sections.append(self) # Automatically add the section to the respective course course

class Lecture(Section):
    def __init__(self, name, days, time, instructor, course):
        super().__init__(name, days, time, instructor, course)
        self.type = 'Lecture'

class Tutorial(Section):
    def __init__(self, name, days, time, instructor, course):
        super().__init__(name, days, time, instructor, course)
        self.type = 'Tutorial'

class Lab(Section):
    def __init__(self, name, days, time, instructor, course):
        super().__init__(name, days, time, instructor, course)
        self.type = 'Lab'


class TimeTable:
    tt = [['','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
          ['8:00-9:00', '', '', '', '', '', ''],
          ['9:00-10:00', '', '', '', '', '', ''],
          ['10:00-11:00', '', '', '', '', '', ''],
          ['11:00-12:00', '', '', '', '', '', ''],
          ['12:00-1:00', '', '', '', '', '', ''],
          ['1:00-2:00', '', '', '', '', '', ''],
          ['2:00-3:00', '', '', '', '', '', ''],
          ['3:00-4:00', '', '', '', '', '', ''],
          ['4:00-5:00', '', '', '', '', '', '']]
    
    def __init__(self):
        self.sections = []

    def enroll_subject(self, section):
        self.sections.append(section)
        self.check_clashes()
    
    def remove_subject(self, section):
        self.sections.remove(section)

    def check_clashes(self):
        for i in range(len(self.sections)-1):
            if self.sections[i].days == self.sections[-1].days and self.sections[i].time[:4] == self.sections[-1].time[:4]:
                print("\nClash found, section not added")
                self.sections.pop()
                break
            else:
                print("\nSection was added to the Time Table.")
                pass

    def export_to_csv(self):
        for section in self.sections:
            for day in section.days:
                for i in range(len(TimeTable.tt[0])):
                    if TimeTable.tt[0][i] == day:
                        for j in range(len(TimeTable.tt)):
                            if TimeTable.tt[j][0] == section.time:
                                TimeTable.tt[j][i] = section.name + ' '+ section.course.name +' '+ section.instructor
                                break
                            elif section.time[:4] in TimeTable.tt[j][0]:
                                TimeTable.tt[j][i] = section.name + ' '+ section.course.name +' '+ section.instructor
                                

        with open('timetable.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([""] + TimeTable.tt[0])  

            for row in TimeTable.tt[1:]:
                writer.writerow(row)  
        

def populate_subject(filename): #Adding from Excel file

    wb = openpyxl.load_workbook(filename)
    sheet = wb.active
    courses = []
    for row in sheet.iter_rows(values_only=True):
        if len(row[0]) > 2:
            course_name = row[0]
            exam_date = row[1]
            course = Course(course_name, exam_date)
        else:
            section_name = row[0]
            section_days = [row[1], row[2], row[3]]
            section_time = row[4]
            section_instructor = row[5]
            section = Section(section_name, section_days, section_time, section_instructor, course)
        
        courses.append(course)
                
    print("\nAll courses added successfully.")


#__________________________________________________________________________________
from getpass import *

class Admin:
    Admins = []

    def __init__(self, name, pwd):
        self.name = name
        self.pwd = pwd
        Admin.Admins.append(self)

class Students:
    Students = []

    def __init__(self, name, pwd):
        self.name = name
        self.pwd = pwd
        Students.Students.append(self)

class AdminMenu:

    def admin_login(self): #Login System
        n = 0
        while True:
            print("\nAdmin Login:")
            print("1. Login")
            print("2. Signup")
            print("0. Exit")
            choice = input("\nEnter your choice: ")

            match choice:
                case '1':
                    name = input("\nEnter Name: ")
                    pwd = getpass("Enter Password: ")

                    
                    for admin in Admin.Admins:
                        if name == admin.name and pwd == admin.pwd:
                            print("\nLogin Successful.")
                            self.run_admin_menu()
                            break
                    else:
                        print("\nInvalid Credentials. Please try again.")
                        n += 1

                    if n >= 3:
                        print("\nToo many attempts. Please try again later.")
                        break

                case '2':
                    name = input("\nEnter Name: ")
                    pwd = getpass("Enter Password: ")
                    c_pwd = getpass("Confirm Password: ")

                    if name not in Admin.Admins:
                        pass
                    else:
                        print("\nAdmin already exists. Please try again.")

                    if pwd == c_pwd: 
                        Admin(name, pwd)
                        print("\nAdmin created successfully.")
                    else:
                        print("\nPassword did not match. Please try again.")
                
                case '0':
                    break
                case _ :
                    "Invalid choice. Please try again."


    @staticmethod
    def run_admin_menu(): #Actual Admin Menu
        while True:
            print("\nAdmin Menu:")
            print("1. Create Courses")
            print("2. Create Section of a Course")
            print("3. Delete a Course")
            print("4. Delete a Section")
            print("5. View all courses")
            print("0. Exit")
            choice = input("\nEnter your choice: ")

            match choice:

                case '1': #Add Course

                    print("\nAdd Courses:")
                    print("1. Use Excel File")  #To use populate subject function
                    print("2. Manually")        #To create a new course object
                    choice = input("\nEnter your choice: ")

                    if choice == '1':
                        file = input("\nEnter the file name: ")
                        populate_subject(file)

                    elif choice == '2': 

                        course_name = input("\nEnter course name: ")
                        exam_date = input("Enter exam date: ")
                        course = Course(course_name, exam_date)
                        print(f"\nCourse {course_name} added.")

                    else:
                        print("\nInvalid choice. Please try again.")

                case '2': #Populate Sections
                    
                    course_name = input("\nEnter the course name to add sections: ")
                    course = next((c for c in Course.all_course if c.name == course_name), None)
                    if course:
                        course.populate_section()
                    else:
                        print(f"Course with code {course_name} not found.")
                
                case '3':
                    course = input("Enter the course you want to delete: ")
                    print(f"Are you sure you want to delete {course} course?(Y/N): ")
                    choice = input()
                    if choice == 'Y' or choice =='y':
                        course.delete_course()

                case '4':
                    course = input("Enter the course of the section: ")
                    section = input("Enter the section you want to delete: ")

                    course.delete_section(section)

                case '5': #Print all sections of all courses
                    print("\n-------------------------------------------------------------------------------------------")
                    for course in Course.all_course:
                        print("\n")
                        course.__str__()
                        course.get_all_sections()
                    print("\n-------------------------------------------------------------------------------------------")

                case '0':
                    print("\nConfirm Log out? (Y/N)")
                    choice = input("Enter your choice: ")

                    if choice == 'Y' or choice == 'y':
                        print ("\nLogged out successfully.")
                        break
                    else:
                        pass

                case _:

                    print("Invalid choice. Please try again.")


class StudentMenu:
    def __init__(self):
        self.st_timetable = TimeTable()

    def check_student(self):
        student = input("Enter Name: ")



    def run_student_menu(self):
        while True:
            print("\nStudent Menu:")
            print("1. View All Sections")
            print("2. Display Timetable")
            print("3. Add Section to Timetable")
            print("4. Remove Section from Timetable")
            print("5. Export Timetable to CSV")
            print("0. Exit")
            choice = input("\nEnter your choice: ")

            match choice:
                case '1':
                    print("\n-------------------------------------------------------------------------------------------")
                    for course in Course.all_course:
                        lect = 0
                        tut = 0
                        lab = 0

                        print("\n")
                        course.__str__()
                        for section in self.st_timetable.sections: #To check if a type of section has already been added to the timetable
                            if section.type == 'Lecture' and section.course.name == course.name:
                                lect += 1
                            elif section.type == 'Tutorial' and section.course.name == course.name:
                                tut += 1
                            elif section.type == 'Lab' and section.course.name == course.name:
                                lab += 1
                            else:
                                pass
                        
                        course.get_all_sections(lect , tut, lab) #Print sections of the course that can still be picked
                    print("\n-------------------------------------------------------------------------------------------")

                case '2':
                    for section in self.st_timetable.sections:
                        print(f"Section Name: {section.name}, Course:{section.course.name}, Instructor: {section.instructor}, Days: {section.days}, Time: {section.time}")

                case '3':

                    try:
                        course=None
                        course_name = input("\nEnter the course name to add to your timetable: ")

                        for c in Course.all_course:
                            if c.name == course_name:
                                course = c
                                break
                            
                        section_name = input("Enter the section name to add to your timetable: ")
                        for s in course.sections:
                            if s.name == section_name:
                                section = s
                                break

                        self.st_timetable.enroll_subject(section)

                    except AttributeError:
                        print("\nCourse or Section not found. Please try again.")

                case '4':
                    course_name = input("\nEnter the course name of section to remove from your timetable: ")
                    section_name = input("Enter the section name to remove from your timetable: ")
                    for s in self.st_timetable.sections:
                        if s.name == section_name and s.course.name == course_name:
                            self.st_timetable.remove_subject(s)
                            break

                case '5':
                    self.st_timetable.export_to_csv()

                case '0':
                    break

                case _ :
                    print("Invalid choice. Please try again.")



# Usage
timetable = TimeTable()

admin_menu = AdminMenu()
student_menu = StudentMenu()

while True:
    print("\nMain Menu:")
    print("1. Admin Menu")
    print("2. Student Menu")
    print("0. Exit")
    main_choice = input("Enter your choice: ")

    if main_choice == '1':
        #admin_menu.admin_login() #To remove login, change to -> "admin_menu.run_admin_menu()"
        admin_menu.run_admin_menu()

    elif main_choice == '2':
        student_menu.run_student_menu()

    elif main_choice == '0':
        break

    else:
        print("Invalid choice. Please try again.")
