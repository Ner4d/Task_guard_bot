import re
import datetime

text = '21.12.2012 18:54'

pattern = r'\d\d.\d\d.\d\d\d\d\s\d\d:\d\d'
find = re.search(pattern, text)
print(type(find))
if find:
    cancel_time = datetime.datetime.strptime(find.group(), '%d.%m.%Y %H:%M')
    print(cancel_time, type(cancel_time))
else:
    print(find)
