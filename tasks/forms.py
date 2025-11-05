from django import forms
from tasks.models import Task,TaskDetails

# Django Form
class TaskForm (forms.Form) :
    title = forms.CharField(max_length=250, label="Task Title")
    descriptions = forms.CharField(widget=forms.Textarea,label="Task Descriptions")
    due_date = forms.DateField(widget=forms.SelectDateWidget, label="Due Date")
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[], label="Assigned To")

    def __init__(self, *args, **kwargs):
        employees = kwargs.pop("employees", [])
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices = [(emp.id, emp.name) for emp in employees]

class styledFormMixin :
    """Mixin to apply Styled for Django Model Form"""
    default_classes = "border border-gray-500 rounded-sm w-full resize-none  focus:outline-none focus:border-gray-200"

    def apply_styled_widgets(self) :
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    "class" : self.default_classes,
                    "placeholder" : f"enter the task {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    "class" : self.default_classes,
                    "placeholder" : f"enter the task {field.label.lower()}",
                    "rows" : "5"
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    "class" : "border bg-gray-600 border-gray-500 rounded-sm resize:none focus:outline-none focus:border-gray-200"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    "class" : "space-y-2"
                })

# Django Model Form
class TaskModelForm (styledFormMixin,forms.ModelForm) :
    class Meta :
        model = Task
        fields = ['title','description','due_date']
        widgets = {
            "due_date" : forms.SelectDateWidget,
            "assigned_to" : forms.CheckboxSelectMultiple
        }

    """Widgets using Mixins"""
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()

class TaskDetailsForm(styledFormMixin,forms.ModelForm) :
    class Meta:
        model = TaskDetails
        fields = ["priority", "notes"]

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()