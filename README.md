# Kria: Horse/Rider Match Analysis Application

**Author:** [Antonio Matarazzo Affonso Ferreira]  
**Link to GitHub Repository: https://github.com/AntonioMatarazzo2002/AI---QM.git**
**Link to YouTube video: https://youtu.be/wcJHSfSkWN0**

## Context
I've been a rider for the last 20 years. In the last two, I built and sold a marketplace for sports horses. With the experience, I learned that what riders lack the most is not actually options of horses to buy, but someone not interested in the negotiation (eg someone not earning any comissions) to see the horse and say if it will or will not be a good fit with the rider. This web-page does exactly that. I've made some adaptations so that you guys can understand what is happening, but the original version is in portuguese, and I'll deploy it to test my idea in some weeks. This is the initial version, translated to english


## Overview

Kria is a web application designed to help understand if a specific horse is a good option for him to ride. By analyzing historical performance data of horses (times, consistency, adaptability to different competitors, and tendencies such as being a “paleteador”), the system provides tailored advice based on the rider’s experience level and goals. Whether you’re a beginner looking for a stable partner or a professional evaluating detailed metrics, Kria guides you toward informed decisions. We are alazying a specific set of horses from Brazil that do barrel racing. 

Note on Data Origin:  
The `novabase.db` file contains real performance data for horses, which was collected by web scraping from [https://www.sgpsistema.com](https://www.sgpsistema.com). This ensures that the analysis is based on real-world performance rather than synthetic examples.

## Features

- **User Accounts and Authentication:**  
  Users can create an account and log in. User data is stored securely in a local SQLite database (`app.db`).
  
- **Rider Profile Classification:**  
  The application classifies riders as Beginner (Iniciante), Intermediate (Intermediaria), Advanced (Avancada), or Professional (Profissional), tailoring advice accordingly.
  
- **Horse Performance Analysis:**  
  Analyzes horse performance data (from `novabase.db`), checking for consistency, adaptability, the presence of “paleteador” behavior, and comparing average times against the user’s desired time.
  
- **Real-World Data:**  
  The `novabase.db` file contains performance data scraped from [sdpsistema.com](https://www.sdpsistema.com), adding authenticity to the analysis.

- **Horse Name Suggestions:**  
  As the user types a horse’s name, suggestions are provided once four letters are typed, guiding the user toward valid horse entries.

## Requirements

- **Runtime Environment:**  
  - Python 3.10 or higher recommended.
  
- **Dependencies:**
  - Flask==2.3.2
  - gunicorn==20.1.0 (I'm currently trying to deploy it in portugues on heroku, thats why this prerequisite is here and thast why the "Procfile" exists as well)

No complex database setup is required. Both user (`app.db`) and horse (`novabase.db`) databases are SQLite files, which are supported natively by Python’s standard library.

## Running the Application Locally

# Application Setup Script

**1. Set Up a Virtual Environment**
python3 -m venv venv
source venv/bin/activate

**2. Install Requirements**
- pip install -r requirements.txt

**3. Run the Application**
- python3 app.py

# 4. Optional: Simulate Production Environment with Gunicorn
**Gunicorn will run the app with 3 worker processes and bind to port 8000**
- gunicorn -w 3 -b 0.0.0.0:8000 app:app
- Notes: The application will start on http://127.0.0.1:8000. Visit this URL in your web browser to access the application.


# Application Usage Instructions

**1. Create an Account**
- Access the URL: /create-account
- Enter your details and submit the form to create your account.

**2. Login**
- Go to the URL: /login
- Enter your registered credentials to log in.

**3. Horse-Rider Match**
 - Access the URL: /check-horse-rider-match
- Type at least four letters of a horse's name to receive suggestions.
- Select your desired time and rider type, then submit to see the analysis.

**4. Report View and Download**
- After analysis, access the URL: /report
- View the results of the analysis or download a text version of the report if needed.


# Notes on Localization and Design
- This version of the application is kept offline and in English for demonstration purposes only.
- The main production version of the application is in Portuguese.
- Branding and CSS design elements are still undergoing refinement for the production release.
