# Address Book Bot
## Description
This bot is designed for managing contacts and birthdays in an address book. It supports a set of commands for creating, modifying, and viewing contacts and birthdays.

## Installation
1.Ensure you have Python 3.6 or higher installed.

`pip install taipan-assistant==1.0.10`

## Install and run the Bot
To run the bot, use the following command:

`taipan-assistant`

## How to run as local package
`python -m pip install -e .` - run it in the root of the repository. You should see folder `taipan_assistant-*` in the .venv/lib/python3.*/site-packages and a `taipan-assistant` in a .venv/bin directory

`taipan-assistant` - run as a binary name.

## Commands
Here is a list of available commands and their descriptions:

- help: Prints a list of available commands.
- hello: Prints a greeting message.
- add [name] [phone number]: Creates a new contact with the specified phone number.
- change [name] [phone number]: Changes the phone number of an existing contact.
- phone [name]: Prints the phone number of the specified contact.
- all: Prints all contacts.
- add-birthday [name] [birthday]: Adds a birthday to the specified contact.
- show-birthday [name]: Prints the birthday of the specified contact.
- birthdays: Prints all birthdays.
- close or exit: Terminates the program.

## Usage Examples
- To add a new contact:
>> add John 123-456-7890
- To change a contact's phone number:
>> change John 987-654-3210
- To view a contact's phone number:
>> phone John
- To add a birthday to a contact:
>> add-birthday John 1990-01-01
- To view a contact's birthday:
>> show-birthday John
- To exit the program:
>> close
>> exit