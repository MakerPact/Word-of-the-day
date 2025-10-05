# Word of the day

This script generates a series of git commits with random dates spread across the last year to create a nice heatmap pattern on your GitHub profile.

## How it works

The script:
1. Fetches random words from an online API
2. Creates empty git commits with those words as commit messages
3. Sets random commit dates across the last year
4. Appends each word to a CSV file

## How to use

1. Make sure you're in a git repository
2. Run the script: `python "import os.py"`
3. The script will generate 1000 commits with random dates
4. Push to your GitHub repository to see the changes in your contribution graph

## Customization

You can modify the number of commits by changing the `num_commits` parameter in the `generate_commits()` function call at the bottom of the script.