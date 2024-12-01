import streamlit as st
import google.generativeai as genai
from utils import response_generator, role_to_streamlit
from PIL import Image
import io

# Display Form Title
st.title("Gemini Chatbot")

# Add API key to session state
if "api_key" not in st.session_state:
    api_key = st.secrets['api']['api_key']
    if api_key:
        st.session_state.api_key = api_key

try:
    genai.configure(api_key = st.session_state.api_key)
except AttributeError as e:
    st.warning("Provide Gemini API Key")

model = genai.GenerativeModel('gemini-1.5-pro')

# Add a Gemini Chat history object to Streamlit session state
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

uploaded_file = st.file_uploader("Load file: ")
# Process the uploaded file
if uploaded_file:
    try:
        # Convert the uploaded file to a PIL Image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
    except Exception as e:
        st.error(f"Failed to process the uploaded file: {e}")
        image = None

# Display chat messages from history above current input box
for message in st.session_state.chat.history:
    with st.chat_message(role_to_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Accept user's next message, add to context, resubmit context to Gemini
if prompt := st.chat_input("Enter message"):
    # Display user's last message
    st.chat_message("user").markdown(prompt)

    # Display last
    with st.chat_message("assistant"):
        # Send user entry to Gemini and read the response
        if image:
            response = st.session_state.chat.send_message([prompt, image])
        else:
            response = st.session_state.chat.send_message(prompt)

        st.write_stream(response_generator(response))

