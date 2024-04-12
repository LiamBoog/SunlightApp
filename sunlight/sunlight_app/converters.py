import re


class HexadecimalConverter:
    regex = "[0-9a-fA-F]{6}"

    def to_python(self, value: str) -> str | ValueError:
        if re.fullmatch(self.regex, value):
            return value
        return ValueError

    def to_url(self, value: str) -> str | ValueError:
        return self.to_python(value)

