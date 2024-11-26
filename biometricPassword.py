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
    stdscr.addstr(5, 0, "Enter your password:")
    stdscr.refresh()

    password = record_input(stdscr, 6)

    stdscr.addstr(8, 0, "Your password is now set.")
    stdscr.addstr(9, 0, "Now enter your password to be authenticated")
    stdscr.addstr(10, 0, "At any point, submit an empty guess to end the program.")
    
    stdscr.addstr(12, 0, "Enter your guess:")

    attempt = record_input(stdscr, 14)
    while attempt[0]:
    
        if attempt == password:
            stdscr.addstr(12, 0, "Password is correct! You have been authenticated. Try again?")
        else:
            stdscr.addstr(12, 0, "Incorrect password. You were not authenticated. Try again?")
        stdscr.refresh()

        attempt = record_input(stdscr, 14)

def record_input(stdscr, row):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(100)  # Refresh every 100ms

    pressed_keys = []
    recorded_times = []

    stdscr.refresh()
    
    start_time = time.time()

    while True:
        key = stdscr.getch()

        if key != -1:  # If a key is pressed
            end_time = time.time()
            time_between_depressions = end_time - start_time
            start_time = end_time

            pressed_keys.append(chr(key))  # Add the key to the pressed list
            recorded_times.append(time_between_depressions)            
            
            if key == 10: # If the enter key is pressed
                break
    stdscr.move(row, 0) 
    stdscr.clrtobot()

    recorded = "".join(pressed_keys)[:-1] # exclude the last keypress (the enter button)
    recorded_times.pop(0) # exclude the first time interval (time from message to first key)

    stdscr.addstr(row, 0, f"You entered: {recorded}. The times were: {recorded_times}")

    return [recorded, recorded_times]

# Automatically handles initialization and cleanup
curses.wrapper(main)

