from Controller.main_menu import MenuController


# Define the main function which will be the entry point of the program
def main():

    # Create a new instance of MenuController
    # and call the main_menu_start() method on it
    MenuController().main_menu()


# If the current script is being run as the main program
# (not imported as a module), execute the main() function
if __name__ == "__main__":
    main()
