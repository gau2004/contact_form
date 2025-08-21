from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

FILE_NAME = "messages.txt"

# Load existing messages from file
def load_messages():
    try:
        with open(FILE_NAME, "r") as f:
            lines = f.readlines()
            return [eval(line.strip()) for line in lines]  # convert string → dict
    except FileNotFoundError:
        return []

# Save new message to file
def save_message(msg):
    with open(FILE_NAME, "a") as f:
        f.write(str(msg) + "\n")

# Clear all messages from file
def clear_messages():
    open(FILE_NAME, "w").close()  # empty file

messages = load_messages()

@app.route("/", methods=["GET", "POST"])
def home():
    global messages
    if request.method == "POST":
        if "clear" in request.form:  # Clear button clicked
            clear_messages()
            messages = []
            return redirect(url_for("home"))
        else:
            name = request.form["name"]
            msg = request.form["message"]
            new_msg = {"name": name, "message": msg}
            messages.append(new_msg)
            save_message(new_msg)   # save to file
    return render_template("contact.html", messages=messages)

if __name__ == "__main__":
    app.run(debug=True)
