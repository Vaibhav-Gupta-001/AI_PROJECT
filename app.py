import json
from flask import Flask, render_template_string, request, jsonify

# --- EXPERT SYSTEM CORE LOGIC ---
# The rules are now divided into Tier 1 (3 conditions) and Tier 2 (2 conditions) for targeted searching.
# The Tier 2 set is minimized to prevent repetitive fallbacks, pushing more unmatched searches to the "Sorry!" message.

# TIER 1: Highly specific rules (3 conditions) - Highest match quality.
Tiers1_Rules = [
    # Electronics/Tech (Specific Focus) - EXPANDED TO COVER COMMON GAPS
    {"Product": "High-End Gaming Laptop (e.g., ROG, Alienware)", "Conditions": {"electronics", "high", "gaming"}},
    {"Product": "Compact Mirrorless Camera Kit (e.g., Sony a6000 series)", "Conditions": {"electronics", "high", "photography"}},
    {"Product": "Studio Monitor Headphones (e.g., Sennheiser HD 660S)", "Conditions": {"electronics", "high", "music"}},
    {"Product": "Premium Noise-Cancelling Headphones (e.g., Sony/Bose)", "Conditions": {"electronics", "high", "general"}}, 
    {"Product": "Advanced Running Watch with GPS (e.g., Garmin Fenix)", "Conditions": {"electronics", "high", "running"}}, 
    {"Product": "Premium E-Ink Tablet (e.g., reMarkable, high-end Kindle)", "Conditions": {"electronics", "high", "reading"}}, 
    
    {"Product": "Mid-Range Smartphone (e.g., Pixel A-series, Samsung A-series)", "Conditions": {"electronics", "medium", "general"}},
    {"Product": "VR Headset and Content Bundle (e.g., Meta Quest 3)", "Conditions": {"electronics", "medium", "gaming"}},
    {"Product": "Advanced Drone for Aerial Photos (e.g., DJI Mini 4 Pro)", "Conditions": {"electronics", "medium", "photography"}},
    {"Product": "Budget Wireless Headphones (e.g., Anker Soundcore)", "Conditions": {"electronics", "low", "general"}},
    {"Product": "Basic E-Reader (e.g., Kindle Basic)", "Conditions": {"electronics", "low", "reading"}},
    
    # Education/Learning (Specific Focus)
    {"Product": "University Degree Program Enrollment (e.g., Online MBA)", "Conditions": {"education", "high", "general"}},
    {"Product": "Executive Coaching Program (e.g., specialized mentorship)", "Conditions": {"education", "high", "learning"}},
    {"Product": "Foreign Language Immersion Software (e.g., Babbel, Duolingo Premium)", "Conditions": {"education", "high", "culture"}},
    {"Product": "Advanced Python Course (e.g., Coursera specialization, Udemy advanced)", "Conditions": {"education", "medium", "learning"}},
    {"Product": "Music Production Software (e.g., Ableton Live Lite, GarageBand)", "Conditions": {"education", "medium", "music"}},
    {"Product": "E-Book Subscription Service (e.g., Kindle Unlimited, Scribd)", "Conditions": {"education", "low", "reading"}},
    {"Product": "Free Language Exchange App Membership (e.g., HelloTalk Pro)", "Conditions": {"education", "low", "culture"}},
    
    # Health/Wellness (Specific Focus)
    {"Product": "Personalized Meal Prep Service (e.g., HelloFresh, Blue Apron)", "Conditions": {"health", "high", "general"}},
    {"Product": "Marathon Training Plan (e.g., Nike Run Club Pro Plan)", "Conditions": {"health", "high", "running"}},
    {"Product": "Advanced Home Gym Equipment (e.g., Bowflex, Peloton)", "Conditions": {"health", "high", "fitness"}},
    {"Product": "GPS Smartwatch for Running (e.g., Apple Watch, Coros)", "Conditions": {"health", "medium", "running"}},
    {"Product": "Smart Fitness Tracker (e.g., Garmin, Fitbit)", "Conditions": {"health", "medium", "fitness"}},
    {"Product": "Personal Safety Alarm (e.g., SABRE Personal Alarm)", "Conditions": {"health", "low", "general"}},
    {"Product": "Resistance Band Set and Home Workout Guide", "Conditions": {"health", "low", "fitness"}},
    
    # Finance/Investment (Specific Focus)
    {"Product": "Private Financial Consulting Session (e.g., Certified Planner Meeting)", "Conditions": {"finance", "high", "learning"}},
    {"Product": "Robo-Advisor Investment App (e.g., Betterment, Wealthfront)", "Conditions": {"finance", "high", "investment"}},
    {"Product": "Stock Market Analysis Software Subscription (e.g., TradingView Pro)", "Conditions": {"finance", "medium", "investment"}},
    {"Product": "Retirement Planning Guide (e.g., Vanguard, Fidelity guides)", "Conditions": {"finance", "low", "learning"}},
    
    # Travel/Adventure (Specific Focus)
    {"Product": "Guided Mountaineering Expedition Package (e.g., Everest Base Camp)", "Conditions": {"travel", "high", "adventure"}},
    {"Product": "Premium Travel Insurance and Concierge Service", "Conditions": {"travel", "high", "general"}},
    {"Product": "Durable Travel Backpack (e.g., Osprey Farpoint, Peak Design)", "Conditions": {"travel", "medium", "adventure"}},
    {"Product": "City Walking Tour App Subscription (e.g., Rick Steves audio guides)", "Conditions": {"travel", "low", "culture"}},

    # Creative/Art (Specific Focus)
    {"Product": "Art Portfolio Review and Masterclass (e.g., high-end mentorship)", "Conditions": {"creative", "high", "general"}},
    {"Product": "Professional Drawing Tablet (e.g., Wacom Intuos Pro)", "Conditions": {"creative", "high", "art"}},
    {"Product": "Photo Editing Software Subscription (e.g., Adobe Photoshop/Lightroom)", "Conditions": {"creative", "medium", "photography"}},
    {"Product": "Basic MIDI Keyboard Controller (e.g., Akai MPK Mini)", "Conditions": {"creative", "low", "music"}},
    {"Product": "Beginner Watercolor Set (e.g., Winsor & Newton Cotman set)", "Conditions": {"creative", "low", "art"}},
]

