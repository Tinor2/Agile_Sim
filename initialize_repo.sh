#!/bin/sh

# Navigate to the project directory
cd /Users/ronitbhandari/Desktop/Agile Simulation

# Initialize a new git repository
git init

# Add all files to the repository
git add .

# Commit the changes
git commit -m "Initial commit"

# Add the remote repository URL (replace <USERNAME> and <REPO> with your GitHub username and repository name)
git remote add origin https://github.com/<USERNAME>/<REPO>.git

# Push the changes to the remote repository
git push -u origin master
