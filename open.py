import os
import datetime
from subprocess import call

# Get the file
files = []
for file in os.listdir("."):
    if file.endswith(".md"):
        files.append(file)

files.sort(reverse=True)

# Read data from old file
old_file_name = ""
content = []
if len(files) > 0:
    old_file_name = files[0]
    with open(old_file_name) as f:
        content = f.readlines()
    content = [x.strip() for x in content]     

do_str = "# DO"
done_str = "# DONE"
waiting_str = "# Waiting"

do_elements = []
done_elements = []
waiting_elements = []

read_state = 0 #0 nothing, 1 do, 2 done, 3 waiting
for row in content:
    if row==do_str:
        read_state = 1
    elif row==done_str:
        read_state = 2
    elif row==waiting_str:
        read_state = 3
    else:
        if read_state == 1:
            do_elements.append(row)
        elif read_state == 2:
            done_elements.append(row)
        elif read_state == 3:
            waiting_elements.append(row)

# Create todays file
now = datetime.datetime.now()
current_date = str(now)[:10]
file_name = current_date + ".md"
if os.path.exists(file_name):
    print("File already exists: " + file_name)
    call(["gvim",file_name])
else:
    new_file = open(file_name,"w")
    new_file.write("## From: "+old_file_name+"\n")
    
    new_file.write(do_str+"\n")
    for row in do_elements:
        new_file.write(row+"\n")

    new_file.write(done_str+"\n")
    
    new_file.write(waiting_str+"\n")
    for row in waiting_elements:
        new_file.write(row+"\n")

    new_file.close()
    
    call(["gvim",file_name])
