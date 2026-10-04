import re
import json

with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

prices = re.findall(
    r"x\s+(\d+(?: \d{3})*,\d{2})",
    text
)

products = re.findall(
    r"^\d+\.\s*\n(.+)$",
    text,
    re.MULTILINE
)

total_match = re.search(
    r"ИТОГО:\s*\n([\d ]+,\d{2})",
    text
)

total = total_match.group(1) if total_match else None

datetime_match = re.search(
    r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})",
    text
)

if datetime_match:
    date = datetime_match.group(1)
    time = datetime_match.group(2)
else:
    date = None
    time = None

# 5. Find payment method
payment_match = re.search(
    r"(Банковская карта):\s*\n[\d ]+,\d{2}",
    text
)

payment_method = payment_match.group(1) if payment_match else None

receipt = {
    "products": products,
    "prices": prices,
    "total": total,
    "date": date,
    "time": time,
    "payment_method": payment_method
}

print(json.dumps(receipt, ensure_ascii=False, indent=4))