import streamlit as st
import streamlit.components.v1 as components

st.title("Healthcare Agent Services")

bot_secret = "7tlWEiTwjIsOKxLgdo8WIviFNEBBdoivYIp7CFYYIV0j8NBe7GTQJQQJ99BBACHYHv6AArohAAABAZBS75uW.2IVzK9IgeeE2AJBZVUWnugQoBPjOLlC1gTZJaKAGK3XCIg1XonDDJQQJ99BBACHYHv6AArohAAABAZBS4DZr"

# HTML + JavaScript for embedding the bot with enhanced UI
bot_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Healthcare Agent Services</title>
    <script src="https://cdn.botframework.com/botframework-webchat/latest/webchat.js"></script>
    <style>
        body {{
            font-family: 'Roboto', sans-serif;
            margin: 0;
            padding: 0;
            background: #f4f7f6;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            box-sizing: border-box;
        }}
        .chat-container {{
            background-color: #ffffff;
            width: 400px;
            max-width: 100%;
            height: 600px;
            border-radius: 10px;
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);
            display: flex;
            flex-direction: column;
            padding: 20px;
        }}
        .header {{
            background-color: #0078D4;
            color: white;
            text-align: center;
            padding: 10px 0;
            font-size: 18px;
            font-weight: bold;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        #webchat {{
            flex-grow: 1;
            border-radius: 8px;
            overflow: hidden;
        }}
        .webchat-container {{
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            height: 100%;
        }}
        .webchat-container .wc-send-box {{
            background-color: #f1f1f1;
            border-top: 1px solid #ddd;
            padding: 10px;
            border-radius: 5px;
        }}
        .wc-send-box input {{
            width: 100%;
            padding: 10px;
            font-size: 14px;
            border-radius: 5px;
            border: 1px solid #ddd;
        }}
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="header">
            Healthcare Assistant
        </div>
        <div class="webchat-container">
            <div id="webchat" role="main"></div>
            <script>
                (async function() {{
                    const store = window.WebChat.createStore({{}}, function({{
                        dispatch
                    }}) {{
                        return function(next) {{
                            return function(action) {{
                                return next(action);
                            }};
                        }};
                    }});

                    const res = await fetch("https://directline.botframework.com/v3/directline/tokens/generate", {{
                        method: "POST",
                        headers: {{
                            "Authorization": "Bearer {bot_secret}",
                            "Content-Type": "application/json"
                        }}
                    }});

                    const data = await res.json();
                    const token = data.token;

                    window.WebChat.renderWebChat({{
                        directLine: window.WebChat.createDirectLine({{ token }}),
                        userID: "user123",
                        username: "User",
                        locale: "en-US",
                        styleOptions: {{
                            bubbleBackground: "#e6f7ff",
                            bubbleFromUserBackground: "#0078D4",
                            bubbleFromUserTextColor: "#ffffff",
                            suggestedActionBorder: "1px solid #0078D4",
                            primaryFont: "'Roboto', sans-serif",
                            botAvatarBackgroundColor: "#0078D4",
                            userAvatarBackgroundColor: "#f1f1f1"
                        }}
                    }}, document.getElementById("webchat"));
                }})();
            </script>
        </div>
    </div>
</body>
</html>
"""

# Embed the enhanced bot UI in Streamlit
components.html(bot_html, height=700, scrolling=True)
