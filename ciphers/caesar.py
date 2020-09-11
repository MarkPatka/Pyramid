def encrypt_caesar(plaintext: str) -> str:
    """
    >>> encrypt_caesar('PYTHON')
    'SBWKRQ'
    >>> encrypt_caesar('python')
    'sbwkrq'
    >>> encrypt_caesar('Python3.6')
    'Sbwkrq3.6'
    >>> encrypt_caesar('')
    ''
    """
    ciphertext = ""
    for i in range(len(plaintext)):
        letter = plaintext[i]
        i = ord(letter)
        if i in range(65, 91):
            if i == 88 or i == 89 or i == 90:
                i = i - 23
            else:
                i = i + 3
            ciphertext += chr(i)
        elif i in range(97, 123):
            if i == 120 or i == 121 or i == 122:
                i = i - 23
            else:
                i = i + 3
            ciphertext += chr(i)
        else:
            ciphertext += chr(i)
    return ciphertext


def decrypt_caesar(ciphertext: str) -> str:
    """
    >>> decrypt_caesar('SBWKRQ')
    'PYTHON'
    >>> decrypt_caesar('sbwkrq')
    'python'
    >>> decrypt_caesar('Sbwkrq3.6')
    'Python3.6'
    >>> decrypt_caesar('')
    ''
    """
    plaintext = ""
    for i in range(len(ciphertext)):
        letter = ciphertext[i]
        i = ord(letter)
        if i in range(65, 91):
            if i == 65 or i == 66 or i == 67:
                i = i + 23
            else:
                i = i - 3
            plaintext += chr(i)
        elif i in range(97, 123):
            if i == 97 or i == 98 or i == 99:
                i = i + 23
            else:
                i = i - 3
            plaintext += chr(i)
        else:
            plaintext += chr(i)
    return plaintext
