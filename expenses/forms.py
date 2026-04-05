from.models import *
from django import forms
from jalali_date.widgets import AdminJalaliDateWidget

class FixedExpenseForm(forms.ModelForm):
    date = forms.CharField(label='تاریخ',widget=AdminJalaliDateWidget(attrs={"placeholder": "0/0/0000", "id": "datepicker16",'class': 'form-control' }))
    class Meta:
          model = FixedExpense
          fields =  ["name","amount","description","date","total_amount"]
                
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Updating widget attributes for each field
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "عنوان مصرف خویش را بنویسید"}
        )
        
        self.fields["total_amount"].widget.attrs.update(
            {"class": "form-control", "placeholder": "مقدار عمومی مصرف خویش را بنویسید"}
        )
        self.fields["amount"].widget.attrs.update(
            {"class": "form-control", "placeholder": "مقدار مصرف خویش را بنویسید"}
        )
      
        self.fields["description"].widget.attrs.update(
            {"class": "form-control", "placeholder": "توضیحات اضافی (اختیاری)"}
        )





class LoanApproveForm(forms.ModelForm):
    class Meta:
          model = LoanApprove
          fields =  ["datea","amounta","descriptiona"]
                
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Updating widget attributes for each field
        self.fields["datea"].widget.attrs.update(
            {"class": "form-control", "placeholder": "عنوان مصرف خویش را بنویسید"}
        )
        self.fields["amounta"].widget.attrs.update(
            {"class": "form-control", "placeholder": "مقدار مصرف خویش را بنویسید"}
        )
    
        self.fields["descriptiona"].widget.attrs.update(
            {"class": "form-control", "placeholder": "توضیحات اضافی (اختیاری)"}
        )
