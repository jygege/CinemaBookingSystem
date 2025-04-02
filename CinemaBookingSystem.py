class CinemaBookingSystem:
    def __init__(self):
        self.movie_title = ""
        #seating map demension
        self.rows = 0
        self.seats_per_row = 0
        self.seats_left = 0
        self.middle_seat = 0
        #seating map as matrix
        self.seating_map = []
        #current booking seats
        self.current_booking = []
        self.booking_id_counter = 1
        #booking id -> seats
        self.bookings = {}

    def input_seating_map(self):
        while True:
            # Ask user for movie title and seating map in the [Title] [Row] [SeatsPerRow] format
            movie_input = input("Please define movie title and seating map in [Title] [Row] [SeatsPerRow] format:\n> ")
            try:
                movie_title, rows, seats_per_row = movie_input.split()
                self.movie_title = movie_title
                self.rows = int(rows)
                self.seats_per_row = int(seats_per_row)
            except ValueError:
                print("Invalid input format. Please follow the [Title] [Row] [SeatsPerRow] format.\n>")
                continue

            if not (1 <= self.rows <= 26) or not (1 <= self.seats_per_row <= 50):
                print("Invalid input. Maximum rows are 26 and seats per row are 50.")
                continue
                
            self.middle_seat = (self.seats_per_row-1) // 2
            self.seats_left = self.rows * self.seats_per_row

            # Create seating map with all seats available ('.' = available, 'O' = booked)
            self.seating_map = [[' .'] * self.seats_per_row for _ in range(self.rows)]
            break
        return True

    def display_seats(self, booking_id):
        if booking_id in self.bookings:
            self.current_booking = self.bookings[booking_id]
        print(f"\nBooking ID: {booking_id}\nSelected seats:")
        print(" " + "S C R E E N".center(self.seats_per_row * 3))  # Center screen text       
        print("-" * (self.seats_per_row * 3)) 
        
        for row in range(self.rows-1, -1, -1):
#             row_display = [chr(ord('a') + self.rows- 1 - row).upper()]
            row_display = [chr(ord('a') + row).upper()]
            for seat in range(self.seats_per_row):
                if self.seating_map[row][seat] != ' .': 
                    if (row, seat) in self.current_booking:
                        row_display.append(" O")  # Reserved seats
                    else :
                        row_display.append(" #")  # Reserved for current booking
                else:
                    row_display.append(" .")  # Available seats
            print(" ".join(row_display))
        seat_numbers = " ".join('{:>2}'.format(str(i)) for i in range(1, self.seats_per_row+1))
        print(f"  {seat_numbers}")

    def book_seats_default(self, num_tickets):
        tickets_needed = num_tickets
        booked_seats = []
        row = 0
        self.current_booking = []

        while tickets_needed > 0:
            if row == self.rows:
                break
            row_seats = self.seating_map[row]
            #split the seats to (0 .. mid) and (mid+ 1, end)
            left = self.middle_seat 
            right = self.middle_seat + 1 
            while left >= 0 or right <= self.seats_per_row-1:
                # Try to book the left seat if left side has more seats
                if left >= 0 and left + 1 >= self.seats_per_row - right:
                    if row_seats[left] == ' .':
                        self.seating_map[row][left] = " #"  # Mark as reserved for this booking
                        self.current_booking.append((row, left))
                        tickets_needed -= 1
                    left -= 1
                # Try to book the right seat if right side has more seats
                elif right < self.seats_per_row and left + 1 < self.seats_per_row - right:
                    if row_seats[right] == ' .':
                        self.seating_map[row][right] = " #"  # Mark as reserved for this booking
                        self.current_booking.append((row, right))
                        tickets_needed -= 1
                    right+= 1

                if tickets_needed == 0:
                    booked_seats = self.current_booking
                    break
                
                if left < 0 and right > self.seats_per_row-1 and tickets_needed >0:
                    row += 1
                    break

        return booked_seats

    def book_seats_custom(self, num_tickets, start_row, start_seat):
        self.current_booking = []
        tickets_needed = num_tickets
        booked_seats = []
        print(f"Booking {num_tickets} tickets from custom starting position...")

        # Start from the specified row and seat
        row = start_row
        seat = start_seat - 1
        while tickets_needed > 0 :
            if row > self.rows-1:
                break
            row_seats = self.seating_map[row]

            # Try to fill all seats from the specified starting seat towards the right
            for i in range(seat, self.seats_per_row):
                if tickets_needed == 0:
                    break
                if row_seats[i] == ' .':
                    self.seating_map[row][i] = " #"  # Mark as reserved for this booking
                    booked_seats.append((row, i))
                    tickets_needed -= 1

            # If there are still tickets left, move to the next row towards screen
            if tickets_needed > 0:
                if row < self.rows:  
                    row += 1  # Overflow to the next row
                    seat = 0  # Start from the first seat of the new row
                else:
                    break  # No more rows to overflow to

        self.current_booking = booked_seats
        return booked_seats

    def generate_booking_id(self):
        booking_id = f"GIC{self.booking_id_counter:05d}"
        self.booking_id_counter += 1
        return booking_id
    
    def get_booking_id(self):
        booking_id = input("Enter booking id, or enter blank to go back to main menu:\n> ")
        if booking_id in self.bookings:
            return booking_id
        else:
            print("Booking id doesnt exist, please try again")
            self.main_menu()

    def booking_workflow(self):
        while True:
            # Ask for the number of tickets to book
            num_tickets = int(input("\nEnter the number of tickets to book, or enter blank to go back to main menu:\n> "))
            if num_tickets == '':
                break
            elif isinstance(num_tickets, int) :
                if num_tickets > self.seats_left:
                    print(f"Sorry, there are only {self.seats_left} seats available.")
                    continue

                booked_seats = self.book_seats_default(num_tickets)

                # generate a new booking id
                booking_id = self.generate_booking_id()

                print(f"\nSuccessfully reserved {len(booked_seats)} {self.movie_title} tickets.")
                self.display_seats(booking_id)

                while True:
                    confirm = input("\nEnter blank to accept seat selection, or enter new seating position: ").lower()
                    if confirm != '':

                        for row, seat in self.current_booking:
                            # reset default booking
                            self.seating_map[row][seat] = ' .'
                        try:
                            start_row, start_seat = ord(confirm[0])-ord('a'), int(confirm[1:])
                        except ValueError:
                            print("Invalid input format. Please follow the [Row][SeatsPerRow] format. (e.g. A5, B9, etc.)")
                            return False

                        booked_seats = self.book_seats_custom(num_tickets, start_row, start_seat)
                        print(f"\nSuccessfully reserved {len(booked_seats)} {self.movie_title} tickets.")
                        self.display_seats(booking_id)
                        continue
                    else:
                        break

                print(f"\nBooking id:  {booking_id} confirmed.")
                self.bookings[booking_id] = self.current_booking
                self.seats_left -= len(self.current_booking)
                break
            else:
                continue

    def main_menu(self):
        while True:
            print(f"\nWelcome to GIC Cinemas")
            print(f"[1] Book tickets for {self.movie_title} ({self.seats_left} seats available)")
            print("[2] Check bookings")
            print("[3] Exit")

            choice = input("Please enter your selection:\n> ")

            if choice == '1':
                self.booking_workflow()
            elif choice == '2':
                booking_id = self.get_booking_id()
                self.display_seats(booking_id)
            elif choice == '3':
                print("\nThank you for using GIC Cinemas system. Bye!")
                break
            else:
                print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    cinema_system = CinemaBookingSystem()
    if cinema_system.input_seating_map():
        cinema_system.main_menu()
