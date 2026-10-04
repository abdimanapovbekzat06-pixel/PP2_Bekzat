import re
text = input()
pattern = r"[A-Z][a-z]+"
if re.fullmatch(pattern, text):
    print("Match")
else:
    print("No match")