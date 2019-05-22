# Mnist Data Augmentation

Scripts to generate single and batches of numbers using mnist digits as a baseline

## Getting Started

It is advised to use a virtual environment to run this demo.

The set of instructions given here are using the Python Env Wrapper Pew
https://github.com/berdario/pew

A basic version of python3 and pip3 is necessary for this to work

Atleast 12MB of RAM for the mnist dataset to fit


### Installing

If you do not have a python3 or pip on your machine run those commands
```
sudo apt update
sudo apt -y install python3
sudo apt -y install python3-pip
```

Those commands should get you the modules necessary for the project to work

```
sudo apt install python3
sudo pip3 install pew
pew new --python=python3 -i numpy -i matplotlib -i scipy -i scikit-image -i termcolor data_augmentation
sudo apt install python3-tk
```

## Testing

Simply run

```
./test.py
```

The test: "test_generate_batch_numbers" takes from 10 to 30 seconds depending on your CPU

Will take even more time if this is the first time you run anything as it downloads mnist


## Examples

From the command line execute:
```
./single_image_generator.py --number 31456 --min_max 5 15 --image_width 150
```

This should display an image of the number 31456 with the format 28x150 each digit
is separated by 5 to 15 pixels.

The image will be saved under:

```
data/generated_numbers/5_digits_numbers/31456_[1-9][0-9]*.png
```

--number [int] is the number that will be generated

--min_max [int] Will produce a range that is the disance between two digits in pixels

--image_width [int] The final width of the image (height not changed)


To generate batches of image at a time use:

```
./batch_image_generator.py --batch_size 10 --number_of_digits 7 --min_max 2 25 --image_width 250
```

This will generate 10 images of numbers of length 7 (containing 7 digits).
All saved in:

```
data/generated_numbers/7_digits_numbers/XXXXX_[1-9][0-9]*.png
```

--min_max and --image_width are the same as for single images

--batch_size [int] The number of images to process

--number_of_digits [int] The number of digits in the image being created

Another couple of options that have been added are:

--rotation_angle [int] The angle in degrees by which the digits will be turned

--max_range_angle [int] HAS TO BE USED COUPLED WITH --rotation_angle. Creates a range of angles between --rotation_angle and --max_range_angle for the digits to take.


For example:

```
./batch_image_generator.py --batch_size 500 --number_of_digits 19 --min_max 2 25 --image_width 1000 --rotation_angle -60 --max_range_angle 60
```

Have fun tweaking the parameters.

## Extra features

This is a bit ad hocky but cheaky_demo.py shows how you can add any kind of transformations to your image.

It uses the same options as the single_image_generator and all the fancy transformations are hard coded in the python (a bit of lazyness on my part)

```
./cheaky_demo.py --number 314560234 --min_max 5 15 --image_width 250
```
Will generate generate an image with white replace by red, black replace by green, some random noise and rotations


The purpose of this script is mainly to show off the flexibility of the functional design that the scripts have.


### Defining your own transformations

You can write any kind of transformation and apply them to the image by adding the function to either:

```
final_image_transformations (for transformations after the digits have been merged)

or

digit_wise_transformation (for transformations before the digits have been merged)
```

Before calling either

```
generate_number_image()

or

generate_image_batch()
```

The documentation for generate_image_batch() says:

```
 def generate_image_batch(batch_size, number_length,
                      merge_digits_function,
                      final_image_transformations=[],
                      digit_wise_transformations=[]):
     '''
     Generate batch_size random numbers images with number_length digits
     Returns a tuple of the images and the digits generated
     -Applies transformations in digit_wise_transformations to single digit
     images extracted from mnist.
     -Merges the digits images into batch_size ones using the merge_digits_function
     -Applies transformations in final_image_transofrmations to the merged
     digits images
     '''
```

The user defined function should take a numpy.array as input (2D for number_image and 3D for image_batch), apply the modification to the image(s) and return it(them)
If your function needs other meta parameters, use a lambda to assign them before adding it to the list of transformation, for example, this is what I do for the rotate function:

```
angle = int(args.rotation_angle)
max_angle = int(args.max_range_angle) if args.max_range_angle else None
rotato = lambda images: rotate(images, angle=angle, max_angle=max_angle)
```

In the case of image_batch, the returned images should all have the same dimension as a np.array needs all the dimensions to be the same

On that point...

### IMPORTANT NOTE

Both generate_number_image and generate_image_batch have similar API (taking lists to pointer to functions)

It is to note though that when using generate_image_batch the first transformation in:

final_image_transformations should always be center_function.

This is a side effect of my optimal_horizontal_merge not resulting in uniform dimensions.

This of course could be fixed by writing another merge function! (Which is a parameter of both generate_* function)
