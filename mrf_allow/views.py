from typing import Optional

from django.http import HttpResponse
from django.shortcuts import loader, render

import thorax_core.allowlist as allowlist
from thorax_core.settings import get_settings
from mrf_allow.models import InstanceUrlForm


# Create your views here.
def allow(request):
    if request.method == "POST":
        form = InstanceUrlForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            instance_url = data['instance_url']
            if data["operation_type"] == "0":
                try:
                    allowlist.add_instance(instance_url,"added through thorax-fe")
                except ValueError:
                    return HttpResponse(f"Attempting to add already existing instance \"{instance_url}\"")
            elif data["operation_type"] == "1":
                try:
                    allowlist.remove_instance(instance_url)
                except ValueError:
                    return HttpResponse(f"Not in Allowlist \"{instance_url}\"")
    form = InstanceUrlForm()
    instances = allowlist.list_instances()
    context = {
             "instance_list": instances,
             "host": get_settings()["host"],
             "form": form,
        }
    return render(request, "mrf_allow/index.html",context)

#     template = loader.get_template("mrf_allow/index.html")
#     instances = allowlist.list_instances()
#     # search = request.GET.get("search", None)
#     # if search:
#     #     instances = [instance for instance in instances if search in instance]
#     context = {
#         "instance_list": instances,
#         "host": get_settings()["host"],
#     }
#     return HttpResponse(template.render(context, request))
