from django import forms
import csv
import os 

class SearchForm(forms.Form):
    selected_column = forms.ChoiceField(choices=[], required=True)
    selected_value = forms.CharField(max_length=100, required=True)
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/jinaapp/JINAbase2021_RA_DEC_deg.csv')
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            self.fields['selected_column'].choices = [(col, col) for col in header]
