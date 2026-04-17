import sys
from app import Application


def main():
    app = Application(sys.argv)
    app.exec()


if __name__ == "__main__":
    main()
