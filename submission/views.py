from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.core.files.base import ContentFile
from dal import autocomplete
import json
from io import BytesIO
from .utils import PDFGenerator, has_edit_permission, check_researcher_documents, get_next_form, get_previous_form
from .utils.pdf_generator import generate_submission_pdf
from .gpt_analysis import ResearchAnalyzer
from django.core.cache import cache
from .utils.permissions import check_submission_permission

from .models import (
    Submission,
    CoInvestigator,
    ResearchAssistant,
    FormDataEntry,
    Document,
    VersionHistory,
    PermissionChangeLog,
)
from .forms import (
    SubmissionForm,
    ResearchAssistantForm,
    CoInvestigatorForm,
    DocumentForm,
    generate_django_form,
)
from forms_builder.models import DynamicForm
from messaging.models import Message, MessageAttachment
from users.models import SystemSettings, UserProfile
from django import forms
import logging

logger = logging.getLogger(__name__)

from django.db.models import Q
from django.db import transaction
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import IntegrityError

def get_system_user():
    """Get or create the system user for automated messages."""
    try:
        with transaction.atomic():
            # First try to get existing system user
            try:
                system_user = User.objects.get(username='system')
            except User.DoesNotExist:
                # Create new system user if doesn't exist
                system_user = User.objects.create(
                    username='system',
                    email=SystemSettings.get_system_email(),
                    first_name='System',
                    last_name='User',
                    is_active=True
                )
            
            # Try to get or create UserProfile
            try:
                profile = UserProfile.objects.get(user=system_user)
            except UserProfile.DoesNotExist:
                profile = UserProfile.objects.create(
                    user=system_user,
                    full_name='System User',
                    phone_number='',
                    department='',
                    position='System'
                )
            
            return system_user
            
    except Exception as e:
        logger.error(f"Error in get_system_user: {str(e)}")
        logger.error("Error details:", exc_info=True)
        
        # Final fallback - just get or create the user without profile
        try:
            system_user = User.objects.get(username='system')
        except User.DoesNotExist:
            system_user = User.objects.create(
                username='system',
                email='aidi@khcc.jo',
                first_name='System',
                last_name='User',
                is_active=True
            )
        return system_user

@login_required
def dashboard(request):
    """Display user's submissions dashboard."""
    from django.db.models import Max
    
    submissions = Submission.objects.filter(
        is_archived=False
    ).select_related(
        'primary_investigator__userprofile'
    ).order_by('-date_created')
    
    # Get the actual latest version for each submission from FormDataEntry
    for submission in submissions:
        latest_version = FormDataEntry.objects.filter(
            submission=submission
        ).values('version').aggregate(Max('version'))['version__max']
        submission.actual_version = latest_version or 1  # Use 1 if no entries found

    return render(request, 'submission/dashboard.html', {'submissions': submissions})

@login_required
def edit_submission(request, submission_id):
    """Redirect to start_submission with existing submission ID."""
    return redirect('submission:start_submission_with_id', submission_id=submission_id)

@login_required
def start_submission(request, submission_id=None):
    """Start or edit a submission."""
    if submission_id:
        submission = get_object_or_404(Submission, pk=submission_id)
        print(f"Found submission with PI: {submission.primary_investigator}")
        print(f"Current user: {request.user}")
        
        if submission.is_locked:
            messages.error(request, "This submission is locked and cannot be edited.")
            return redirect('submission:dashboard')
        if not has_edit_permission(request.user, submission):
            messages.error(request, "You do not have permission to edit this submission.")
            return redirect('submission:dashboard')
        
        # Only set initial data for primary_investigator, not is_primary_investigator
        initial_data = {
            'primary_investigator': submission.primary_investigator
        }
    else:
        submission = None
        initial_data = {}

    if request.method == 'POST':
        print(f"POST data: {request.POST}")
        form = SubmissionForm(request.POST, instance=submission)
        action = request.POST.get('action')
        
        if action == 'exit_no_save':
            return redirect('submission:dashboard')
            
        if form.is_valid():
            submission = form.save(commit=False)
            # Get is_pi directly from POST data instead of cleaned_data
            is_pi = request.POST.get('is_primary_investigator') == 'on'
            
            if is_pi:
                submission.primary_investigator = request.user
            else:
                pi_user = form.cleaned_data.get('primary_investigator')
                if not pi_user:
                    messages.error(request, 'Please select a primary investigator.')
                    return render(request, 'submission/start_submission.html', {
                        'form': form,
                        'submission': submission
                    })
                submission.primary_investigator = pi_user
                
            submission.save()
            messages.success(request, f'Temporary submission ID {submission.temporary_id} generated.')
            
            if action == 'save_exit':
                return redirect('submission:dashboard')
            elif action == 'save_continue':
                return redirect('submission:add_research_assistant', submission_id=submission.temporary_id)
    else:
        form = SubmissionForm(instance=submission, initial=initial_data)
        # Explicitly set is_primary_investigator based on current state
        if submission and submission.primary_investigator == request.user:
            form.fields['is_primary_investigator'].initial = True
        else:
            form.fields['is_primary_investigator'].initial = False

    return render(request, 'submission/start_submission.html', {
        'form': form,
        'submission': submission,
    })

from django import forms
from django.contrib.auth.models import User
from .models import ResearchAssistant  # Add this import

