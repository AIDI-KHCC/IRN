# submission/admin.py

from django.contrib import admin
from .models import Submission, CoInvestigator, ResearchAssistant, FormDataEntry

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('temporary_id', 'title', 'primary_investigator', 'irb_number', 'status', 'date_created')
    search_fields = ('title', 'primary_investigator__username', 'irb_number')
    list_filter = ('status', 'study_type')
    ordering = ('-date_created',)
    fields = ('title', 'study_type', 'primary_investigator', 'irb_number', 'status', 'date_created', 'last_modified')
    readonly_fields = ('date_created', 'last_modified')

@admin.register(CoInvestigator)
class CoInvestigatorAdmin(admin.ModelAdmin):
    list_display = ('user', 'submission', 'role_in_study', 'can_submit', 'can_edit')
    list_filter = ('can_submit', 'can_edit', 'can_view_communications')
    search_fields = ('user__username', 'submission__title', 'role_in_study')

@admin.register(ResearchAssistant)
class ResearchAssistantAdmin(admin.ModelAdmin):
    list_display = ('user', 'submission', 'can_submit', 'can_edit')
    list_filter = ('can_submit', 'can_edit', 'can_view_communications')
    search_fields = ('user__username', 'submission__title')

@admin.register(FormDataEntry)
class FormDataEntryAdmin(admin.ModelAdmin):
    list_display = ('submission', 'form', 'field_name', 'date_saved', 'version')
    list_filter = ('form', 'version')
    search_fields = ('submission__title', 'field_name', 'value')
    readonly_fields = ('date_saved',)