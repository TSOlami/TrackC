#!/bin/bash

pip install --upgrade pip
# Change directory to the location of your Flask app's code
#cd /path/to/your/flask/app

# Activate the virtual environment (if applicable)
# Uncomment the following line if you're using a virtual environment
# source venv/bin/activate

# Install Flask app dependencies from requirements.txt
pip install -r requirements.txt

# Change directory to the location of your Tailwind CSS files
#cd /path/to/your/tailwind/css

# Install Node.js dependencies (if needed)
# Uncomment the following line if you have a package.json file and need to install Node.js dependencies
# npm install

# Build the Tailwind CSS
npm run tw-build
