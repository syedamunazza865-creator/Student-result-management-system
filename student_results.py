import csv
import os
import pandas as pd
import matplotlib.pyplot as plt

file_name="student_data.csv"
def initialize_file():
    if not os.path.exists(file_name):
        with open(file_name,"w",newline="") as file:
            writer=csv.writer(file)
            writer.writerow(["Name", "Roll", "Maths", "Science",
                "English", "Hindi", "Computer",
                "Total", "Percentage", "Grade"])
        print("Student database created!")

def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B+"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    elif percentage >= 35:
        return "D"
    else:
        return "F"

def get_marks(subject):
    while True:
        try:
            marks=float(input(f"Enter {subject} marks(0-100):"))
            if marks<0 or marks>100:
                raise ValueError("Marks must be bw 0 and 100!")
            return marks
        except ValueError as e:
             print(f"Invalid: {e}")

def add_student():
    print("\n--- ADD NEW STUDENT ---")
    try:
        name = input("Enter student name: ").strip()
        if not name:
            raise ValueError("Name cannot be empty!")
        roll = input("Enter roll number: ").strip()
        if not roll:
            raise ValueError("Roll cannot be empty!")
        
        print("\nEnter marks:")
        maths = get_marks("Mathematics")
        science = get_marks("Science")
        english = get_marks("English")
        hindi = get_marks("Hindi")
        computer = get_marks("Computer")
        
        total = maths + science + english + hindi + computer
        percentage = total / 5
        grade = calculate_grade(percentage)
        
        with open(file_name, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                name, roll, maths, science,
                english, hindi, computer,
                total, round(percentage, 2), grade
            ])
        
        print(f"\n'{name}' added! ✅")
        print(f"Percentage: {percentage:.2f}% | Grade: {grade}")
        
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def view_all_students():
    print("\n--- ALL STUDENTS ---")
    try:
        with open(file_name,"r") as file:
            reader = csv.DictReader(file)
            students = list(reader)
        
        if len(students) == 0:
            print("No students found!")
            return
        
        print(f"Total: {len(students)} students")
        print("=" * 60)
        
        for i, student in enumerate(students, 1):
            print(f"\nStudent {i}:")
            print(f"Name       : {student['Name']}")
            print(f"Roll No    : {student['Roll']}")
            print(f"Total      : {student['Total']}/500")
            print(f"Percentage : {student['Percentage']}%")
            print(f"Grade      : {student['Grade']}")
            print("-" * 40)
            
    except FileNotFoundError:
        print("No data file found!")
    except Exception as e:
        print(f"Error: {e}")
    

def search_student():
    print("\n--- SEARCH STUDENT ---")
    try:
        search_name = input("Enter name: ").strip()
        found = False
        
        with open(file_name, "r") as file:
            reader = csv.DictReader(file)
            for student in reader:
                if student["Name"].lower() == search_name.lower():
                    print(f"\nFound! ✅")
                    print(f"Name       : {student['Name']}")
                    print(f"Total      : {student['Total']}/500")
                    print(f"Percentage : {student['Percentage']}%")
                    print(f"Grade      : {student['Grade']}")
                    found = True
                    break
        
        if not found:
            print(f"'{search_name}' not found! ❌")
            
    except FileNotFoundError:
        print("No data file found!")
    except Exception as e:
        print(f"Error: {e}")


def generate_statistics():
    print("\n--- STATISTICS ---")
    try:
        df = pd.read_csv(file_name)
        if len(df) == 0:
            print("No students found!")
            return
        
        print(f"Total Students : {len(df)}")
        print(f"Class Average  : {df['Percentage'].mean():.2f}%")
        print(f"Highest Score  : {df['Percentage'].max()}%")
        print(f"Lowest Score   : {df['Percentage'].min()}%")
        print(f"Passed         : {len(df[df['Percentage'] >= 35])}")
        print(f"Failed         : {len(df[df['Percentage'] < 35])}")
        
        print("\nGrade Distribution:")
        grade_counts = df["Grade"].value_counts()
        for grade, count in grade_counts.items():
            print(f"Grade {grade}: {count} students")
            
    except FileNotFoundError:
        print("No data file found!")
    except Exception as e:
        print(f"Error: {e}")

def create_charts():
    print("\n--- CREATING CHARTS ---")
    try:
        df = pd.read_csv(file_name)
        if len(df) == 0:
            print("No students to chart!")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle("Student Performance Report",
                     fontsize=16, fontweight="bold")
        
        axes[0].bar(df["Name"], df["Percentage"],
                    color="steelblue", edgecolor="black")
        axes[0].set_title("Student Percentages")
        axes[0].set_xlabel("Students")
        axes[0].set_ylabel("Percentage")
        axes[0].set_ylim(0, 100)
        axes[0].axhline(y=35, color="red",
                        linestyle="--", label="Pass Mark")
        axes[0].legend()
        
        grade_counts = df["Grade"].value_counts()
        axes[1].pie(grade_counts.values,
                    labels=grade_counts.index,
                    autopct="%1.1f%%", shadow=True)
        axes[1].set_title("Grade Distribution")
        
        plt.tight_layout()
        plt.savefig("results_chart.png", dpi=150,
                    bbox_inches="tight")
        plt.show()
        print("Chart saved! ✅")
        
    except FileNotFoundError:
        print("No data file found!")
    except Exception as e:
        print(f"Error: {e}")


def main_menu():
    initialize_file()
    print("=" * 50)
    print("   STUDENT RESULT MANAGEMENT SYSTEM")
    print("=" * 50)
    
    while True:
        print("\n1. Add New Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Generate Statistics")
        print("5. Create Performance Charts")
        print("6. Exit")
        
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == "1":
            add_student()
        elif choice == "2":
            view_all_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            generate_statistics()
        elif choice == "5":
            create_charts()
        elif choice == "6":
            print("\nGoodbye! 👋")
            break
        else:
            print("Invalid choice!")

main_menu()

# PROJECTS

# Student Result Management System
# Python | Pandas | Matplotlib | CSV

# - Built a complete student result 
#   management application in Python
# - Implemented CSV file handling for 
#   permanent data storage
# - Used Pandas for data analysis and 
#   Matplotlib for visualization
# - Applied exception handling for 
#   robust error-free operation
# - Features: Add students, calculate 
#   grades, search, statistics and charts

# GitHub: github.com/yourname/student-result-management-system
    