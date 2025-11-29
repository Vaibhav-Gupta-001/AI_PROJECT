Project Title:
Rule-Based Expert System for Product Recommendation

Abstract (Short & Clear):
This project implements a Rule-Based Expert System using Python (Flask) and a custom HTML + TailwindCSS frontend.
The system takes three inputs from the user:

-> Domain / Category
-> Budget Priority
-> Focus / Activity

Based on these inputs, it applies Tier-1 (specific) and Tier-2 (fallback) rules to generate a suitable recommendation.

Objective:

-> To design a lightweight expert system that recommends items using if–then rules instead of machine learning.
-> To demonstrate how knowledge representation, rule matching, and inference work in AI.
-> To build a simple web interface for user interaction.

System Overview:

The system works in three main steps:
-> User gives preferences → (domain, importance, focus)
-> System compares preferences with stored rule-base
-> Most matching rule → Recommendation Returned

✨ HOW THE RULE BASE WORKS
Tier 1 Rules (High Priority / Accurate Match) :

Each rule contains 3 conditions
If user’s inputs match all 3 → Direct recommendation
These are highly specific
Example:
electronics + high + gaming → High-End Gaming Laptop

Tier 2 Rules (Fallback / General Match) :

Each rule contains 2 conditions
Used only when no Tier-1 rule matches
Example:
education + medium → Balanced Educational Materials Kit

No Match Case:

If neither Tier 1 nor Tier 2 matches →
"No matching product found"

🚀 HOW THE RECOMMEND FUNCTION WORKS
def recommend(preferences):
    preferences_set = set(p.lower() for p in preferences)


✔ Converts input to lowercase and set → easy matching.

Step 1: Identify the main domain for UI icons

It checks which domain the user selected so the frontend can show a matching icon.

Step 2: Search Tier 1 Rules

It loops through all Tier-1 rules and checks:

if rule["Conditions"].issubset(preferences_set):
        return rule["Product"]


✔ If all 3 conditions match → Immediate output.

Step 3: Search Tier 2 Rules

If Tier-1 fails, it tries broader 2-condition rules.

Step 4: No Result

If no rule matches →
return "No matching product found"

🖥 FLASK BACKEND (Simple Explanation)
Route 1: /

Loads the index.html file (your frontend).

Route 2: /api/recommend (POST API)

Receives the 3 user inputs in JSON

Calls the recommend() function

Returns output as JSON:

{
  "recommendation": "...",
  "domain": "..."
}

🎨 FRONTEND (index.html) — College Level Explanation

Fully built using Tailwind CSS

Contains 3 dropdowns for user input

Uses fetch() API to send data to Flask

Displays the recommendation in a styled card

Has a modern UI but still simple and static (no frameworks)

📂 TECHNOLOGIES USED
Backend:

Python 3

Flask Framework

Rule-Based Logic

Frontend:

HTML

Tailwind CSS

JavaScript

SVG icons

📌 ADVANTAGES (Short Points)

Simple and fast

No training required (unlike ML models)

Easy to add or modify rules

Works offline (rule-based)

Clear explainable logic

📌 LIMITATIONS

Cannot handle ambiguous/unexpected user input

Recommendations are limited to the rules defined

Not adaptive (doesn’t learn over time)

📚 Applications

Product recommendation

Career guidance

Basic medical expert systems

Loan eligibility systems

Smart assistant rule engines
