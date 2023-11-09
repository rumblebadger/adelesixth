# adelesixth

## To users who know what they're doing with python:
Open the code and edit skills_input (and a few other optional parameters near the top of the file if you so choose) and then run the script. It requires numpy, so pip install that if you don't have it already.

## To users who don't know what they're doing with python:
I'll be writing this like you're using a windows machine because if you're seeing this you probably play maplestory and are on a windows machine. Below, whenever I say type 'something like this', just type what is between the single quotes - don't include the single quotes themselves.

1) You will have to have python installed. Go do that. Once you've done that, open a terminal (open the start menu, type 'cmd', then hit enter) and type 'python --version'. If you get an error you don't have python in your path, and you'll need to google how to fix that.

2) Once python is installed, you have to install numpy. Simply type 'pip install numpy' in your terminal from above.

3) After that, you need to download the adelesixth.py script. Download it to somewhere and open that file location in a file explorer window.

4) To run the script, hold shift and right click on adelescript.py, then select the option 'Copy as path'. Go back to your terminal and type 'python <copy your path here>' then hit enter. When you paste the path it will probably come with double quotes around it - that's fine. It should print out stuff! If it doesn't something is wrong. Womp womp.

5) If you want to edit the script to fit your desired situation, you'll have to open the script (right click -> open with -> pick notepad (or another ide if you have one)). You'll want to look for something called skill_inputs near the top. There should be some long comments (inside of triple quotes """ like this """) that explain what the values mean. It looks really gross I'm sorry. Basically for each adele skill you'll want to edit ba_percent and/or burst_frac inside skill_inputs. Hopefully the explanations inside are sufficient. When you're done editing the values, save (ctrl+s), then rerun the 'python <copy your path here>' command. It will give you a new optimized order! Wow!

