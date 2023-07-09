# TrackC - Building a free crypto investment tracker

TrackC is a web application that allows users to track their cryptocurrency transactions, manage their portfolio, and stay updated with the latest cryptocurrency news. It provides real-time updates on the current value of their holdings, calculates the portfolio worth, and displays equity percentages. The app uses data from the CoinGecko API to fetch live cryptocurrency price updates and news articles.

## Features

- **User Authentication:** Users can create an account, log in, and log out securely.
- **Add Transactions:** Users can add their cryptocurrency transactions, including the coin name, number of coins bought, and price purchased.
- **Remove Transactions:** Users can remove previously added transactions by specifying the coin name and number of coins sold.
- **Real-time Data:** The app fetches live cryptocurrency prices from the CoinGecko API to provide real-time updates on the current value of each transaction and the overall portfolio worth.
- **Equity Calculation:** The app calculates the equity percentage for each transaction based on the price purchased and the current value, displaying it with a color-coded indicator (green for positive equity, red for negative equity).
- **Portfolio Summary:** The app displays the total portfolio worth and the total equity percentage for the entire portfolio.
- **Cryptocurrency News:** The app fetches the latest news articles from the CoinGecko API, providing users with up-to-date information about the cryptocurrency market.

## Table of Content
* [Deployment](#deployment)
* [Technologies Used](#technologies-used)
* [Setup and Installation](#setup-and-installation)
* [Usage](#usage)
* [File Descriptions](#file-descriptions)
* [Examples of use](#examples-of-use)
* [Bugs](#bugs)
* [Contributing](#contributing)
* [Authors](#authors)
* [License](#license)

## Deployment

The app has been deployed on **[Render]** and can be accessed at [app URL](https://trackc-flask-app-wg3p.onrender.com/).


## Technologies Used

- Python
- Flask (web framework)
- SQLAlchemy (database toolkit)
- CoinGecko API (for live cryptocurrency prices and news)
- HTML/CSS
- JavaScript

## Setup and Installation
1. Clone this repository:
 `git clone https://github.com/TSOlami/TrackC.git`
2. Access the directory:
 `cd TrackC`
3. Create a virtual environment and activate it: 
 `python3 -m venv venv`
 `source venv/bin/activate`
4. Install the dependencies:
 `pip install -r requirements.txt`
5. Set the environment variables:
 * Rename the `.env.example` file to `.env`.
 * Open the `.env` file and provide your values for the `SECRET_KEY`
6. Set up the database:
 * Rename the `config.py.example` file to `config.py`. 
 * Open the `config.py` file and provide your values for your database URI
7. Run the application:
 Navigate to the directory where the main.py file is located and run `python main.py`
8. Open your web browser and visit http://localhost:5000 to access the application.

## Usage
1. Create a new account or log in with your existing credentials
2. Go to the transactions page and add your cryptocurrency transactions using the "Add Transaction" form. Enter the coin name, number of coins bought, and the price purchased.
3. Remove transactions using the "Remove Transaction" form. Specify the coin name and the number of coins sold.
4. The app will fetch live cryptocurrency prices and provide real-time updates on the current value of each transaction.
5. View the list of transactions, including details such as coin name, symbol, price purchased, number of coins, time transacted, time updated, cost basis, current value, and equity.
6. The portfolio worth and total equity for the entire portfolio will be displayed at the bottom of the transactions table.
7. Stay updated with the latest cryptocurrency news by visiting the "News" section of the app. The news articles are fetched from the CoinGecko API and provide valuable insights into the cryptocurrency market.

## File Descriptions
* [/main.py](/main.py) - The main entry point of the application. It contains the Flask app setup.
* [/requirements.txt](/requirements.txt ) - List of Python dependencies required by the application.
* [/tailwind.config.js](/tailwind.config.js) -  Configuration file for Tailwind CSS.
* [/README.md](/README.md) - The project's README file.
* [/package.json](/package.json) - Configuration file for npm and Node.js packages.
* [/package-lock.json](/package-lock.json) - Generated file that locks the versions of npm packages.
* [/build.sh](/build.sh) - A shell script for building the project.
* [/.gitignore](/.gitignore) -  Specifies which files and directories should be ignored by Git.
* [/node_modules](/node_modules) -  Directory containing the installed Node.js packages.
* [/tailwind-elements](/tailwind-elements) - Directory for custom Tailwind CSS components.
* [/webapp/](/webapp) - Directory containing the web application code.
*   [/init.py](/webapp/__init__.py) -  Initialization file for the web application.
*   [/.env](/webapp/.env) -  Environment variables file (not to be committed to version control).
*   [/auth.py](/webapp/auth.py) - Module handling user authentication and authorization.
*   [/config.py](/webapp/config.py) - Configuration file for the web application (not to be committed to version control)..
*   [/models.py](/webapp/models.py) - Database models and schema definitions.
*   [/views.py](/webapp/views.py) - Contains the route handlers and views.
*   [/static/](/webapp/static) - Directory for static files (CSS, JavaScript, etc.).
*    [/static/css/](/webapp/static/css) -  Directory for CSS files.
*    [/static/css/dist/](/webapp/static/css/dist) - Directory for compiled CSS files.
*    [/static/css/dist/output.css](/webapp/static/css/dist/output.css) - Compiled CSS file for the project.
*    [/static/src/](/webapp/static/src) - Directory for source CSS and JavaScript files.
*    [/static/src/input.css](/webapp/static/src/input.css) - Example source CSS file.
*    [/static/scripts/](/webapp/static/scripts:) -  Directory for JavaScript files.
*    [/static/scripts/index.js](/webapp/static/scripts/index.js) - Example JavaScript file.
*    [/static/scripts/alert-dismiss.js](/webapp/static/scripts/alert-dismiss.js) - JavaScript file for dismissing alerts.
*    [/static/main.css](/webapp/static/main.css) - Example main CSS file.
*  [templates/](/webapp/templates) - Directory for HTML templates.
*    [/templates/about.html](/webapp/templates/about.html) - Example About page template.
*    [/templates/base.html](/webapp/templates/base.html) - Base template used as the layout for other templates.
*    [/templates/landing.html](/webapp/templates/landing.html) - Example landing page template.
*    [/templates/login.html](/webapp/templates/login.html) -  Login page template.
*    [/templates/home.html](/webapp/templates/home.html) - Home page template.
*    [/templates/news.html](/webapp/templates/news.html) - News page template.
*    [/templates/sign_up.html](/webapp/templates/sign_up.html) - Sign up page template.
*    [/templates/transactions.html](/webapp/templates/transactions.html) - Transactions page template.

## Bugs
No known bugs at this time. 

## Contributing
Contributions to the Portfolio Tracker project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request. You can also contact us through our [email](trackcteam@gmail.com)

## Authors
1. Tijani Saheed Olalekan - [Github](https://github.com/TSOlami) / [Twitter](https://twitter.com/def_input_name) / [Linkedin](https://linkedin.com/in/saheed-tijani-b9935625b)
2. Timilehin Olusa - [Github](https://github.com/DeepBrain07) / [Twitter](https://twitter.com/TimmieOlusa) / [Linkedin](https://www.linkedin.com/in/timilehin-olusa-781386250/)
3. Abdulkareem Abdulquddus Olayinka - [Github](https://github.com/Slimanyy) / [Twitter](https://twitter.com/Slimany_) / [Linkedin](https://www.linkedin.com/in/slimany/)

## License
Public Domain. No copy write protection. 