@login_required
def add_research_assistant(request, submission_id):
    """Add or manage research assistants for a submission."""
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # Check if user has permission to modify research assistants
    if not submission.can_user_edit(request.user):
        messages.error(request, "You don't have permission to modify research assistants.")
        return redirect('submission:dashboard')

    if submission.is_locked:
        messages.error(request, "This submission is locked and cannot be edited.")
        return redirect('submission:dashboard')

    # Initialize form variable
    form = ResearchAssistantForm(submission=submission)

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'delete_assistant':
            assistant_id = request.POST.get('assistant_id')
            if assistant_id:
                try:
                    assistant = ResearchAssistant.objects.get(id=assistant_id, submission=submission)
                    # Log the deletion
                    PermissionChangeLog.objects.create(
                        submission=submission,
                        user=assistant.user,
                        changed_by=request.user,
                        permission_type='removed',
                        old_value=True,
                        new_value=False,
                        role='research_assistant',
                        notes=f"Research Assistant removed from submission by {request.user.get_full_name()}"
                    )
                    assistant.delete()
                    messages.success(request, 'Research assistant removed successfully.')
                except ResearchAssistant.DoesNotExist:
                    messages.error(request, 'Research assistant not found.')
            return redirect('submission:add_research_assistant', submission_id=submission.temporary_id)

        if action in ['back', 'exit_no_save', 'save_continue']:
            if action == 'back':
                return redirect('submission:start_submission_with_id', submission_id=submission.temporary_id)
            elif action == 'exit_no_save':
                return redirect('submission:dashboard')
            elif action == 'save_continue':
                return redirect('submission:add_coinvestigator', submission_id=submission.temporary_id)

        form = ResearchAssistantForm(request.POST, submission=submission)
        if form.is_valid():
            assistant = form.cleaned_data.get('assistant')
            if assistant:
                try:
                    with transaction.atomic():
                        # Create new research assistant
                        ra = ResearchAssistant(
                            submission=submission,
                            user=assistant,
                            can_submit=form.cleaned_data.get('can_submit', False),
                            can_edit=form.cleaned_data.get('can_edit', False),
                            can_view_communications=form.cleaned_data.get('can_view_communications', False)
                        )
                        
                        # Save first
                        ra.save()
                        
                        # Then log permission changes
                        ra.log_permission_changes(changed_by=request.user, is_new=True)

                        # Create notification
                        Message.objects.create(
                            sender=get_system_user(),
                            subject=f'Added as Research Assistant to {submission.title}',
                            body=f"""
You have been added as a Research Assistant to:

Submission ID: {submission.temporary_id}
Title: {submission.title}
Principal Investigator: {submission.primary_investigator.get_full_name()}

Your permissions:
- Can Edit: {'Yes' if ra.can_edit else 'No'}
- Can Submit: {'Yes' if ra.can_submit else 'No'}
- Can View Communications: {'Yes' if ra.can_view_communications else 'No'}

Please log in to view the submission.
                            """.strip(),
                            related_submission=submission
                        ).recipients.add(assistant)

                        messages.success(request, 'Research assistant added successfully.')
                        
                        if action == 'save_exit':
                            return redirect('submission:dashboard')
                        elif action == 'save_add_another':
                            return redirect('submission:add_research_assistant', 
                                         submission_id=submission.temporary_id)

                except IntegrityError:
                    messages.error(request, 'This user is already a research assistant for this submission.')
                except Exception as e:
                    logger.error(f"Error saving research assistant: {str(e)}")
                    messages.error(request, f'Error adding research assistant: {str(e)}')

    # Get research assistants with permission information
    assistants = ResearchAssistant.objects.filter(submission=submission).select_related('user')
    
    # Get permission change history
    permission_history = PermissionChangeLog.objects.filter(
        submission=submission,
        role='research_assistant'
    ).select_related('user', 'changed_by').order_by('-change_date')[:10]

    return render(request, 'submission/add_research_assistant.html', {
        'form': form,
        'submission': submission,
        'assistants': assistants,
        'permission_history': permission_history,
        'can_modify': submission.can_user_edit(request.user)
    })

