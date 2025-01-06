from django.http import HttpResponse
from django.template.loader import render_to_string

def render_htmx_message(context: dict) -> HttpResponse:
    if "message" in context:
        context["messages"] = [context["message"]]
    html_message = render_to_string('authentication_app/message.html', context=context)
    return HttpResponse(html_message)
