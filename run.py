#!/usr/bin/env python3
#
# Pelican to Hugo v20180603
#
# Convert Markdown files using the pseudo YAML frontmatter syntax
# from Pelican to files using the strict YAML frontmatter syntax
# that Hugo and other static engines expect.
#
# Anthony Nelzin-Santos
# https://anthony.nelzin.fr
# anthony@nelzin.fr
#
# European Union Public Licence v1.2
# https://joinup.ec.europa.eu/collection/eupl/eupl-text-11-12

import os, os.path, re
import glob
import shutil
import sys

#  Add the path to your files below
path = '/Users/wklken/workspace/github/wklken-hugo/content/posts'
# files = os.listdir(path)

all_files = []
files = glob.glob(path + "/*/*.md")
files2 = glob.glob(path + "/*/*/*.md")

all_files.extend(files)
all_files.extend(files2)

print(all_files)
print(len(all_files))
# sys.exit(1)

for file in all_files:
    file_name, file_extension = os.path.splitext(file)
    # Input files will be left in place,
    # output files will be suffixed with "_hugo".
    regexed_file = file_name + '_hugo' + file_extension

    # Only convert visible Markdown files.
    # This precaution is useless… until it is useful,
    # mainly on .DS_Store-ridden macOS folders.
    if not file_name.startswith('.') and file_extension in ('.md') :
        input_file = os.path.join(path, file)
        output_file = os.path.join(path, regexed_file)

        # The files will be edited line by line using regex.
        # The conversion of a thousand files only takes a few seconds.
        with open(input_file, 'rU') as fi, open(output_file, 'w') as fo:
            for line in fi:
                # Add opening frontmatter delimiter before the title.
                line = re.sub(r'(Title:)', r'---\n\1', line)
                # Add closing frontmatter delimiter after the tags.
                line = re.sub(r'(Tags: .*)$$', r'\1\n---', line)
                # Enclose the title in quotes.
                line = re.sub(r'Title: (.*)', r'Title: "\1"', line)
                # Change date formatting.
                linea = line

                line = re.sub(r'(Date: \d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})', r'\1T\2+08:00', line)
                if line == linea:
                    line = re.sub(r'(Date: \d{4}-\d{2}-\d{2})', r'\1T08:00:00+08:00', line)

                # line = re.sub(r'(Date: \d{4}-\d{2}-\d{2}) (\d{2}:\d{2})', r'\1T\2:00+08:00', line)
                # Slow but insightful way to edit the tags.
                if re.match(r'Tags: (.*)', line):
                    # Split the comma separated list of tags.
                    tag_split = re.sub(r'(.*)', r'\1', line).split(', ')
                    # Output the new list of tags.
                    tag_plist = '\n- '.join(tag_split)
                    # Insert a newline before the list.
                    tag_list = re.sub(r'Tags: (.*)', r'Tags: \n- \1', tag_plist)
                    # And enclose the tags in quotes.
                    line = re.sub(r'- (.*)', r'- "\1"', tag_list)
                fo.write(line)
            # Print a little something about the conversion.
            print(file_name + ' converted.')

        shutil.move(output_file, input_file)