@login_required
def add_coinvestigator(request, submission_id):
    """Add or manage co-investigators for a submission."""
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # Check if user has permission to modify co-investigators
    if not submission.can_user_edit(request.user):
        messages.error(request, "You don't have permission to modify co-investigators.")
        return redirect('submission:dashboard')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'delete_coinvestigator':
            coinvestigator_id = request.POST.get('coinvestigator_id')
            if coinvestigator_id:
                try:
                    coinvestigator = CoInvestigator.objects.get(id=coinvestigator_id, submission=submission)
                    # Log the deletion
                    PermissionChangeLog.objects.create(
                        submission=submission,
                        user=coinvestigator.user,
                        changed_by=request.user,
                        permission_type='removed',
                        old_value=True,
                        new_value=False,
                        role='co_investigator',
                        notes=f"Co-investigator removed from submission by {request.user.get_full_name()}"
                    )
                    coinvestigator.delete()
                    messages.success(request, 'Co-investigator removed successfully.')
                except CoInvestigator.DoesNotExist:
                    messages.error(request, 'Co-investigator not found.')
            return redirect('submission:add_coinvestigator', submission_id=submission.temporary_id)

        if action in ['back', 'exit_no_save', 'save_continue']:
            if action == 'back':
                return redirect('submission:add_research_assistant', submission_id=submission.temporary_id)
            elif action == 'exit_no_save':
                return redirect('submission:dashboard')
            elif action == 'save_continue':
                first_form = submission.study_type.forms.order_by('order').first()
                if first_form:
                    return redirect('submission:submission_form', 
                                  submission_id=submission.temporary_id,
                                  form_id=first_form.id)
                else:
                    return redirect('submission:submission_review', 
                                  submission_id=submission.temporary_id)

        form = CoInvestigatorForm(request.POST, submission=submission)
        if form.is_valid():
            investigator = form.cleaned_data.get('investigator')
            selected_roles = form.cleaned_data.get('roles')
            
            if investigator:
                try:
                    with transaction.atomic():
                        # Create new co-investigator
                        coinv = CoInvestigator(
                            submission=submission,
                            user=investigator,
                            can_submit=form.cleaned_data.get('can_submit', False),
                            can_edit=form.cleaned_data.get('can_edit', False),
                            can_view_communications=form.cleaned_data.get('can_view_communications', False)
                        )
                        
                        # Set roles (it's a list field, not M2M)
                        coinv.roles = list(selected_roles)
                        
                        # Save first
                        coinv.save()
                        
                        # Then log permission changes
                        coinv.log_permission_changes(changed_by=request.user, is_new=True)

                        # Create notification
                        Message.objects.create(
                            sender=get_system_user(),
                            subject=f'Added as Co-Investigator to {submission.title}',
                            body=f"""
You have been added as a Co-Investigator to:

Submission ID: {submission.temporary_id}
Title: {submission.title}
Principal Investigator: {submission.primary_investigator.get_full_name()}

Your roles: {', '.join(coinv.get_role_display())}

Your permissions:
- Can Edit: {'Yes' if coinv.can_edit else 'No'}
- Can Submit: {'Yes' if coinv.can_submit else 'No'}
- Can View Communications: {'Yes' if coinv.can_view_communications else 'No'}

Please log in to view the submission.
                            """.strip(),
                            related_submission=submission
                        ).recipients.add(investigator)

                        messages.success(request, 'Co-investigator added successfully.')
                        
                        if action == 'save_exit':
                            return redirect('submission:dashboard')
                        elif action == 'save_add_another':
                            return redirect('submission:add_coinvestigator', 
                                         submission_id=submission.temporary_id)

                except IntegrityError:
                    messages.error(request, 'This user is already a co-investigator for this submission.')
                except Exception as e:
                    logger.error(f"Error saving co-investigator: {str(e)}")
                    messages.error(request, f'Error adding co-investigator: {str(e)}')
            else:
                messages.error(request, 'Please select a co-investigator.')
    else:
        form = CoInvestigatorForm()

    coinvestigators = CoInvestigator.objects.filter(submission=submission)
    
    # Get permission change history
    permission_history = PermissionChangeLog.objects.filter(
        submission=submission,
        role='co_investigator'
    ).select_related('user', 'changed_by').order_by('-change_date')[:10]

    return render(request, 'submission/add_coinvestigator.html', {
        'form': form,
        'submission': submission,
        'coinvestigators': coinvestigators,
        'permission_history': permission_history,
        'can_modify': submission.can_user_edit(request.user)
    })

