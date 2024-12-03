import random
from flask import Flask, render_template_string, request, session

app = Flask(__name__)

# Set a secret key for sessions (required for Flask session functionality)
app.secret_key = "your_secret_key"


@app.route("/", methods=["GET", "POST"])
def number_guessing():
    # Initialize session variables if they don't exist
    if "score" not in session:
        session["score"] = 5  # starting score
    if "number" not in session:
        session["number"] = random.randint(1, 100)  # random number to guess

    score = session["score"]
    number = session["number"]
    message = "Guess the correct number between 1 and 100."

    if request.method == "POST":
        try:
            guess = int(request.form["guess"])
        except ValueError:
            message = "Please enter a valid number."
        else:
            if guess > 100 or guess < 1:
                session["score"] -= 1
                score = session["score"]
                message = f"Your guess is out of range. You lost a chance. Score: {score}"
            elif guess == number:
                message = f"Congratulations! YOU WON!!! Final Score: {score}"
                session.pop("score", None)  # Clear score after winning
                session.pop("number", None)  # Clear the number after winning
            elif guess < number:
                session["score"] -= 1
                score = session["score"]
                message = f"Your guess was too low. Try a higher number. Score: {score}"
            elif guess > number:
                session["score"] -= 1
                score = session["score"]
                message = f"Your guess was too high. Try a lower number. Score: {score}"

            if score == 0:
                message = "Game Over! You lost."
                session.pop("score", None)  # Clear score
                session.pop("number", None)  # Clear the number

    return render_template_string("""
        <html>
            <body>
                <h2>{{ message }}</h2>
                <form method="POST">
                    <input type="number" name="guess" required>
                    <button type="submit">Submit Guess</button>
                </form>
            </body>
        </html>
    """, message=message)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
