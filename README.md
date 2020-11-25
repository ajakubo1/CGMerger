# CGMerger
CodinGame Merger (merges files from a folder into one file served by Coding Game
 web plugin)

## Installation

Currently, the only option of using the script is just by doing a git clone or
 downloading a zip from the script. I'm working on creating something more official :).

## Running the script

The script can be run from the console by simply typing ``python3 main.py`` command.

## Usage

The script works as following:
1. It searches all of the files in folder specified by ``--workdir`` argument (by
 default, the folder it searches for is named ``codingame``)
2. It takes all of the file names from that folder, filtered by ``--file-regex
`` argument (by default, it's ``.*`` - it matches every file in that folder). It **does
 not** search other folders in that folder (only first level of files is taken)
3. Copies the contents of all of the files, excluding lines matched by 
``--exclude-line-regex`` into single ``--output`` file in directory where the script
 runs (by default the file is named ``codingame.volatile.py``)

The script **does not** create any folders and files on it's own. It checks if
 ``--output`` file exists and inform the user if it doesn't (same thing for ``--workdir``)
 
## Writing a config file

You can write your own config file for the script. In the begining of the run, the
 script will search for ``cgmerger.conf`` file and reads the configuration from it
 . You can still override the values provided by that script by specifying arguments
  in command line.
  
Instead of writing your own ``cgmerger.conf``, you can simply run the script with
 ``python3 main.py --write``. This will create a ``cgmerger.conf`` from currently
  loaded script setup. Next time you run the script, you don't have to specify any
   arguments in the command

## Parameters

If you want to know more about parameters, you can issue ``--help`` command. More
 explanations on each of the options:
 
### output/--output _(conf file/command argument)_

This is the file to which the script will write the data from all of the files in
 ``--workdir`` folder. This file should not be edited in any way - it is volatile and
  will be overriden if you issue the fully configured command. 
  ``codingame.volatile.py`` by default

### workdir/--workdir _(conf file/command argument)_

This is the folder that is searched for files that will be merged into ``--output
`` file. ``codingame`` by default

### main/--main _(conf file/command argument)_

This is the last file that will be copied to the ``--output`` file. If you are
 working in python, this should probably be the file where the main 
 ``while True`` loop is placed. ``main.py`` by default.

### file_regex/--file-regex _(conf file/command argument)_

If you don't want some files in ``--workdir`` to be matched - you should probably
 change the default ``.*`` regex to something more specific. E.g. if you want the
  script only to target ``.py`` files, ``file_regex`` should be set to ``.*.py``.
  
### exclude_line_regex/--exclude-line-regex _(conf file/command argument)_

sometimes during the merge operations, you don't want some of the contents of a file
 to be copied. This is the regex you will like. By default it excludes regexes for
  python: ``^from codingame\.|^import codingame|^from \.|^import \.``. This means
   that for python I'm excluding lines starting from ``from codingame\.``,  
   ``import codingame``, ``from .`` and ``import .``. Those are probably all of the
    local imports that will be used, and can be excluded. For e.g. ``C#`` - you might
     want to exclude all of the ``using`` entries, and defining a ``--header`` file.

### header/--header _(conf file/command argument)_

Header file is optional and when specified - the contents of that file will be added
 to the beginning of the ``--output`` file. You should probably put all of he imports
  in there.
  
### comment/--comment _(conf file/command argument)_

What comment character is used in your language  -``#`` for python - the default
 value - if you are using different language, you should specify the corresponding
  comment sign (e.g. ``//`` for Java and C#)

## Example/Template project

## Smart usage

I use the script with PyCharm. I define a new file watcher that is pointing to 
``main.py`` file. It works perfectly for ``python`` env.

## Todo

If anyone wants to help, there are a couple of big things to do:
- Create a proper setup file nad publish the lib, so it is available to anyone who
 uses ``pip``
- Create tests.
- Do some manual testing on different languages (I only tested it on ``python`` so far)
