def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    keyword *= len(plaintext) // len(keyword) + 1
    for i, el in enumerate(plaintext):
        charNumber = (ord(el) + ord(keyword[i]))
        if el.isupper():
            ciphertext += chr(charNumber % 26 + 65)
        elif el.islower():
            ciphertext += chr(charNumber % 97 % 26 + 97)
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    keyword *= len(plaintext) // len(keyword) + 1
    for i, el in enumerate(ciphertext):
        charNumber = (ord(el) - ord(keyword[i]))
        if el.isupper():
            plaintext += chr(charNumber % 26 + 65)
        elif el.islower():
            plaintext += chr(charNumber % 97 % 26 + 97)
    return plaintext
