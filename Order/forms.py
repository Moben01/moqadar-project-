from.models import *
from django import forms


class OrderForm(forms.ModelForm):
     class Meta:
          model = Order
          fields =  ["customer","status","total_amount","reg_date"]

     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)

          self.fields["customer"].widget.attrs.update(
          {"class": "form-control", "placeholder": "تامین کننده"}
          )
          self.fields["status"].widget.attrs.update(
          {"class": "form-control", "placeholder": "وضعیت"}
          )
          self.fields["reg_date"].widget.attrs.update(
          {"class": "form-control", "placeholder": "تاریخ را وارد کنید"}
          )
          self.fields["total_amount"].widget.attrs.update(
          {"class": "form-control", "placeholder": "مقدار کُل را وارد کنید"}
          )


class Order_ItemForm(forms.ModelForm):
     class Meta:
          model = Order_Item
          fields =  ["order","product","quantity","price_per_unit","total_price"]

     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)

          self.fields["order"].widget.attrs.update(
          {"class": "form-control", "placeholder": "سفارش"}
          )

          self.fields["product"].widget.attrs.update(
          {"class": "form-control", "placeholder": "محصول"}
          )
          self.fields["quantity"].widget.attrs.update(
          {"class": "form-control", "placeholder": "مقدار را وارد کنید"}
          )
          # self.fields["total_amount"].widget.attrs.update(
          # {"class": "form-control", "placeholder": "مقدار کُل را وارد کنید"}
          # )
          self.fields["price_per_unit"].widget.attrs.update(
          {"class": "form-control", "placeholder": "مقدار فی واحد را وارد کنید"}
          )
          self.fields["total_price"].widget.attrs.update(
          {"class": "form-control", "placeholder": "مقدار تمام پول را وارد کنید"}
          )


from jalali_date.widgets import AdminJalaliDateWidget
class SaleForm(forms.ModelForm):
     reg_date = forms.CharField(label='تاریخ',widget=AdminJalaliDateWidget(attrs={"placeholder": "0/0/0000", "id": "datepicker19",'class': 'form-control' }))

     class Meta:
          model = Sale
          fields =  ["reg_date","customer"]
          

     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)

          self.fields["customer"].widget.attrs.update(
          {"class": "form-control", "placeholder": "تاریخ به اساس قمری "}
          )
          self.fields['customer'].queryset = Customer.objects.filter(role__in=['مشتری', 'هردو'])
     



class sale_itemForm(forms.ModelForm):
     class Meta:
          model = sale_item_part
          fields =  ["product","quantity","price_per_unit","weight","warehouse","paid_amount_for_every_record","status",'notes']

     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields["warehouse"].widget.attrs.update(
          {"class": "form-control", "placeholder": "محصول"}
          )
          self.fields['product'].queryset = product.objects.all()
          self.fields['product'].widget.attrs.update({'class': 'form-control'})

          self.fields["quantity"].widget.attrs.update(
          {"class": "form-control", "placeholder": "مقدار را وارد کنید",'id':"quantity"}
          )
          self.fields["paid_amount_for_every_record"].widget.attrs.update(
          {"class": "form-control", "placeholder": "مقدار را وارد کنید",'id':"quantity"}
          )
          self.fields["weight"].widget.attrs.update(
          {"class": "form-control", "placeholder": "مقدار تعداد یا کیلوگرام را وارد کنید", 'id':"weight"}
          )
          self.fields["price_per_unit"].widget.attrs.update(
          {"class": "form-control", "placeholder": "مقدار که باید پرداخت شود"}
          )
          self.fields["status"].widget.attrs.update(
          {"class": "form-control", "placeholder": "مقدار که باید پرداخت شود"}
          )
          self.fields["notes"].widget.attrs.update(
          {"class": "form-control", "placeholder": "توضیحات"}
          )




class ReturnForm(forms.ModelForm):
     class Meta:
          model = Return
          fields =  ["quantity","data","price_per","weight"]

     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)


          self.fields["quantity"].widget.attrs.update(
          {"class": "form-control", "placeholder": "مقدار را وارد کنید"}
          )
          self.fields["data"].widget.attrs.update(
          {"class": "form-control", "placeholder": "تاریخ را وارد کنید"}
          )
          self.fields["price_per"].widget.attrs.update(
          {"class": "form-control", "placeholder": "مقدار قی را وارد کنید"}
          )
          self.fields["weight"].widget.attrs.update(
          {"class": "form-control", "placeholder": "تغداد یا وزن را وارد کنید"}
          )





class order_loanForm(forms.ModelForm):
     class Meta:
          model = order_loan
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