@login_required
@check_submission_permission('edit')
def submission_form(request, submission_id, form_id):
    """Handle dynamic form submission and display."""
    submission = get_object_or_404(Submission, temporary_id=submission_id)
    if not has_edit_permission(request.user, submission):
        messages.error(request, "You do not have permission to edit this submission.")
        return redirect('submission:dashboard')
    if submission.is_locked:
        messages.error(request, "This submission is locked and cannot be edited.")
        return redirect('submission:dashboard')

    dynamic_form = get_object_or_404(DynamicForm, pk=form_id)
    action = request.POST.get('action')

    previous_form = get_previous_form(submission, dynamic_form)

    def process_field_value(value, field_type):
        """Helper function to process field values based on field type."""
        if field_type == 'checkbox':
            try:
                if isinstance(value, str):
                    if value.startswith('['):
                        return json.loads(value)
                    # Handle comma-separated string values
                    return [v.strip() for v in value.split(',') if v.strip()]
                return value
            except json.JSONDecodeError:
                return []
        return value

    if request.method == 'POST':
        # Handle navigation actions without form processing
        if action == 'back':
            # If there's a previous form, go to it
            if previous_form:
                return redirect('submission:submission_form', 
                              submission_id=submission.temporary_id, 
                              form_id=previous_form.id)
            # Otherwise go back to co-investigators
            return redirect('submission:add_coinvestigator', 
                          submission_id=submission.temporary_id)
            return redirect('submission:dashboard')

        # Create form instance without validation
        DynamicFormClass = generate_django_form(dynamic_form)
        
        # Save all form fields without validation
        for field_name, field in DynamicFormClass.base_fields.items():
            if isinstance(field, forms.MultipleChoiceField):
                # Handle multiple choice fields (including checkboxes)
                values = request.POST.getlist(f'form_{dynamic_form.id}-{field_name}')
                value = json.dumps(values) if values else '[]'
            else:
                value = request.POST.get(f'form_{dynamic_form.id}-{field_name}', '')
                
            FormDataEntry.objects.update_or_create(
                submission=submission,
                form=dynamic_form,
                field_name=field_name,
                version=submission.version,
                defaults={'value': value}
            )
        
        # Handle post-save navigation
        if action == 'save_exit':
            return redirect('submission:dashboard')
        elif action == 'save_continue':
            next_form = get_next_form(submission, dynamic_form)
            if next_form:
                return redirect('submission:submission_form', 
                              submission_id=submission.temporary_id, 
                              form_id=next_form.id)
            return redirect('submission:submission_review', 
                          submission_id=submission.temporary_id)
    
    # GET request handling
    DynamicFormClass = generate_django_form(dynamic_form)
    current_data = {}
    
    # Get current version's data
    for entry in FormDataEntry.objects.filter(
        submission=submission,
        form=dynamic_form,
        version=submission.version
    ):
        field = DynamicFormClass.base_fields.get(entry.field_name)
        if field:
            if isinstance(field, forms.MultipleChoiceField):
                try:
                    current_data[entry.field_name] = process_field_value(
                        entry.value, 
                        getattr(dynamic_form.fields.get(name=entry.field_name), 'field_type', None)
                    )
                except json.JSONDecodeError:
                    current_data[entry.field_name] = []
            else:
                current_data[entry.field_name] = entry.value

    # If no current data and not version 1, get previous version's data
    if not current_data and submission.version > 1 and not submission.is_locked:
        for entry in FormDataEntry.objects.filter(
            submission=submission,
            form=dynamic_form,
            version=submission.version - 1
        ):
            field = DynamicFormClass.base_fields.get(entry.field_name)
            if field:
                if isinstance(field, forms.MultipleChoiceField):
                    try:
                        current_data[entry.field_name] = process_field_value(
                            entry.value,
                            getattr(dynamic_form.fields.get(name=entry.field_name), 'field_type', None)
                        )
                    except json.JSONDecodeError:
                        current_data[entry.field_name] = []
                else:
                    current_data[entry.field_name] = entry.value

    # Create form instance with processed data
    form_instance = DynamicFormClass(
        initial=current_data,
        prefix=f'form_{dynamic_form.id}'
    )

    context = {
        'form': form_instance,
        'submission': submission,
        'dynamic_form': dynamic_form,
        'previous_form': previous_form, 
    }
    return render(request, 'submission/dynamic_form.html', context)


# submission/views.py

