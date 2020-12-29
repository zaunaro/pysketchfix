# PySketchFix

PySketchFix is a Automated Program Repair Tool for Python based on the Java Idea of https://github.com/SketchFix/SketchFix. 
The tool needs a buggy code file and a unit test suite which has failing and passing tests.

The idea is to generate sketches (with holes) of the bug file. Therefore AST Token Transformation is used. 
Then these sketches are run and filled while test execution.

Here also an own implementation of Ochiai and Tarantula is used to identify buggy statements in the code.

## Installation and Setup

First of all ensure you installed Python 3.7.

Then install the ast tokens library with:

```bash
pip install asttokens
```
And install the numpy library with:

```bash
pip install numpy
```

You also have to install the coverage library with:

```bash
pip install coverage
```

Then you have to set up the configuration file.
Important here is to change the python interpreter and the python coverage folder to your own. Unless the tool is not working.


Here '../PySketchFix/..' is the folder where the git repository is located on your computer.
Here '../python' is the folder where your interpreter of Python 3.7 (with installed asttokens library) lies.
There are five given bug files which you can test (Here mid.py is taken). You also can test maximum, minimum, positive_indicator and is_prime.

## Usage - Fault Localization with the example of mid.py
First of all you have to edit your input_tests.txt file in the folder: ../PySketchFix/BugFile/mid/tests_for_fault_localization/
Here the path of all unit tests for the fault localizations are written. You have to edit the path to the location of your folder of the Git Repo.

All this is done, because the fault localization only works with different unit test files and not with one single test suite (which is used for PySketchFix).

Now you can execute the fault localization with:
```bash
../python ../PySketchFix/FaultLocalizer.py ../PySketchFix/BugFile/mid/mid.py ../BugFile/mid/tests_for_fault_localization/input_tests.txt tarantula
```
The first argument is the fault localizer script then the bug file, next is the input.txt file which you modified earlier. Then you can choose between ochiai and tarantula.
At the end the array of buggy lines is printed in the output like: "1,5,2"

## Usage - Create sketches with the example of mid.py
Then you can create sketches. Therefore you need the buggy lines of the bug file (which you can define by yourself) or you can take the generated lines from your Fault Localization, done before.
```bash
../python ../PySketchFix/SketchMaker.py ../PySketchFix/BugFile/mid/mid.py 1,5,2
```
Here the first argument is the sketch maker which is the script used to start creating sketches. Next the bug file is taken as argument and then the buggy lines seperated with commas.
You get now an output that sketches are created. These sketches you can find in the ../PySketchFix/BugFileSketches/ folder.

## Usage - Test generated sketches with the example of mid.py
Now sketches are created. Then you can check and fill your sketches by running the unit test suite. Therefore use:
```bash
../python ../PySketchFix/PatchFinder.py ../PySketchFix/BugFile/mid/mid.py ../PySketchFix/BugFile/mid/testsuite/test_mid.py
```
Here the first argument is the patch finder which is the script to test your sketches. Next the bug file is taken as argument and then the unit test file of the buggy file. It is important to use only one file as a unittest suite. 
At the end your patches are created. The result is found in the ../PySketchFix/BugFilePatches/ folder.
Here you can see in which sketch at which line you have to replace the hole with the code.

## Contributing
Questions and Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
