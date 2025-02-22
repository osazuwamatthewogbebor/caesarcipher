# import requests
import re


def encrypt():
    """
    Encrypting Function
    """
    shift = enter_shift()
    text = enter_text()

    processed_text = ""

    for char in text:
        # Checking for Capital Letters
        if 65 <= ord(char) <= 90:
            new_unicode = ord(char) + shift
            if new_unicode > 90:
                new_unicode -= 26
            processed_text += chr(new_unicode)
        elif 97 <= ord(char) <= 122:
            new_unicode = ord(char) + shift
            if new_unicode > 122:
                new_unicode -= 26
            processed_text += chr(new_unicode)
        else:
            processed_text += char

    return processed_text


def decrypt():
    """
    Decrypting function
    """
    shift = enter_shift()
    text = enter_text()
    processed_text = ""

    for char in text:
        # Checking for Capital Letters
        if 65 <= ord(char) <= 90:
            new_unicode = ord(char) - shift
            if new_unicode < 65:
                new_unicode += 26
            processed_text += chr(new_unicode)
        elif 97 <= ord(char) <= 122:
            new_unicode = ord(char) - shift
            if new_unicode < 97:
                new_unicode += 26
            processed_text += chr(new_unicode)
        else:
            processed_text += char

    return processed_text


def detect():
    """
        Function to detect the shift value used
    """
    print("\nREAD ME:\nNote that the result of this detection may not be 100% accurate.\n"
          "For better accuracy, ensure your cipher text contains words with four or more characters.\n"
          "Also ensure the original text, when decrypted, is in English.\n\nGood luck!\n\n")
    cipher = enter_text()
    shift_value = "not yet assigned"

    possible_list = []
    possible_shifts = []
    possible_count = 0
    accuracy = detection_accuracy()
    print("\nChecking for Caesar Cipher. Be patient >>>")

    for shift_val in range(1, 27):
        processed_text = ""
        for char in cipher:
            # Checking for Capital Letters
            if 65 <= ord(char) <= 90:
                new_unicode = ord(char) - shift_val
                if new_unicode < 65:
                    new_unicode += 26
                processed_text += chr(new_unicode)
            elif 97 <= ord(char) <= 122:
                new_unicode = ord(char) - shift_val
                if new_unicode < 97:
                    new_unicode += 26
                processed_text += chr(new_unicode)
            else:
                processed_text += char
        processed_text_list = processed_text.split()

        # Using a dictionary api or perdefined wordlist to check for English words.
        with open("./words.txt", "r") as file:
            word_list = file.read()
        for word in processed_text_list:
            if len(word) > accuracy:
                # url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
                # response = requests.get(url)
                # if response.text[3:7] == "word":
                with open("./words.txt", "r", encoding="utf-8") as file:
                    content = file.read()
                    if re.search(rf"\b{word}\b", content):
                        possible_count += 1
                        cipher_first_letter_code = ord(cipher[0])
                        first_letter_code = ord(processed_text[0])
                        shift_value = cipher_first_letter_code - first_letter_code
                        if shift_value < 0:
                            shift_value += 26

                        # Add text to list of possible originals provided it wasn't in the list before
                        if processed_text not in possible_list:
                            possible_list.append(processed_text)
                            possible_shifts.append(shift_value)
                        break

    if possible_count > 1:
        print(f"Caesar Cipher algorithm detected \n")
    see_original = input("Would you like to see the original text? ' 'y' or 'n': ").lower()
    possible_original = " none found"
    possible_shift = " none found"

    print(f"{possible_count} possible results detected\n")

    if see_original == "y":
        for index in range(0, len(possible_shifts)):
            possible_shift = possible_shifts[index]
            possible_original = possible_list[index]
        print(f"Possible shift value: {possible_shift} \nPossible original text: {possible_original}\n")
    elif see_original == "n":
        for index in range(0, len(possible_shifts)):
            possible_shift = possible_shifts[index]
        print(f"Possible shift value: {possible_shift}\n")
        print("That would be all!")


def detection_accuracy():
    det_given = False
    while not det_given:
        accuracy_level = input("\nHow accurate do you want the detection tool to be? \n"
                               "Enter 'low', 'mid', 'high', or 'precise' accuracy level: ").lower()

        if accuracy_level == 'low':
            word_length_check = 1
            det_given = True
        elif accuracy_level == 'mid':
            word_length_check = 2
            det_given = True
        elif accuracy_level == 'high':
            word_length_check = 3
            det_given = True
        elif accuracy_level == 'precise':
            word_length_check = 4
            det_given = True
        else:
            print("\nChoose an accuracy level\n")

    return word_length_check


def enter_shift():
    """
        Function to get the shift value from the user.
    """
    while True:
        try:
            shift_value = int(input("Enter your shift value: ")) % 26
            return shift_value
        except ValueError:
            print("Only integers allowed.\n")


def enter_text():
    """
        Function to get the text from the user either as text or as a txt file.
    """
    while True:
        text_choice = input("Do you want to enter the text on the console (type 'con') "
                            "or submit a txt file (type 'txt')?: ").lower()

        if text_choice == 'con':
            text_input = input("Enter text: ")
            return text_input

        elif text_choice == 'txt':
            text_path = input("Enter file path: ")
            try:
                with open(text_path, 'r') as file:
                    text_input = file.read()
                    return text_input
            except FileNotFoundError:
                print("Make sure you enter the right file path\n")

        else:
            print("Invalid input\n")


def output_text(result):
    """
        Function to output the resulting text either to the console
        or as a txt file based on the users choice.
    """
    while True:
        output_choice = input("Do you want the result printed on the console (type 'con') "
                              "or saved as a txt file (type 'txt')?: ").lower()

        if output_choice == 'con':
            print(f"\nHere's your resulting text:\n{result}\n")
            break
        elif output_choice == 'txt':
            with open('./result.txt', 'w') as file:
                file.write(result)
                print("\ntxt file generated\n")
                break
        else:
            print("Invalid selection.\n")


# Function to begin the program
def main():
    while True:
        task = input("Type 'enc' to encrypt 'dec' to decrypt 'det' to detect or 'exit' to end the program: ").lower()
        if task == 'enc':
            result_text = encrypt()
            output_text(result_text)

        elif task == 'dec':
            result_text = decrypt()
            output_text(result_text)

        elif task == 'det':
            detect()

        elif task == 'exit':
            quit()

        else:
            print("Invalid selection.\n")


if __name__ == "__main__":
    main()

