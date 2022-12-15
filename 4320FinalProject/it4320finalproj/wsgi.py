"""Application entry point.""" 
from flask_wtforms_tutorial import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

def get_cost_matrix():
    cost_matrix = [[100,75,50,100] for row in range(12)]
    return cost_matrix

def get_initial_map():
    seat_map = [['O']*4 for row in range (12)]
    with open("reservations.txt","r") as file:
        for line in file:
            string = line.split(",")
            i = int(string[1])
            j = int(string[2])
            seat_map[i][j] = 'x'
    file.close()
    return seat_map

def admin_details():
    admin = {}
    with open("passodes.txt", "r") as file:
        for line in file:
            string = line.split(",")
            admin[string[0].strip()] = string[1].strip()
    return admin

def print_seat_map(seat_map):
    print("\nPrinting Seat Map\n")
    for i in seat_map:
        print(i)

def total_sales(seat_map, cost_matrix):
    total = 0
    for i in range(12):
        for j in range(4):
            if seat_map[i][j] == 'X':
                total += cost_matrix[i][j]
    return total

def reserve_seat(seat_map):
    print("\nMake Reservation")
    firstname = input("\nEnter first name: ")
    lastname = input("\nEnter last name: ")
    print_seat_map(seat_map)
    print()
    isValid = False
    i,j = 0,0
    while not isValid:
        i = int(input("\nWhich seat row would you like? "))
        j = int(input("\nWhich seat column would you like? "))

        if seat_map[i-1][j-1] == 'X':
            print("\nRow:{0} and Seat:{1} are already assigned. Please choose again.\n".format(i,j))
        else:
            print("\nYour requested seat Row:{0} and Seat:{1} have been assigned.\n".format(i,j))
            isValid = True
            seat_map[i-1][j-1] = 'X'
    print_seat_map(seat_map)
    print()
    e_ticket = ""
    code = "INFOTC4320"
    for index in range(len(firstname)):
        e_ticket += firstname[index]
        e_ticket += code[index]
    e_ticket += code[len(firstname):]
    string = ", ".join([str("\n"+firstname), str(i), str(j), e_ticket])
    with open("reservations.txt", "a") as file:
        file.write(string)
    file.close()
    print("\nCongratulations {0} {1}, your trip is booked. Enjoy and have fun!".format(firstname,lastname))
    print("Your e-ticket number is: {0}".format(e_ticket))

def menu_get_option():
    print("\n1. Admin Log-in")
    print("\n2. Reserve a seat")
    print("\n1. Exit")
    option = int(input("\nChoose an option: "))
    return option

def get_admin_login(seat_map):
    print("\nAdmin Log-in")
    admin_detail = admin_details()
    while True:
        username = input("\nEnter Username: ")
        password = input("\nEnter Password: ")

        if username not in admin_detail.keys():
            print("\nInvalid username/password")
        elif admin_detail[username] != password:
            print("\nInvalid username/password")
        else:
            print_seat_map(seat_map)
            print("\nTotal Sales: ${0}".format(total_sales(seat_map,get_cost_matrix())))
            print("\nYou are now logged out.")
            break

def main():
    print("\nIt-4320 Trip Reservation System")
    option = 0
    seat_map = get_initial_map()
    while option != 3:
        option = menu_get_option()
        if option not in [1,2,3]:
            print("\nThis is an invalid option. Please select 1,2, or 3.")
        else:
            if option == 1:
                get_admin_login(seat_map)
            elif option == 2:
                reserve_seat(seat_map)
            else:
                print("\nThank you for using the Trip Reservation System!")
main()

