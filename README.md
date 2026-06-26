# Serie A Match Predictor

## Project Description
This project consists in an API or web tool that you can run on your local machine built to predict the final outcomes of Italian Serie A football matches, classifying them into Home Win (1), Draw (X), or Away Win (2). I choose this project because I wanted to see if we can predict match results using numbers and statistics instead of just feeling or personal bias. To do this, I collected data from the last three Serie A seasons, covering everything from ball possession and accurate passes to more specific stats like Expected Goals (xG) and shots inside the box.

The core idea is very simple: the user selects the starting eleven and the optional bench players for the two teams previously chosen. Then, the system calculates the overall team rating and combines it with historical team data to predict how the match will end. All the statistics automatically inserted can be modified with the exception of the team rating. This project is essentially a web app for football fans who want a data-based prediction without getting lost in overly complicated dashboards. You just pick the teams, look at the stats, and get a prediction based on real-world performances. <br>
In addition to a web app, you can also use the standard API via the curl command:
- Example of a cURL command from the Windows PowerShell: <br><code>Invoke-WebRequest -Method Get -Uri 'http://127.0.0.1:8080/api?data=[45,1.3,2.5,67,77,2,5,6,1,0.8,1.4,1.2,1.0,0.4,0.8,7.45,6.23]'</code>
- Example of a cURL command from a Linux terminal: <br><code>curl -X GET "http://127.0.0.1:8080/api?data=[45,1.3,2.5,67,77,2,5,6,1,0.8,1.4,1.2,1.0,0.4,0.8,7.45,6.23]"</code>

## Dataset Description
The project relies on data scraped directly from FotMob, processed and explored in the `data_exploration.ipynb` notebook and fed to an ML model in the `summary.ipynb` notebook. The data is divided into:

1. **Match Fixtures (`Styled_Fixture_Final.xlsx`):** A dataset containing 1,140 matches. I cleaned the original 99 columns to keep only the most useful ones. I extracted clean percentages for pass accuracy, removed useless identifiers, and kept key stats like ball possession, shots (inside/outside the box), and xG (open play, set play, on target).
2. **Team Averages:** I grouped the data to calculate the average performance stats for each team (both for home and away matches). This acts as a baseline the webapp, each time a user select a team, some of the fields get automatically filled with this values.

## Project Results
During the training phase, I tested four different machine learning models to see which one could predict the match outcomes best: AutoML, Logistic Regression, Random Forest Classifier, and Gradient Boosting. Overall, they all performed quite similarly, around an accuracy of 64%. However, the Logistic Regression model came out on top, reaching an accuracy of almost 66%. 

At first glance, 66% might not sound like a good value, but we have to consider the unpredictable nature of football, where unexpected things happen all the time: a shot hitting the post, a sudden penalty, or an underdog team having the game of their lives against a top-tier club. Because of these random events, predicting the result of a football match is tough. Reaching 66% is actually a good result, even if a truly optimal model would ideally hit 70% or higher. 
This unpredictability also explains another interesting finding from the tests: the hardest result to predict is the draw (X). Since no team actively goes on the pitch aiming just to tie a game from the very first minute, and a single lucky bounce can break a tie at the 90th minute, draws remain the trickiest outcome for any model to catch accurately.


## Commands to Run the Code
To set up the project and run the web app on your local machine, follow these simple steps:

1. install docker if not already installed
2. Pull the package from github: 
    <code>docker pull ghcr.io/piro22/my_seriea_webapp:latest</code>
3. Run the container:
    <code>docker run -d -p 8080:8080 ghcr.io/piro22/my_seriea_webapp:latest</code>
4. Go to http://localhost:8080/ in order to access the webapp