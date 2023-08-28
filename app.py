from flask import Flask, request, render_template
import datetime
import json

app = Flask(__name__)

# Store user interactions and assessment data in memory (for demo purposes)
user_interactions = {}
user_assessment_data = {}


def assess_mental_health(interactions):
    # Placeholder logic for mental health assessment
    # You should use actual assessment tools for accurate results
    total_interactions = len(interactions)
    stress_level = total_interactions % 5  # Placeholder stress calculation
    return stress_level


@app.route('/', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        user_message = request.form['user_message']
        user_id = request.form['user_id']

        # Store user interactions
        if user_id not in user_interactions:
            user_interactions[user_id] = []
        user_interactions[user_id].append((datetime.datetime.now(), user_message))

        # Assess mental health and store assessment data
        stress_level = assess_mental_health(user_interactions[user_id])
        if user_id not in user_assessment_data:
            user_assessment_data[user_id] = {
                'stress_levels': [],
                'last_assessment': None
            }
        user_assessment_data[user_id]['stress_levels'].append((datetime.datetime.now(), stress_level))
        user_assessment_data[user_id]['last_assessment'] = datetime.datetime.now()

        # Generate chatbot response (dummy response for illustration)
        bot_response = "It sounds like you've been chatting a lot. Remember to take breaks and practice self-care."

        return render_template('index.html', bot_response=bot_response)

    return render_template('index.html', bot_response=None)


@app.route('/analysis/<user_id>', methods=['GET'])
def analysis(user_id):
    if user_id in user_assessment_data:
        assessment_data = user_assessment_data[user_id]
        # Perform in-depth analysis and generate report (dummy report for illustration)
        analysis_report = {
            'total_interactions': len(user_interactions[user_id]),
            'average_stress_level': sum(level for _, level in assessment_data['stress_levels']) / len(
                assessment_data['stress_levels'])
        }
        return json.dumps(analysis_report, indent=4)
    else:
        return "User not found"


if __name__ == '__main__':
    app.run(debug=True)
