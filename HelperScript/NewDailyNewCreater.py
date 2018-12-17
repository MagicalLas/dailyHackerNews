from datetime import date

print('if you excute this, file clear to template.')
print('your data will deleted.')
name = input('input your username : ')

path = '../DailyNews/'
today = str(date.today())
fileopen_mode = 'w'
filepath = path+today+'.md'

template=\
"""# Daily Hacker News by %s

## ARTICLE_NAME

SUMMERY_INFOMATION

### Comments

- SUMMER_COMMENTS
- TRANSLATE_COMMENT

### Metadata

- point
- link
"""%name

file = open(filepath, fileopen_mode)

file.write(template)

file.close()
