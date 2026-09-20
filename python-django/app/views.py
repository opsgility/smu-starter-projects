"""App views."""

from django.http import HttpResponse, JsonResponse


def home(request):
    return HttpResponse(
        "<h1>SkillMeUp Labs</h1>"
        "<p>Your Django application is running!</p>"
        '<p>Try the API endpoint: <a href="/api/hello">/api/hello</a></p>'
    )


def hello_api(request):
    return JsonResponse({"message": "Hello from Django!"})
