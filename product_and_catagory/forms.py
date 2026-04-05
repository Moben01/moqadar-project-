from.models import *
from django import forms

class catagoriesForm(forms.ModelForm):
     class Meta:
          model = catagories
          fields =  ["name","description","reg_date"]
         
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
         
          self.fields["reg_date"].widget.attrs.update(
          {"class": "form-control", "placeholder": "تاریخ را وارد کنید"}
          )
          self.fields["name"].widget.attrs.update(
          {"class": "form-control", "placeholder": "اسم نوعیت محصول را بنویسید"}
          )
          self.fields["description"].widget.attrs.update(
          {"class": "form-control", "placeholder": "توضیخات"}
          )
      

class productForm(forms.ModelForm):
     class Meta:
          model = product
          fields =  ["meat_catagory","meat_name","description","product_type","reg_date"]
         
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
         
          self.fields["meat_catagory"].widget.attrs.update(
          {"class": "form-control", "placeholder": "اسم نوعیت محصول را بنویسید"}
          )
          self.fields["meat_name"].widget.attrs.update(
          {"class": "form-control", "placeholder": "نام محصول را بنویسید"}
          )
        
          self.fields["description"].widget.attrs.update(
          {"class": "form-control", "placeholder": "توضیخات"}
          )
          self.fields["product_type"].widget.attrs.update(
          {"class": "form-control", "placeholder": ""}
          )
          self.fields["reg_date"].widget.attrs.update(
          {"class": "form-control", "placeholder": "تاریخ را وارد کنید"}
          )
