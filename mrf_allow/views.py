from typing import Optional

from django.shortcuts import render, loader
from django.http import HttpResponse
import app.allowlist as allowlist
from app.settings import get_settings


# Create your views here.
def allow(request):
    template = loader.get_template("mrf_allow/index.html")
    instances = allowlist.list_instances()
    # search = request.GET.get("search", None)
    # if search:
    #     instances = [instance for instance in instances if search in instance]
    context = {
        "instance_list": instances,
        "host": get_settings()["host"],
    }
    return HttpResponse(template.render(context, request))
