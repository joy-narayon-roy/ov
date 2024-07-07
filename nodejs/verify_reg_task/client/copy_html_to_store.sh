#!/bin/bash
old=$(ls -1 ./store/html | wc -l)
echo "Store HTML : "$old

html=$(ls -1 ./html | wc -l)
echo "Copy HTML : "$html

find html/ -name '*.html' -print0 | xargs -0 cp -t store/html
newhtml=$(ls -1 ./store/html | wc -l)
echo "Now Store HTML :" $newhtml

# Copy logs
old_log=$(ls -1 ./store/log | wc -l)
echo "Store Log : "$old_log

log=$(ls -1 ./log | wc -l)
echo "Copy Log : "$log

find log/ -name '*.log' -print0 | xargs -0 cp -t store/log
new_log=$(ls -1 ./store/log | wc -l)
echo "Now Store Log :" $new_log
# Copy logs


# Prompt the user for input
echo "Run the clean HTML? (y/n):"
read user_input
# Check if the user input is "y"
if [ "$user_input" == "y" ]; then
    echo "Running clean html..."
    python ./clean_invalid_html.py
fi