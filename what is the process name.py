import os

for item in os.popen('tasklist').read().splitlines()[4:]:  
    print(item)
