#helper functions for the hole code

import sqlite3
from werkzeug.security import check_password_hash
import statistics
from collections import defaultdict

# check to see if the user information is correct and can be send to our database
def validate_user_data(email, password, name, sex, age, experience):
    if not email or not password or not name or not sex or not age or not experience:
        return "All fields are required."
    if sex not in ["male", "female"]:
        return "Sex must be 'male' or 'female'."
    try:
        age = int(age)
        experience = int(experience)
        if age < 1 or experience < 0:
            return "Age must be greater than 0, and experience cannot be negative."
    except ValueError:
        return "Invalid age or experience."
    if len(password) < 6:
        return "Password must be at least 6 characters long."
    return None

# insert the user information in to our database
def insert_user(email, password, name, sex, age, experience):
    try:
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (email, password, name, sex, age, experience)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (email, password, name, sex, age, experience))
        conn.commit()
    except sqlite3.IntegrityError:
        return "Email already in use."
    finally:
        conn.close()
    return None

# check to see if the user information is in our database
def validate_login_credentials(email, password):
    try:
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()
        # Check if the user exists in the database
        cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()
        if not result:
            return "Invalid email or user does not exist."
        # Check if the provided password matches the hashed password
        stored_password = result[0]
        if not check_password_hash(stored_password, password):
            return "Incorrect password. Please try again."
        conn.close()
        return None  # No errors
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
#get the user info using his email
def get_user_info_by_email(email):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, sex, age, experience FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "name": row[0],
            "sex": row[1],
            "age": row[2],
            "experience": row[3]
        }
    return None


