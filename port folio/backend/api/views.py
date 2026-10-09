from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from pymongo import MongoClient

from django.conf import settings

import json


# MongoDB connection
client = MongoClient(settings.MONGO_URI)

db = client[settings.MONGO_DB]

messages_collection = db["messages"]


def portfolio_data(request):

    data = {
        "name": "Uday Kumar",
        "role": "Python Full Stack Developer",
        "about": "I am a Computer Science graduate interested in backend development and AI.",
        "skills": [
            "Python",
            "Django",
            "HTML",
            "CSS",
            "JavaScript",
            "MongoDB"
        ],
        "projects": [
            {
                "title": "Portfolio Website",
                "description": "Simple portfolio using HTML, CSS, JavaScript and Django."
            },
            {
                "title": "Fake News Detection",
                "description": "BERT based fake news classification project."
            },
            {
                "title": "Jira Clone",
                "description": "Project management application using FastAPI and React."
            }
        ]
    }

    return JsonResponse(data)


@csrf_exempt
def send_message(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST method is allowed"},
            status=405
        )

    try:

        data = json.loads(request.body)

        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        if not name or not email or not message:
            return JsonResponse(
                {"error": "All fields are required"},
                status=400
            )

        message_data = {
            "name": name,
            "email": email,
            "message": message
        }

        messages_collection.insert_one(message_data)

        return JsonResponse({
            "success": True,
            "message": "Message sent successfully"
        })

    except Exception as error:

        return JsonResponse({
            "success": False,
            "error": str(error)
        }, status=500)