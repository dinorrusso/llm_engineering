import gradio as gr
import ollama

OLLAMA_MODEL= "llama3.2"


def format_history(message, history, system_prompt):
    chat_history = [{"role": "system", "content" : system_prompt}]
    for query, response in history:
        chat_history.append({"role": "system", "content" : query})
        chat_history.append({"role": "assistant", "content" : response})
    chat_history.append({"role": "user", "content" : message})
    return chat_history

def generate_ollama_response(message, history, system_prompt):
    chat_history = format_history(message, history, system_prompt)
    response = ollama.chat(model = OLLAMA_MODEL, stream=True, messages=chat_history)
    message=""
    #stream/typewritter effect
    for partial_response in response: 
        token = partial_response["message"]["content"]
        message += token
        yield message



chatbot = gr.ChatInterface(
    generate_ollama_response,
    chatbot = gr.Chatbot(
        avatar_images=["user.jpg", "chatbot.png"],
        height="64vh"
    ),
    additional_inputs=[
        gr.Textbox("act as personal assitant",
                    label="System Prompt" )
    ],
    title = OLLAMA_MODEL + " Chatbot using ollama module",
    description="Ask a question.",
    theme="soft",
    submit_btn="⬅ Send"
)
chatbot.launch()