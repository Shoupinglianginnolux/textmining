from django import forms
from .models import Keywords, Auth_approval, Auth_application
from django.forms import widgets

class ClassificationSearchForm(forms.Form):

    marcas=(
        (0,'cases'),
        (1,'SRQs'),
        (2,'both'),)

    start_date = forms.DateField(label="Start Date", required=False)
    end_date = forms.DateField(required=False)
    data_source = forms.CharField(max_length=2, widget=forms.Select(choices= marcas), required=False)
    model_name = forms.CharField(max_length=255, required=False)
    error_code = forms.CharField(max_length=255, required=False)
    keywords = forms.CharField(max_length=255, required=False)
    SQR_Number = forms.CharField(max_length=255, required=False)
    SN_Number = forms.CharField(max_length=255, required=False)

    def clean(self):
        cleaned_data = super(ClassificationSearchForm, self).clean()  # Get the cleaned data from default clean, returns cleaned_data
        field1 = cleaned_data.get("start_date")
        field2 = cleaned_data.get("end_date"),

        if not field1 and not field2:
            raise forms.ValidationError('Please fill in both fields.')

        return cleaned_data

class KeywordSearchForm(forms.Form):

    marcas=(
        (0,'cases'),
        (1,'SRQs'),
        (2,'both'),)

    # CHOICES = ((0, '破片'),(1, '腳架斷裂'),(2, '機台燃燒'),(3, '緊急事件'))

    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)
    data_source = forms.CharField(max_length=2, widget=forms.Select(choices= marcas))
    search_class = forms.CharField(widget=widgets.Select())


class OSRSearchForm(forms.Form):

    marcas=(
        (0,'------'),
        (1,'Power'),
        (2,'Wifi'),)
    customer_machine_model_selection =(
        (0,'------'),
        (1,'50 inch'),
        (2,'32 inch'),
    )

    start_date = forms.DateField(label="Start Date", required=True,widget=forms.TextInput(attrs={'placeholder': '2020-03-01', 'autocomplete':'off'}))
    end_date = forms.DateField(required=True,widget=forms.TextInput(attrs={'placeholder': '2020-03-02', 'autocomplete':'off'}))
    part = forms.CharField(max_length=2, widget=forms.Select(choices= marcas))
    customer_machine_model = forms.CharField(max_length=255, widget=forms.Select(choices= customer_machine_model_selection))

class PostForm(forms.Form):
    username = forms.CharField(max_length=20, initial="", label="請輸入開機帳號")
    password = forms.CharField(max_length=20, required=False, initial="", label="請輸入開機密碼", widget=forms.PasswordInput)


class Auth_applicationForm(forms.ModelForm):
    reason = forms.CharField(
        widget=forms.Textarea(
        attrs={
            'style': 'width:400px;height:200px;', 'rows':5, 'cols':10,
            },
        ), max_length=255, required=False)
    class Meta:
        model = Auth_application
        fields = '__all__'


class Auth_approvalForm(forms.ModelForm):
    opinion = forms.CharField(
        widget=forms.Textarea(
        attrs={
            'style': 'width:400px;height:200px;', 'rows':5, 'cols':10,
            },
        ), max_length=255, required=False)
    CHOICES = [('0', '同意'), ('1', '不同意')]
    approval = forms.ChoiceField(widget=forms.RadioSelect(
        attrs={
            'style': "list-style-type:none;"
            },
    ), choices=CHOICES)
    class Meta:
        model = Auth_approval
        fields = '__all__'
