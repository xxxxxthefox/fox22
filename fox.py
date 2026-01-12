import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # السماح لأي موقع بالوصول، بما في ذلك Roblox HttpService

@app.route("/", methods=["GET"])
def home():
    return "🚀 KidzApp Spam Checker API is Running!"

@app.route("/spamcheck/<email>", methods=["GET"])
def spamcheck_email(email):
    try:
        email = email.strip()
        if not email:
            return jsonify({"status": "failed", "message": "No email provided"}), 400

        # منع بريد معين
        if email.lower() == "xxxxxthefox@gmail.com":
            return jsonify({
                "status": "failed",
                "email": email,
                "sent": False,
                "message": "🚫 This email is blocked."
            })

        headers = {
            'authority': 'api.kidzapp.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-AU,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
            'client-version': 'kidzapp, web, 3.3.5',
            'content-type': 'application/json',
            'kidzapp-platform': 'web',
            'origin': 'https://kidzapp.com',
            'referer': 'https://kidzapp.com/',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        }

        json_data = {
            'email': email,
            'sdk': 'web',
            'platform': 'desktop',
        }

        response = requests.post(
            'https://api.kidzapp.com/api/3.0/customlogin/',
            headers=headers,
            json=json_data,
            timeout=15
        ).text

        if 'EMAIL SENT' in response:
            return jsonify({
                "status": "success",
                "email": email,
                "sent": True,
                "message": "✅ Email sent successfully!"
            })
        else:
            return jsonify({
                "status": "failed",
                "email": email,
                "sent": False,
                "message": "❌ Email was NOT sent."
            })

    except Exception as e:
        return jsonify({
            "status": "error",
            "email": email,
            "sent": False,
            "message": f"⚠️ Error occurred: {str(e)}"
        }), 500

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
