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

# Function to create a commit with a given message and date
def create_commit_with_date(message, commit_date):
    date_str = commit_date.strftime('%Y-%m-%d %H:%M:%S')
    # Set environment variables for commit date
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = date_str
    env['GIT_COMMITTER_DATE'] = date_str
    subprocess.run(['git', 'commit', '--allow-empty', '-m', message], env=env)

# Function to append a word to the CSV file
def append_to_csv(word, csv_file="words.csv"):
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([word])

# Main function to generate commits
def generate_commits(num_commits=4, csv_file="words.csv"):
    # Start date is 1 year ago
    start_date = datetime.now() - timedelta(days=365)
    
    # Fetch words in batches (API typically limits to ~100-500 words per request)
    batch_size = 100
    all_words = []
    
    print(f"Fetching {num_commits} words in batches of {batch_size}...")
    for i in range(0, num_commits, batch_size):
        words_to_fetch = min(batch_size, num_commits - i)
        words_batch = fetch_real_words(words_to_fetch)
        all_words.extend(words_batch)
        print(f"Fetched {len(all_words)}/{num_commits} words...")
    
    print(f"Creating {num_commits} commits...")
    for idx, word in enumerate(all_words, 1):
        # Generate a random date within the last year
        random_days = random.randint(0, 365)
        commit_date = start_date + timedelta(days=random_days)
        
        # Create a commit with the specified date
        create_commit_with_date(word, commit_date)
        
        # Append the word to the CSV file
        append_to_csv(word, csv_file)
        
        # Progress indicator
        if idx % 50 == 0:
            print(f"Created {idx}/{num_commits} commits...")
    
    print(f"Successfully created {num_commits} commits!")

if __name__ == "__main__":
    # Ensure you are in a git repository
    if not os.path.exists('.git'):
        print("This script must be run in a git repository.")
        exit(1)
    
    # Ensure the repository has at least one commit
    if not os.path.exists('.git/refs/heads/main') and not os.path.exists('.git/refs/heads/master'):
        subprocess.run(['git', 'commit', '--allow-empty', '-m', 'Initial commit'])
    
    # Generate the commits (1000 commits)
    generate_commits(num_commits=1000)
    
    # Push all commits at the end with upstream tracking
    subprocess.run(['git', 'push', '--set-upstream', 'origin', 'master'])