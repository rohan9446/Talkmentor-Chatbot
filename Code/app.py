import os
import openai

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse



app = Flask(__name__)

openai.api_key = os.environ.get('OPENAI_API_KEY')


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=600):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature= temperature,
        max_tokens = max_tokens,
    )

    return response.choices[0].message["content"]


delimiter = "####"
system_message = f"""
You are TalkMentor, a friendly AI bot available in whatsapp to help, provide guidance and to interact with students and learners. \
The user message will be delimited with {delimiter} characters. \
Your task is to provide informative and engaging responses. \
Remember, while you strive to be helpful, you are not a substitute for thorough research or professional advice. \
You should not encourage or suggest the students to participate in malpractice, doing Plagiarism. \

"""

@app.route("/Talkmentor", methods=['POST'])

def wreply():
    user_message = request.form.get('Body').lower()

    messages = [
        {'role': 'system',
         'content': system_message},
        {'role': 'user',
         'content': f"{delimiter}{user_message}{delimiter}"},
    ]

    answer = get_completion_from_messages(messages)
    twilio_response = MessagingResponse()
    reply = twilio_response.message()
    reply.body(answer)
    return str(twilio_response)

if __name__=='__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)

