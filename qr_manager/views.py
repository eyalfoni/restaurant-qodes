import os

import qrcode

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.decorators import login_required

from qr_manager.models import QRCode
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from .forms import CreateQRForm


SERVER_BASE_URL = os.environ.get('SERVER_BASE_URL') or 'http://b97fde1e65c0.ngrok.io'  # TODO: change to heroku env variable


class RouteQRCode(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RouteQRCode, self).dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        qrcode_id = kwargs.get('qrcode_id')
        qrcode_object = QRCode.objects.get(pk=qrcode_id)

        return redirect(qrcode_object.forwarding_url)


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            qr_codes = QRCode.objects.filter(owner=self.request.user)
            serialized_qr_codes = [dict(
                id=qr.id,
                forwarding_url=qr.forwarding_url,
                qr_code_img=SERVER_BASE_URL + "/static/qr_{}.jpeg".format(qr.id)
            ) for qr in qr_codes]
            context['qrcodes'] = serialized_qr_codes
        return context


@login_required
def create_qr(request):
    if request.method == "POST":
        form = CreateQRForm(request.POST)
        if form.is_valid():
            qr = QRCode.objects.create(
                owner=request.user,
                forwarding_url=form.cleaned_data['url'],
            )

            qr_img = qrcode.make(SERVER_BASE_URL + "/api/goto/{}".format(qr.id))
            f = open('static/qr_{}.jpeg'.format(qr.id), 'wb')
            qr_img.save(f)
            qr.qr_code_img = os.path.relpath(f.name)
            qr.save()
            f.close()
            messages.success(request, 'You added a QRCode successfully!', extra_tags='alert')
            return redirect("create_qr")
    else:
        form = CreateQRForm()
        return render(request, "create_qr.html", {"form": form})


@login_required
def edit_qr(request, qrcode_id):
    qr = get_object_or_404(QRCode, pk=qrcode_id)
    if request.method == "POST":
        form = CreateQRForm(request.POST)
        if form.is_valid():
            qr.forwarding_url = form.cleaned_data['url']
            qr.save()
            messages.success(request, 'You updated a QRCode successfully!', extra_tags='alert')
            return redirect("home")
    else:
        form = CreateQRForm()
        form.fields['url'].label = 'New Link:'
        return render(request, "edit_qr.html", {"form": form, "qr": qr})
