# https://pypi.org/project/simple-term-menu/
#!/usr/bin/env python3

from simple_term_menu import TerminalMenu


def main():
    fruits = ["[a] apple", "[b] banana", "[o] orange"]
    terminal_menu = TerminalMenu(fruits, title="Fruits")
    menu_entry_index = terminal_menu.show()


if __name__ == "__main__":
    main()