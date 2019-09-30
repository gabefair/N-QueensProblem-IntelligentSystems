import sys
import random

def main():
    """Main function of program."""

    arg_length = len(sys.argv)

    if (arg_length > 1):
        #print("Starting Import with the following parameters: " + str(sys.argv))
    else:
        print("Hello World")
        

if __name__ == "__main__":
    main()
