import curses
import time
import statistics

ATTEMPTS_REQUIRED_FOR_SIGNUP = 3 
STDS_ALLOWED = 5

def start(stdscr):
    stdscr.clear()
    stdscr.refresh()

    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(100)  # Refresh every 100ms

    # Intro messages
    stdscr.addstr(0, 0, "Welcome to the biometric password authenticator!")
    stdscr.addstr(1, 0, "This program uses keystroke dynamics for authentication.")
    stdscr.addstr(2, 0, "First you need to set a password.")
    stdscr.addstr(4, 0, f"Enter your new password {ATTEMPTS_REQUIRED_FOR_SIGNUP} times.")
    stdscr.refresh()    
    
    passwords = set()
    timings = []

    # Collect n passwords and their timings
    for i in range(ATTEMPTS_REQUIRED_FOR_SIGNUP):
        stdscr.addstr(5 + i, 0, f"{i + 1}.")
        stdscr.refresh()
        password, timing = record_input(stdscr)
        passwords.add(password)
        timings.append(timing)
        stdscr.addstr(5 + i, 3, password)
        stdscr.refresh()
    
    # Check that the passwords were all the same
    if len(passwords) != 1:
        stdscr.addstr(6 + ATTEMPTS_REQUIRED_FOR_SIGNUP, 0, "Your passwords did not match. Try again? (y/n)")
        while True:
            key = stdscr.getch()

            if key == ord('y'):
                curses.wrapper(start)
                break
            elif key == ord('n'):
                break
    else:
        stdscr.addstr(6 + ATTEMPTS_REQUIRED_FOR_SIGNUP, 0, "Your password is set")
        stdscr.refresh()
        
        avgs = average(timings)
        stds = std(timings)
        password = list(passwords)[0]
      
        handle_attempts(stdscr, password, avgs, stds, 7 + ATTEMPTS_REQUIRED_FOR_SIGNUP)

def handle_attempts(stdscr, password, avgs, stds, row):
    stdscr.move(row, 0) 
    stdscr.clrtobot()

    stdscr.addstr(row, 0, "You may now attempt to sign in using the password you set. (Enter nothing to exit)")

    attempt, timings = record_input(stdscr)
    attempt_num = 1
    success_cnt = 0
    while attempt:
        stdscr.move(row + 2, 0) 
        stdscr.clrtobot()    
        
        stdscr.addstr(row + 2, 0, f"Attempt {attempt_num}: {attempt}")

        if attempt == password and isExpectedTiming(timings, avgs, stds):
            stdscr.addstr(row + 3, 0, "You entered the right password! Feel free to try again!")
            success_cnt += 1
        else:
            stdscr.addstr(row + 3, 0, "You entered the wrong password. Try again.")
        stdscr.addstr(row + 5, 0, f"Success rate: {round(success_cnt / attempt_num, 2) * 100}%")
        stdscr.refresh()
        attempt, timings = record_input(stdscr)
        attempt_num += 1

def isExpectedTiming(timings, avgs, stds):
    for timing, avg, std in zip(timings, avgs, stds):
        if abs(timing - avg) > std * STDS_ALLOWED:
            return False
    return True


def record_input(stdscr):
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

    recorded = "".join(pressed_keys)[:-1] # exclude the last keypress (the enter button)
    recorded_times.pop(0) # exclude the first time interval (time from message to first key)

    return [recorded, recorded_times]

def average(timings):
    avgs = []
    for differences in zip(*timings):
        avg = sum(differences) / len(differences)
        avgs.append(avg)
    return avgs

def std(timings):
    stds = []
    for differences in zip(*timings):
        std = statistics.stdev(differences)
        stds.append(std)
    return stds

# Automatically handles initialization and cleanup
curses.wrapper(start)

