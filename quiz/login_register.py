from data_handler import read_users,write_users,read_subjects
import hashlib
from User import User
from subject import Subject
from take_test import takeTest
from Score import Score
import re


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_regex, email))

def verify_password_length(password):
    return bool(len(password)>=8)

#udpos213
def register(fullname,email,username,password):
    users = read_users()

    if not is_valid_email(email): return "Invalid email! Please try again."

    for user in users:
        if user['email'] == email:
            return "Email already exists! Please try a different one."
        if user['username'] == username:
            return "Username already exists! Please try a different one."

    if not verify_password_length(password):
        return "Password must be at least 8 characters long! Please try again."

    new_user = User(fullname,email,username,hash_password(password))

    users.append(new_user.to_dict())
    write_users(users)
    return new_user

#udpos213
def login(username,password):
    users = read_users()

    hashed_password = hash_password(password)

    for user in users:
        if user['username'] == username and user['password'] == hashed_password:
            logged_in_user = User.from_dict(user)
            return logged_in_user

    return "Invalid email or password. Please try again."


def main():
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Select an option (1/2/3): ")

        if choice == "1":
            fullname = input("Enter your fullname name: ")
            email = input("Enter your email: ")
            username = input("Choose a username: ")
            password = input("Choose a password: ")

            result = register(fullname, email, username, password)

            if isinstance(result, User):
                print(f"Registration successful! Welcome, {result.fullname}!")
            else:
                print(f"Error: {result}")

        elif choice == "2":
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            result = login(username, password)

            if isinstance(result, User):
                print(f"Welcome back, {result.fullname}!")

                print("\nAvailable courses:")
                #------- This is for the main
                Subject.print_all_subjects()
                # print(Subject.get_all_courses())

                course = input("\nEnter the name of the course for the test: ")
                find = False

                for cou in Subject.get_all_courses():
                    if cou['title'] == course:
                        find = True
                        break

                if not find:
                    print("The specified course does not exist. Please try again.")
                    continue

                print("\nAvailable chapters:")

                Subject.print_all_chapters_of_course(course)
                Subject.get_all_chapters_of_course(course)

                chapter_id = int(input("\nEnter the chapter ID for the test: "))

                chapter_name = Subject.get_all_chapters_of_course(course)[chapter_id]['title']

                subject = Subject(course, chapter_id, chapter_name)

                test_instance = takeTest(result, subject)

                questions = test_instance.get_questions()

                print("\nStarting the quiz. Please answer the following questions:")
                answers = []

                for idx, question in enumerate(questions, 1):
                    print(f"Q{idx}: {question['question']}")
                    for opt_idx, option in enumerate(question['answers'], 1):
                        print(f"  {opt_idx}. {option}")
                    while True:
                        try:
                            answer = int(input("Your answer (choose the option number): ")) - 1
                            if 0 <= answer < len(question['answers']):
                                answers.append(answer)
                                break
                            else:
                                print("Invalid choice. Try again.")
                        except ValueError:
                            print("Please enter a valid number.")

                test_instance.set_list_of_answers(answers)

                print("\nQuiz Results:")
                results = test_instance.get_results_of_test()

                print(f"Final Score: {results['finalScore']}")

                print("Your Answers:")
                for idx, ans in enumerate(results['listOfAnswers'], 1):
                    print(f"  Q{idx}: {questions[idx-1]['answers'][ans]}")
                print("Correct Answers:")
                for idx, ans in enumerate(results['correctAnswers'], 1):
                    print(f"  Q{idx}: {questions[idx-1]['answers'][ans]}")

                print(f"\nNumber of Questions: {test_instance.get_number_of_questions()}")
                print(f"Correct Answers Count: {len([a for a, c in zip(answers, results['correctAnswers']) if a == c])}")

            else:
                print(f"Error: {result}")

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
    # Subject.print_all_chapters_of_course('Cyber Security')
    # print(Subject.get_all_chapters_of_course("Cyber Security"))
    # Subject.print_all_subjects()
    # Subject.print_all_chapters_of_course('Cyber Security')
    # subject=Subject('Cyber Security',2)
    # Subject.display_questions_in_coonsole(subject)
    # Subject.print_all_subjects()

    # user=login('schakib','123456789')
    # print(user)
    # if isinstance(user, User):
    #     print(user.view_scores())
    # else:
    #     print(user)

    # test_instance=takeTest(user,Subject('Cyber Security',2,'Risk Management and Threats'))
    # score = Score(Subject('Cyber Security',2,'Risk Management and Threats'),98)
    # user.scores.append(score)
    # users = read_users()
    #
    # for u in users:
    #     if u['username'] == user.username:
    #         u['scores'].append(score.to_dict())
    #         write_users(users)
