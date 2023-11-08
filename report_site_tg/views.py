import os
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, DetailView, TemplateView, ListView
from .forms import ReportSiteForm, TextAddForm
from .models import Order, Report, Text
from .consumers import send_browser_report
import asyncio
from browser_reports.start import ReportBrowser
import threading


class Index(FormView):
    form_class = ReportSiteForm
    template_name = 'report_site_tg/index.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            order = form.save()
            th = threading.Thread(
                target=ReportBrowser,
                args=(order.count_threads, order.count_reports, order.url_report, order.uuid)
            )
            th.start()
            return redirect(f'/site_reports/order/{order.uuid}/')

        return redirect('index')


class OrderView(DetailView):
    template_name = 'report_site_tg/order.html'
    model = Order
    context_object_name = 'order'

    def get_object(self, queryset=None):
        return self.model.objects.get(uuid=self.kwargs['uuid'])


class TextReportView(ListView):
    template_name = 'report_site_tg/texts.html'
    model = Text
    context_object_name = 'texts'


class EditText(FormView):
    template_name = 'report_site_tg/edit_text.html'
    form_class = TextAddForm

    def post(self, request, *args, **kwargs):
        text = request.POST.get('new_text')
        text = text.replace('\r\n', '\n').replace('\n\n', '\n')
        arr = text.split('\n')
        for i in arr:
            if i.strip():
                t = Text(content=i.strip())
                t.save()

        return redirect('/site_reports/texts/')


@csrf_exempt
def save_report(request):
    if request.method == 'POST':
        order_uuid = request.POST.get('uuid')
        report_dict = dict(**request.POST)
        report_dict = {i: report_dict[i][0] for i in report_dict}
        del report_dict['uuid']
        report = Report(**report_dict)
        order = Order.objects.get(uuid=order_uuid)
        report.save()
        order.reports.add(report)
        asyncio.run(send_browser_report(order_uuid, report))
        return JsonResponse({'status': 'ok'})
