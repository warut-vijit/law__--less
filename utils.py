"""
Various utility functions for miscellaneous tasks
@warut-vijit
"""

def encryptxor(key, message):
    """
    Takes two strings, key and message, and returns an encrypted ascii string
    """
    message_ord = [ord(char) for char in message]
    key_ord = [ord(key[index%len(key)]) for index in range(len(message))]
    return "".join([chr(key_ord[i] ^ message_ord[i]) for i in range(len(message))])
