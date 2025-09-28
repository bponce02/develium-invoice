from django.db import models
from django.shortcuts import render, redirect
from django.utils.html import format_html
from nanodjango import Django

app = Django()

STATUS_CHOICES = (
    ("draft", "Draft"),
    ("sent", "Sent"),
    ("paid", "Paid"),
)

def open_invoice_html(modeladmin, request, queryset):
    if queryset.count() == 1:
        invoice = queryset.first()
        url = f"/invoice/{invoice.number}/"
        return redirect(url)
    else:
        modeladmin.message_user(request, "Please select only one invoice to view.")
open_invoice_html.short_description = "Open selected invoice as HTML"

@app.admin(actions=[open_invoice_html])
class Invoice(models.Model):
    number = models.AutoField(primary_key=True)
    client = models.ForeignKey("Client", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    hours = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    supplier = models.ForeignKey("Supplier", on_delete=models.CASCADE, null=True)
    
    def view_invoice_link(self):
        url = f"/invoice/{self.number}/"
        return format_html('<a href="{}" target="_blank">View Invoice</a>', url)
    view_invoice_link.short_description = "Invoice"

@app.admin
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    
@app.admin
class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    
@app.route("/")
def home(request):
    return redirect('/admin/')

@app.route("/invoice/<int:invoice_number>/")
def view_invoice(request, invoice_number):
    try:
        invoice = Invoice.objects.select_related('client', 'supplier').get(number=invoice_number)
    except Invoice.DoesNotExist:
        invoice = None
    
    return render(request, "invoice.html", {"invoice": invoice})
