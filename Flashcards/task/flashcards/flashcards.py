# print("Input the number of cards:")
# cards_quantity = int(input())
# cards = {}
# for _ in range(cards_quantity):
#     print(f'The term for card #{_+1}:')
#     term = input()
#     while term in cards.keys():
#         print(f'The term "{term}" already exists. Try again:')
#         term = input()
#     print(f'The definition for card #{_+1}:')
#     definition = input()
#     while definition in cards.values():
#         print(f'The definition "{definition}" already exists. Try again:')
#         definition = input()
#     card = {term: definition}
#     cards.update(card)
# # Evaluation
# for term, definition in cards.items():
#     print(f'Print the definition of "{term}":')
#     answer = input()
#     result = ''
#     if answer == definition:
#         result = 'Correct!'
#     else:
#         result = f'Wrong. The right answer is "{definition}"'
#         if answer in cards.values():
#             term_index = list(cards.values()).index(answer)
#             value_for_answer = list(cards.keys())[term_index]
#             result += f', but your definition is correct for "{value_for_answer}"'
#         result += '.'
#     print(result)

from io import StringIO
import argparse

parser = argparse.ArgumentParser(description="This program prints recipes \
consisting of the ingredients you provide.")
parser.add_argument("--export_to")
parser.add_argument("--import_from")
args = parser.parse_args()
import_file = args.import_from
export_file = args.export_to

def initialize_cards(path):
    with open(path, 'r') as file:
        lines = file.readlines()
        imported_cards = {}

        for line in lines:
            info = line.strip().split(':')
            card = {info[0]: [info[1], int(info[2])]}
            imported_cards.update(card)

    print(f'{len(imported_cards)} cards have been loaded.')
    return imported_cards

all_cards = {}

if import_file:
    all_cards = initialize_cards(import_file)

memory_log = StringIO()

currently_cards = {}

def add():
    process_message('The card:')

    term = request_info()

    while term in all_cards.keys():
        process_message(f'The term "{term}" already exists. Try again:')
        term = request_info()

    definition = request_info()
    existing_definitions = [i[0] for i in all_cards.values()]
    while definition in existing_definitions:
        process_message(f'The definition "{definition}" already exists. Try again:')
        definition = request_info()

    card = {term: [definition, 0]}
    all_cards.update(card)
    process_message(f'The pair ("{term}":"{definition}") has been added')


def remove():
    process_message('Which card?')
    term = request_info()
    if term in all_cards.keys():
        all_cards.pop(term)
        process_message('The card has been removed.')
    else:
        process_message(f'Can\'t remove "{term}": there is no such card.')

def update_cards(cards):
    for term, definition in cards.items():
        if term in all_cards.keys():
            all_cards[term] = definition
        else:
            card = {term, definition}
            all_cards.update(card)

def import_cards():
    process_message('File name:')
    cards_file = request_info()
    try:
        with open(cards_file, 'r') as file:
            lines = file.readlines()
            imported_cards = {}

            for line in lines:
                info = line.strip().split(':')
                card = {info[0]: [info[1], int(info[2])]}
                imported_cards.update(card)

            update_cards(imported_cards)

            process_message(f'{len(imported_cards)} cards have been loaded.')
    except FileNotFoundError:
        process_message('File not found')

def export_cards():
    process_message('File name:')
    cards_file = request_info()
    with open(cards_file, 'w') as file:
        for term, definition in all_cards.items():
            file.write(f'{term}:{definition[0]}:{definition[1]}\n')
    process_message(f'{len(all_cards)} cards have been saved.')

def update_mistakes(term):
    result = all_cards.get(term)
    definition = result[0]
    mistakes = result[1]
    all_cards[term] = [definition, mistakes + 1]

def ask():
    process_message('How many times to ask?')
    cards_quantity = int(request_info())
    # print(cards_quantity)
    counter = 0
    while counter != cards_quantity:
        for term, definition in all_cards.items():
            definition = definition[0]
            if counter == cards_quantity:
                break
            else:
                counter += 1
            process_message(f'Print the definition of "{term}":')
            answer = request_info()
            result = ''
            if answer == definition:
                result += 'Correct!'
            else:
                update_mistakes(term)
                result += f'Wrong. The right answer is "{definition}"'
                existing_values = [i[0] for i in all_cards.values()]
                if answer in existing_values:
                    term_index = list(existing_values).index(answer)
                    value_for_answer = list(all_cards.keys())[term_index]
                    result += f', but your definition is correct for "{value_for_answer}"'
                result += '.'
            process_message(result)

def update_log(data):
    print(data, file=memory_log)

def process_message(message):
    print(message)
    update_log(message)

def request_info():
    info = input()
    update_log(info)
    return info

def log_cards():
    process_message('File name:')
    log_file = request_info()
    with open(log_file, 'w') as log:
        for line in memory_log.getvalue().split('\n'):
            log.write(f'{line}\n')
    print('The log has been saved.')

def get_hardest_card():
    mistakes = [value[1] for value in all_cards.values()]
    # print(mistakes)
    cards_with_errors = len(mistakes) != 0
    max_mistake = max(mistakes) if cards_with_errors else 0
    cards_with_errors = max_mistake != 0
    if cards_with_errors:
        cards = [term for term, value in all_cards.items() if value[1] == max_mistake]
        amount_cars = len(cards)
        # print(cards[-1])
        if amount_cars > 1:
            cards = [f'"{term}"' for term in cards]
            message = ", ".join(cards[:-1]) + cards[-1]
            process_message(f'The hardest cards are {message}')
        else:
            process_message(f'The hardest card is "{cards[-1]}". '
                            f'You have {all_cards.get(cards[-1])[1]} errors answering it')
    else:
        process_message(f'There are no cards with errors.')

def reset_mistakes():
    for term, value in all_cards.items():
        all_cards[term] = [value[0], 0]
    process_message('Card statistics have been reset.')

def save_all(path):
    with open(path, 'w') as file:
        for term, definition in all_cards.items():
            file.write(f'{term}:{definition[0]}:{definition[1]}\n')
    process_message(f'{len(all_cards)} cards have been saved.')
while True:
    process_message('Input the action (add, remove, import, export, '
                    'ask, exit, log, hardest card, reset stats):')

    option = request_info()
    if option == 'add':
        add()
    elif option == 'remove':
        remove()
    elif option == 'import':
        import_cards()
    elif option == 'export':
        export_cards()
    elif option == 'ask':
        ask()
    elif option == 'log':
        log_cards()
    elif option == 'hardest card':
        get_hardest_card()
    elif option == 'reset stats':
        reset_mistakes()
    elif option == 'exit':
        print('Bye bye!')
        if export_file:
            save_all(export_file)
        memory_log.close()
        break
