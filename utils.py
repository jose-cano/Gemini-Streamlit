import time

# Streamed response emulator
def response_generator(response):

    for word in response.text.split(" "):
        yield word + " "
        time.sleep(0.05)

# Gemini uses 'model' for assistant; Streamlit uses 'assistant'
def role_to_streamlit(role):
    if role == "model":
        return "assistant"
    else:
        return role