# TIER 2: Broader rules (2 conditions: Domain + Priority) - Minimal, generic fallbacks only.
# If these fallbacks are triggered, they return a generic, non-specific suggestion.
Tiers2_Rules = [
    # Electronics Fallback (only for the least covered priority)
    {"Product": "General Electronics Accessory Guide (Fallback)", "Conditions": {"electronics", "low"}},
    
    # Education Fallbacks (only for high/medium where focus is unusual)
    {"Product": "High-Value Learning Resource Access (Fallback)", "Conditions": {"education", "high"}},
    {"Product": "Balanced Educational Materials Kit (Fallback)", "Conditions": {"education", "medium"}},

    # Health Fallback
    {"Product": "Essential Wellness Starter Kit (Fallback)", "Conditions": {"health", "low"}},
    
    # Finance Fallback
    {"Product": "General Investment Strategy E-Book (Fallback)", "Conditions": {"finance", "medium"}},
    
    # Travel Fallback
    {"Product": "Global Travel Preparation Checklist (Fallback)", "Conditions": {"travel", "medium"}},

    # Creative Fallback
    {"Product": "Online Creative Portfolio Hosting (Fallback)", "Conditions": {"creative", "medium"}},
]


def recommend(preferences):
    """
    Expert System recommendation function.
    Searches first for Tier 1 (3-condition) match, then Tier 2 (2-condition) match.
    """
    preferences_set = set(p.lower() for p in preferences)
    
    # Identify the input domain to send back for icon selection
    input_domain = next((p for p in preferences_set if p in ["electronics", "education", "health", "finance", "travel", "creative"]), "general")
    
    # Print the user's signature/watermark as requested
    print("VAIBHAV GUPTA, 408, 3AIML-B - Recommendation Query\n") 
    print(f"User Preferences: {', '.join(preferences_set)}")

    # 1. Search for Tier 1 (Specific, 3-condition match)
    for rule in Tiers1_Rules:
        if rule["Conditions"].issubset(preferences_set):
            print(f"Match found (Tier 1): {rule['Product']} (Required conditions: {', '.join(rule['Conditions'])})")
            return rule["Product"], input_domain
    
    # 2. Search for Tier 2 (Broad, 2-condition match)
    for rule in Tiers2_Rules:
        if rule["Conditions"].issubset(preferences_set):
            print(f"Match found (Tier 2): {rule['Product']} (Required conditions: {', '.join(rule['Conditions'])})")
            return rule["Product"], input_domain
    
    # 3. If no Tier 1 or Tier 2 match is found (the 20% failure case).
    print("No specific (Tier 1 or Tier 2) product found. Returning generic no-match signal.")
    return "No matching product found", input_domain

# --- FLASK APPLICATION SETUP ---

app = Flask(__name__)

# To serve the single-file HTML frontend (index.html)
def get_frontend_html():
    """Reads the content of the single-file frontend."""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Error: index.html not found! Please ensure it is in the same directory.</h1>"


@app.route('/')
def home():
    """Renders the main single-page application frontend."""
    # This assumes index.html is in the same directory as app.py
    return get_frontend_html()

@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    """API endpoint to receive user preferences and return a recommendation."""
    try:
        data = request.get_json()
        if not data or 'domain' not in data or 'importance' not in data or 'focus' not in data:
            return jsonify({"error": "Missing required preference data"}), 400

        # Extract preferences from the JSON payload
        domain = data.get('domain', '').strip()
        importance = data.get('importance', '').strip()
        focus = data.get('focus', '').strip()

        # Compile all preferences into a list for the recommend function
        user_preferences = [domain, importance, focus]
        
        # Get the recommendation and the domain
        recommended_product, matched_domain = recommend(user_preferences)
        
        # Return the result as JSON, including the domain for the icon
        return jsonify({
            "recommendation": recommended_product,
            "domain": matched_domain
        })

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An internal server error occurred during recommendation."}), 500

if __name__ == '__main__':
    # Running on localhost:5000 by default
    app.run(debug=True)