@login_required
@check_submission_permission('submit')
def submission_review(request, submission_id):
    submission = get_object_or_404(Submission, temporary_id=submission_id)
    
    if submission.is_locked and not has_edit_permission(request.user, submission):
        messages.error(request, "You do not have permission to edit this submission.")
        return redirect('submission:dashboard')

    missing_documents = check_researcher_documents(submission)
    validation_errors = {}
    
    # Validate all forms
    for dynamic_form in submission.study_type.forms.order_by('order'):
        django_form_class = generate_django_form(dynamic_form)
        entries = FormDataEntry.objects.filter(
            submission=submission, 
            form=dynamic_form, 
            version=submission.version
        )
        saved_data = {
            f'form_{dynamic_form.id}-{entry.field_name}': entry.value
            for entry in entries
        }
        
        form_instance = django_form_class(data=saved_data, prefix=f'form_{dynamic_form.id}')
        is_valid = True
        errors = {}
        
        for field_name, field in form_instance.fields.items():
            if isinstance(field, forms.MultipleChoiceField):
                field_key = f'form_{dynamic_form.id}-{field_name}'
                field_value = saved_data.get(field_key)
                if not field_value and field.required:
                    is_valid = False
                    errors[field_name] = ['Please select at least one option']
            else:
                field_value = form_instance.data.get(f'form_{dynamic_form.id}-{field_name}')
                if field.required and not field_value:
                    is_valid = False
                    errors[field_name] = ['This field is required']

        if not is_valid:
            validation_errors[dynamic_form.name] = errors

    documents = submission.documents.all()
    doc_form = DocumentForm()
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'submit_final':
            missing_certs = check_researcher_documents(submission)
            if missing_certs:
                messages.error(request, 'Cannot submit: All team members must have valid certificates uploaded in the system.')
                return redirect('submission:submission_review', submission_id=submission_id)
            
            if missing_documents or validation_errors:
                messages.error(request, 'Please resolve the missing documents and form errors before final submission.')
            else:
                try:
                    with transaction.atomic():
                        # Lock submission and update status
                        submission.is_locked = True
                        submission.status = 'submitted'
                        submission.date_submitted = timezone.now()
                        
                        # Create version history entry
                        VersionHistory.objects.create(
                            submission=submission,
                            version=submission.version,
                            status=submission.status,
                            date=timezone.now()
                        )
			# Generate PDF once and store in buffer
                        buffer = generate_submission_pdf(
                            submission=submission,
                            version=submission.version,
                            user=request.user,
                            as_buffer=True
                        )

                        if not buffer:
                            raise ValueError("Failed to generate PDF for submission")

                        # Get system user for automated messages
                        system_user = get_system_user()
                        
                        # Create PDF filename
                        pdf_filename = f"submission_{submission.temporary_id}_v{submission.version}.pdf"

                        # Send confirmation to PI with PDF attachment
                        pi_message = Message.objects.create(
                            sender=system_user,
                            subject=f'Submission {submission.temporary_id} - Version {submission.version} Confirmation',
                            body=f"""
Dear {submission.primary_investigator.userprofile.full_name},

Your submission (ID: {submission.temporary_id}) has been successfully submitted.
Please find the attached PDF for your records.

Your submission will be reviewed by the OSAR who will direct it to the appropriate review bodies.

Best regards,
AIDI System
                            """.strip(),
                            related_submission=submission
                        )
                        pi_message.recipients.add(submission.primary_investigator)
                        
                        # Attach PDF to PI message
                        pi_attachment = MessageAttachment(message=pi_message)
                        pi_attachment.file.save(pdf_filename, ContentFile(buffer.getvalue()))

                        # Notify OSAR with PDF attachment
                        osar_coordinators = User.objects.filter(groups__name='OSAR')
                        osar_notification = Message.objects.create(
                            sender=system_user,
                            subject=f'New Submission For Review - {submission.title}',
                            body=f"""
A new research submission requires your initial review and forwarding.

Submission Details:
- ID: {submission.temporary_id}
- Title: {submission.title}
- PI: {submission.primary_investigator.userprofile.full_name}
- Study Type: {submission.study_type.name}
- Submitted: {timezone.now().strftime('%Y-%m-%d %H:%M')}

Please review the attached PDF and forward this submission to the appropriate review bodies.

Access the submission here: {request.build_absolute_uri(reverse('review:review_dashboard'))}

Best regards,
AIDI System
                            """.strip(),
                            related_submission=submission
                        )
                        
                        for coordinator in osar_coordinators:
                            osar_notification.recipients.add(coordinator)
                            
                        # Attach PDF to OSAR message
                        osar_attachment = MessageAttachment(message=osar_notification)
                        osar_attachment.file.save(pdf_filename, ContentFile(buffer.getvalue()))

                        # Notify co-investigators of required forms
                        notify_pending_forms(submission)

                        # Increment version AFTER everything else is done
                        submission.version += 1
                        submission.save()

                        messages.success(request, 'Submission has been finalized and sent to OSAR.')
                        return redirect('submission:dashboard')


                except Exception as e:
                    logger.error(f"Error in submission finalization: {str(e)}")
                    messages.error(request, f"Error during submission: {str(e)}")
                    return redirect('submission:dashboard')

        elif action == 'back':
            last_form = submission.study_type.forms.order_by('-order').first()
            if last_form:
                return redirect('submission:submission_form',
                              submission_id=submission.temporary_id,
                              form_id=last_form.id)
            return redirect('submission:add_coinvestigator',
                          submission_id=submission.temporary_id)

        elif action == 'exit_no_save':
            return redirect('submission:dashboard')

        elif action == 'upload_document':
            doc_form = DocumentForm(request.POST, request.FILES)
            if doc_form.is_valid():
                document = doc_form.save(commit=False)
                document.submission = submission
                document.uploaded_by = request.user
                
                ext = document.file.name.split('.')[-1].lower()
                if ext in Document.ALLOWED_EXTENSIONS:
                    document.save()
                    messages.success(request, 'Document uploaded successfully.')
                else:
                    messages.error(
                        request,
                        f'Invalid file type: .{ext}. Allowed types are: {", ".join(Document.ALLOWED_EXTENSIONS)}'
                    )
            else:
                messages.error(request, 'Please correct the errors in the document form.')

    context = {
        'submission': submission,
        'missing_documents': missing_documents,
        'validation_errors': validation_errors,
        'documents': documents,
        'doc_form': doc_form,
        'gpt_analysis': cache.get(f'gpt_analysis_{submission.temporary_id}_{submission.version}'),
        'can_submit': submission.can_user_submit(request.user), 
    }

    return render(request, 'submission/submission_review.html', context)

@login_required
def document_delete(request, submission_id, document_id):
    """Delete a document from a submission."""
    submission = get_object_or_404(Submission, pk=submission_id)
    document = get_object_or_404(Document, pk=document_id, submission=submission)
    
    if request.user == document.uploaded_by or has_edit_permission(request.user, submission):
        document.file.delete()
        document.delete()
        messages.success(request, 'Document deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this document.')
    
    return redirect('submission:submission_review', submission_id=submission_id)

@login_required
def version_history(request, submission_id):
    """View version history of a submission."""
    submission = get_object_or_404(Submission, pk=submission_id)
    if not has_edit_permission(request.user, submission):
        messages.error(request, "You do not have permission to view this submission.")
        return redirect('submission:dashboard')
        
    # Get all versions from version history, ordered by version number descending
    histories = VersionHistory.objects.filter(
        submission=submission
    ).order_by('-version')
    
    # Add a flag to each history item indicating if it can be compared
    for history in histories:
        history.can_compare = history.version > 1
    
    return render(request, 'submission/version_history.html', {
        'submission': submission,
        'histories': histories,
    })

