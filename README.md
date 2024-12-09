# Kria: Horse/Rider Match Analysis Application

**Author:** [Antonio Matarazzo Affonso Ferreira]  

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

Since we are not deploying this English version online, follow these steps to run it on your local machine:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/kria.git
   cd kria
