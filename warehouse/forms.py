from .models import *
from django import forms


NON_NEGATIVE_MESSAGE = "مقدار نمی‌تواند منفی باشد."


def set_non_negative_attrs(form, field_names):
     for field_name in field_names:
          form.fields[field_name].widget.attrs.update({"min": "0", "step": "any"})


def validate_non_negative(cleaned_data, form, field_names):
     for field_name in field_names:
          value = cleaned_data.get(field_name)
          if value is not None and value < 0:
               form.add_error(field_name, NON_NEGATIVE_MESSAGE)
     return cleaned_data


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
          set_non_negative_attrs(self, ["quantity", "weight"])

     def clean(self):
          cleaned_data = super().clean()
          validate_non_negative(cleaned_data, self, ["quantity", "weight"])

          source_warehouse = cleaned_data.get("source_warehouse")
          to_warehouse = cleaned_data.get("to_warehouse")
          if source_warehouse and to_warehouse and source_warehouse == to_warehouse:
               self.add_error("to_warehouse", "گدام گیرنده باید از گدام ارسال کننده متفاوت باشد.")

          return cleaned_data




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
         
          set_non_negative_attrs(self, ["capacity", "capacity_by_num"])

          self.fields["description"].widget.attrs.update(
          {"class": "form-control", "placeholder": "توضیخات"}
          )
          self.fields["reg_date"].widget.attrs.update(
          {"class": "form-control", "placeholder": "تاریخ را وارد کنید"}
          )
     def clean(self):
          cleaned_data = super().clean()
          return validate_non_negative(cleaned_data, self, ["capacity", "capacity_by_num"])
