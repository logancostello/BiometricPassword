import curses
import time

def main(stdscr):
    # Clear the screen initially
    stdscr.clear()
    stdscr.refresh()

    # Display initial message
    stdscr.addstr(0, 0, "Welcome to the biometric password authenticator!")
    stdscr.addstr(1, 0, "You will be prompted to set a password.")
    stdscr.addstr(2, 0, "Afterwards, you can attempt to enter the correct password.")
    stdscr.addstr(3, 0, "However, the way in which you type the password will be used for authentication")
    stdscr.refresh()

    password = record_input(stdscr, 5)

    stdscr.addstr(8, 0, "Your password is now set.")
    stdscr.addstr(9, 0, "Now enter your password to be authenticated")
    stdscr.addstr(10, 0, "At any point, submit an empty guess to end the program.")
   
    row = 12
    attempt = record_input(stdscr, row)
    while attempt:
    
        if attempt == password:
            stdscr.addstr(row + 3, 0, "Password is correct! You have been authenticated.")
        else:
            stdscr.addstr(row + 3, 0, "Incorrect password. You were not authenticated.")
        stdscr.refresh()

        row += 5
        attempt = record_input(stdscr, row)

def record_input(stdscr, row):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(100)  # Refresh every 100ms

    pressed_keys = []
    
    stdscr.addstr(row, 0, "Reading your input. Hit enter when you are done:") 
    stdscr.refresh()

    while True:
        key = stdscr.getch()

        if key == 10:  # Enter key (newline) is pressed to exit
            break

        if key != -1:  # If a key is pressed
            pressed_keys.append(chr(key))  # Add the key to the pressed list


    recorded = "".join(pressed_keys)
    stdscr.addstr(row + 1, 0, f"You entered: {recorded}")

    return recorded

# Automatically handles initialization and cleanup
curses.wrapper(main)

