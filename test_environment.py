import sys

def main():
    required_version = (3, 10)
    
    if sys.version_info < required_version:
        raise TypeError(
            "This project requires Python {}.{} or higher. Found: Python {}".format(
                required_version[0], required_version[1], sys.version))
    else:
        print(">>> Development environment passes all tests!")


if __name__ == '__main__':
    main()