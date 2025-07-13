from pymongo import MongoClient
import pandas as pd
import json

# CONFIG
MONGODB_URI=""
PRE_PILOT_DB=""
PILOT_DB=""
COLLECTION_SUB = "submissions"
COLLECTION_PROB = "problems"

def extract_submissions(db_name, client):
    db = client[db_name]
    sub_col = db[COLLECTION_SUB]
    prob_col = db[COLLECTION_PROB]

    # Build a lookup map from problem_id → problem details
    problems_lookup = {
        prob["problem_id"]: prob
        for prob in prob_col.find()
    }

    rows = []
    for item in sub_col.find():
        problem_id = item.get("problem_id")
        problem_data = problems_lookup.get(problem_id, {})

        user_input = item.get("user_input", [])
        input_text_or_link = ""
        if user_input and isinstance(user_input, list):
            first_input = user_input[0]
            if first_input["type"] == "text":
                input_text_or_link = first_input.get("text", "")
            elif first_input["type"] == "image_url":
                input_text_or_link = first_input.get("image_url", {}).get("url", "")
            elif first_input["type"] == "file_input":
                input_text_or_link = first_input.get("file", {}).get("file_id", "")

        full_feedback = item.get("full_feedback", {})
        full_feedback_json = json.dumps(full_feedback, indent=2)

        row = {
            "Memberstack id": item.get("memberstack_user_id", ""),
            "Timestamp": item.get("time", ""),
            "Problem statement": problem_data.get("problem_statement", ""),
            "Problem id": problem_id,
            "Correct solution(s)": problem_data.get("correct_solutions", ""),
            "Input_solution": input_text_or_link,
            "Overall grade": item.get("overall_grade", ""),
            "Model feedback[Sanity Reruns]": full_feedback.get("Sanity_Statuses_Reruns", ""),
            "Model feedback[Validity Reruns]": full_feedback.get("Validity_Grades_Reruns", ""),
            "Model feedback[Quality Reruns]": full_feedback.get("Quality_Grades_Reruns", ""),
            "Model feedback[major conceptual errors]": full_feedback.get("Major_Conceptual_Errors", ""),
            "Model feedback[unjustified claims]": full_feedback.get("Nontrivial_Mistakes_or_Unjustified_Claims", ""),
            "Full Model feedback": full_feedback_json
        }
        rows.append(row)

    return pd.DataFrame(rows)

def main():
    client = MongoClient(MONGODB_URI)

    print("Extracting Pre-Pilot submissions...")
    df_pre = extract_submissions(PRE_PILOT_DB, client)
    df_pre.to_csv("pre_pilot.csv", index=False)
    print("Saved to pre_pilot.csv")

    print("Extracting Pilot submissions...")
    df_pilot = extract_submissions(PILOT_DB, client)
    df_pilot.to_csv("pilot.csv", index=False)
    print("Saved to pilot.csv")

if __name__ == "__main__":
    main()