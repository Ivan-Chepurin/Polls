from django import forms
from django.forms.widgets import RadioSelect, CheckboxInput, TextInput, CheckboxSelectMultiple
from .models import Answer, Choice


class MultipleAnswerForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # choice_list = [choice for choice in question.get_choice_list()]

        choice_list = []
        for choice in question.get_choices_list():
            print(choice)
            choice_list.append(choice)

        print(choice_list)
        self.fields['choices'] = forms.MultipleChoiceField(
            choices=choice_list,
            widget=CheckboxSelectMultiple
        )


class OneAnswerForm(forms.ModelForm):
    choice = forms.ModelChoiceField(
        queryset=None,
        widget=RadioSelect(attrs={'class': "form-check-input",
                                  'type': "radio",
                                  'name': "flexRadioDefault",
                                  'id': "flexRadioDefault1"
                                  }),
        empty_label=None)

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('queryset', None)
        super(OneAnswerForm, self).__init__(*args, **kwargs)
        self.fields['choice'].queryset = queryset

    class Meta:
        model = Answer
        fields = ['choice']
        widgets = {'choice': RadioSelect(attrs={'class': "form-check-input",
                                                'type': "radio",
                                                'name': "flexRadioDefault",
                                                'id': "flexRadioDefault1"
                                                })}


class WritenAnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        widgets = {'text': TextInput(attrs={
            'type': "text",
            'class': "form-control",
            'id': "floatingInput",
            'placeholder': "name@example.com"
        })}
