from django.db import models

from django.db import models

class FixedExpense(models.Model):
    # Fields for each specific fixed expense type
    name = models.CharField(max_length=300, blank=False)
    date = models.CharField(max_length=300, blank=False)
    amount = models.IntegerField()
    total_amount = models.IntegerField()
    reamin_amonts = models.IntegerField()
    description = models.TextField(blank=True, null=True, help_text="Optional description for the expense")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Time when the record was created")

    def __str__(self):
        return f"Fixed Expenses - Name: {self.name}, Amount: {self.amount}, created: {self.created_at}, ..."

    class Meta:
        verbose_name = 'Fixed Expense'
        verbose_name_plural = 'Fixed Expenses'



# class pay_salary(models.Model):
#     expenses_foriengkey = models.ForeignKey(FixedExpense, on_delete=models.CASCADE, blank=False)
#     pay_amount_of_salary = models.FloatField()
#     date = models.CharField(max_length=200)
#     description = models.CharField(max_length=200)
#     def __str__(self):
#         return f"Fixed Expenses - Name: {self.date}"
#     class Meta:
#         verbose_name = 'pau salary'
#         verbose_name_plural = 'pay salary'



class LoanApprove(models.Model):
    expenses_foriengkey = models.ForeignKey(FixedExpense, on_delete=models.CASCADE, blank=False) 
    datea = models.CharField(max_length=300, blank=False)
    amounta = models.IntegerField()
    descriptiona = models.TextField(blank=True, null=True, help_text="Optional description for the expense")

    def __str__(self):
        return f"Fixed Expenses - Name: {self.datea}"

    class Meta:
        verbose_name = 'loan Expense'
        verbose_name_plural = 'loan Expenses'


    