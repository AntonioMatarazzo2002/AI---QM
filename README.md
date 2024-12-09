# Kria: Horse/Rider Match Analysis Application

**Author:** [Antonio Matarazzo Affonso Ferreira]  
**Domain:** (https://foal-future.com)(https://foal-future.com) or use (https://webhorse-85dcffe88126.herokuapp.com/) Note: The domain name “foal-future.com” is from an older idea. The current project is called “Kria”, and I plan to purchase a domain that matches the company name in the future; if the "foal-future" domain is not working, it is due to the 48h delay to the DNS to connect. You can use the other link (it comes directly from heroku)

## Context
I've been a rider for the last 20 years. In the last two, I built and sold a marketplace for sports horses. With the experience, I learned that what riders lack the most is not actually options of horses to buy, but someone not interested in the negotiation (eg someone not earning any comissions) to see the horse and say if it will or will not be a good fit with the rider. This web-page does exactly that. I've made some adaptations so that you guys can understand what is happening, but the original version is in portuguese, and I'll deploy it to test my idea in some weeks. This is the initial version, translated to english


## Overview

Kria is a web application designed to help understand if a specific horse is a good option for him to ride. By analyzing historical performance data of horses (times, consistency, adaptability to different competitors, and tendencies such as being a “paleteador”), the system provides tailored advice based on the rider’s experience level and goals. Whether you’re a beginner looking for a stable partner or a professional evaluating detailed metrics, Kria guides you toward informed decisions. We are alazying a specific set of horses from Brazil that do barrel racing. 

Note on Data Origin:  
The `novabase.db` file contains real performance data for horses, which was collected by web scraping from [https://www.sgpsistema.com](https://www.sgpsistema.com). This ensures that the analysis is based on real-world performance rather than synthetic examples.

## Features

1. **User Accounts and Authentication:**  
   Users must create an account and log in to access the horse-rider match analysis. The application securely stores hashed passwords in a SQLite database (`app.db`).

2. **Rider Profile Classification:**  
   Riders are classified into four categories based on their experience level and status (amateur or professional):  
   - Iniciante (Beginner)  
   - Intermediaria (Intermediate)  
   - Avancada (Advanced)  
   - Profissional (Professional)

   This classification tailors the advice to the user’s experience. Beginners receive supportive guidance, while advanced riders get straightforward data.

3. **Horse Performance Analysis:**  
   Each horse in the `novabase.db` database (scraped from sgpsistema.com) has historical performance entries:
   - **Constancy:** Checks if the horse’s performance (run times) is stable and predictable.
   - **Adaptability to Different Competitors:** Evaluates if the horse’s consistency holds under various riders.
   - **Paleteador Check:** Determines if the horse frequently knocks barrels or incurs technical penalties.
   - **Average Time vs. Desired Time:** Compares the horse’s average run time to the user’s goal, advising if training or adjustments might be needed.

4. **Detailed, Contextual Feedback:**  
   The application generates a comprehensive report based on the user’s profile and the horse’s metrics. Beginners see detailed explanations of each finding, while advanced riders get a more concise report trusting their ability to interpret the data.

5. **Horse Name Suggestions:**  
   To prevent typos or invalid names, as soon as the user types four letters of a horse’s name, the app queries `novabase.db` and suggests valid horse names. This improves user experience by guiding them toward correct inputs.

## Requirements

- **Runtime Environment:**  
  Python 3.10 or above recommended.
  
- **Core Dependencies:**
  - Flask==2.3.2  
  - gunicorn==20.1.0

- **Database Files:**
  - `app.db` for user accounts.
  - `novabase.db` for horse data (collected from sdpsistema.com).

Ensure `requirements.txt` is up to date and includes both Flask and Gunicorn. SQLite is part of Python’s standard library, so no extra installation is needed for database functionality.

## Database Configuration
- app.db: Created automatically when users register. It stores user credentials and profile info.
- novabase.db: Contains scraped real-world performance data from sdpsistema.com, including horses and race_results. The horses table links animal_name to horse_id, and race_results provides time_to_complete and competitor_name

## Using the Application
Create an Account: Visit /create-account, fill out the form (email, password, name, sex, age, experience), and submit.

Login: Go to /login, enter your credentials.

Check Horse-Rider Match: On /check-horse-rider-match, begin typing a horse’s name. After four characters, suggestions appear based on novabase.db data.
Enter your desired time and select your rider type (amateur or professional). Submit to receive a detailed report.

View and Download Report: After analysis, /report displays the results. A download option lets you save a text version of the report.
