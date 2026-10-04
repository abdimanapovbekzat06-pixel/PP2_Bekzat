import re
text = input()
pattern = r"[a-z]+_[a-z]+"
if re.fullmatch(pattern, text):
    print("Match")
else:
    print("No match")