#get the horse id in the database
def get_horse_id_by_name(horse_name):
    conn = sqlite3.connect("novabase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT horse_id FROM horses WHERE animal_name = ?", (horse_name,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0]
    return None

#get the time and the competitors to analyze the horse
def get_times_and_competitors_for_horse(horse_id):
    conn = sqlite3.connect("novabase.db")
    cursor = conn.cursor()
    # DB structure: horse_id; competitor_name; time_to_complete na tabela race_results
    cursor.execute("SELECT time_to_complete, competitor_name FROM race_results WHERE horse_id = ?", (horse_id,))
    rows = cursor.fetchall()
    conn.close()
    # Separte in to two lists
    times = [row[0] for row in rows]          # all times
    competitors = [row[1] for row in rows]    # corresponding competitors

    return times, competitors

#gets the information from the user and decides which type of rider he is
def classify_user_profile(experience, rider_type):
    """
    Classify the user as beginner, intermediate, advanced, or professional.
    rider_type: "amateur" or "professional"
    experience: years of experience (int)
    """
    if rider_type == "professional":
        return "profissional"
    else:
        # rider_type amador
        if experience < 6:
            return "iniciante"
        elif 6 <= experience <= 10:
            return "intermediaria"
        else:
            return "avancada"
        
#complete logic of the horse analysis
def analyze_horse_performance(times, competitors):
    """
    times: list of times (float)
    competitors: list of the same length as times, indicating the name of the competitor in each race
    """
    data_warning = None 
    if not times:
        return {
            "constant": False,
            "constant_with_various_competitors": False,
            "paleteador": False,
            "average_time": None,
            "data_warning": "No race times available."
        }
    # filter non-zero times for some analysis
    non_zero_times = [t for t in times if t > 0]
    # Overall consistency: use standard deviation
    # We consider it consistent if std_dev < 10% of the average, for example.
    if len(non_zero_times) > 1:
        avg = statistics.mean(non_zero_times)
        std_dev = statistics.pstdev(non_zero_times)
        constant = (std_dev / avg) < 0.4  
    else:
        # With limited data, we consider it consistent due to a lack of data.
        constant = True
        avg = statistics.mean(non_zero_times) if non_zero_times else None
        std_dev = 0
    if avg is None and non_zero_times:
        avg = statistics.mean(non_zero_times)
    
    # Consistency with different competitors
    # Calculate the average per competitor and check if the averages do not vary significantly.
    from collections import defaultdict
    times_by_competitor = defaultdict(list)
    for t, comp in zip(times, competitors):
        if t > 0:
            times_by_competitor[comp].append(t)
            
    if len(times_by_competitor) > 1:
        competitor_avgs = []
        for comp, comp_times in times_by_competitor.items():
            competitor_avgs.append(statistics.mean(comp_times))
        # If the variation between the competitors' averages is small, we consider it consistent across different competitors.
        overall_std = statistics.pstdev(competitor_avgs) if len(competitor_avgs) > 1 else 0
        # Criterion: variation between competitors is also < 10% of the overall average.
        constant_with_various_competitors = (overall_std / avg) < 0.4 if avg else True
    else:
        # Only one competitor or none – it’s not possible to determine if it’s consistent with multiple riders.
        constant_with_various_competitors = False

# Detect if the horse is a "paleteador", a bad characteristic for amateurs, it means that the horse faals a lot
# Criteria:
# - Are there zeroed times (> 2)?
# - Is there a cluster around x and another around x+5?
# To simplify, find the smallest non-zero time (x) and check if there is a cluster around (x+5).
# A "cluster" can be determined if there is a significant number of times between (x+4.5 and x+5.5).
    zero_count = sum(1 for t in times if t == 0)
    paleteador = False
    if zero_count > 2 and non_zero_times:
        min_time = min(non_zero_times)
        cluster_5 = [t for t in non_zero_times if (t > min_time+4.5 and t < min_time+5.5)]
        # If there is a cluster of times around min_time+5 and we also have zeroed times, we consider the horse a "paleteador."
        if len(cluster_5) > 0:
            paleteador = True
    if len(non_zero_times) <= 2:
        data_warning = "Insufficient race data for reliable analysis."
    elif len(times_by_competitor) <= 1:
        data_warning = "Insufficient competitor diversity for reliable analysis."
    # Average time (ignoring zeros) is already calculated: it is avg.    
    return {
        "constant": constant,
        "constant_with_various_competitors": constant_with_various_competitors,
        "paleteador": paleteador,
        "average_time": avg
    }



# Generates a report based on the match between horse and rider
def generate_report(user_profile, horse_analysis, desired_time):
    # Get horses information
    constant = horse_analysis["constant"]
    constant_with_var = horse_analysis["constant_with_various_competitors"]
    paleteador = horse_analysis["paleteador"]
    avg_time = horse_analysis["average_time"]
    data_warning = horse_analysis.get("data_warning") 

    message = []

    if data_warning:
        message.append(f"Note: {data_warning}")

    # Always mention each analyzed point in detail before going into profile-specific logic:
    # 1. Constancy
    if constant:
        message.append("Firstly, let's analyze the horse's overall consistency. In reviewing its historical performance data, we observe that the horse maintains relatively stable times across its runs. This indicates a predictable pattern, suggesting that the horse does not fluctuate wildly in terms of speed and behavior. Such consistency can be extremely beneficial, as it allows a rider to anticipate the horse’s responses and better strategize for future improvements. A horse that consistently performs within a tight range of times reduces guesswork and makes it simpler to develop riding techniques and training plans tailored to that horse’s steady performance level.")
    else:
        message.append("Firstly, let's analyze the horse's overall consistency. After examining its performance records, it becomes apparent that the horse does not maintain a stable pattern in its runs. Instead, its times and behaviors show considerable variation. This fluctuation might mean that one run could be very different from the next, introducing an element of unpredictability. Riders interacting with this horse may find it challenging to rely on past results as indicators of future performance, potentially complicating training approaches and making it harder to develop a solid strategy around the horse’s changing tendencies.")

    # 2. Constancy with various competitors
    if constant_with_var:
        message.append("Next, let’s consider the horse’s adaptability to different riders, often assessed by checking if it performs consistently with multiple competitors. In this case, the horse’s performance does not drastically depend on who is riding it. Such versatility and adaptability mean that the horse can be handled by various individuals without dramatically altering its core pattern of behavior and run times. This adaptability is a strong asset, as it indicates that the horse’s consistency and reliability are not tied to a single rider’s style or technique, making it more universally approachable.")
    else:
        message.append("Next, let’s look at how the horse behaves with different competitors. The data suggests that this horse’s steady performance might be limited to one particular rider, or that its behavior shifts noticeably when someone else takes the reins. Such a scenario can indicate that the horse has developed a strong rapport or understanding with a single individual, potentially struggling to replicate its good performance under a different handler. This limitation in adaptability may pose a challenge for riders who are not accustomed to the horse’s nuances, as it could lead to inconsistent experiences if the rider’s style, strength, or technique differ from that of the rider with whom the horse performs best.")

    # 3. Paleteador
    if paleteador:
        message.append("We also investigate whether the horse is what we refer to as a 'paleteador', a term generally used to describe a horse that frequently knocks barrels or incurs penalties leading to disqualification (often represented by 0 seconds or a distinct time penalty pattern). The data reveals evidence that this horse may fit that definition, as indicated by clusters of zeroed runs and times repeatedly showing a baseline plus an added 5 seconds, strongly hinting at frequent barrel knocks. Such a tendency can complicate training and competition, as the rider must continually account for and correct these errors, potentially diminishing confidence and consistency in performance.")
    else:
        message.append("We also examine if the horse could be considered a 'paleteador', meaning a horse that often knocks barrels or incurs technical penalties. In reviewing its performance, there is no significant pattern suggesting that the horse frequently knocks barrels or accumulates penalty-inducing errors. Without these problematic patterns, the horse maintains cleaner runs, reducing the frustration and difficulty associated with correcting repeated mistakes. This absence of penalty-prone behavior makes the horse’s performance more predictable in technical scenarios and helps maintain the rider’s confidence.")

    # 4. Average time vs. desired time
    if avg_time is not None:
        diff = abs(avg_time - desired_time)
        if diff > 1:
            message.append(f"Finally, we assess how the horse’s average time aligns with your desired target. The average race time we calculated is {avg_time:.2f}s, while your goal is around {desired_time:.2f}s. The difference here is approximately {diff:.2f}s, which is significant. A horse performing notably faster or slower than your ideal time may require additional training, adjustments in technique, or rethinking your strategy to meet your objectives. Such a discrepancy can mean extra effort to bridge the gap, either by working to increase the horse’s speed if it’s too slow, or refining technique and precision if it’s too fast.")
        else:
            message.append(f"Finally, we compare the horse’s average time to your desired target. The horse’s average race time is {avg_time:.2f}s, and your desired time is approximately {desired_time:.2f}s. With a difference of only {diff:.2f}s, the horse’s performance closely aligns with what you’re aiming for. This near-match suggests that only minor adjustments, such as slight tweaks to riding technique or incremental conditioning, might be needed to fully achieve your time goal. Starting from a point so close to your target reduces the trial-and-error element and can accelerate your path to optimal performance.")
    else:
        message.append("Finally, we attempted to evaluate the horse’s average time against your desired target. Unfortunately, due to the lack of sufficient or reliable data, we were unable to accurately calculate an average race time. Without this metric, it’s harder to gauge how much the horse’s baseline performance might deviate from what you hope to achieve. Additional data collection or careful observation of more runs would be necessary to draw meaningful conclusions on this point.")

    # Now proceed with the original user profile logic and conditional messages (unchanged):

    if user_profile == "iniciante":
        if not constant:
            message.append("Unfortunately, this horse does not maintain consistent performance across its runs. As a beginner rider, consistency in a horse’s performance is crucial. When a horse is constant, its times and behavior are more predictable, making it easier for you to learn, adapt, and gradually improve your skills. Since this horse varies significantly from one run to another, it may create confusion and a steeper learning curve for you at this stage. We recommend considering a more consistent horse to help build your confidence and foundational riding abilities.")
        if not constant_with_var:
            message.append("Upon reviewing this horse's performance, it seems that it is only consistent when ridden by a specific individual. This suggests that the horse may have developed a strong bond or understanding with that rider, making it less adaptable to others. For a beginner, this can be particularly challenging, as the horse may respond unpredictably to new handling styles or riding techniques. As a beginner, it’s important to choose a horse that demonstrates consistent behavior with a variety of riders, as this indicates greater adaptability and reliability. We recommend considering a different horse that has shown steady performance with amateur riders, which will help you build confidence and skills more effectively. Additionally, if you're still interested in this horse, you might want to learn about the specific rider’s techniques to see if they can be incorporated into your training.")
        if paleteador:
            message.append("After analyzing its performance records, I noticed some patterns that suggest it may be what we call a paleteador. The first indication comes from the several runs recorded with 0 points and 0 seconds. This often indicates SAT (Sem aproveitamento técnico), meaning there were issues like disqualification during the run, commonly caused by knocking over barrels. Additionally, the results show two distinct groups of times: one consistent baseline (e.g., time X) and another group with a consistent addition of approximately 5 seconds to that baseline. This pattern strongly suggests that the horse often knocks barrels, leading to penalties or disqualifications. For an amateur just starting out, a horse prone to knocking barrels can present significant challenges. Frequent errors like these can lead to frustration and undermine confidence, which is something to avoid at the beginning of your journey. I’d recommend considering a horse with a more consistent performance history to ensure a positive and confidence-building experience in your initial competitions. ")
        if avg_time is not None:
            diff = abs(avg_time - desired_time)
            if diff > 1:
                message.append(f"The avarage race time of the horse ({avg_time:.2f}s) difers a lot form what you want ({desired_time:.2f}s).")

        if not [m for m in message if "Unfortunately," in m or "Upon reviewing" in m or "After analyzing its performance records" in m or "The avarage race time" in m]:
            message.append("Good news! After analyzing the horse's performance, we can confirm that it is stable when ridden by different people, demonstrating consistent behavior regardless of the rider. Additionally, it does not exhibit characteristics of a 'paleteador,' meaning it completes clean, smooth turns around the barrels without making unnecessary extra movements. Even better, its average time aligns closely with the range you are looking for, making it a strong match for your needs. This consistency and reliability make it a great option for building confidence and achieving your goals, whether you’re competing or training.")

    elif user_profile == "intermediaria":
        if not constant:
            message.append("Unfortunately, this horse does not maintain consistent performance across its runs. As a intermediary rider, consistency in a horse’s performance is crucial. When a horse is constant, its times and behavior are more predictable, making it easier for you to learn, adapt, and gradually improve your skills. Since this horse varies significantly from one run to another, it may create confusion and a steeper learning curve for you at this stage. We recommend considering a more consistent horse to help build your confidence and foundational riding abilities.")
        elif not constant_with_var:
            message.append("After analyzing the horse's performance, we noticed that it is consistent only with a specific rider. This likely indicates that the horse has developed a unique bond or understanding with that individual, which could make it harder for the horse to adapt to other riders. While this isn’t necessarily a problem, it is a point of caution, especially if the next rider has a different riding style or experience level. It may be worth observing how the horse performs in training sessions with other riders before making a final decision.")
        
        if paleteador:
            message.append("After analyzing its performance records, I noticed some patterns that suggest it may be what we call a paleteador. The first indication comes from the several runs recorded with 0 points and 0 seconds. This often indicates SAT (Sem aproveitamento técnico), meaning there were issues like disqualification during the run, commonly caused by knocking over barrels. Additionally, the results show two distinct groups of times: one consistent baseline (e.g., time X) and another group with a consistent addition of approximately 5 seconds to that baseline. This pattern strongly suggests that the horse often knocks barrels, leading to penalties or disqualifications. For an amateur just starting out, a horse prone to knocking barrels can present significant challenges. Frequent errors like these can lead to frustration and undermine confidence, which is something to avoid at the beginning of your journey. I’d recommend considering a horse with a more consistent performance history to ensure a positive and confidence-building experience in your initial competitions. ")
        
        if avg_time is not None:
            diff = abs(avg_time - desired_time)
            if diff > 1:
                message.append(f"The avarage race time of the horse ({avg_time:.2f}s) difers a lot form what you want ({desired_time:.2f}s).")

        if not [m for m in message if "Unfortunately," in m or "After analyzing the horse's performance" in m or "After analyzing its performance records" in m or "The avarage race time" in m]:
            message.append("Good news! After analyzing the horse's performance, we can confirm that it is stable when ridden by different people, demonstrating consistent behavior regardless of the rider. Additionally, it does not exhibit characteristics of a 'paleteador,' meaning it completes clean, smooth turns around the barrels without making unnecessary extra movements. Even better, its average time aligns closely with the range you are looking for, making it a strong match for your needs. This consistency and reliability make it a great option for building confidence and achieving your goals, whether you’re competing or training.")

    elif user_profile in ["avancada", "profissional"]:
        message.append("You already have enough experience. Here are the characteristics of the analyzed horse. We will leave the interpretation of this data and decision-making to you. We trust that, at your stage of riding, you will be able to interpret the information and make the best possible decision on your own.")
        message.append(f"- Constant: {'Yes' if constant else 'No'}")
        message.append(f"- Constant with different competitors: {'Yes' if constant_with_var else 'No'}")
        message.append(f"- Paleteador: {'Yes' if paleteador else 'No'}")
        if avg_time is not None:
            message.append(f"- Avarage time: {avg_time:.2f}s (Desired Time): {desired_time:.2f}")
        else:
            message.append("- Avarege time: Error")
        message.append("If you need a more detailed explanation of how we analyzed these points, feel free to send an email to tommatarazzo7@gmail.com.")

    return "\n".join(message)
