__version__ = "0.1.0"
__author__ = "Finn Drünert"


class Morse:
    def __init__(
        self, dash: str = "-", dot: str = ".", pause: str = "/", separator: str = " "
    ):

        chars = {dash, dot, pause, separator}
        assert len(chars) == 4

        self.dash = dash
        self.dot = dot
        self.pause = pause
        self.separator = separator

        self.dot_length = 0.1
        self.dash_length = 0.3

        self.morse_alphabet = {
            "a": ".-",
            "b": "-...",
            "c": "-.-.",
            "d": "-..",
            "e": ".",
            "f": "..-.",
            "g": "--.",
            "h": "....",
            "i": "..",
            "j": ".---",
            "k": "-.-",
            "l": ".-..",
            "m": "--",
            "n": "-.",
            "o": "---",
            "p": ".--.",
            "q": "--.-",
            "r": ".-.",
            "s": "...",
            "t": "-",
            "u": "..-",
            "v": "...-",
            "w": ".--",
            "x": "-..-",
            "y": "-.--",
            "z": "--..",
            "ä": ".-.-",
            "ö": "---.",
            "ü": "..--",
            "ß": "......",
            "1": ".----",
            "2": "..---",
            "3": "...--",
            "4": "....-",
            "5": ".....",
            "6": "-....",
            "7": "--...",
            "8": "---..",
            "9": "----.",
            "0": "-----",
            ".": ".-.-.-",
            ",": "--..--",
            "?": "..--..",
            "'": ".----.",
            "!": "-.-.--",
            "/": "-..-.",
            "(": "-.--.",
            ")": "-.--.-",
            "&": ".-...",
            ":": "---...",
            ";": "-.-.-.",
            "=": "-...-",
            "+": ".-.-.",
            "-": "-....-",
            "_": "..--.-",
            '"': ".-..-.",
            "$": "...-..-",
            "@": ".--.-.",
            "¿": "..-.-",
            "¡": "--...-",
        }
        self.morse_alphabet = {
            char: code.replace("-", self.dash).replace(".", self.dot)
            for char, code in self.morse_alphabet.items()
        }
        self.morse_alphabet_reversed = {
            code: char for char, code in self.morse_alphabet.items()
        }

    def letter_to_morse(self, letter: str) -> str:
        assert len(letter) == 1 and letter != " "
        return self.morse_alphabet[letter.lower()]

    def word_to_morse(self, word: str) -> str:
        assert " " not in word
        out = ""
        for i, letter in enumerate(word):
            out += self.letter_to_morse(letter) + (
                self.separator if i + 1 != len(word) else ""
            )
        return out

    def string_to_morse(self, string: str) -> str:
        out = ""
        words = string.split(" ")
        for i, word in enumerate(words):
            out += self.word_to_morse(word) + (
                self.pause if i + 1 != len(words) else ""
            )
        return out

    def morse_to_letter(self, morse: str) -> str:
        return self.morse_alphabet_reversed[morse]

    def morse_to_word(self, morse: str) -> str:
        return "".join(
            [self.morse_to_letter(letter) for letter in morse.split(self.separator)]
        )

    def morse_to_string(self, morse: str) -> str:
        return "".join(
            [f"{self.morse_to_word(word)} " for word in morse.split(self.pause)]
        )[:-1]
