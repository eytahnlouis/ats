from .parsing import extract_text_from_file
import os
#lines  = [ x for x in open("backend/cvs/score.txt").readlines() if x.strip() != ""] #ligne test, à changer avec commande finale. Objectif : recupérer les notes données par les recruteurs
lines = [] #Ligne test, à changer avec commande finale. Objectif : recupérer les notes données par les recruteurs
keywords = {line.split(',')[0]: int(line.split(',')[1]) for line in lines}
total_score = sum(keywords.values()) # Calculate the total score based on keywords
def score_resume(resume_text):
    """
    Scores a resume based on the presence of keywords.
    """
    score = 0
    for keyword, points in keywords.items():
        if keyword.lower() in resume_text.lower():
            score += points
    return score

if __name__ == "__main__":
    while True:
        try:
            score = score_resume(extract_text_from_file) # Score the resume
            if score >= total_score * 0.5: # Check if the score is above 50% of the total score
                print("Resume is a good match.")
            else:
                print("Resume is not a good match.")
        # Print the score
            print(f"Score: {score}/{total_score}")
        # Print the total score
            print(f"Total Score: {total_score}")
            break
        except Exception as e:
            print(f"An error occurred: {e}") # Print any errors that occur