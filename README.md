##Requirments
It is advised to use a virtual environment to run this demo.
The set of instructions given here are using the Python Env Wrapper Pew
https://github.com/berdario/pew
A basic version of python3 and pip3 is necessary for this to work
Atleast 12MB of RAM for the mnist dataset to fit

##Instructions

sudo pip3 install pew
pew new --python=pypy -i numpy -i matplotlib -i scipy -i scikit-image -i termcolor data_augmentation
sudo apt install python3-tk

#Run
./single_image_generator.py --number 31456 --min_max 5 15 --image_width 150

Should display an image of the number 31456 with the format 28x150 each digit
is separated by 5 to 15 pixels.
Image will be saved under:
data/generated_numbers/5_digits_numbers/31456_[1-9][0-9]*.png
Have fun tweaking the parameters.


##Tests
--Merging mnist arrays
--Numbers picked randomly are the proper ones in data_train / data_test
--Random Numbers within range??
--image_width respected
--distance between digits respected
--test min_dist < max_dist


--Perf?
