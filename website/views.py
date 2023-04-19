import json
from django.http import HttpResponse
from django.shortcuts import render
import requests
import replicate
from dotenv import load_dotenv
load_dotenv()
model = replicate.models.get("stability-ai/stable-diffusion")
version = model.versions.get("db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf")

def process_query(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #query = data['query']
        #new_image_url = generate_image(query=query)[0]
        #json_data = json.dumps(new_image_url)
        json_data='testing'
        return HttpResponse(json_data, content_type='application/json')

def generate_image(query):

    inputs = {
        'prompt':query,
        'image_dimensions':'512x512',
        'num_outputs':1,
        'num_inference_steps':50,
        'guidance_scale':7.5,
        'scheduler':'K_EULER'
    }

    output = version.predict(**inputs)
    return output

def send_message(message):

    bot_token = '5909950907:AAGLUOiH7a8BuE7WkfuJXFJfkAK_jQzY_JQ'
    #chat_id = '5289262606'
    chat_id = '-910348659'

    # Send a message to the specified chat using the Telegram Bot API
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    data = {'chat_id': chat_id, 'text': message}

    response = requests.post(url, data=data)

    if response.status_code == 200:
        status = 'Message sent successfully!'
    else:
        status = 'An error occurred while sending the message.'

    return status

# Create your views here.
def index(request):
    if request.method == 'POST':
        msg = request.POST.get('msg')
        user=request.POST.get('user')
        prompts = request.POST.get('prompts')
        image_url = request.POST.get('image-url')
        formatted_string = f'User: {user}\n\nMessage: {msg}\n\nImage URL: {image_url}\n\nPrompts Used:"{prompts}"'
        result = send_message(formatted_string)
        return render(request, 'index.html', {
            'result':result,
        })
    else:
        return render(request, 'index.html', {})