from .models import *
from django import forms
from jalali_date.widgets import AdminJalaliDateWidget

class incomeForm(forms.ModelForm):
     rec_date = forms.CharField(label='تاریخ',widget=AdminJalaliDateWidget(attrs={"placeholder": "0/0/0000", "id": "datepicker1",'class': 'form-control' }))

     class Meta:
          model = income
          fields =  ["rec_date","income_amount","curr","exchagne_rate","descriiption","olabrate"]
         
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          
          self.fields["income_amount"].widget.attrs.update(
          {"class": "form-control", "placeholder": "مقدار پول به افغانی"}
          )
          self.fields["curr"].widget.attrs.update(
          {"class": "form-control", "placeholder": "واحد پولی"}
          )
          self.fields["exchagne_rate"].widget.attrs.update(
          {"class": "form-control", "placeholder": "نرخ"}
          )
          self.fields["descriiption"].widget.attrs.update(
          {"class": "form-control", "placeholder": "توضیحات"}
          )
          self.fields["olabrate"].widget.attrs.update(
          {"class": "form-control", "placeholder": "دهنده پول"}
          )
         

class out_comeForm(forms.ModelForm):
     rec_date = forms.CharField(label='تاریخ',widget=AdminJalaliDateWidget(attrs={"placeholder": "0/0/0000", "id": "datepicker10",'class': 'form-control' }))

     class Meta:
          model = income
          fields =  ["rec_date","income_amount","curr","exchagne_rate","descriiption","olabrate"]
         
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
         
          self.fields["income_amount"].widget.attrs.update(
          {"class": "form-control", "placeholder": "مقدار پول به افغانی"}
          )
          self.fields["curr"].widget.attrs.update(
          {"class": "form-control", "placeholder": "واحد پولی"}
          )
          self.fields["exchagne_rate"].widget.attrs.update(
          {"class": "form-control", "placeholder": "نرخ"}
          )
          self.fields["descriiption"].widget.attrs.update(
          {"class": "form-control", "placeholder": "توضیحات"}
          )
          self.fields["olabrate"].widget.attrs.update(
          {"class": "form-control", "placeholder": "دهنده پول"}
          )
         
class cuurencyForm(forms.ModelForm):
     class Meta:
          model = cuurency
          fields = ["curr_name"]
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
         
          self.fields["curr_name"].widget.attrs.update(
          {"class": "form-control", "placeholder": "واحد پولی"}
          )


class coolaboratorsForm(forms.ModelForm):
     class Meta:
          model = coolaborators
          fields =  ["reg_date","name_opf","phone_num","adreess"]
         
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
         
          self.fields["reg_date"].widget.attrs.update(
          {"class": "form-control", "placeholder": "تاریخ ثبت"}
          )
          self.fields["name_opf"].widget.attrs.update(
          {"class": "form-control", "placeholder": "اسم شریک"}
          )
          self.fields["phone_num"].widget.attrs.update(
          {"class": "form-control", "placeholder": "شماره موبایل"}
          )
          self.fields["adreess"].widget.attrs.update(
          {"class": "form-control", "placeholder": "آدرس"}
          )



class exchagn_money_in_systemForm(forms.ModelForm):
     class Meta:
          model = exchagn_money_in_system
          fields =  ["currency_that_you_want_tochage","amount","currency_that_you_want_to_get_money","want_amount","exchabge_rate","note"]
         
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
         
          self.fields["currency_that_you_want_tochage"].widget.attrs.update(
          {"class": "form-control", "placeholder": "تاریخ ثبت"}
          )
          self.fields["amount"].widget.attrs.update(
          {"class": "form-control", "placeholder": ""}
          )
          self.fields["currency_that_you_want_to_get_money"].widget.attrs.update(
          {"class": "form-control", "placeholder": ""}
          )
          self.fields["want_amount"].widget.attrs.update(
          {"class": "form-control", "placeholder": ""}
          )
          self.fields["exchabge_rate"].widget.attrs.update(
          {"class": "form-control", "placeholder": ""}
          )
          self.fields["note"].widget.attrs.update(
          {"class": "form-control", "placeholder": ""}
          )