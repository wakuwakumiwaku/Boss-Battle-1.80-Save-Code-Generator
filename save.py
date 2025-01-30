import random

playername: str = input("Enter your username (case-sensitive): ")
lvl: int = int(input("Enter the level you want to restore (between 0 and 100): "))
exp: int = int(input("Enter the amount of XP you want to restore: "))


save_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
encryption_sets = [
    "",  
    "JCYVQSB71EXK65WZ0LTA2POM8UIRHD43N9FG",
    "A09UYH1R3CMZBK4DQ8OTS5LVIXPF7NGJ2E6W",
    "92QXCID71KOLZ0PH6UWNMTB5GS38VJERAFY4",
    "7MWYO49IVESG10ZC2NUTQ8AJFXR6K5BHDLP3",
    "JU9RAWQYL4ICP73K8OSFM1BTN6EXVD025GHZ",
    "YXN70HR64ZBG9UIJE3DWS5TOPCLMAKF2V81Q"
]


save_slots = [4, 2]  
key_int = random.randint(1, 6)
encryption_set = list(encryption_sets[key_int])


def encode_number(number, length):
    encoded = []
    for i in range(length):
        divisor = 36 ** (length - i - 1)
        digit = number // divisor
        encoded.append(save_chars[digit])
        number = number % divisor
    return ''.join(encoded)

encoded_xp = encode_number(exp, save_slots[0])
encoded_lvl = encode_number(lvl, save_slots[1])
en_string = encoded_xp + encoded_lvl


sum_total = sum(save_chars.index(c) for c in en_string)
checksum1 = save_chars[sum_total % 36]
en_string += checksum1


name_sum = len(playername)
for k in range(2):
    if k < len(playername):
        char = playername[k]
        for j in range(36):
            if char == encryption_sets[1][j]:
                name_sum += (j + 1)
                break
checksum2 = save_chars[name_sum % 36]
en_string += checksum2


substituted = []
for i, c in enumerate(en_string, 1):
    idx = save_chars.index(c)
    substituted.append(encryption_set[idx])
    if i % 6 == 0:
        substituted.append('-')


key_char = save_chars[key_int]
code = f"{key_char}-{''.join(substituted).strip('-')}"
print(f"Generated Code: {code}")
