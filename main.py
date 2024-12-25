from quiz.authentication import authenticate_user, add_user

def main():
    print("Welcome to the Quiz Application!")
    choice = int(input("Would you like to Login[1] or Register yourself[2] (choose 1 or 2)"))
    match choice:
        case 1:
            user_id = input("Enter your user ID: ")
            password = input("Enter your password: ")
            if authenticate_user(user_id, password):
                print("Authentication successful!")
            else:
                print("Invalid credentials. Please try again.")
        case 2:
            user_id = input("Enter your user ID: ")
            name = input("Enter your name: ")
            password = input("Enter your password: ")
            if add_user(user_id, name, password):
                print("Registered succesfully")
            else:
                print(f"User ID '{user_id}' already exists.")

    

if __name__ == "__main__":
    main()