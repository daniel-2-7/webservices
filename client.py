import requests

BASE_URL = "http://127.0.0.1:8000/api/"

def register():
    username = input("Enter a username: ")
    email = input("Enter an email: ")
    password = input("Enter a password: ")

    data = {"username": username, "email": email, "password": password}
    response = requests.post(BASE_URL + "register/", json=data)

    if response.status_code == 201:
        print("Registration successful!")
    else:
        print("Registration failed:", response.json())


def login(login_url):
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    data = {"username": username, "password": password}

    try:
        response = requests.post(login_url, json=data)

        if response.status_code == 200:
            print("Login successful!")
            return response.json()  # This is where the error occurs, ensure response is in JSON format
        else:
            print("Login failed:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")


    
def logout(token):
    header = {"Authorization": f"Bearer {token}"}
    response = requests.post(BASE_URL + "logout/", headers=header)

    if response.status_code == 200:
        print("Logout successful!")
    else:
        print("Logout failed:", response.json())


def modules_list():
    response = requests.get(BASE_URL + "list/")

    if response.status_code == 200:
        modules = response.json()

        print("\n Modules List:")
        for module in modules:
            print(f"Module Code: {module['module_code']} | Name: {module['module_name']} | Year: {module['year']} | Semester: {module['semester']}")
            print("Taught by:")
            for professor in module.get('professors',[]):
                print(f" - {professor}")
            print("-" * 50)
    else:
        print("Failed to fetch modules list:", response.json())

def view_avg_ratings():
    response = requests.get(BASE_URL + "view/")

    if response.status_code == 200:
        ratings = response.json()

        print("\n Professor Ratings:")
        for professor in ratings:
            print(f"The rating of Professor {professor['professor_name']} ({professor['professor_id']}) is {professor['average_rating']}")
    else:
        print("Failed to fetch professor ratings:", response.json())


def rate_professor(token):
    header = {"Authorization": f"Bearer {token}"}
    professor_id = input("Enter the professor ID: ")
    module_code = input("Enter the module code: ")
    year = input("Enter the year: ")
    semester = input("Enter the semester (semester1/semester2): ")
    rating = input("Enter the rating (1-5): ")

    data = {"professor_id": professor_id, "module_code": module_code, "year": year, "semester": semester, "rating": rating}
    response = requests.post(BASE_URL + "rate-professor/", json=data, headers=header)

    if response.status_code in [200,201]:
        print("Rating submitted successfully!")
    else:
        print("Failed to submit rating:", response.json())


def view_prof_module_ratings():
    professor_id = input("Enter the professor ID: ")
    module_code = input("Enter the module code: ")

    response = requests.get(BASE_URL + f"average/{professor_id}/{module_code}/")

    if response.status_code == 200:
        data = response.json()
        print(f"\nThe average rating of Professor {data['professor_name']} ({data['professor_id']}) in {data['module_name']} ({data['module_code']}) is {data['average_rating']}")
    else:
        print("Failed to fetch average rating:", response.json())


def main():
    token = None

    while True:
        command = input("\n Enter a command (register, login <url>, logout, list, view, average, rate, exit)")

        if command.startswith("login "):  
            parts = command.split(" ", 1)  
            if len(parts) == 2:
                login_url = parts[1]  
                token = login(login_url)  
            else:
                print("Invalid format. Please use: login <url>")

        elif command == "register":
            register()

        elif command == "logout":
            if token:
                logout(token)
                token = None
            else:
                print("You are not logged in")

        elif command == "list":
                modules_list()

        elif command == "view":
                view_avg_ratings()

        elif command == "average":
            view_prof_module_ratings()

        elif command == "rate":
            if token is None:
                print("You must be logged in to rate a professor")
            else:
                rate_professor(token)

        elif command == "exit":
            print("Goodbye!")
            break
        
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()