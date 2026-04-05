from.models import *
from django import forms
from product_and_catagory.models import product
from jalali_date.widgets import AdminJalaliDateWidget


# testsssss
# kjlkasdfafasdf
class ParchaseForm(forms.ModelForm):
     date = forms.CharField(label='تاریخ',widget=AdminJalaliDateWidget(attrs={"placeholder": "0/0/0000", "id": "datepicker19",'class': 'form-control' }))

     class Meta:
          model = Parchase
          fields =  ["supplaier","product","warehouse","quantity", "price_per_unit","paid_amount","wegiht","date",'details',"status"]

     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)

          self.fields["supplaier"].widget.attrs.update(
          {"class": "form-control", "placeholder": "اسم نوعیت گوشت را بنویسید"}
          )
          self.fields['product'].queryset = product.objects.all()
          self.fields['product'].widget.attrs.update({'class': 'form-control'})


          self.fields["warehouse"].widget.attrs.update(
          {"class": "form-control", "placeholder": "قیمت نوع گوشت"}
          )
          self.fields["quantity"].widget.attrs.update(
          {"class": "form-control", "placeholder": "مقدار"}
          )

          self.fields["price_per_unit"].widget.attrs.update(
          {"class": "form-control", "placeholder": "قیمت فی واحد"}
          )
          self.fields["paid_amount"].widget.attrs.update(
          {"class": "form-control", "placeholder": "مقدار پول پرداخت شده"}
          )
          
          self.fields["wegiht"].widget.attrs.update(
          {"class": "form-control", "placeholder": "مقدار وزن را بنویسید  "}
          )
          self.fields["details"].widget.attrs.update(
          {"class": "form-control", "placeholder": "جزیات معامله را بنویسید  ",  "rows": "4"}
          )
          self.fields["status"].widget.attrs.update(
          {"class": "form-control", "placeholder": "مقدار که باید پرداخت شود"}
          )

          self.fields['supplaier'].queryset = Customer.objects.filter(role__in=['تامین کننده', 'هردو'])




class item_dealsForms(forms.ModelForm):
     date_day = forms.CharField(label='تاریخ',widget=AdminJalaliDateWidget(attrs={"placeholder": "0/0/0000", "id": "datepicker15",'class': 'form-control' }))
     class Meta:
          model = item_deals
          fields =  ["date_day","item","godam","number", "weighht","notes"]

     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)

         
          self.fields['item'].queryset = product.objects.all()
          self.fields['item'].widget.attrs.update({'class': 'form-control'})


          self.fields["godam"].widget.attrs.update(
          {"class": "form-control", "placeholder": "قیمت نوع گوشت"}
          )
          self.fields["number"].widget.attrs.update(
          {"class": "form-control", "placeholder": "مقدار"}
          )

          self.fields["weighht"].widget.attrs.update(
          {"class": "form-control", "placeholder": "قیمت فی واحد"}
          )
          self.fields["notes"].widget.attrs.update(
          {"class": "form-control", "placeholder": "مقدار پول پرداخت شده"}
          )
        









class Purchase_loanForm(forms.ModelForm):
     class Meta:
          model = Purchase_loan
          fields =  ["pay_amount","naem_of_giver","date_of_giving"]

     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)

          self.fields["pay_amount"].widget.attrs.update(
          {"class": "form-control", "placeholder": "مقدار پرداخت را بنویسید "}
          )
          self.fields["naem_of_giver"].widget.attrs.update(
          {"class": "form-control", "placeholder": "اسم دهنده پول "}
          )
          self.fields["date_of_giving"].widget.attrs.update(
          {"class": "form-control", "placeholder": "تاریخ پرداخت را بنویسید "}
          )
