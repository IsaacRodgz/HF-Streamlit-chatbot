import requests
import streamlit as st
from streamlit_chat import message as st_message
#from transformers import BlenderbotTokenizer
#from transformers import BlenderbotForConditionalGeneration

API_URL = "https://api-inference.huggingface.co/models/allenai/cosmo-xl"
headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}


@st.experimental_singleton
def get_models():
    # it may be necessary for other frameworks to cache the model
    # seems pytorch keeps an internal state of the conversation
    #model_name = "facebook/blenderbot-400M-distill"
    #tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
    #model = BlenderbotForConditionalGeneration.from_pretrained(model_name)
    #return tokenizer, model
    return None, None

if "history" not in st.session_state:
    st.session_state.history = []

st.title("Hello Chatbot")


def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()


def generate_answer():
    #tokenizer, model = get_models()

    if len(st.session_state.input_text) == 0 or not st.session_state.input_text:
         return "It seems like you didn't write anything..."

    user_message = st.session_state.input_text

    user_history = [m["message"] for m in st.session_state.history if m["is_user"]]
    bot_history = [m["message"] for m in st.session_state.history if not m["is_user"]]

    output = query({
        "inputs": {
            "past_user_inputs": user_history,
            "generated_responses": bot_history,
            "text": st.session_state.input_text
        },
    })

    print(output)
    
    #inputs = tokenizer(st.session_state.input_text, return_tensors="pt")
    #result = model.generate(**inputs)
    #message_bot = tokenizer.decode(
    #    result[0], skip_special_tokens=True
    #)  # .replace("<s>", "").replace("</s>", "")
    
    if "error" in output:
         return "What did you say?"

    message_bot = output["generated_text"]

    st.session_state.history.append({"message": user_message, "is_user": True})
    st.session_state.history.append({"message": message_bot, "is_user": False})


st.text_input("Talk to the bot", key="input_text", on_change=generate_answer)

for chat in st.session_state.history:
    st_message(**chat)  # unpacking
