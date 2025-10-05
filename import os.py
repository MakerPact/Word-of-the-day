import os
import random
import subprocess
import csv
from datetime import datetime, timedelta
import requests

# Function to fetch a list of real words
def fetch_real_words(num_words=4):
    # Using an online word list API or a static word list
    response = requests.get("https://random-word-api.herokuapp.com/word?number=" + str(num_words))
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch words. Ensure you have an internet connection.")
        exit(1)

# Function to create a commit with a given message
def create_commit(message):
    subprocess.run(['git', 'commit', '--allow-empty', '-m', message])

# Function to set the commit date
def set_commit_date(commit_date):
    date_str = commit_date.strftime('%Y-%m-%d %H:%M:%S')
    subprocess.run(['git', 'commit', '--amend', '--no-edit', '--date', date_str, '--allow-empty'])

# Function to append a word to the CSV file
def append_to_csv(word, csv_file="words.csv"):
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([word])

# Main function to generate commits
def generate_commits(num_commits=4, csv_file="words.csv"):
    # Start date is 4 years ago
    start_date = datetime.now() - timedelta(days=1*365)
    
    # Fetch real words
    words = fetch_real_words(num_commits)
    
    for word in words:
        # Generate a random date within the last 4 years
        random_days = random.randint(0, 4*365)
        commit_date = start_date + timedelta(days=random_days)
        
        # Create an empty commit with the word as the message
        create_commit(word)
        
        # Set the commit date
        set_commit_date(commit_date)
        
        # Append the word to the CSV file
        append_to_csv(word, csv_file)

if __name__ == "__main__":
    # Ensure you are in a git repository
    if not os.path.exists('.git'):
        print("This script must be run in a git repository.")
        exit(1)

    # Ensure the repository has at least one commit
    if not os.path.exists('.git/refs/heads/main'):
        subprocess.run(['git', 'commit', '--allow-empty', '-m', 'Initial commit'])

    # Generate the commits
    generate_commits()

    # Push all commits at the end
    subprocess.run(['git', 'push'])