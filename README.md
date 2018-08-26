##Requirments
python3
mnist dataset : http://yann.lecun.com/exdb/mnist/
mnist lib (more details on that, or just copy what's necessary)
python libs: numpy, matplotlib, termcolor, sys


Load all the data to memory so atleast 12MB of RAM

##Tests
--Merging mnist arrays
--Numbers picked randomly are the proper ones in data_train / data_test
--Random Numbers within range??
--image_width respected
--distance between digits respected
--test min_dist < max_dist


--Perf?

##Question
Should max_dist be included (if we have min dist = 0 max_dist = 10 is it from 0 to 9 pixel distance or 0 to 10)
Is it possible that min_dist and max_dist are negative (numbers are intertwined)
