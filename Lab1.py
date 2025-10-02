def caesar_cipher(text, key1, key2, mode):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    result = ""
    key2_shifts = [alphabet.find(c.lower()) for c in key2]
    for i, char in enumerate(text):
        if char.isalpha():
            is_upper = char.isupper()
            char_lower = char.lower()
            index = alphabet.find(char_lower)
            if i % 2 == 0:
                shift = key1
            else:
                shift = key2_shifts[i % len(key2_shifts)]
            if mode == "encrypt":
                new_index = (index + shift) % 26
            elif mode == "decrypt":
                new_index = (index - shift + 26) % 26
            else:
                return "Invalid mode. Choose 'encrypt' or 'decrypt'."
            new_char = alphabet[new_index]
            result += new_char.upper() if is_upper else new_char
        else:
            result += char
    return result
def main():
    while True:
        while True:
            word = input("Inscrie cuvantul (doar litere): ")
            if word.isalpha():
                break
            else:
                print("Cuvantul trebuie sa contina doar litere, fara cifre sau simboluri.")
        while True:
            mode_choice = input("Alege 'e' pentru encrypt sau 'd' pentru decrypt: ").lower()
            if mode_choice in ["e", "d"]:
                mode_choice = "encrypt" if mode_choice == "e" else "decrypt"
                break
            else:
                print("Scrie doar 'e' pentru encrypt sau 'd' pentru decrypt.")
        while True:
            try:
                key1 = int(input("Introdu o cheie numerica intre (1-25): "))
                if 1 <= key1 <= 25:
                    break
                else:
                    print("Cheia trebuie sa fie intre 1 si 25.")
            except ValueError:
                print("Pune o cifra pentru cheie.")
        while True:
            key2 = input("Introdu cheia 2 (doar litere, min 7 caractere): ")
            if key2.isalpha() and len(key2) >= 7:
                break
            else:
                print("Cheia 2 trebuie sa contina doar litere si min 7 caractere.")
        if mode_choice == "encrypt":
            encrypted_word = caesar_cipher(word, key1, key2, "encrypt")
            print(f"Cuvantul incriptat: {encrypted_word}")
        else:
            decrypted_word = caesar_cipher(word, key1, key2, "decrypt")
            print(f"Cuvantul decriptat: {decrypted_word}")
        another_round = input("Alta operatie? (da/nu): ").lower()
        if another_round != "da":
            break
if __name__ == "__main__":
    main()