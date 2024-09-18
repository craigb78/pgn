import re

try:

    # The search() function returns a Match object:

    ch = r'"one\"two"'

    # x= re.match(r'"(.)*"', ch)

    x = re.match(r'\"([^\"]*)\"', ch)

    print(f"{x.groups()}")


except Exception as e:
    print(e)
    raise e