@login_required
def compare_version(request, submission_id, version):
    """Compare a version with its previous version."""
    submission = get_object_or_404(Submission, pk=submission_id)
    if not has_edit_permission(request.user, submission):
        messages.error(request, "You do not have permission to view this submission.")
        return redirect('submission:dashboard')

    # Can't compare version 1 as it has no previous version
    if version <= 1:
        messages.error(request, "Version 1 cannot be compared as it has no previous version.")
        return redirect('submission:version_history', submission_id=submission_id)

    previous_version = version - 1
    comparison_data = []
    
    # Get all forms associated with this submission's study type
    forms = submission.study_type.forms.all()
    
    for form in forms:
        # Get entries for both versions
        entries_previous = FormDataEntry.objects.filter(
            submission=submission,
            form=form,
            version=previous_version
        ).select_related('form')
        
        entries_current = FormDataEntry.objects.filter(
            submission=submission,
            form=form,
            version=version
        ).select_related('form')

        # Convert entries to dictionaries for easier comparison
        data_previous = {entry.field_name: entry.value for entry in entries_previous}
        data_current = {entry.field_name: entry.value for entry in entries_current}

        # Get field display names from form definition
        field_definitions = {
            field.name: field.displayed_name 
            for field in form.fields.all()
        }

        # Compare fields
        form_changes = []
        all_fields = sorted(set(data_previous.keys()) | set(data_current.keys()))
        
        for field in all_fields:
            displayed_name = field_definitions.get(field, field)
            value_previous = data_previous.get(field, 'Not provided')
            value_current = data_current.get(field, 'Not provided')

            # Handle JSON array values (e.g., checkbox selections)
            try:
                if isinstance(value_previous, str) and value_previous.startswith('['):
                    value_previous_display = ', '.join(json.loads(value_previous))
                else:
                    value_previous_display = value_previous
                    
                if isinstance(value_current, str) and value_current.startswith('['):
                    value_current_display = ', '.join(json.loads(value_current))
                else:
                    value_current_display = value_current
            except json.JSONDecodeError:
                value_previous_display = value_previous
                value_current_display = value_current

            # Only add to changes if values are different
            if value_previous != value_current:
                form_changes.append({
                    'field': displayed_name,
                    'previous_value': value_previous_display,
                    'current_value': value_current_display
                })

        # Only add form to comparison data if it has changes
        if form_changes:
            comparison_data.append({
                'form_name': form.name,
                'changes': form_changes
            })

    return render(request, 'submission/compare_versions.html', {
        'submission': submission,
        'version': version,
        'previous_version': previous_version,
        'comparison_data': comparison_data,
    })

@login_required
def download_submission_pdf(request, submission_id, version=None):
    """Generate and download PDF version of a submission."""
    try:
        submission = get_object_or_404(Submission, pk=submission_id)
        if not has_edit_permission(request.user, submission):
            messages.error(request, "You do not have permission to view this submission.")
            return redirect('submission:dashboard')

        # If version is not specified, use version 1 for new submissions
        if version is None:
            # If submission.version is 2, it means we just submitted version 1
            version = submission.version 
            print(f"Version is {version}")
            
        logger.info(f"Generating PDF for submission {submission_id} version {version}")

        # Check if form entries exist for this version
        form_entries = FormDataEntry.objects.filter(
            submission=submission,
            version=version
        )
        
        if not form_entries.exists():
            logger.warning(f"No form entries found for version {version}, checking version 1")
            # Try version 1 as fallback
            version = 1
            form_entries = FormDataEntry.objects.filter(
                submission=submission,
                version=version
            )

        # Generate PDF
        response = generate_submission_pdf(
            submission=submission,
            version=version,
            user=request.user,
            as_buffer=False
        )
        
        if response is None:
            messages.error(request, "Error generating PDF. Please try again later.")
            logger.error(f"PDF generation failed for submission {submission_id} version {version}")
            return redirect('submission:dashboard')
            
        return response

    except Exception as e:
        logger.error(f"Error in download_submission_pdf: {str(e)}")
        logger.error("Error details:", exc_info=True)
        messages.error(request, "An error occurred while generating the PDF.")
        return redirect('submission:dashboard')

@login_required
def update_coinvestigator_order(request, submission_id):
    """Update the order of co-investigators in a submission."""
    if request.method == 'POST':
        submission = get_object_or_404(Submission, pk=submission_id)
        if not has_edit_permission(request.user, submission):
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        try:
            order = json.loads(request.POST.get('order', '[]'))
            for index, coinvestigator_id in enumerate(order):
                CoInvestigator.objects.filter(
                    id=coinvestigator_id,
                    submission=submission
                ).update(order=index)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def user_autocomplete(request):
    term = request.GET.get('term', '').strip()
    submission_id = request.GET.get('submission_id')
    user_type = request.GET.get('user_type')  # 'investigator', 'assistant', or 'coinvestigator'
    
    if len(term) < 2:
        return JsonResponse([], safe=False)

    # Start with base user query
    users = User.objects.filter(
        Q(userprofile__full_name__icontains=term) |
        Q(first_name__icontains=term) |
        Q(last_name__icontains=term) |
        Q(email__icontains=term)
    )

    if submission_id:
        submission = get_object_or_404(Submission, pk=submission_id)
        
        # Exclude users already assigned to this submission in any role
        excluded_users = []
        
        # Exclude primary investigator
        if submission.primary_investigator:
            excluded_users.append(submission.primary_investigator.id)
        
        # Exclude research assistants
        assistant_ids = ResearchAssistant.objects.filter(
            submission=submission
        ).values_list('user_id', flat=True)
        excluded_users.extend(assistant_ids)
        
        # Exclude co-investigators
        coinvestigator_ids = CoInvestigator.objects.filter(
            submission=submission
        ).values_list('user_id', flat=True)
        excluded_users.extend(coinvestigator_ids)

        users = users.exclude(id__in=excluded_users)

    users = users.distinct()[:10]

    results = [
        {
            'id': user.id,
            'label': f"{user.userprofile.full_name or user.get_full_name()} ({user.email})"
        }
        for user in users
    ]

    return JsonResponse(results, safe=False)

