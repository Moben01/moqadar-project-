from .models import *
from django import forms

class tranfer_productsForm(forms.ModelForm):
     class Meta:
          model = tranfer_products
          fields = ["date","source_warehouse","to_warehouse","product_send","quantity","weight"]
          widgets = {
               "source_warehouse": forms.Select(attrs={"id": "source_warehouse"}),
               "to_warehouse": forms.Select(attrs={"id": "to_warehouse"}),
          }
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)

          self.fields["date"].widget.attrs.update(
          {"class": "form-control", "placeholder": "تاریخ"}
          )
          self.fields["source_warehouse"].widget.attrs.update(
          {"class": "form-control", "placeholder": "گدام ارسال کننده"}
          )
          self.fields["to_warehouse"].widget.attrs.update(
          {"class": "form-control", "placeholder": "گدام گیرنده"}
          )
          self.fields["product_send"].widget.attrs.update(
          {"class": "form-control", "placeholder": "محصول"}
          )
          self.fields["quantity"].widget.attrs.update(
          {"class": "form-control", "placeholder": "تعداد"}
          )
          self.fields["weight"].widget.attrs.update(
          {"class": "form-control", "placeholder": "وزن"}
          )
     



class warehouse_infoForm(forms.ModelForm):
     class Meta:
          model = warehouse_info
          fields =  ["name","location","capacity","description","capacity_by_num",'reg_date']
         
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
         
          self.fields["name"].widget.attrs.update(
          {"class": "form-control", "placeholder": "اسم  گدام را بنویسید"}
          )
          self.fields["location"].widget.attrs.update(
          {"class": "form-control", "placeholder": "موقعیت گدام را بنویسید"}
          )
          self.fields["capacity"].widget.attrs.update(
          {"class": "form-control", "placeholder": "ظرفیت گدام را به کیلوگرام بنویسید"}
          ) 
          self.fields["capacity_by_num"].widget.attrs.update(
          {"class": "form-control", "placeholder": "ظرفیت گدام را به تعداد بنویسید"}
          )
         
          self.fields["description"].widget.attrs.update(
          {"class": "form-control", "placeholder": "توضیخات"}
          )
          self.fields["reg_date"].widget.attrs.update(
          {"class": "form-control", "placeholder": "تاریخ را وارد کنید"}
          )