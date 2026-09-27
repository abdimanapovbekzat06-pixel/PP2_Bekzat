from datetime import datetime
from zoneinfo import ZoneInfo

Bishkek = datetime.now(ZoneInfo("Asia/Bishkek"))
print(Bishkek)