@login_required
def submission_autocomplete(request):
    """View for handling submission autocomplete requests"""
    term = request.GET.get('term', '')
    user = request.user
    
    # Query submissions that the user has access to
    submissions = Submission.objects.filter(
        Q(primary_investigator=user) |
        Q(coinvestigators__user=user) |
        Q(research_assistants__user=user),
        Q(title__icontains=term) |
        Q(khcc_number__icontains=term)
    ).distinct()[:10]

    results = []
    for submission in submissions:
        label = f"{submission.title}"
        if submission.khcc_number:
            label += f" (IRB: {submission.khcc_number})"
        results.append({
            'id': submission.temporary_id,
            'text': label
        })

    return JsonResponse({'results': results}, safe=False)




@login_required
def submission_detail(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    versions = submission.version_histories.all()
    return render(request, 'submission/submission_detail.html', {
        'submission': submission,
        'versions': versions
    })

@login_required
def view_version(request, submission_id, version_number):
    """View a specific version of a submission."""
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # Check permissions
    if not has_edit_permission(request.user, submission):
        messages.error(request, "You do not have permission to view this submission.")
        return redirect('submission:dashboard')

    # Check if version exists
    version_history = get_object_or_404(
        VersionHistory, 
        submission=submission, 
        version=version_number
    )

    # Get form data for this version
    form_data = {}
    for form in submission.study_type.forms.all():
        entries = FormDataEntry.objects.filter(
            submission=submission,
            form=form,
            version=version_number
        ).select_related('form')
        
        form_data[form.name] = {
            'form': form,
            'entries': {entry.field_name: entry.value for entry in entries}
        }

    # Get documents that existed at this version
    # You might need to adjust this depending on how you track document versions
    documents = submission.documents.filter(
        uploaded_at__lte=version_history.date
    )

    context = {
        'submission': submission,
        'version_number': version_number,
        'version_history': version_history,
        'form_data': form_data,
        'documents': documents,
        'is_current_version': version_number == submission.version,
    }
    
    return render(request, 'submission/view_version.html', context)


# views.py
@login_required
def investigator_form(request, submission_id, form_id):
    """Handle investigator form submission."""
    submission = get_object_or_404(Submission, pk=submission_id)
    form = get_object_or_404(DynamicForm, pk=form_id)
    
    # Check if user is allowed to submit this form
    if request.user != submission.primary_investigator and \
       not submission.coinvestigators.filter(user=request.user).exists():
        messages.error(request, "You are not authorized to submit this form.")
        return redirect('submission:dashboard')
        
    # Check if form is already submitted
    if InvestigatorFormSubmission.objects.filter(
        submission=submission,
        form=form,
        investigator=request.user,
        version=submission.version
    ).exists():
        messages.error(request, "You have already submitted this form.")
        return redirect('submission:dashboard')

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'submit_form':
            form_class = generate_django_form(form)
            form_instance = form_class(request.POST)
            
            if form_instance.is_valid():
                try:
                    with transaction.atomic():
                        # Save form data
                        for field_name, value in form_instance.cleaned_data.items():
                            FormDataEntry.objects.create(
                                submission=submission,
                                form=form,
                                field_name=field_name,
                                value=value,
                                version=submission.version
                            )
                        
                        # Record form submission
                        InvestigatorFormSubmission.objects.create(
                            submission=submission,
                            form=form,
                            investigator=request.user,
                            version=submission.version
                        )

                        # Check if all forms are complete
                        if submission.are_all_investigator_forms_complete():
                            # Notify all users who can submit
                            notify_form_completion(submission)

                        messages.success(request, f"Form '{form.name}' submitted successfully.")
                        return redirect('submission:dashboard')
                        
                except Exception as e:
                    logger.error(f"Error saving investigator form: {str(e)}")
                    messages.error(request, "An error occurred while saving your form.")
            else:
                messages.error(request, "Please correct the errors in the form.")
    else:
        form_class = generate_django_form(form)
        form_instance = form_class()

    return render(request, 'submission/investigator_form.html', {
        'form': form_instance,
        'dynamic_form': form,
        'submission': submission
    })

def notify_form_completion(submission):
    """Notify relevant users when all forms are complete."""
    system_user = get_system_user()
    
    # Get all users who can submit
    recipients = []
    recipients.append(submission.primary_investigator)
    recipients.extend([
        ci.user for ci in submission.coinvestigators.filter(can_submit=True)
    ])
    recipients.extend([
        ra.user for ra in submission.research_assistants.filter(can_submit=True)
    ])
    
    # Create notification message
    message = Message.objects.create(
        sender=system_user,
        subject=f'All Required Forms Completed - {submission.title}',
        body=f"""
All investigators have completed their required forms for:

Submission ID: {submission.temporary_id}
Title: {submission.title}

The submission is now ready for review.

Best regards,
AIDI System
        """.strip(),
        related_submission=submission
    )
    
    # Add recipients
    for recipient in recipients:
        message.recipients.add(recipient)

def notify_pending_forms(submission):
    """Notify co-investigators of pending forms."""
    system_user = get_system_user()
    required_forms = submission.get_required_investigator_forms()
    
    if not required_forms.exists():
        return
        
    form_names = ", ".join([form.name for form in required_forms])
    
    # Create notification for all co-investigators
    message = Message.objects.create(
        sender=system_user,
        subject=f'Forms Required - {submission.title}',
        body=f"""
You need to complete the following forms for:

Submission ID: {submission.temporary_id}
Title: {submission.title}

Required Forms:
{form_names}

Please log in to the system and complete these forms at your earliest convenience.

Best regards,
AIDI System
        """.strip(),
        related_submission=submission
    )
    
    # Add all co-investigators as recipients
    for coinv in submission.coinvestigators.all():
        message.recipients.add(coinv.user)


@login_required
def check_form_status(request, submission_id):
    """AJAX endpoint to check form completion status."""
    submission = get_object_or_404(Submission, pk=submission_id)
    
    if not has_edit_permission(request.user, submission):
        return JsonResponse({'error': 'Permission denied'}, status=403)
        
    status = submission.get_investigator_form_status()
    all_complete = submission.are_all_investigator_forms_complete()
    
    return JsonResponse({
        'status': status,
        'all_complete': all_complete
    })


# if you don't want to allow submission withouth coauthors filling their forms.
# views.py

# @login_required
# def submission_review(request, submission_id):
#     """Existing submission review view - add this to the submit_final section"""
#     if request.method == 'POST':
#         action = request.POST.get('action')
        
#         if action == 'submit_final':
#             if missing_documents or validation_errors:
#                 messages.error(request, 'Please resolve the missing documents and form errors before final submission.')
#             else:
#                 try:
#                     with transaction.atomic():
#                         # ... existing submission code ...
                        
#                         # Add this after submission is created but before redirecting
#                         required_forms = submission.get_required_investigator_forms()
#                         if required_forms.exists():
#                             # Notify co-investigators of required forms
#                             notify_pending_forms(submission)
                        
#                         messages.success(request, 'Submission has been finalized and sent to OSAR.')
#                         return redirect('submission:dashboard')
                        
#                 except Exception as e:
#                     logger.error(f"Error in submission finalization: {str(e)}")
#                     messages.error(request, f"Error during submission: {str(e)}")
#                     return redirect('submission:dashboard')

# # Optional: Add periodic check for overdue forms
# @login_required
# def check_overdue_forms(request):
#     """Administrative view to check for overdue forms."""
#     if not request.user.is_staff:
#         messages.error(request, "Permission denied.")
#         return redirect('submission:dashboard')
        
#     overdue_submissions = Submission.objects.filter(
#         status='submitted'
#     ).exclude(
#         study_type__forms__requested_per_investigator=False
#     )
    
#     overdue_data = []
#     for submission in overdue_submissions:
#         if not submission.are_all_investigator_forms_complete():
#             overdue_data.append({
#                 'submission': submission,
#                 'status': submission.get_investigator_form_status()
#             })
    
#     return render(request, 'submission/overdue_forms.html', {
#         'overdue_data': overdue_data
#     })

# # Add this URL if you want the overdue forms check
# urlpatterns += [
#     path('check-overdue-forms/',
#          views.check_overdue_forms,
#          name='check_overdue_forms'),
# ]

@login_required
def archive_submission(request, submission_id):
    """Archive a submission."""
    submission = get_object_or_404(Submission, temporary_id=submission_id)
    if request.method == 'POST':
        try:
            submission.is_archived = True
            submission.archived_at = timezone.now()
            submission.save(update_fields=['is_archived', 'archived_at'])
            messages.success(request, f'Submission "{submission.title}" has been archived.')
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required
def unarchive_submission(request, submission_id):
    """Unarchive a submission."""
    submission = get_object_or_404(Submission, temporary_id=submission_id)
    if request.method == 'POST':
        try:
            submission.is_archived = False
            submission.archived_at = None
            submission.save(update_fields=['is_archived', 'archived_at'])
            messages.success(request, f'Submission "{submission.title}" has been unarchived.')
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required
def archived_dashboard(request):
    """Display archived submissions dashboard."""
    submissions = Submission.objects.filter(
        is_archived=True
    ).select_related(
        'primary_investigator__userprofile'
    ).order_by('-date_created')

    return render(request, 'submission/archived_dashboard.html', {
        'submissions': submissions,
    })

@login_required
def view_submission(request, submission_id):
    """View submission details."""
    submission = get_object_or_404(Submission, temporary_id=submission_id)
    if not has_edit_permission(request.user, submission):
        messages.error(request, "You do not have permission to view this submission.")
        return redirect('submission:dashboard')
        
    context = {
        'submission': submission,
        'versions': submission.version_histories.all().order_by('-version'),
    }
    return render(request, 'submission/view_submission.html', context)