# forms_builder/admin.py

from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse
from .models import StudyType, DynamicForm, FormField
import json
from reversion.admin import VersionAdmin
from reversion.models import Version

@admin.register(StudyType)
class StudyTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class DynamicFormAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Generate the correct admin URL
        example_json_url = reverse('admin:forms_builder_dynamicform_example_json')
        self.fields['json_input'] = forms.CharField(
            widget=forms.Textarea(attrs={'rows': 20, 'cols': 80}),
            help_text=f'Enter form data in JSON format. <a href="{example_json_url}" target="_blank">View Example JSON Format</a>.',
            required=False
        )

    class Meta:
        model = DynamicForm
        fields = ('name', 'version', 'requested_per_investigator', 'study_types', 'json_input')

    def clean_json_input(self):
        json_input = self.cleaned_data.get('json_input')
        if json_input:
            try:
                data = json.loads(json_input)
                if 'fields' not in data:
                    raise forms.ValidationError("JSON must contain a 'fields' key.")
                for field in data['fields']:
                    if 'name' not in field or 'field_type' not in field:
                        raise forms.ValidationError("Each field must contain 'name' and 'field_type'.")
                    if 'displayed_name' not in field:
                        field['displayed_name'] = field['name']  # Use name as fallback
            except json.JSONDecodeError as e:
                raise forms.ValidationError(f"Invalid JSON format: {str(e)}")
        # else:
        #     raise forms.ValidationError("This field is required.")
        return json_input

@admin.register(DynamicForm)
class DynamicFormAdmin(VersionAdmin):
    form = DynamicFormAdminForm
    list_display = ('name', 'version', 'date_created')
    readonly_fields = ('form_json', 'date_created')
    search_fields = ('name', 'version')
    list_filter = ('requested_per_investigator', 'study_types')
    change_form_template = 'admin/forms_builder/dynamicform_change_form.html'

    def form_json(self, obj):
        return format_html('<pre>{}</pre>', obj.to_json())

    form_json.short_description = 'Form JSON'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        json_input = form.cleaned_data.get('json_input')
        if json_input:
            data = json.loads(json_input)
            obj.fields.all().delete()
            for field_data in data.get('fields', []):
                field_name = field_data.get('name', '').lower().replace(' ', '_')
                displayed_name = field_data.get('displayed_name', field_data.get('name'))
                field_type = field_data.get('field_type')
                default_value = field_data.get('default_value', '')
                max_length = field_data.get('max_length')
                rows = field_data.get('rows', 3)
                choices = field_data.get('choices', [])
                choices_str = ','.join(choices) if choices else ''
                required = field_data.get('required', False)
                help_text = field_data.get('help_text', '')
                
                FormField.objects.create(
                    form=obj,
                    name=field_name,
                    displayed_name=displayed_name,
                    field_type=field_type,
                    default_value=default_value,
                    max_length=max_length,
                    rows=rows,
                    choices=choices_str,
                    required=required,
                    help_text=help_text
                )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['json_input'].initial = obj.to_json()
        else:
            form.base_fields['json_input'].initial = '''{
  "fields": [
    {
      "name": "field_name",
      "displayed_name": "Field Display Name",
      "field_type": "text",
      "default_value": "",
      "max_length": 255,
      "choices": [],
      "required": false,
      "help_text": "Enter explanation for this field here"
    }
  ]
}'''
        return form

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('example_json/', self.admin_site.admin_view(self.example_json_view), name='forms_builder_dynamicform_example_json'),
            path('<int:object_id>/history/<int:version_id>/', self.admin_site.admin_view(self.revision_view), name='forms_builder_dynamicform_revision'),
        ]
        return custom_urls + urls

    def example_json_view(self, request):
        example_json = '''{
  "fields": [
    {
      "name": "research_title",
      "displayed_name": "Research Title",
      "field_type": "text",
      "default_value": "",
      "max_length": 255,
      "choices": [],
      "required": true,
      "help_text": "Enter the full title of the research project"
    },
    {
      "name": "project_description",
      "displayed_name": "Project Description",
      "field_type": "textarea",
      "default_value": "",
      "max_length": 2000,
      "rows": 5,
      "choices": [],
      "required": true,
      "help_text": "Provide a detailed description of the research project"
    }
  ]
}'''
        context = dict(
            self.admin_site.each_context(request),
            title='Example JSON Format',
            example_json=example_json,
        )
        return TemplateResponse(request, 'admin/forms_builder/example_json.html', context)

    def history_view(self, request, object_id, extra_context=None):
        response = super().history_view(request, object_id, extra_context)
        versions = Version.objects.get_for_object(self.get_object(request, object_id))
        # Pass the versions to the context
        response.context_data['versions'] = versions
        return response

    def revision_view(self, request, object_id, version_id):
        obj = get_object_or_404(self.model, pk=object_id)
        version = get_object_or_404(Version, pk=version_id)
        revision = version._object_version.object  # Get the historical object
        json_input = revision.to_json()  # Get the JSON representation at this version
        context = dict(
            self.admin_site.each_context(request),
            title='Historical Form Version',
            form_name=revision.name,
            version=version,
            json_input=json_input,
        )
        return TemplateResponse(request, 'admin/forms_builder/revision_view.html', context)
