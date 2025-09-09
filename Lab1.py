def caesar_cipher(text, key, mode):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    result = ""

    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            char_lower = char.lower()
            index = alphabet.find(char_lower)

            if mode == "encrypt":
                new_index = (index + key) % 26
            elif mode == "decrypt":
                new_index = (index - key + 26) % 26  # Add 26 to handle negative results
            else:
                return "Invalid mode. Choose 'encrypt' or 'decrypt'."

            new_char = alphabet[new_index]
            result += new_char.upper() if is_upper else new_char
        else:
            result += char
    return result


def main():
    while True:
        word = input("Inscrie cuvantul: ")

        while True:
            mode_choice = input("Alege 'encrypt' or 'decrypt': ").lower()
            if mode_choice in ["encrypt", "decrypt"]:
                break
            else:
                print("Alege.'encrypt' or 'decrypt'.")

        while True:
            try:
                key = int(input("Introdu o cheie intre (1-25): "))
                if 1 <= key <= 25:
                    break
                else:
                    print("Cheia trebuie sa fie intre 1 si 25.")
            except ValueError:
                print("Pune o cifra pentru cheie.")

        if mode_choice == "encrypt":
            encrypted_word = caesar_cipher(word, key, "encrypt")
            print(f"Cuvantul incriptat: {encrypted_word}")
        else:
            decrypted_word = caesar_cipher(word, key, "decrypt")
            print(f"Cuvantul decriptat: {decrypted_word}")

        another_round = input("Alta operatie? (yes/no): ").lower()
        if another_round != "yes":
            break
if __name__ == "__main__":
    main()