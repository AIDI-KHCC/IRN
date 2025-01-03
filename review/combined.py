# Combined Python and HTML files
# Generated from directory: C:\Users\isult\Dropbox\AI\Projects\IRN3\review
# Total files found: 63



# Contents from: .\pdf\dashboard_export.html
{# review/templates/review/pdf/dashboard_export.html #}
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .header { text-align: center; margin-bottom: 20px; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left;
        font-size: 12px; }
        th { background-color: #f5f5f5; }
        .status-badge {
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 11px;
            color: white;
        }
        .status-pending { background-color: #ffc107; }
        .status-accepted { background-color: #17a2b8; }
        .status-completed { background-color: #28a745; }
        .status-overdue { background-color: #dc3545; }
        .section-header { 
            font-size: 16px;
            font-weight: bold;
            margin: 20px 0 10px 0;
            padding-bottom: 5px;
            border-bottom: 2px solid #333;
        }
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            text-align: center;
            font-size: 10px;
            padding: 10px 0;
            border-top: 1px solid #ddd;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Review Dashboard Export</h1>
        <p>Generated on: {{ date|date:"F d, Y H:i" }}</p>
        <p>Reviewer: {{ user.userprofile.full_name }}</p>
    </div>

    <div class="section-header">Pending Reviews</div>
    <table>
        <thead>
            <tr>
                <th>Title</th>
                <th>Primary Investigator</th>
                <th>Study Type</th>
                <th>Deadline</th>
                <th>Status</th>
                <th>Days Remaining</th>
            </tr>
        </thead>
        <tbody>
            {% for review in pending_reviews %}
            <tr>
                <td>{{ review.submission.title }}</td>
                <td>{{ review.submission.primary_investigator.userprofile.full_name }}</td>
                <td>{{ review.submission.study_type.name }}</td>
                <td>{{ review.deadline|date:"M d, Y" }}</td>
                <td>
                    <span class="status-badge status-{{ review.status|lower }}">
                        {{ review.get_status_display }}
                    </span>
                </td>
                <td>{{ review.days_until_deadline }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <div class="section-header">Completed Reviews</div>
    <table>
        <thead>
            <tr>
                <th>Title</th>
                <th>Primary Investigator</th>
                <th>Study Type</th>
                <th>Submitted On</th>
            </tr>
        </thead>
        <tbody>
            {% for review in completed_reviews %}
            <tr>
                <td>{{ review.submission.title }}</td>
                <td>{{ review.submission.primary_investigator.userprofile.full_name }}</td>
                <td>{{ review.submission.study_type.name }}</td>
                <td>{{ review.date_submitted|date:"M d, Y" }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <div class="footer">
        <p>Generated from iRN System - Page {page_number} of {total_pages}</p>
    </div>
</body>
</html>

{# review/templates/review/includes/review_actions.html #}
<div class="btn-group" role="group">
    {% if review.status == 'pending' %}
    <a href="{% url 'review:submit_review' review.id %}" class="btn btn-sm btn-primary">
        <i class="fas fa-edit"></i> Review
    </a>
    {% elif review.status == 'accepted' %}
    <a href="{% url 'review:submit_review' review.id %}" class="btn btn-sm btn-info">
        <i class="fas fa-check"></i> Complete
    </a>
    {% endif %}
    
    <button type="button" class="btn btn-sm btn-secondary dropdown-toggle" data-bs-toggle="dropdown">
        <i class="fas fa-ellipsis-v"></i>
    </button>
    <ul class="dropdown-menu">
        <li>
            <a class="dropdown-item" href="{% url 'review:view_review' review.id %}">
                <i class="fas fa-eye"></i> View Details
            </a>
        </li>
        {% if review.status == 'pending' %}
        <li>
            <a class="dropdown-item text-warning" href="{% url 'review:request_extension' review.id %}">
                <i class="fas fa-clock"></i> Request Extension
            </a>
        </li>
        <li>
            <a class="dropdown-item text-danger" href="{% url 'review:decline_review' review.id %}">
                <i class="fas fa-times"></i> Decline Review
            </a>
        </li>
        {% endif %}
        <li>
            <a class="dropdown-item" href="{% url 'messaging:compose_message' %}?related_review={{ review.id }}">
                <i class="fas fa-envelope"></i> Send Message
            </a>
        </li>
    </ul>
</div>

# Contents from: .\templates\review\assign_khcc_number.html
{% extends "base.html" %}

{% block content %}
<div class="container mt-4">
    <h2>Assign KHCC #</h2>
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{{ submission.title }}</h5>
            <p class="card-text">Primary Investigator: {{ submission.primary_investigator.get_full_name }}</p>
            
            <form method="post">
                {% csrf_token %}
                <div class="mb-3">
                    <label for="khcc_number" class="form-label">KHCC #</label>
                    <input type="text" 
                           class="form-control" 
                           id="khcc_number" 
                           name="khcc_number" 
                           value="{{ suggested_irb }}"
                           required>
                    <div class="form-text">Suggested format: YYYY-XXX</div>
                </div>
                
                <div class="mt-3">
                    <button type="submit" class="btn btn-primary">Assign KHCC #</button>
                    <a href="{% url 'review:review_summary' submission.temporary_id %}" 
                       class="btn btn-secondary">Cancel</a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %} 

# Contents from: .\templates\review\create_review_request.html
<!-- review/templates/review/create_review_request.html -->
{% extends 'base.html' %}
{% block content %}
<h2>Create Review Request for "{{ submission.title }}" (Version {{ submission.version }})</h2>
<form method="post">
    {% csrf_token %}
    {{ form.non_field_errors }}

    <div class="form-group">
        {{ form.requested_to.label_tag }}
        <select name="requested_to" id="id_requested_to" class="form-control select2"></select>
        {{ form.requested_to.errors }}
        <small class="form-text text-muted">{{ form.requested_to.help_text }}</small>
    </div>

    <div class="form-group">
        {{ form.deadline.label_tag }}
        {{ form.deadline }}
        {{ form.deadline.errors }}
        <small class="form-text text-muted">{{ form.deadline.help_text }}</small>
    </div>

    <div class="form-group">
        {{ form.message.label_tag }}
        {{ form.message }}
        {{ form.message.errors }}
        <small class="form-text text-muted">{{ form.message.help_text }}</small>
    </div>

    <div class="form-group">
        {{ form.selected_forms.label_tag }}
        {{ form.selected_forms }}
        {{ form.selected_forms.errors }}
        <small class="form-text text-muted">
            Available forms for {{ submission.study_type.name }}. 
            Select all applicable review forms.
        </small>
    </div>

    <div class="form-check mb-3">
        {{ form.can_forward }}
        <label class="form-check-label" for="{{ form.can_forward.id_for_label }}">
            Allow reviewer to forward this request to others
        </label>
    </div>

    <button type="submit" class="btn btn-primary">Send Review Request</button>
</form>
{% endblock %}

{% block page_specific_js %}
<script>
    $(document).ready(function() {
        $('#id_requested_to').select2({
            theme: 'bootstrap4',
            ajax: {
                url: '{% url "submission:user-autocomplete" %}',
                dataType: 'json',
                delay: 250,
                data: function (params) {
                    return {
                        term: params.term,
                        submission_id: '{{ submission.id }}',
                        user_type: 'reviewer'
                    };
                },
                processResults: function (data) {
                    return {
                        results: data.map(function(item) {
                            return {
                                id: item.id,
                                text: item.label
                            };
                        })
                    };
                },
                cache: true
            },
            minimumInputLength: 2,
            placeholder: 'Search for reviewer...',
            allowClear: true,
            width: '100%'
        });

        // Handle initial value if it exists
        {% if form.requested_to.initial %}
            var initialUser = {
                id: '{{ form.requested_to.initial.id }}',
                text: '{{ form.requested_to.initial.get_full_name|escapejs }}'
            };
            var initialOption = new Option(initialUser.text, initialUser.id, true, true);
            $('#id_requested_to').append(initialOption).trigger('change');
        {% endif %}
    });
</script>
{% endblock %}


# Contents from: .\templates\review\dashboard.html
{% extends 'base.html' %}
{% load static %}
{% load review_tags %}
{% csrf_token %}



{% block content %}
<script type="text/babel">
// Define the ToggleSwitch component
const ToggleSwitch = ({ submissionId, initialState = false, label = '', type = '' }) => {
    const [isEnabled, setIsEnabled] = React.useState(initialState === 'true');
    const [isLoading, setIsLoading] = React.useState(false);

    const handleToggle = async () => {
        setIsLoading(true);
        try {
            const response = await fetch(`/review/submission/${submissionId}/toggle-visibility/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `toggle_type=${type}&csrfmiddlewaretoken=${document.querySelector('[name=csrfmiddlewaretoken]').value}`
            });

            if (response.ok) {
                const data = await response.json();
                setIsEnabled(data.visible);
            }
        } catch (error) {
            console.error('Error toggling visibility:', error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="form-check form-switch mb-2">
            <input
                className="form-check-input"
                type="checkbox"
                checked={isEnabled}
                onChange={handleToggle}
                disabled={isLoading}
                id={`switch-${type}-${submissionId}`}
            />
            <label className="form-check-label ms-2" htmlFor={`switch-${type}-${submissionId}`}>
                {label}
            </label>
        </div>
    );
};

// Define the VisibilityToggles component
const VisibilityToggles = ({ submissionId, initialIrbState, initialRcState }) => {
    return (
        <div className="d-flex flex-column">
            <ToggleSwitch 
                submissionId={submissionId} 
                initialState={initialIrbState} 
                label="IRB" 
                type="irb" 
            />
            <ToggleSwitch 
                submissionId={submissionId} 
                initialState={initialRcState} 
                label="RC" 
                type="rc" 
            />
        </div>
    );
};
</script>

<div class="container">
    <!-- Dynamic Dashboard Header based on user group -->
    {% if is_irb %}
        <h2 class="mb-4">IRB Dashboard</h2>
    {% elif is_rc %}
        <h2 class="mb-4">RC Dashboard</h2>
    {% elif is_osar %}
        <h2 class="mb-4">OSAR Dashboard</h2>
    {% else %}
        <h2 class="mb-4">Review Dashboard</h2>
    {% endif %}
    
    <!-- Submissions Section - Only visible for OSAR, IRB, or RC members -->
    {% if is_osar or is_irb or is_rc %}
        <div class="card mb-4">
            <div class="card-header">
                <h2 class="card-title">Submissions</h2>
            </div>

            <div class="card-body">
                <!-- Filter Controls -->
                <div class="row g-3 mb-4">
                    <div class="col-md-4">
                        <label for="statusFilter" class="form-label">Filter by Status:</label>
                        <select id="statusFilter" class="form-select">
                            <option value="">All Statuses</option>
                            {% for status, label in submission_status_choices %}
                                <option value="{{ status }}">{{ label }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div class="col-md-2">
                        <label for="entriesFilter" class="form-label">Show entries:</label>
                        <select id="entriesFilter" class="form-select">
                            <option value="10">10</option>
                            <option value="25">25</option>
                            <option value="50">50</option>
                            <option value="-1">All</option>
                        </select>
                    </div>
                    <div class="col-md-6">
                        <label for="searchFilter" class="form-label">Search:</label>
                        <input type="search" id="searchFilter" class="form-control" placeholder="Type to search...">
                    </div>
                </div>

            <div class="card-body">
                {% if submissions %}
                    <div class="table-responsive">
                        <table id="osarSubmissionsTable" class="table table-hover">
                            <thead>
                                <tr>
                                    <th>KHCC#</th>
                                    <th>Title</th>
                                    <th>Submission Date</th>
                                    <th>Primary Investigator</th>
                                    <th>Requests</th>
                                    <th>Days</th>
                                    <th>✅</th>
                                    <th>Status</th>
                                    {% if is_osar%}
                                        <th>Visibility</th>
                                    {% endif %}
                                    <th>Actions</th>
                                    <th>
                                        {% if is_osar or is_irb %}
                                            Decision
                                        {% endif %}
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for submission in submissions %}
                                <tr>
                                    <td>{{ submission.khcc_number|default:"-" }}</td>
                                    <td>{{ submission.title }}</td>
                                    <td>{{ submission.date_submitted|date:"Y-m-d"|default:"-" }}</td>
                                    <td>{{ submission.primary_investigator.userprofile.full_name }}</td>
                                    <td>
                                        {% if submission.review_requests.exists %}
                                            <ul class="list-unstyled mb-0">
                                            {% for request in submission.review_requests.all %}
                                                <li>
                                                    <strong>
                                                        <a href="{% url 'messaging:compose_message' %}?recipient={{ request.requested_to.id }}&submission={{ submission.id }}" 
                                                           class="text-primary text-decoration-none">
                                                            {{ request.requested_to.userprofile.user}}
                                                        </a>
                                                    </strong>
                                                </li>
                                            {% endfor %}
                                            </ul>
                                        {% else %}
                                            No requests yet
                                        {% endif %}
                                    </td>
                                    <td>
                                        {% if submission.review_requests.exists %}
                                            <ul class="list-unstyled mb-0">
                                            {% for request in submission.review_requests.all %}
                                                <li>
                                                    {% with days=request.created_at|timesince_in_days %}
                                                        {{ days }}
                                                    {% endwith %}
                                                </li>
                                            {% endfor %}
                                            </ul>
                                        {% else %}
                                            -
                                        {% endif %}
                                    </td>
                                    <td>
                                        {% if submission.review_requests.exists %}
                                            <ul class="list-unstyled mb-0">
                                            {% for request in submission.review_requests.all %}
                                                <li>
                                                    {% if request.status == 'completed' %}
                                                        <span class="text-success">✅</span>
                                                    {% elif request.status == 'declined' %}
                                                        <span class="text-danger">❌</span>
                                                    {% elif request.status == 'pending' %}
                                                        <span class="text-warning">⏳</span>
                                                    {% else %}
                                                        <span class="text-secondary">-</span>
                                                    {% endif %}
                                                </li>
                                            {% endfor %}
                                            </ul>
                                        {% else %}
                                            -
                                        {% endif %}
                                    </td>
                                    <td>
                                        <span class="badge badge-{{ submission.status|slugify }}">
                                            {{ submission.get_status_display|default:"" }}
                                        </span>
                                    </td>
                                    {% if is_osar %}
                                        <td>
                                            <div id="toggle-container-{{ submission.temporary_id }}" class="visibility-toggles"></div>
                                            <script type="text/babel">
                                                {
                                                    const container = document.getElementById('toggle-container-{{ submission.temporary_id }}');
                                                    const root = ReactDOM.createRoot(container);
                                                    root.render(
                                                        <VisibilityToggles 
                                                            submissionId="{{ submission.temporary_id }}"
                                                            initialIrbState="{{ submission.show_in_irb|yesno:'true,false' }}"
                                                            initialRcState="{{ submission.show_in_rc|yesno:'true,false' }}"
                                                        />
                                                    );
                                                }
                                            </script>
                                        </td>
                                    {% endif %}
                                    <td>
                                        <div class="action-buttons">
                                            {% if is_osar %}
                                                <a href="{% url 'review:create_review_request' submission.pk%}" 
                                                   class="btn btn-primary btn-sm" style="width: 85px;">
                                                    <i class="fas fa-plus"></i> Request
                                                </a>
                                            {% endif %}
                                            <a href="{% url 'review:review_summary' submission.pk %}" 
                                               class="btn btn-success btn-sm" style="width: 85px;">
                                                <i class="fas fa-info-circle"></i> Details
                                            </a>
                                            {% if is_osar or is_irb and not submission.khcc_number %}
                                                <a href="{% url 'review:assign_irb' submission.pk %}" 
                                                   class="btn btn-info btn-sm" style="width: 85px;">
                                                    <i class="fas fa-hashtag"></i> KHCC#
                                                </a>
                                            {% endif %}
                                            <a href="{% url 'review:view_notepad' submission.pk group_name %}" 
                                               class="btn {% if submission.has_unread_notes %}btn-danger{% else %}btn-info{% endif %} btn-sm" 
                                               style="width: 85px;">
                                                <i class="fas fa-sticky-note"></i> Notes
                                               
                                            </a>
                                        </div>
                                    </td>
                                    <td>
                                        {% if is_osar or is_irb %}
                                            {% if submission.status not in 'accepted,rejected,closed,withdrawn'|stringformat:'s'|split_string %}
                                                <div class="action-buttons">
                                                    <button type="button" 
                                                            class="btn btn-warning btn-sm decision-btn" 
                                                            style="width: 100px;"
                                                            data-bs-toggle="modal" 
                                                            data-bs-target="#decisionModal"
                                                            data-submission-id="{{ submission.pk }}"
                                                            data-action="revision_requested">
                                                        <i class="fas fa-undo"></i> Revision
                                                    </button>
                                                    <button type="button" 
                                                            class="btn btn-danger btn-sm decision-btn" 
                                                            style="width: 100px;"
                                                            data-bs-toggle="modal" 
                                                            data-bs-target="#decisionModal"
                                                            data-submission-id="{{ submission.pk }}"
                                                            data-action="rejected">
                                                        <i class="fas fa-times"></i> Reject
                                                    </button>
                                                        <button type="button" 
                                                                    class="btn btn-info btn-sm decision-btn" 
                                                                    style="width: 100px;"
                                                                    data-bs-toggle="modal" 
                                                                    data-bs-target="#decisionModal"
                                                                    data-submission-id="{{ submission.pk }}"
                                                                    data-action="provisional_approval">
                                                                <i class="fas fa-check-circle"></i>Provisional
                                                            </button>
                                                            <button type="button" 
                                                            class="btn btn-success btn-sm decision-btn" 
                                                            style="width: 100px;"
                                                            data-bs-toggle="modal" 
                                                            data-bs-target="#decisionModal"
                                                            data-submission-id="{{ submission.pk }}"
                                                            data-action="accepted">
                                                        <i class="fas fa-check"></i> Accept
                                                    </button>
                                                </div>
                                            {% endif %}
                                            {% if submission.status == 'accepted' %}
                                            <div class="action-buttons">
                                                <button type="button" 
                                                        class="btn btn-danger btn-sm decision-btn" 
                                                        style="width: 100px;"
                                                        data-bs-toggle="modal" 
                                                        data-bs-target="#decisionModal"
                                                        data-submission-id="{{ submission.pk }}"
                                                        data-action="suspended">
                                                    <i class="fas fa-pause"></i> Suspend
                                                </button>
                                            </div>
                                            {% endif %}
                                        {% endif %}
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                {% else %}
                    <p class="mb-0">No submissions found.</p>
                {% endif %}
            </div>
        </div>
    {% endif %}

    <!-- Decision Modal -->
    <div class="modal fade" id="decisionModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Make Decision</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="decisionForm" method="post">
                        {% csrf_token %}
                        <input type="hidden" name="action" id="decisionAction">
                        <div class="mb-3">
                            <label for="comments" class="form-label">Comments</label>
                            <textarea class="form-control" id="comments" name="comments" rows="4" required></textarea>
                            <div class="form-text">
                                Please provide detailed comments explaining your decision.
                            </div>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" id="submitDecision">Submit Decision</button>
                </div>
            </div>
        </div>
    </div>



{# Common Section for All Users - Pending Reviews #}
<div class="card mb-4">
    <div class="card-header">
        <h3 class="card-title mb-0">My Pending Reviews</h3>
    </div>
    <div class="card-body">
        {% if pending_reviews %}
            <div class="table-responsive">
                <table id="pendingReviewsTable" class="table table-hover">
                    <thead>
                        <tr>
                            <th>Title</th>
                            <th>Primary Investigator</th>
                            <th>Requested By</th>
                            <th>Deadline</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for review in pending_reviews %}
                        <tr>
                            <td>{{ review.submission.title }}</td>
                            <td>{{ review.submission.primary_investigator.userprofile.full_name }}</td>
                            <td>{{ review.requested_by.userprofile.full_name }}</td>
                            <td>{{ review.deadline }}</td>
                            <td>{{ review.get_status_display }}</td>
                            <td>
                                <div class="btn-group">
                                    <a href="{% url 'review:submit_review' review.id %}" class="btn btn-primary btn-sm">
                                        <i class="fas fa-paper-plane"></i> Submit Review
                                    </a>
                                    {% if review.can_forward and review.submission %}
                                        <a href="{% url 'review:create_review_request' submission_id=review.submission.pk %}" 
                                           class="btn btn-info btn-sm">
                                            <i class="fas fa-share"></i> Request Review
                                        </a>
                                    {% endif %}
                                    <a href="{% url 'review:decline_review' review.id %}" class="btn btn-danger btn-sm">
                                        <i class="fas fa-times"></i> Decline
                                    </a>
                                    <a href="{% url 'review:request_extension' review.id %}" class="btn btn-warning btn-sm">
                                        <i class="fas fa-clock"></i> Request Extension
                                    </a>
                                    <a href="{% url 'review:review_summary' review.submission.pk %}" class="btn btn-success btn-sm">
                                        <i class="fas fa-info-circle"></i>  Details
                                    </a>
                                </div>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        {% else %}
            <p class="mb-0">No pending reviews.</p>
        {% endif %}
    </div>
</div>

{# Common Section for All Users - Completed Reviews #}
<div class="card">
    <div class="card-header">
        <h3 class="card-title mb-0">My Completed Reviews</h3>
    </div>
    <div class="card-body">
        {% if completed_reviews %}
            <div class="table-responsive">
                <table id="completedReviewsTable" class="table table-hover">
                    <thead>
                        <tr>
                            <th>Title</th>
                            <th>Primary Investigator</th>
                            <th>Requested By</th>
                            <th>Completion Date</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for review in completed_reviews %}
                        <tr>
                            <td>{{ review.submission.title }}</td>
                            <td>{{ review.submission.primary_investigator.userprofile.full_name }}</td>
                            <td>{{ review.requested_by.userprofile.full_name }}</td>
                            <td>{{ review.updated_at }}</td>
                            <td>
                                <div class="btn-group">
                                    <a href="{% url 'review:view_review' review.id %}" class="btn btn-info btn-sm">View Review</a>
                                    <a href="{% url 'review:download_review_pdf' review.id %}" class="btn btn-primary btn-sm">PDF</a>
                                    <a href="{% url 'review:review_summary' review.submission.pk %}" class="btn btn-success btn-sm">Details</a>
                                </div>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        {% else %}
            <p class="mb-0">No completed reviews.</p>
        {% endif %}
    </div>
</div>
</div>


{% endblock %}
{% block page_specific_js %}
<script src="https://cdn.datatables.net/1.10.24/js/jquery.dataTables.min.js"></script>
<script src="https://cdn.datatables.net/1.10.24/js/dataTables.bootstrap4.min.js"></script>
<script src="https://cdn.datatables.net/buttons/2.2.3/js/dataTables.buttons.min.js"></script>
<script src="https://cdn.datatables.net/buttons/2.2.3/js/buttons.bootstrap4.min.js"></script>
<script>
$(document).ready(function() {
    // Initialize DataTables with custom controls
    var submissionsTable = $('#osarSubmissionsTable').DataTable({
        order: [[1, 'desc']],
        pageLength: 10,
        lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
        dom: 'Brt<"bottom"ip>',
        buttons: ['copy', 'excel', 'pdf']
    });

    // Connect custom filter controls
    $('#entriesFilter').on('change', function() {
        submissionsTable.page.len($(this).val()).draw();
    });

    $('#searchFilter').on('keyup', function() {
        submissionsTable.search(this.value).draw();
    });

    // Status Filter
    $('#statusFilter').on('change', function() {
        var selectedStatus = $(this).val();
        
        // Clear existing filter
        submissionsTable.column(7).search('').draw();
        
        // Apply new filter if a status is selected
        if (selectedStatus) {
            submissionsTable.column(7).search(selectedStatus, true, false).draw();
        }
    });

    // Handle Decision Modal
    const decisionModal = document.getElementById('decisionModal');
    const decisionForm = document.getElementById('decisionForm');
    const decisionAction = document.getElementById('decisionAction');
    const submitButton = document.getElementById('submitDecision');
    let currentSubmissionId;

    // Handle modal opening
    decisionModal.addEventListener('show.bs.modal', function(event) {
        const button = event.relatedTarget;
        currentSubmissionId = button.dataset.submissionId;
        decisionAction.value = button.dataset.action;
        
        // Update modal title based on action
        const actionDisplay = decisionAction.value
            .replace(/_/g, ' ')
            .replace(/\b\w/g, l => l.toUpperCase());
            
        this.querySelector('.modal-title').textContent = actionDisplay;
        
        // Clear previous comments
        document.getElementById('comments').value = '';
        
        // Reset submit button
        submitButton.disabled = false;
        submitButton.innerHTML = 'Submit Decision';

        console.log('Modal opened for submission:', currentSubmissionId, 'action:', decisionAction.value);
    });

 // Handle decision submission
submitButton.addEventListener('click', function() {
    const comments = document.getElementById('comments').value.trim();
    if (!comments) {
        alert('Please provide comments for your decision');
        return;
    }

    // Show loading state
    this.disabled = true;
    this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';

    // Create the request data
    const requestData = {
        action: decisionAction.value,
        comments: comments
    };

    console.log('Submitting decision:', requestData);

    fetch(`/review/submission/${currentSubmissionId}/process-decision/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify(requestData)
    })
    .then(response => {
        console.log('Response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data);
        if (data.status === 'success') {
            // Hide modal before reload
            const modalInstance = bootstrap.Modal.getInstance(decisionModal);
            modalInstance.hide();
            
            // Show success message
            alert('Decision submitted successfully!');
            
            // Reload page
            window.location.reload();
        } else {
            throw new Error(data.message || 'An error occurred');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
        this.disabled = false;
        this.innerHTML = 'Submit Decision';
    });
});

    // Add color classes to status badges
    document.querySelectorAll('.status-badge').forEach(badge => {
        const status = badge.textContent.trim().toLowerCase();
        const className = `status-${status.replace(/\s+/g, '-')}`;
        badge.classList.add(className);
    });

    // Initialize all tables with their specific configurations
    const tableConfigs = {
        submissionsNeedingReview: {
            order: [[1, 'desc']]
        },
        forwardedReviews: {
            dom: 'Bfrtip',
            buttons: ['copy', 'excel', 'csv'],
            order: [[1, 'desc']]
        },
        pendingIRBDecisions: {
            order: [[1, 'desc']]
        },
        departmentSubmissions: {
            order: [[1, 'desc']]
        },
        aahrppSubmissions: {
            order: [[1, 'desc']]
        },
        pendingReviews: {
            dom: 'Bfrtip',
            buttons: ['copy', 'excel', 'csv'],
            order: [[3, 'asc']]
        },
        completedReviews: {
            dom: 'Bfrtip',
            buttons: ['copy', 'excel', 'csv'],
            order: [[3, 'desc']]
        }
    };

    // Initialize all tables with their specific configurations
    Object.keys(tableConfigs).forEach(tableId => {
        const table = $(`#${tableId}Table`);
        if (table.length) {
            table.DataTable({
                processing: true,
                serverSide: false,
                pageLength: 10,
                ...tableConfigs[tableId]
            });
        }
    });
});
</script>
{% endblock %}

# Contents from: .\templates\review\dashboard\quality_dashboard.html
{# review/templates/review/dashboard/quality_dashboard.html #}
{% extends 'base.html' %}
{% load static %}

{% block extra_css %}
<style>
    .metric-card {
        background: white;
        border-radius: 8px;
        padding: 2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        height: 100%;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c5282;
        margin: 1rem 0;
    }
    .metric-label {
        color: #4a5568;
        font-size: 1rem;
        margin-bottom: 1rem;
    }
    .metric-definition {
        color: #718096;
        font-size: 0.875rem;
        margin-top: 1rem;
    }
    .chart-container {
        background: white;
        border-radius: 8px;
        padding: 2rem;
        margin-bottom: 2rem;
        height: 600px;
    }
    .chart-container.large {
        height: 700px;
    }
    .dashboard-section {
        margin-bottom: 3rem;
    }
    .section-header {
        margin-bottom: 2rem;
    }
</style>
{% endblock %}

{% block content %}
<div class="container-fluid py-5">
    <div class="row mb-5 section-header">
        <div class="col">
            <h2 class="mb-2">Quality Dashboard</h2>
            <p class="text-muted">Real-time metrics and analytics</p>
        </div>
    </div>

    <!-- Top Metrics -->
    <div class="row dashboard-section">
        <div class="col-md-3">
            <div class="metric-card">
                <div class="metric-label">Total Submissions</div>
                <div class="metric-value" id="totalSubmissions">-</div>
                <div class="metric-definition">Total number of research submissions excluding drafts</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="metric-card">
                <div class="metric-label">Active Reviewers</div>
                <div class="metric-value" id="activeReviewers">-</div>
                <div class="metric-definition">Number of reviewers with pending review assignments</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="metric-card">
                <div class="metric-label">Avg Review Time (days)</div>
                <div class="metric-value" id="avgReviewTime">-</div>
                <div class="metric-definition">Average time from review request to completion</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="metric-card">
                <div class="metric-label">Pending Reviews</div>
                <div class="metric-value" id="pendingReviews">-</div>
                <div class="metric-definition">Number of reviews currently awaiting completion</div>
            </div>
        </div>
    </div>

    <!-- Committee Review Times -->
    <div class="row dashboard-section">
        <div class="col-md-6">
            <div class="chart-container">
                <h5 class="mb-4">IRB Response Time Distribution</h5>
                <div id="irbTimeChart" style="width: 100%; height: 100%;"></div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="chart-container">
                <h5 class="mb-4">RC Response Time Distribution</h5>
                <div id="rcTimeChart" style="width: 100%; height: 100%;"></div>
            </div>
        </div>
    </div>

    <!-- Trends and Status -->
    <div class="row dashboard-section">
        <div class="col-md-8">
            <div class="chart-container large">
                <h5 class="mb-4">Monthly Submission Trends</h5>
                <div id="monthlyChart" style="width: 100%; height: 100%;"></div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="chart-container large">
                <h5 class="mb-4">Status Distribution</h5>
                <div id="statusChart" style="width: 100%; height: 100%;"></div>
            </div>
        </div>
    </div>

    <!-- Role and Institution Distribution -->
    <div class="row dashboard-section">
        <div class="col-md-6">
            <div class="chart-container">
                <h5 class="mb-4">PI Role Distribution</h5>
                <div id="roleChart" style="width: 100%; height: 100%;"></div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="chart-container">
                <h5 class="mb-4">Institution Distribution</h5>
                <div id="institutionChart" style="width: 100%; height: 100%;"></div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block page_specific_js %}
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const charts = {};
    
    function initializeChart(elementId) {
        const chart = echarts.init(document.getElementById(elementId));
        charts[elementId] = chart;
        return chart;
    }

    function updateDashboard() {
        fetch('/review/api/dashboard-data/')
            .then(response => response.json())
            .then(data => {
                // Update metrics
                document.getElementById('totalSubmissions').textContent = data.totalSubmissions || 0;
                document.getElementById('activeReviewers').textContent = data.activeReviewers || 0;
                document.getElementById('avgReviewTime').textContent = 
                    (data.avgReviewTime ? `${data.avgReviewTime.toFixed(1)}` : '-');
                document.getElementById('pendingReviews').textContent = data.pendingReviews || 0;

                // Monthly Submissions Chart
                const monthlyChart = initializeChart('monthlyChart');
                monthlyChart.setOption({
                    tooltip: { trigger: 'axis' },
                    xAxis: {
                        type: 'category',
                        data: data.submissionTrends.map(item => item.month)
                    },
                    yAxis: { type: 'value' },
                    series: [{
                        data: data.submissionTrends.map(item => item.count),
                        type: 'line',
                        smooth: true,
                        name: 'Submissions',
                        areaStyle: {}
                    }]
                });

                // Status Distribution Chart
                const statusChart = initializeChart('statusChart');
                statusChart.setOption({
                    tooltip: {
                        trigger: 'item',
                        formatter: '{a} <br/>{b}: {c} ({d}%)'
                    },
                    legend: {
                        orient: 'vertical',
                        left: 'left',
                        type: 'scroll'
                    },
                    series: [{
                        name: 'Status Distribution',
                        type: 'pie',
                        radius: '70%',
                        data: data.statusDistribution,
                        emphasis: {
                            itemStyle: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }]
                });

                // Role Distribution Chart
                const roleChart = initializeChart('roleChart');
                roleChart.setOption({
                    tooltip: {
                        trigger: 'item',
                        formatter: '{a} <br/>{b}: {c} ({d}%)'
                    },
                    legend: {
                        orient: 'vertical',
                        left: 'left',
                        type: 'scroll'
                    },
                    series: [{
                        name: 'Role Distribution',
                        type: 'pie',
                        radius: '70%',
                        data: data.roleDistribution,
                        emphasis: {
                            itemStyle: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }]
                });

                // Institution Distribution Chart
                const institutionChart = initializeChart('institutionChart');
                institutionChart.setOption({
                    tooltip: {
                        trigger: 'item',
                        formatter: '{a} <br/>{b}: {c} ({d}%)'
                    },
                    legend: {
                        orient: 'vertical',
                        left: 'left',
                        type: 'scroll'
                    },
                    series: [{
                        name: 'Institution Distribution',
                        type: 'pie',
                        radius: '70%',
                        data: data.institutions,
                        emphasis: {
                            itemStyle: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }]
                });

                // Review Time Distribution Charts
                ['irb', 'rc'].forEach(committee => {
                    const chart = initializeChart(`${committee}TimeChart`);
                    const timeData = data[`${committee}TimeDistribution`];
                    const avgTime = data[`${committee}AvgTime`];
                    
                    chart.setOption({
                        title: {
                            text: `Average: ${avgTime.toFixed(1)} days`,
                            left: 'center',
                            top: 0
                        },
                        tooltip: {
                            trigger: 'axis',
                            formatter: '{b} days: {c} reviews'
                        },
                        xAxis: {
                            type: 'category',
                            name: 'Days',
                            data: timeData.map(item => item.days)
                        },
                        yAxis: {
                            type: 'value',
                            name: 'Number of Reviews'
                        },
                        series: [{
                            data: timeData.map(item => item.count),
                            type: 'bar',
                            name: 'Reviews',
                            itemStyle: {
                                color: committee === 'irb' ? '#0088FE' : '#00C49F'
                            }
                        }]
                    });
                });
            })
            .catch(error => console.error('Error updating dashboard:', error));
    }

    // Handle window resize
    window.addEventListener('resize', function() {
        Object.values(charts).forEach(chart => chart.resize());
    });

    // Initial update
    updateDashboard();

    // Update every 5 minutes
    setInterval(updateDashboard, 300000);
});
</script>
{% endblock %}

# Contents from: .\templates\review\decline_review.html
{% extends 'users/base.html' %}
{% load crispy_forms_tags %}

{% block title %}Decline Review Request{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-8 offset-md-2">
            <div class="card">
                <div class="card-header bg-danger text-white">
                    <h2 class="mb-0">Decline Review Request</h2>
                </div>
                <div class="card-body">
                    <!-- Review Details -->
                    <div class="alert alert-info">
                        <h5>Review Details</h5>
                        <p><strong>Submission:</strong> {{ review_request.submission.title }}</p>
                        <p><strong>Requested By:</strong> {{ review_request.requested_by.userprofile.full_name }}</p>
                        <p><strong>Deadline:</strong> {{ review_request.deadline|date:"F d, Y" }}</p>
                        {% if review_request.message %}
                        <p><strong>Original Request Message:</strong></p>
                        <div class="border-left pl-3">{{ review_request.message|linebreaks }}</div>
                        {% endif %}
                    </div>

                    <form method="post" novalidate>
                        {% csrf_token %}
                        
                        <!-- Reason -->
                        <div class="mb-3">
                            <label for="reason" class="form-label required">Reason for Declining</label>
                            <textarea class="form-control" 
                                      id="reason" 
                                      name="reason" 
                                      rows="4"
                                      required
                                      placeholder="Please provide a detailed reason for declining this review request..."></textarea>
                            <div class="form-text">This message will be sent to the requester and the primary investigator.</div>
                        </div>

                        <!-- Confirmation Checkbox -->
                        <div class="mb-3">
                            <div class="form-check">
                                <input class="form-check-input" 
                                       type="checkbox" 
                                       id="confirm" 
                                       required>
                                <label class="form-check-label" for="confirm">
                                    I confirm that I want to decline this review request
                                </label>
                            </div>
                        </div>

                        <!-- Submit Buttons -->
                        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                            <a href="{% url 'review:review_dashboard' %}" 
                               class="btn btn-secondary me-md-2">
                                <i class="fas fa-arrow-left"></i> Cancel
                            </a>
                            <button type="submit" 
                                    class="btn btn-danger" 
                                    id="submitBtn" 
                                    disabled>
                                <i class="fas fa-times"></i> Decline Review
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block page_specific_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const form = document.querySelector('form');
        const reasonInput = document.getElementById('reason');
        const confirmCheckbox = document.getElementById('confirm');
        const submitBtn = document.getElementById('submitBtn');

        // Enable/disable submit button based on form state
        function updateSubmitButton() {
            submitBtn.disabled = !(
                reasonInput.value.trim().length >= 10 && 
                confirmCheckbox.checked
            );
        }

        reasonInput.addEventListener('input', updateSubmitButton);
        confirmCheckbox.addEventListener('change', updateSubmitButton);

        // Form validation
        form.addEventListener('submit', function(e) {
            if (!reasonInput.value.trim()) {
                e.preventDefault();
                alert('Please provide a reason for declining.');
                reasonInput.focus();
                return false;
            }

            if (!confirmCheckbox.checked) {
                e.preventDefault();
                alert('Please confirm that you want to decline this review.');
                return false;
            }

            if (reasonInput.value.trim().length < 10) {
                e.preventDefault();
                alert('Please provide a more detailed reason (at least 10 characters).');
                reasonInput.focus();
                return false;
            }
        });
    });
</script>
{% endblock %}

# Contents from: .\templates\review\forward_review.html
{# review/templates/review/forward_review.html #}
{% extends 'users/base.html' %}
{% load static %}

{% block title %}Forward Review Request{% endblock %}

{% block page_specific_css %}
<style>
    .review-chain {
        position: relative;
        margin-bottom: 2rem;
    }
    .chain-item {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    .chain-connector {
        position: absolute;
        left: 15px;
        top: 30px;
        bottom: 0;
        width: 2px;
        background-color: #dee2e6;
    }
    .chain-node {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background-color: #007bff;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 1rem;
        position: relative;
        z-index: 1;
    }
    .chain-content {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        flex-grow: 1;
    }
    .reviewer-select {
        min-height: 200px;
    }
    .selected-reviewers {
        margin-top: 1rem;
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 0.5rem;
    }
    .selected-reviewer {
        display: inline-block;
        background-color: #e9ecef;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        margin: 0.25rem;
    }
</style>
{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-8">
            <!-- Main Forwarding Form -->
            <div class="card">
                <div class="card-header">
                    <h2>Forward Review Request</h2>
                </div>
                <div class="card-body">
                    <!-- Submission Info -->
                    <div class="alert alert-info">
                        <h5>Submission Details</h5>
                        <p><strong>Title:</strong> {{ review_request.submission.title }}</p>
                        <p><strong>Primary Investigator:</strong> 
                           {{ review_request.submission.primary_investigator.userprofile.full_name }}</p>
                        <p><strong>Study Type:</strong> 
                           {{ review_request.submission.study_type.name }}</p>
                        <p><strong>Current Status:</strong> 
                           <span class="badge bg-{{ review_request.submission.status|lower }}">
                               {{ review_request.submission.get_status_display }}
                           </span>
                        </p>
                    </div>

                    <form method="post" class="needs-validation" novalidate>
                        {% csrf_token %}
                        
                        <!-- Reviewer Selection -->
                        <div class="mb-3">
                            <label class="form-label required">Select Reviewers</label>
                            <select name="reviewers" multiple class="form-select reviewer-select" required>
                                {% for reviewer in available_reviewers %}
                                <option value="{{ reviewer.id }}">
                                    {{ reviewer.userprofile.full_name }} 
                                    ({{ reviewer.groups.first.name }})
                                </option>
                                {% endfor %}
                            </select>
                            <div class="form-text">
                                Hold Ctrl/Cmd to select multiple reviewers
                            </div>
                        </div>

                        <!-- Selected Reviewers Preview -->
                        <div class="selected-reviewers d-none">
                            <h6>Selected Reviewers:</h6>
                            <div id="selectedReviewersList"></div>
                        </div>

                        <!-- Deadline -->
                        <div class="mb-3">
                            <label for="deadline" class="form-label required">Review Deadline</label>
                            <input type="date" 
                                   class="form-control" 
                                   id="deadline" 
                                   name="deadline"
                                   min="{{ min_date }}"
                                   value="{{ suggested_date }}"
                                   required>
                        </div>

                        <!-- Message -->
                        <div class="mb-3">
                            <label for="message" class="form-label required">Message to Reviewers</label>
                            <textarea class="form-control" 
                                      id="message" 
                                      name="message" 
                                      rows="4"
                                      required></textarea>
                        </div>

                        <!-- Forward Permission -->
                        <div class="mb-3">
                            <div class="form-check">
                                <input class="form-check-input" 
                                       type="checkbox" 
                                       id="allow_forwarding" 
                                       name="allow_forwarding" 
                                       value="true">
                                <label class="form-check-label" for="allow_forwarding">
                                    Allow these reviewers to forward to others
                                </label>
                            </div>
                        </div>

                        <!-- Submit Buttons -->
                        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                            <button type="button" 
                                    class="btn btn-secondary me-md-2" 
                                    onclick="history.back()">
                                Cancel
                            </button>
                            <button type="submit" class="btn btn-primary">
                                Forward Review Request
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <div class="col-md-4">
            <!-- Review Chain Visualization -->
            <div class="card">
                <div class="card-header">
                    <h5 class="card-t

# Contents from: .\templates\review\irb_dashboard.html
{% extends 'base.html' %}
{% load static %}
{% load review_tags %}

{% block extra_css %}
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.24/css/dataTables.bootstrap4.min.css">
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/buttons/2.2.3/css/buttons.bootstrap4.min.css">
<style>
    .btn-green {
        background-color: #28a745;
        border-color: #28a745;
        color: #fff;
    }
    .btn-green:hover {
        background-color: #218838;
        border-color: #1e7e34;
        color: #fff;
    }
</style>
{% endblock %}

{% block content %}
<div class="container">
    <h2 class="mb-4">IRB Dashboard</h2>
    
    <!-- Submissions Needing Review -->
    <div class="card mb-4">
        <div class="card-header">
            <h3 class="card-title mb-0">Submissions Needing Review</h3>
        </div>
        <div class="card-body">
            {% if irb_submissions %}
                <div class="table-responsive">
                    <table id="irbSubmissionsTable" class="table table-hover">
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>Submission Date</th>
                                <th>Days Since Submission</th>
                                <th>Primary Investigator</th>
                                <th>Study Type</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for submission in irb_submissions %}
                            <tr>
                                <td>{{ submission.title }}</td>
                                <td>{{ submission.date_submitted|date:"Y-m-d" }}</td>
                                <td>{{ submission.date_submitted|timesince_in_days }}</td>
                                <td>{{ submission.primary_investigator.userprofile.full_name }}</td>
                                <td>{{ submission.study_type }}</td>
                                <td>{{ submission.get_status_display }}</td>
                                <td>
                                    <a href="{% url 'review:create_review_request' submission.pk %}" class="btn btn-primary btn-sm">Create Review Request</a>
                                    <a href="{% url 'review:review_summary' submission.pk %}" class="btn btn-success btn-sm">Details</a>
                                    <a href="{% url 'review:view_notepad' submission.pk 'IRB' %}" class="btn btn-info btn-sm">
                                        <i class="fas fa-sticky-note"></i> Notepad
                                    </a>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <p class="mb-0">No submissions currently need review.</p>
            {% endif %}
        </div>
    </div>

    <!-- Pending IRB Decisions -->
    <div class="card mb-4">
        <div class="card-header">
            <h3 class="card-title mb-0">Pending IRB Decisions</h3>
        </div>
        <div class="card-body">
            {% if pending_irb_decisions %}
                <div class="table-responsive">
                    <table id="pendingIRBDecisionsTable" class="table table-hover">
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>Submission Date</th>
                                <th>Primary Investigator</th>
                                <th>Study Type</th>
                                <th>Requests</th>
                                <th>Days</th>
                                <th>✅</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for submission in pending_irb_decisions %}
                            <tr>
                                <td>{{ submission.title }}</td>
                                <td>{{ submission.date_submitted|date:"Y-m-d" }}</td>
                                <td>{{ submission.primary_investigator.userprofile.full_name }}</td>
                                <td>{{ submission.study_type }}</td>
                                <td>
                                    {% if submission.review_requests.exists %}
                                        <ul class="list-unstyled mb-0">
                                        {% for request in submission.review_requests.all %}
                                            <li>
                                                <strong>
                                                    <a href="{% url 'messaging:compose' %}?recipient={{ request.requested_to.id }}&submission={{ submission.id }}" 
                                                       class="text-primary text-decoration-none">
                                                        {{ request.requested_to.get_full_name }}
                                                    </a>
                                                </strong>
                                            </li>
                                        {% endfor %}
                                        </ul>
                                    {% else %}
                                        No requests yet
                                    {% endif %}
                                </td>
                                <td>
                                    {% if submission.review_requests.exists %}
                                        <ul class="list-unstyled mb-0">
                                        {% for request in submission.review_requests.all %}
                                            <li>
                                                {% with days=request.created_at|timesince_in_days %}
                                                    {{ days }}
                                                {% endwith %}
                                            </li>
                                        {% endfor %}
                                        </ul>
                                    {% else %}
                                        -
                                    {% endif %}
                                </td>
                                <td>
                                    {% if submission.review_requests.exists %}
                                        <ul class="list-unstyled mb-0">
                                        {% for request in submission.review_requests.all %}
                                            <li>
                                                {% if request.status == 'completed' %}
                                                    <span class="text-success">✅</span>
                                                {% elif request.status == 'declined' %}
                                                    <span class="text-danger">❌</span>
                                                {% elif request.status == 'pending' %}
                                                    <span class="text-warning">⏳</span>
                                                {% else %}
                                                    <span class="text-secondary">-</span>
                                                {% endif %}
                                            </li>
                                        {% endfor %}
                                        </ul>
                                    {% else %}
                                        -
                                    {% endif %}
                                </td>
                                <td>
                                    <a href="{% url 'review:review_summary' submission.pk %}" class="btn btn-success btn-sm">Details</a>
                                    <a href="{% url 'review:process_decision' submission.pk %}" class="btn btn-primary btn-sm">Make Decision</a>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <p class="mb-0">No submissions pending IRB decision.</p>
            {% endif %}
        </div>
    </div>

    <!-- My IRB Reviews -->
    <div class="card mb-4">
        <div class="card-header">
            <h3 class="card-title mb-0">My IRB Reviews</h3>
        </div>
        <div class="card-body">
            {% if irb_reviews %}
                <div class="table-responsive">
                    <table id="irbReviewsTable" class="table table-hover">
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>Primary Investigator</th>
                                <th>Requested By</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for review in irb_reviews %}
                            <tr>
                                <td>{{ review.submission.title }}</td>
                                <td>{{ review.submission.primary_investigator.userprofile.full_name }}</td>
                                <td>{{ review.requested_by.userprofile.full_name }}</td>
                                <td>{{ review.get_status_display }}</td>
                                <td>
                                    {% if review.requested_to == user or review.requested_by == user %}
                                        <a href="{% url 'review:view_review' review.id %}" 
                                           class="btn btn-info btn-sm">View Review</a>
                                    {% endif %}
                                    {% if review.requested_to == user and review.status == 'pending' %}
                                        <a href="{% url 'review:submit_review' review.id %}" 
                                           class="btn btn-primary btn-sm">Submit Review</a>
                                    {% endif %}
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <p class="mb-0">No IRB reviews assigned.</p>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}

{% block page_specific_js %}
<script src="https://cdn.datatables.net/1.10.24/js/jquery.dataTables.min.js"></script>
<script src="https://cdn.datatables.net/1.10.24/js/dataTables.bootstrap4.min.js"></script>
<script src="https://cdn.datatables.net/buttons/2.2.3/js/dataTables.buttons.min.js"></script>
<script src="https://cdn.datatables.net/buttons/2.2.3/js/buttons.bootstrap4.min.js"></script>
<script>
$(document).ready(function() {
    // Initialize DataTables for all tables
    const tableConfigs = {
        irbSubmissionsTable: {
            order: [[1, 'desc']]
        },
        irbReviewsTable: {
            dom: 'Bfrtip',
            buttons: ['copy', 'excel', 'csv'],
            order: [[1, 'desc']]
        },
        pendingIRBDecisionsTable: {
            order: [[1, 'desc']]
        }
    };

    // Initialize all tables with their specific configurations
    Object.keys(tableConfigs).forEach(tableId => {
        const table = $(`#${tableId}`);
        if (table.length) {
            table.DataTable({
                processing: true,
                serverSide: false,
                pageLength: 10,
                ...tableConfigs[tableId]
            });
        }
    });

    // Handle toggle visibility buttons
    $('.toggle-visibility-btn').on('click', function(e) {
        e.preventDefault();
        
        const btn = $(this);
        const submissionId = btn.data('submission-id');
        const toggleType = btn.data('toggle-type');
        
        $.ajax({
            url: `/review/submission/${submissionId}/toggle-visibility/`,
            method: 'POST',
            data: {
                toggle_type: toggleType,
                csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response.visible) {
                    btn.removeClass('btn-secondary').addClass('btn-success');
                } else {
                    btn.removeClass('btn-success').addClass('btn-secondary');
                }
            },
            error: function(xhr) {
                alert('Error toggling visibility');
            }
        });
    });
});
</script>
{% endblock %}

# Contents from: .\templates\review\my_reviews.html
# templates/reviews/my_reviews.html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h2>My Assigned Reviews</h2>
    {% if reviews %}
        <div class="list-group">
        {% for review in reviews %}
            <a href="{% url 'review_detail' review.review_id %}" class="list-group-item list-group-item-action">
                <div class="d-flex w-100 justify-content-between">
                    <h5 class="mb-1">{{ review.title }}</h5>
                    <small>Status: {{ review.status }}</small>
                </div>
                <small>Assigned: {{ review.created_at|date }}</small>
            </a>
        {% endfor %}
        </div>
    {% else %}
        <p>No reviews assigned yet.</p>
    {% endif %}
</div>
{% endblock %}

# Contents from: .\templates\review\osar_dashboard.html
{% extends 'base.html' %}
{% load static %}
{% load review_tags %}

{% block extra_css %}
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.24/css/dataTables.bootstrap4.min.css">
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/buttons/2.2.3/css/buttons.bootstrap4.min.css">
<style>
    .btn-green {
        background-color: #28a745;
        border-color: #28a745;
        color: #fff;
    }
    .btn-green:hover {
        background-color: #218838;
        border-color: #1e7e34;
        color: #fff;
    }
    
    .form-switch {
        padding-left: 2.5em;
    }
    
    .form-check-input {
        cursor: pointer;
    }
    
    .visibility-toggles {
        padding: 0.5rem;
    }

    .filter-section {
        background-color: #f8f9fa;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 0.25rem;
    }
    
    .filter-section select {
        min-width: 200px;
    }

    .action-buttons .btn {
        margin-right: 0.25rem;
        margin-bottom: 0.25rem;
    }

    .status-badge {
        display: inline-block;
        padding: 0.375rem 0.75rem;
        font-size: 0.875rem;
        font-weight: 500;
        line-height: 1.5;
        text-align: center;
        white-space: nowrap;
        vertical-align: middle;
        border-radius: 0.25rem;
        transition: all 0.15s ease-in-out;
        min-width: 100px;
    }

    .status-badge.draft { 
        background-color: #6c757d;
        color: white;
        border: 1px solid #5a6268;
    }
    .status-badge.submitted { 
        background-color: #007bff;
        color: white;
        border: 1px solid #0056b3;
    }
    .status-badge.under-review { 
        background-color: #17a2b8;
        color: white;
        border: 1px solid #138496;
    }
    .status-badge.revision-requested { 
        background-color: #ffc107;
        color: #000;
        border: 1px solid #d39e00;
    }
    .status-badge.rejected { 
        background-color: #dc3545;
        color: white;
        border: 1px solid #bd2130;
    }
    .status-badge.accepted { 
        background-color: #28a745;
        color: white;
        border: 1px solid #1e7e34;
    }

    /* Filter section styling */
    .card-title {
        font-size: 1.5rem;
        font-weight: 500;
        margin-bottom: 0;
    }

    .form-label {
        font-weight: 500;
        margin-bottom: 0.5rem;
    }

    .form-select, .form-control {
        height: calc(1.5em + 0.75rem + 2px);
        padding: 0.375rem 0.75rem;
        font-size: 1rem;
        line-height: 1.5;
        border: 1px solid #ced4da;
        border-radius: 0.25rem;
        transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    }

    .form-select:focus, .form-control:focus {
        border-color: #80bdff;
        outline: 0;
        box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
    }
</style>
{% endblock %}

{% block content %}
<script type="text/babel">
// Define the ToggleSwitch component
const ToggleSwitch = ({ submissionId, initialState = false, label = '', type = '' }) => {
    const [isEnabled, setIsEnabled] = React.useState(initialState === 'true');
    const [isLoading, setIsLoading] = React.useState(false);

    const handleToggle = async () => {
        setIsLoading(true);
        try {
            const response = await fetch(`/review/submission/${submissionId}/toggle-visibility/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `toggle_type=${type}&csrfmiddlewaretoken=${document.querySelector('[name=csrfmiddlewaretoken]').value}`
            });

            if (response.ok) {
                const data = await response.json();
                setIsEnabled(data.visible);
            }
        } catch (error) {
            console.error('Error toggling visibility:', error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="form-check form-switch mb-2">
            <input
                className="form-check-input"
                type="checkbox"
                checked={isEnabled}
                onChange={handleToggle}
                disabled={isLoading}
                id={`switch-${type}-${submissionId}`}
            />
            <label className="form-check-label ms-2" htmlFor={`switch-${type}-${submissionId}`}>
                {label}
            </label>
        </div>
    );
};

// Define the VisibilityToggles component
const VisibilityToggles = ({ submissionId, initialIrbState, initialRcState }) => {
    return (
        <div className="d-flex flex-column">
            <ToggleSwitch 
                submissionId={submissionId} 
                initialState={initialIrbState} 
                label="IRB" 
                type="irb" 
            />
            <ToggleSwitch 
                submissionId={submissionId} 
                initialState={initialRcState} 
                label="RC" 
                type="rc" 
            />
        </div>
    );
};
</script>

<div class="container">
    <h2 class="mb-4">OSAR Dashboard</h2>
    
    <!-- Submissions Section -->
    <div class="card mb-4">
        <div class="card-header">
            <h2 class="card-title">Submissions</h2>
        </div>

        <div class="card-body">
            <!-- Filter Controls -->
            <div class="row g-3 mb-4">
                <div class="col-md-4">
                    <label for="statusFilter" class="form-label">Filter by Status:</label>
                    <select id="statusFilter" class="form-select">
                        <option value="">All Statuses</option>
                        {% for status, label in submission_status_choices %}
                            <option value="{{ status }}">{{ label }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-2">
                    <label for="entriesFilter" class="form-label">Show entries:</label>
                    <select id="entriesFilter" class="form-select">
                        <option value="10">10</option>
                        <option value="25">25</option>
                        <option value="50">50</option>
                        <option value="-1">All</option>
                    </select>
                </div>
                <div class="col-md-6">
                    <label for="searchFilter" class="form-label">Search:</label>
                    <input type="search" id="searchFilter" class="form-control" placeholder="Type to search...">
                </div>
            </div>

        <div class="card-body">
            {% if osar_submissions %}
                <div class="table-responsive">
                    <table id="osarSubmissionsTable" class="table table-hover">
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>Submission Date</th>
                                <th>Primary Investigator</th>
                                <th>Study Type</th>
                                <th>Requests</th>
                                <th>Days</th>
                                <th>✅</th>
                                <th>Status</th>
                                <th>KHCC #</th>
                                <th>Visibility</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for submission in osar_submissions %}
                            <tr>
                                <td>{{ submission.title }}</td>
                                <td>{{ submission.date_submitted|date:"Y-m-d" }}</td>
                                <td>{{ submission.primary_investigator.userprofile.full_name }}</td>
                                <td>{{ submission.study_type }}</td>
                                <td>
                                    {% if submission.review_requests.exists %}
                                        <ul class="list-unstyled mb-0">
                                        {% for request in submission.review_requests.all %}
                                            <li>
                                                <strong>
                                                    <a href="{% url 'messaging:compose_message' %}?recipient={{ request.requested_to.id }}&submission={{ submission.id }}" 
                                                       class="text-primary text-decoration-none">
                                                        {{ request.requested_to.userprofile.user}}
                                                    </a>
                                                </strong>
                                            </li>
                                        {% endfor %}
                                        </ul>
                                    {% else %}
                                        No requests yet
                                    {% endif %}
                                </td>
                                <td>
                                    {% if submission.review_requests.exists %}
                                        <ul class="list-unstyled mb-0">
                                        {% for request in submission.review_requests.all %}
                                            <li>
                                                {% with days=request.created_at|timesince_in_days %}
                                                    {{ days }}
                                                {% endwith %}
                                            </li>
                                        {% endfor %}
                                        </ul>
                                    {% else %}
                                        -
                                    {% endif %}
                                </td>
                                <td>
                                    {% if submission.review_requests.exists %}
                                        <ul class="list-unstyled mb-0">
                                        {% for request in submission.review_requests.all %}
                                            <li>
                                                {% if request.status == 'completed' %}
                                                    <span class="text-success">✅</span>
                                                {% elif request.status == 'declined' %}
                                                    <span class="text-danger">❌</span>
                                                {% elif request.status == 'pending' %}
                                                    <span class="text-warning">⏳</span>
                                                {% else %}
                                                    <span class="text-secondary">-</span>
                                                {% endif %}
                                            </li>
                                        {% endfor %}
                                        </ul>
                                    {% else %}
                                        -
                                    {% endif %}
                                </td>
                                <td>
                                    <span class="status-badge {{ submission.status|slugify }}">
                                        {{ submission.get_status_display }}
                                    </span>
                                </td>
                                <td>{{ submission.khcc_number|default:"-" }}</td>
                                <td>
                                    <div id="toggle-container-{{ submission.temporary_id }}" class="visibility-toggles"></div>
                                    <script type="text/babel">
                                        {
                                            const container = document.getElementById('toggle-container-{{ submission.temporary_id }}');
                                            const root = ReactDOM.createRoot(container);
                                            root.render(
                                                <VisibilityToggles 
                                                    submissionId="{{ submission.temporary_id }}"
                                                    initialIrbState="{{ submission.show_in_irb|yesno:'true,false' }}"
                                                    initialRcState="{{ submission.show_in_rc|yesno:'true,false' }}"
                                                />
                                            );
                                        }
                                    </script>
                                </td>
                                <td>
                                    <div class="action-buttons">
                                        <a href="{% url 'review:create_review_request' submission.pk%}" 
                                           class="btn btn-primary btn-sm" style="width: 100px;">
                                            <i class="fas fa-plus"></i> Request
                                        </a>
                                        <a href="{% url 'review:review_summary' submission.pk %}" 
                                           class="btn btn-success btn-sm" style="width: 100px;">
                                            <i class="fas fa-info-circle"></i> Details
                                        </a>
                                        {% if not submission.khcc_number %}
                                            <a href="{% url 'review:assign_irb' submission.pk %}" 
                                               class="btn btn-info btn-sm" style="width: 100px;">
                                                <i class="fas fa-hashtag"></i> KHCC #
                                            </a>
                                        {% endif %}
                                        <a href="{% url 'review:view_notepad' submission.pk 'OSAR' %}" 
                                           class="btn btn-info btn-sm" style="width: 100px;">
                                            <i class="fas fa-sticky-note"></i> Notes
                                        </a>

                                        {% if submission.status == 'under_review' %}
                                            <button type="button" 
                                                    class="btn btn-warning btn-sm decision-btn" 
                                                    style="width: 100px;"
                                                    data-bs-toggle="modal" 
                                                    data-bs-target="#decisionModal"
                                                    data-submission-id="{{ submission.pk }}"
                                                    data-action="revision_requested">
                                                <i class="fas fa-undo"></i> Revision
                                            </button>
                                            <button type="button" 
                                                    class="btn btn-danger btn-sm decision-btn" 
                                                    style="width: 100px;"
                                                    data-bs-toggle="modal" 
                                                    data-bs-target="#decisionModal"
                                                    data-submission-id="{{ submission.pk }}"
                                                    data-action="rejected">
                                                <i class="fas fa-times"></i> Reject
                                            </button>
                                            <button type="button" 
                                                    class="btn btn-success btn-sm decision-btn" 
                                                    data-bs-toggle="modal" 
                                                    style="width: 100px;"
                                                    data-bs-target="#decisionModal"
                                                    data-submission-id="{{ submission.pk }}"
                                                    data-action="accepted">
                                                <i class="fas fa-check"></i> Accept
                                            </button>
                                        {% endif %}
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <p class="mb-0">No submissions found.</p>
            {% endif %}
        </div>
    </div>

    <!-- Decision Modal -->
    <div class="modal fade" id="decisionModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Make Decision</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="decisionForm" method="post">
                        {% csrf_token %}
                        <input type="hidden" name="action" id="decisionAction">
                        <div class="mb-3">
                            <label for="comments" class="form-label">Comments</label>
                            <textarea class="form-control" id="comments" name="comments" rows="4" required></textarea>
                            <div class="form-text">
                                Please provide detailed comments explaining your decision.
                            </div>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" id="submitDecision">Submit Decision</button>
                </div>
            </div>
        </div>
    </div>

    <!-- OSAR Reviews -->
    <div class="card mb-4">
        <div class="card-header">
            <h3 class="card-title mb-0">My OSAR Reviews</h3>
        </div>
        <div class="card-body">
            {% if osar_reviews %}
                <div class="table-responsive">
                    <table id="osarReviewsTable" class="table table-hover">
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>Primary Investigator</th>
                                <th>Requested By</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for review in osar_reviews %}
                            <tr>
                                <td>{{ review.submission.title }}</td>
                                <td>{{ review.submission.primary_investigator.userprofile.full_name }}</td>
                                <td>{{ review.requested_by.userprofile.full_name }}</td>
                                <td>{{ review.get_status_display }}</td>
                                <td>
                                    <div class="action-buttons">
                                        {% if review.requested_to == user or review.requested_by == user %}
                                            <a href="{% url 'review:view_review' review.id %}" 
                                               class="btn btn-info btn-sm">
                                                <i class="fas fa-eye"></i> View Review
                                            </a>
                                        {% endif %}
                                        {% if review.requested_to == user and review.status == 'pending' %}
                                            <a href="{% url 'review:submit_review' review.id %}" 
                                               class="btn btn-primary btn-sm">
                                                <i class="fas fa-paper-plane"></i> Submit Review
                                            </a>
                                        {% endif %}
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <p class="mb-0">No OSAR reviews assigned.</p>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}

{% block page_specific_js %}
<script src="https://cdn.datatables.net/1.10.24/js/jquery.dataTables.min.js"></script>
<script src="https://cdn.datatables.net/1.10.24/js/dataTables.bootstrap4.min.js"></script>
<script src="https://cdn.datatables.net/buttons/2.2.3/js/dataTables.buttons.min.js"></script>
<script src="https://cdn.datatables.net/buttons/2.2.3/js/buttons.bootstrap4.min.js"></script>
<script>
$(document).ready(function() {
    // Initialize DataTables with custom controls
    var submissionsTable = $('#osarSubmissionsTable').DataTable({
        order: [[1, 'desc']],
        pageLength: 10,
        lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
        dom: 'Brt<"bottom"ip>',
        buttons: ['copy', 'excel', 'pdf']
    });

    // Connect custom filter controls
    $('#entriesFilter').on('change', function() {
        submissionsTable.page.len($(this).val()).draw();
    });

    $('#searchFilter').on('keyup', function() {
        submissionsTable.search(this.value).draw();
    });

    // Status Filter
    $('#statusFilter').on('change', function() {
        var selectedStatus = $(this).val();
        
        // Clear existing filter
        submissionsTable.column(4).search('').draw();
        
        // Apply new filter if a status is selected
        if (selectedStatus) {
            // Create a regex that matches the status text case-insensitively
            var searchRegex = selectedStatus.replace(/_/g, ' ');
            submissionsTable.column(4).search(searchRegex, true, false).draw();
        }
    });

    // Initialize OSAR reviews table
    $('#osarReviewsTable').DataTable({
        order: [[1, 'desc']],
        pageLength: 10,
        lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
        dom: 'Blfrtip',
        buttons: ['copy', 'excel', 'pdf']
    });

    // Handle Decision Modal
    const decisionModal = document.getElementById('decisionModal');
    const decisionForm = document.getElementById('decisionForm');
    const decisionAction = document.getElementById('decisionAction');
    const submitButton = document.getElementById('submitDecision');
    let currentSubmissionId;

    // Handle modal opening
    decisionModal.addEventListener('show.bs.modal', function(event) {
        const button = event.relatedTarget;
        currentSubmissionId = button.dataset.submissionId;
        decisionAction.value = button.dataset.action;
        
        // Update modal title based on action
        const actionDisplay = decisionAction.value
            .replace(/_/g, ' ')
            .replace(/\b\w/g, l => l.toUpperCase());
            
        this.querySelector('.modal-title').textContent = actionDisplay;
        
        // Clear previous comments
        document.getElementById('comments').value = '';
        
        // Reset submit button
        submitButton.disabled = false;
        submitButton.innerHTML = 'Submit Decision';
    });

    // Handle decision submission
    submitButton.addEventListener('click', function() {
        const comments = document.getElementById('comments').value.trim();
        if (!comments) {
            alert('Please provide comments for your decision');
            return;
        }

        // Show loading state
        this.disabled = true;
        this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';

        const formData = new FormData(decisionForm);
        
        fetch(`/review/submission/${currentSubmissionId}/process-decision/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.reload();
            } else {
                alert(data.message || 'An error occurred');
                this.disabled = false;
                this.innerHTML = 'Submit Decision';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
            this.disabled = false;
            this.innerHTML = 'Submit Decision';
        });
    });

    // Add color classes to status badges
    document.querySelectorAll('.status-badge').forEach(badge => {
        const status = badge.textContent.trim().toLowerCase();
        const className = `status-${status.replace(/\s+/g, '-')}`;
        badge.classList.add(className);
    });
});
</script>
{% endblock %}

# Contents from: .\templates\review\pdf\review_template.html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {
            font-family: Helvetica, Arial, sans-serif;
            font-size: 11px;
            line-height: 1.4;
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        .title {
            font-size: 18px;
            font-weight: bold;
            margin: 10px 0;
        }
        .section {
            margin: 15px 0;
        }
        .section-title {
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .field {
            margin: 5px 0;
        }
        .field-label {
            font-weight: bold;
        }
        .footer {
            margin-top: 30px;
            font-size: 9px;
            text-align: center;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="title">Review Report</div>
    </div>

    <div class="section">
        <div class="section-title">Submission Information</div>
        <div class="field">
            <span class="field-label">Title:</span> {{ review.review_request.submission.title }}
        </div>
        <div class="field">
            <span class="field-label">Primary Investigator:</span> {{ review.review_request.submission.primary_investigator.userprofile.full_name }}
        </div>
        <div class="field">
            <span class="field-label">Study Type:</span> {{ review.review_request.submission.study_type }}
        </div>
        <div class="field">
            <span class="field-label">KHCC #:</span> {{ review.review_request.submission.khcc_number|default:"Not provided" }}
        </div>
    </div>

    <div class="section">
        <div class="section-title">Review Details</div>
        <div class="field">
            <span class="field-label">Reviewer:</span> {{ review.reviewer.userprofile.full_name }}
        </div>
        <div class="field">
            <span class="field-label">Status:</span> {{ review.is_completed|yesno:"Completed,In Progress" }}
        </div>
        <div class="field">
            <span class="field-label">Date Submitted:</span> {{ review.date_submitted|date:"Y-m-d H:i"|default:"Not submitted" }}
        </div>
    </div>

    <div class="section">
        <div class="section-title">Form Responses</div>
        {% for form_response in review.formresponse_set.all %}
            <div class="field">
                <div class="field-label">{{ form_response.form.name }}</div>
                {% for field_name, value in form_response.response_data.items %}
                    <div style="margin-left: 20px;">
                        <strong>{{ field_name }}:</strong>
                        {% if value|length > 0 %}
                            {% if value|first|stringformat:"s"|first == "[" %}
                                {{ value|join:", " }}
                            {% else %}
                                {{ value }}
                            {% endif %}
                        {% else %}
                            No response
                        {% endif %}
                    </div>
                {% endfor %}
            </div>
        {% endfor %}
    </div>

    {% if review.comments %}
    <div class="section">
        <div class="section-title">Additional Comments</div>
        <div>{{ review.comments|linebreaks }}</div>
    </div>
    {% endif %}

    <div class="footer">
        iRN is a property of the Artificial Intelligence and Data Innovation (AIDI) office 
        in collaboration with the Office of Scientific Affairs (OSAR) office @ King Hussein 
        Cancer Center, Amman - Jordan. Keep this document confidential.
    </div>
</body>
</html> 

# Contents from: .\templates\review\process_decision.html
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block title %}Process IRB Decision{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-8 offset-md-2">
            <div class="card">
                <!-- ... process decision content ... -->
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block page_specific_js %}
<script>
    // ... your JavaScript code ...
</script>
{% endblock %} 

# Contents from: .\templates\review\rc_dashboard.html
{% extends 'base.html' %}
{% load static %}
{% load review_tags %}

{% block extra_css %}
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.24/css/dataTables.bootstrap4.min.css">
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/buttons/2.2.3/css/buttons.bootstrap4.min.css">
<style>
    .btn-green {
        background-color: #28a745;
        border-color: #28a745;
        color: #fff;
    }
    .btn-green:hover {
        background-color: #218838;
        border-color: #1e7e34;
        color: #fff;
    }
</style>
{% endblock %}

{% block content %}
<div class="container">
    <h2 class="mb-4">RC Dashboard</h2>
    
    <!-- Submissions Needing Review -->
    <div class="card mb-4">
        <div class="card-header">
            <h3 class="card-title mb-0">Submissions Needing Review</h3>
        </div>
        <div class="card-body">
            {% if rc_submissions %}
                <div class="table-responsive">
                    <table id="rcSubmissionsTable" class="table table-hover">
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>Submission Date</th>
                                <th>Days Since Submission</th>
                                <th>Primary Investigator</th>
                                <th>Study Type</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for submission in rc_submissions %}
                            <tr>
                                <td>{{ submission.title }}</td>
                                <td>{{ submission.date_submitted|date:"Y-m-d" }}</td>
                                <td>{{ submission.date_submitted|timesince_in_days }}</td>
                                <td>{{ submission.primary_investigator.userprofile.full_name }}</td>
                                <td>{{ submission.study_type }}</td>
                                <td>{{ submission.get_status_display }}</td>
                                <td>
                                    <a href="{% url 'review:create_review_request' submission.pk %}" class="btn btn-primary btn-sm">Create Review Request</a>
                                    <a href="{% url 'review:review_summary' submission.pk %}" class="btn btn-success btn-sm">Details</a>
                                    <a href="{% url 'review:view_notepad' submission.pk 'RC' %}" class="btn btn-info btn-sm">
                                        <i class="fas fa-sticky-note"></i> Notepad
                                    </a>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <p class="mb-0">No submissions currently need review.</p>
            {% endif %}
        </div>
    </div>

    <!-- My Department's Submissions -->
    <div class="card mb-4">
        <div class="card-header">
            <h3 class="card-title mb-0">My Department's Submissions</h3>
        </div>
        <div class="card-body">
            {% if department_submissions %}
                <div class="table-responsive">
                    <table id="departmentSubmissionsTable" class="table table-hover">
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>Submission Date</th>
                                <th>Primary Investigator</th>
                                <th>Study Type</th>
                                <th>Requests</th>
                                <th>Days</th>
                                <th>✅</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for submission in department_submissions %}
                            <tr>
                                <td>{{ submission.title }}</td>
                                <td>{{ submission.date_submitted|date:"Y-m-d" }}</td>
                                <td>{{ submission.primary_investigator.userprofile.full_name }}</td>
                                <td>{{ submission.study_type }}</td>
                                <td>
                                    {% if submission.review_requests.exists %}
                                        <ul class="list-unstyled mb-0">
                                        {% for request in submission.review_requests.all %}
                                            <li>
                                                <strong>
                                                    <a href="{% url 'messaging:compose' %}?recipient={{ request.requested_to.id }}&submission={{ submission.id }}" 
                                                       class="text-primary text-decoration-none">
                                                        {{ request.requested_to.get_full_name }}
                                                    </a>
                                                </strong>
                                            </li>
                                        {% endfor %}
                                        </ul>
                                    {% else %}
                                        No requests yet
                                    {% endif %}
                                </td>
                                <td>
                                    {% if submission.review_requests.exists %}
                                        <ul class="list-unstyled mb-0">
                                        {% for request in submission.review_requests.all %}
                                            <li>
                                                {% with days=request.created_at|timesince_in_days %}
                                                    {{ days }}
                                                {% endwith %}
                                            </li>
                                        {% endfor %}
                                        </ul>
                                    {% else %}
                                        -
                                    {% endif %}
                                </td>
                                <td>
                                    {% if submission.review_requests.exists %}
                                        <ul class="list-unstyled mb-0">
                                        {% for request in submission.review_requests.all %}
                                            <li>
                                                {% if request.status == 'completed' %}
                                                    <span class="text-success">✅</span>
                                                {% elif request.status == 'declined' %}
                                                    <span class="text-danger">❌</span>
                                                {% elif request.status == 'pending' %}
                                                    <span class="text-warning">⏳</span>
                                                {% else %}
                                                    <span class="text-secondary">-</span>
                                                {% endif %}
                                            </li>
                                        {% endfor %}
                                        </ul>
                                    {% else %}
                                        -
                                    {% endif %}
                                </td>
                                <td>
                                    <a href="{% url 'review:review_summary' submission.pk %}" class="btn btn-success btn-sm">Details</a>
                                    <a href="{% url 'review:view_notepad' submission.pk 'RC' %}" class="btn btn-info btn-sm">
                                        <i class="fas fa-sticky-note"></i> Notepad
                                    </a>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <p class="mb-0">No submissions in your department.</p>
            {% endif %}
        </div>
    </div>

    <!-- My RC Reviews -->
    <div class="card mb-4">
        <div class="card-header">
            <h3 class="card-title mb-0">My RC Reviews</h3>
        </div>
        <div class="card-body">
            {% if rc_reviews %}
                <div class="table-responsive">
                    <table id="rcReviewsTable" class="table table-hover">
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>Primary Investigator</th>
                                <th>Requested By</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for review in rc_reviews %}
                            <tr>
                                <td>{{ review.submission.title }}</td>
                                <td>{{ review.submission.primary_investigator.userprofile.full_name }}</td>
                                <td>{{ review.requested_by.userprofile.full_name }}</td>
                                <td>{{ review.get_status_display }}</td>
                                <td>
                                    {% if review.requested_to == user or review.requested_by == user %}
                                        <a href="{% url 'review:view_review' review.id %}" 
                                           class="btn btn-info btn-sm">View Review</a>
                                    {% endif %}
                                    {% if review.requested_to == user and review.status == 'pending' %}
                                        <a href="{% url 'review:submit_review' review.id %}" 
                                           class="btn btn-primary btn-sm">Submit Review</a>
                                    {% endif %}
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <p class="mb-0">No RC reviews assigned.</p>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}

{% block page_specific_js %}
<script src="https://cdn.datatables.net/1.10.24/js/jquery.dataTables.min.js"></script>
<script src="https://cdn.datatables.net/1.10.24/js/dataTables.bootstrap4.min.js"></script>
<script src="https://cdn.datatables.net/buttons/2.2.3/js/dataTables.buttons.min.js"></script>
<script src="https://cdn.datatables.net/buttons/2.2.3/js/buttons.bootstrap4.min.js"></script>
<script>
$(document).ready(function() {
    // Initialize DataTables for all tables
    const tableConfigs = {
        rcSubmissionsTable: {
            order: [[1, 'desc']]
        },
        departmentSubmissionsTable: {
            order: [[1, 'desc']]
        },
        rcReviewsTable: {
            dom: 'Bfrtip',
            buttons: ['copy', 'excel', 'csv'],
            order: [[1, 'desc']]
        }
    };

    // Initialize all tables with their specific configurations
    Object.keys(tableConfigs).forEach(tableId => {
        const table = $(`#${tableId}`);
        if (table.length) {
            table.DataTable({
                processing: true,
                serverSide: false,
                pageLength: 10,
                ...tableConfigs[tableId]
            });
        }
    });
});
</script>
{% endblock %}

# Contents from: .\templates\review\request_extension.html
{% extends 'users/base.html' %}
{% load crispy_forms_tags %}

{% block title %}Request Review Extension{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-8 offset-md-2">
            <div class="card">
                <div class="card-header">
                    <h2>Request Review Extension</h2>
                </div>
                <div class="card-body">
                    <!-- Review Details -->
                    <div class="alert alert-info">
                        <h5>Review Details</h5>
                        <p><strong>Submission:</strong> {{ review_request.submission.title }}</p>
                        <p><strong>Current Deadline:</strong> {{ review_request.deadline|date:"F d, Y" }}</p>
                        <p><strong>Days Remaining:</strong> {{ review_request.days_until_deadline }}</p>
                    </div>

                    <form method="post" novalidate>
                        {% csrf_token %}
                        
                        <!-- New Deadline -->
                        <div class="mb-3">
                            <label for="new_deadline" class="form-label">New Deadline</label>
                            <input type="date" 
                                   class="form-control" 
                                   id="new_deadline" 
                                   name="new_deadline"
                                   min="{{ min_date }}"
                                   max="{{ max_date }}"
                                   required>
                            <div class="form-text">Select a new deadline (maximum 30 days extension)</div>
                        </div>

                        <!-- Reason -->
                        <div class="mb-3">
                            <label for="reason" class="form-label">Reason for Extension</label>
                            <textarea class="form-control" 
                                      id="reason" 
                                      name="reason" 
                                      rows="4"
                                      required></textarea>
                            <div class="form-text">Please provide a detailed reason for requesting an extension</div>
                        </div>

                        <!-- Submit Buttons -->
                        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                            <a href="{% url 'review:review_dashboard' %}" 
                               class="btn btn-secondary me-md-2">
                                <i class="fas fa-times"></i> Cancel
                            </a>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-clock"></i> Request Extension
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block page_specific_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Validate form before submission
        document.querySelector('form').addEventListener('submit', function(e) {
            var newDeadline = document.getElementById('new_deadline').value;
            var reason = document.getElementById('reason').value;
            
            if (!newDeadline || !reason) {
                e.preventDefault();
                alert('Please fill in all required fields');
                return false;
            }
            
            var selectedDate = new Date(newDeadline);
            var currentDate = new Date();
            
            if (selectedDate <= currentDate) {
                e.preventDefault();
                alert('New deadline must be in the future');
                return false;
            }
        });
    });
</script>
{% endblock %}

# Contents from: .\templates\review\review_dashboard.html
<!-- Update links in your templates -->
<a href="{% url 'review:view_review' review_request.id %}" class="btn btn-primary">
    View Review
</a> 

# Contents from: .\templates\review\review_detail.html

# templates/reviews/review_detail.html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h2>Review #{{ review.review_id }}</h2>
    <div class="card">
        <div class="card-header">
            <h3>{{ review.title }}</h3>
            <span class="badge badge-primary">{{ review.status }}</span>
        </div>
        <div class="card-body">
            <p>{{ review.content }}</p>
            <p><small>Last updated: {{ review.updated_at|date }}</small></p>
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\templates\review\review_summary.html
{% extends 'base.html' %}

{% block content %}
<div class="container">
    <div class="mb-3">
        <a href="{% url 'review:review_dashboard' %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Back to Dashboard
        </a>
    </div>

    <h2>Review Summary for {{ submission.title }}</h2>
    
    <!-- Basic Submission Info -->
    <div class="card mb-4">
        <div class="card-header">
            <h3>Submission Details</h3>
        </div>
        <div class="card-body">
            <p><strong>Primary Investigator:</strong> {{ submission.primary_investigator.userprofile.full_name }}</p>
            <p><strong>Study Type:</strong> {{ submission.study_type }}</p>
            <p><strong>Submission Date:</strong> {{ submission.date_submitted|date:"F d, Y" }}</p>
            {% if submission.khcc_number %}
                <p><strong>KHCC #:</strong> {{ submission.khcc_number }}</p>
            {% endif %}
            <p><strong>Days Since Submission:</strong> {{ stats.days_since_submission }}</p>
        </div>
    </div>

    <!-- Submission Versions Section -->
    <div class="card mb-4">
        <div class="card-header">
            <h3>Submission Versions</h3>
        </div>
        <div class="card-body">
            <table class="table">
                <thead>
                    <tr>
                        <th>Version</th>
                        <th>Submission Date</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for version in version_histories %}
                        <tr>
                            <td>{{ version.version }}</td>
                            <td>{{ version.date|date }}</td>
                            <td>
                                <div class="btn-group" role="group">
                                    {% if can_download_pdf %}
                                        <a href="{% url 'submission:download_submission_pdf_version' submission_id=submission.temporary_id version=version.version %}" 
                                           class="btn btn-primary btn-sm">
                                            <i class="fas fa-file-pdf"></i> Download PDF
                                        </a>
                                    {% endif %}
                                    
                                    {% if version.next_version %}
                                        <a href="{% url 'submission:compare_version' submission.pk version.version version.next_version %}" 
                                           class="btn btn-info btn-sm">
                                            <i class="fas fa-code-compare"></i> Compare Changes
                                        </a>
                                    {% endif %}
                                </div>
                            </td>
                        </tr>
                    {% empty %}
                        <tr>
                            <td colspan="3" class="text-center">No version history available.</td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    <!-- Review Requests Section -->
    {% if is_osar or is_irb or is_rc %}
        <div class="card mb-4">
            <div class="card-header">
                {% if is_irb %}
                    <h3>IRB Review Requests</h3>
                {% elif is_rc %}
                    <h3>RC Review Requests</h3>
                {% else %}
                    <h3>All Review Requests</h3>
                {% endif %}
            </div>
            <div class="card-body">
                {% if review_requests %}
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Reviewer</th>
                                <th>Requested By</th>
                                <th>Status</th>
                                <th>Submission Date</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for request in review_requests %}
                                <tr>
                                    <td>{{ request.requested_to.userprofile.full_name }}</td>
                                    <td>{{ request.requested_by.userprofile.full_name }}</td>
                                    <td>{{ request.get_status_display }}</td>
                                    <td>
                                        {% if request.review_set.first %}
                                            {{ request.review_set.first.date_submitted|date }}
                                        {% else %}
                                            Not submitted
                                        {% endif %}
                                    </td>
                                    <td>
                                        {% if request.review_set.first %}
                                            {% if request.requested_to == user or request.requested_by == user %}
                                                <a href="{% url 'review:view_review' review_request_id=request.id %}" 
                                                   class="btn btn-info btn-sm">View Review</a>
                                            {% else %}
                                                <span>Review Submitted</span>
                                            {% endif %}
                                        {% else %}
                                            <span class="text-muted">Review pending</span>
                                        {% endif %}
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                {% else %}
                    <div class="alert alert-info">
                        No review requests found.
                        {% if is_osar and can_create_review %}
                            <a href="{% url 'review:create_review_request' submission.pk %}" 
                               class="btn btn-primary btn-sm ml-2">Create Review Request</a>
                        {% endif %}
                    </div>
                {% endif %}
            </div>
        </div>
    {% endif %}

    <!-- Attached Files Section -->
    <div class="card mb-4">
        <div class="card-header">
            <h3>Attached Files</h3>
        </div>
        <div class="card-body">
            {% if submission.documents.exists %}
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>File Name</th>
                                <th>Description</th>
                                <th>Uploaded By</th>
                                <th>Upload Date</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for doc in submission.documents.all %}
                                <tr>
                                    <td>{{ doc.filename }}</td>
                                    <td>{{ doc.description|default:"-" }}</td>
                                    <td>{{ doc.uploaded_by.userprofile.full_name }}</td>
                                    <td>{{ doc.uploaded_at|date:"Y-m-d H:i" }}</td>
                                    <td>
                                        <a href="{{ doc.file.url }}" 
                                           class="btn btn-sm btn-primary"
                                           target="_blank">
                                            <i class="fas fa-download"></i> Download
                                        </a>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <p class="text-muted mb-0">No files attached to this submission.</p>
            {% endif %}
        </div>
    </div>

    <!-- Study Actions History Section -->
    <div class="card mb-4">
        <div class="card-header">
            <h3 class="card-title mb-0">Study Actions History</h3>
        </div>
        <div class="card-body">
            {% if study_actions %}
                <table class="table">
                    <thead>
                        <tr>
                            <th>Action Type</th>
                            <th>Performed By</th>
                            <th>Status</th>
                            <th>Date Created</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for action in study_actions %}
                            <tr>
                                <td>{{ action.action_type }}</td>
                                <td>{{ action.performed_by }}</td>
                                <td>
                                    <span class="badge {% if action.status == 'pending' %}bg-warning{% elif action.status == 'completed' %}bg-success{% else %}bg-danger{% endif %}">
                                        {{ action.status }}
                                    </span>
                                </td>
                                <td>{{ action.date_created }}</td>
                                <td>
                                    <div class="btn-group">
                                        {% if action.documents.exists %}
                                            <a href="{{ action.pdf_url }}" class="btn btn-sm btn-outline-primary">
                                                <i class="fas fa-file-pdf"></i> View PDF
                                            </a>
                                        {% endif %}
                                        
                                        <a href="{% url 'review:download_action_pdf' action.id %}" class="btn btn-sm btn-outline-secondary">
                                            <i class="fas fa-print"></i> Print
                                        </a>

                                        {% if action.status == 'pending' and can_process_actions %}
                                            <button type="button" class="btn btn-sm btn-primary process-action-btn" data-action-id="{{ action.id }}">
                                                Process
                                            </button>
                                        {% endif %}
                                    </div>

                                    <!-- Process Action Form -->
                                    <div class="process-action-form mt-3 bg-light p-3 rounded d-none" id="process-form-{{ action.id }}">
                                        <form>
                                            <div class="mb-3">
                                                <label for="letter-{{ action.id }}" class="form-label">Decision Letter</label>
                                                <textarea class="form-control" id="letter-{{ action.id }}" rows="5" required placeholder="Enter your decision letter text here..."></textarea>
                                                <small class="form-text text-muted">This will be sent to the investigator.</small>
                                            </div>
                                            <div class="mb-3">
                                                <label for="comments-{{ action.id }}" class="form-label">Internal Comments</label>
                                                <textarea class="form-control" id="comments-{{ action.id }}" rows="3" required placeholder="Enter any internal comments about this decision..."></textarea>
                                                <small class="form-text text-muted">These comments will be stored with the action record.</small>
                                            </div>
                                            <div class="d-flex justify-content-end gap-2">
                                                <button type="button" class="btn btn-success approve-btn" data-action-id="{{ action.id }}">
                                                    <i class="fas fa-check"></i> Approve
                                                </button>
                                                <button type="button" class="btn btn-danger reject-btn" data-action-id="{{ action.id }}">
                                                    <i class="fas fa-times"></i> Reject
                                                </button>
                                            </div>
                                        </form>
                                    </div>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            {% else %}
                <div class="alert alert-info">
                    No actions have been recorded yet.
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}

{% block page_specific_js %}
<script>
document.addEventListener('DOMContentLoaded', function() {
    const submissionId = "{{ submission.temporary_id }}";

    // Initialize Process Action buttons
    document.querySelectorAll('.process-action-btn').forEach(button => {
        button.addEventListener('click', function() {
            const actionId = this.dataset.actionId;
            const form = document.getElementById(`process-form-${actionId}`);
            form.classList.toggle('d-none');
        });
    });

    // Process Action Function
    async function processAction(actionId, decision, comments, letterText) {
        try {
            const response = await fetch(`/review/submission/${submissionId}/action/${actionId}/process/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: `decision=${decision}&comments=${encodeURIComponent(comments)}&letter_text=${encodeURIComponent(letterText)}`
            });

            const data = await response.json();
            if (data.status === 'success') {
                window.location.reload();
            } else {
                alert(data.message || 'Error processing action');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    }

    // Approve Button Click Handlers
    document.querySelectorAll('.approve-btn').forEach(button => {
        button.addEventListener('click', function() {
            const actionId = this.dataset.actionId;
            const comments = document.getElementById(`comments-${actionId}`).value.trim();
            const letterText = document.getElementById(`letter-${actionId}`).value.trim();
            
            if (!comments || !letterText) {
                alert('Please provide both a decision letter and internal comments.');
                return;
            }

            if (confirm('Are you sure you want to approve this action?')) {
                processAction(actionId, 'approve', comments, letterText);
            }
        });
    });

    // Reject Button Click Handlers
    document.querySelectorAll('.reject-btn').forEach(button => {
        button.addEventListener('click', function() {
            const actionId = this.dataset.actionId;
            const comments = document.getElementById(`comments-${actionId}`).value.trim();
            const letterText = document.getElementById(`letter-${actionId}`).value.trim();
            
            if (!comments || !letterText) {
                alert('Please provide both a decision letter and internal comments.');
                return;
            }

            if (confirm('Are you sure you want to reject this action?')) {
                processAction(actionId, 'reject', comments, letterText);
            }
        });
    });
});
</script>
{% endblock %}

# Contents from: .\templates\review\submission_detail.html
<!-- submission/templates/submission_detail.html -->
{% extends 'base.html' %}
{% block content %}
<h2>{{ submission.title }}</h2>
<p>Current Version: {{ submission.version }}</p>
<h3>All Versions</h3>
<ul>
    {% for version in versions %}
        <li>
            Version {{ version.version }} - {{ version.status }} on {{ version.date }}
            <a href="{% url 'submission:view_version' submission.id version.version %}">View</a>
            {% if not forloop.last %}
                <a href="{% url 'submission:compare_versions' submission.id version.version submission.version %}">Compare with Latest</a>
            {% endif %}
        </li>
    {% endfor %}
</ul>
{% endblock %}


# Contents from: .\templates\review\submission_table.html
{% comment %}dashboard/submissions_table.html{% endcomment %}

{% if submissions %}
<div class="table-responsive">
  <table id="{{ table_id }}" class="table table-hover">
    <thead>
      <tr>
        <th>Title</th>
        <th>Submission Date</th>
        <th>Primary Investigator</th>
        <th>Study Type</th>
        <th>Requests</th>
        <th>Days</th>
        <th>Status</th>
        <th>KHCC #</th>
        {% if show_visibility %}
        <th>Visibility</th>
        {% endif %}
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      {% for submission in submissions %}
      <tr>
        <td>{{ submission.title }}</td>
        <td>{{ submission.date_submitted|date:"Y-m-d" }}</td>
        <td>{{ submission.primary_investigator.userprofile.full_name }}</td>
        <td>{{ submission.study_type }}</td>
        <td>
          {% include "dashboard/request_list.html" with requests=submission.review_requests.all %}
        </td>
        <td>
          {% include "dashboard/days_list.html" with requests=submission.review_requests.all %}
        </td>
        <td>
          <span class="status-badge {{ submission.status|slugify }}">
            {{ submission.get_status_display }}
          </span>
        </td>
        <td>{{ submission.khcc_number|default:"-" }}</td>
        {% if show_visibility %}
        <td>
          {% include "dashboard/visibility_toggle.html" with submission=submission %}
        </td>
        {% endif %}
        <td>
          {% include "dashboard/action_buttons.html" with submission=submission %}
        </td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% else %}
<p class="mb-0">No submissions found.</p>
{% endif %}

# Contents from: .\templates\review\submission_versions.html
{% extends 'users/base.html' %}
{% block content %}
<div class="container mt-4">
    <h1>Review Versions for "{{ submission.title }}"</h1>
    <div class="mb-3">
        <a href="{% url 'review:review_dashboard' %}" class="btn btn-secondary">Back to Dashboard</a>
    </div>
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Version</th>
                <th>Status</th>
                <th>Date</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for history in histories %}
            <tr>
                <td>{{ history.version }}</td>
                <td>{{ history.get_status_display }}</td>
                <td>{{ history.date }}</td>
                <td>
                    <a href="{% url 'submission:download_submission_pdf_version' submission.temporary_id history.version %}" class="btn btn-sm btn-secondary">Download PDF</a>
                    {% if not forloop.last %}
                    <a href="{% url 'submission:compare_versions' submission.temporary_id history.version submission.version %}" class="btn btn-sm btn-primary">Compare with Latest</a>
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %} 

# Contents from: .\templates\review\submit_review.html
<!-- review/templates/review/submit_review.html -->
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block content %}
<div class="container mt-4">
    <div class="card mb-4">
        <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <h2>Submit Review for {{ review_request.submission.title }}</h2>
                    <p class="text-muted mb-0">
                        Primary Investigator: {{ review_request.submission.primary_investigator.userprofile.full_name }}
                    </p>
                </div>
                <div>
                    <a href="{% url 'review:review_summary' review_request.submission.pk %}" 
                       class="btn btn-success">
                        <i class="fas fa-info-circle"></i> Details
                    </a>
                </div>
            </div>
        </div>
    </div>

    <form method="post" novalidate>
        {% csrf_token %}
        
        {% for form_data in forms_data %}
        <div class="card mb-4">
            <div class="card-header">
                <h3>{{ form_data.template.name }}</h3>
                {% if form_data.template.help_text %}
                <p class="text-muted">{{ form_data.template.help_text }}</p>
                {% endif %}
            </div>
            <div class="card-body">
                {{ form_data.form|crispy }}
            </div>
        </div>
        {% endfor %}

        <div class="card mb-4">
            <div class="card-header">
                <h3>Additional Comments</h3>
            </div>
            <div class="card-body">
                <textarea name="comments" class="form-control" rows="4" 
                          placeholder="Enter any additional comments about this review..."></textarea>
            </div>
        </div>

        <div class="d-grid gap-2 d-md-flex justify-content-md-end mb-4">
            <button type="submit" name="action" value="save_draft" class="btn btn-secondary me-md-2">
                <i class="fas fa-save"></i> Save Draft
            </button>
            <button type="submit" name="action" value="submit" class="btn btn-primary">
                <i class="fas fa-check"></i> Submit Review
            </button>
        </div>
    </form>
</div>
{% endblock %}


# Contents from: .\templates\review\view_notepad.html
{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="container">
    <div class="row mb-4">
        <div class="col">
            <a href="{% url 'review:review_dashboard' %}" class="btn btn-secondary mb-3">
                <i class="fas fa-arrow-left"></i> Back to Dashboard
            </a>
            <h2>{{ notepad_type }} Notepad</h2>
            <h4 class="text-muted">{{ submission.title }}</h4>
        </div>
    </div>

    <!-- New Note Form -->
    <div class="card mb-4">
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                <div class="form-group">
                    <label for="note_text">Add New Note:</label>
                    <textarea 
                        class="form-control" 
                        id="note_text" 
                        name="note_text" 
                        rows="3" 
                        required
                    ></textarea>
                </div>
                <button type="submit" class="btn btn-primary mt-2">Add Note</button>
            </form>
        </div>
    </div>

    <!-- Existing Notes -->
    <div class="card">
        <div class="card-header">
            <h3 class="card-title mb-0">Previous Notes</h3>
        </div>
        <div class="card-body">
            {% if notes %}
            {% for note in notes %}
            <div class="note-entry mb-4 {% if request.user not in note.read_by.all %}font-weight-bold text-danger{% endif %}">
                <div class="note-content">
                    {{ note.text|linebreaks }}
                </div>
                <div class="note-metadata text-muted">
                    <small>
                        Added by {{ note.created_by.userprofile.full_name }} 
                        on {{ note.created_at|date:"F d, Y" }} 
                        at {{ note.created_at|time:"H:i" }}
                    </small>
                </div>
                <hr>
            </div>
        {% endfor %}
            {% else %}
                <p class="text-muted">No notes have been added yet.</p>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %} 

# Contents from: .\templates\review\view_review.html
{% extends 'users/base.html' %}
{% load crispy_forms_tags %}

{% block title %}Review Details{% endblock %}

{% block page_specific_css %}
<style>
    .status-badge {
        padding: 0.4em 0.8em;
        border-radius: 0.25rem;
        font-size: 0.875em;
    }
    .form-response {
        margin-bottom: 2rem;
        padding: 1rem;
        border: 1px solid #dee2e6;
        border-radius: 0.25rem;
    }
    .form-response h3 {
        color: #2c3e50;
        font-size: 1.25rem;
        margin-bottom: 1rem;
    }
    .response-field {
        margin-bottom: 1rem;
    }
    .response-field label {
        font-weight: bold;
        color: #495057;
    }
    .response-field .value {
        margin-left: 1rem;
    }
    .metadata {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.25rem;
        margin-bottom: 1rem;
    }
    .metadata-item {
        margin-bottom: 0.5rem;
    }
</style>
{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Header Section -->
    <div class="card mb-4 shadow-sm">
        <div class="card-body">
            <div class="row">
                <div class="col-md-8">
                    <h2 class="text-primary mb-2">{{ submission.title }}</h2>
                    <div class="text-muted">
                        <strong>Primary Investigator:</strong> 
                        {{ submission.primary_investigator.get_full_name }}
                    </div>
                    <div class="mt-2">
                        <span class="badge bg-info">Version {{ submission.version }}</span>
                    </div>
                </div>
                <div class="col-md-4 text-md-end">
                    
                </div>
            </div>
        </div>
    </div>

    <!-- Review Header -->
    <div class="card mb-4">
        <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
                <h2 class="mb-0">Review Details</h2>
                <div>
                    {% if can_edit %}
                    <a href="{% url 'review:submit_review' review.id %}" class="btn btn-primary">
                        <i class="fas fa-edit"></i> Edit Review
                    </a>
                    {% endif %}
                    <a href="{% url 'review:review_dashboard' %}" class="btn btn-secondary">
                        <i class="fas fa-arrow-left"></i> Back to Dashboard
                    </a>
                </div>
            </div>
        </div>
        <div class="card-body">
            <!-- Metadata Section -->
            <div class="metadata">
                <div class="row">
                    <div class="col-md-6">
                        
                        <div class="metadata-item">
                            
                                <strong>Reviewed by: {{ review.reviewer.get_full_name }}</small><br>
                                                          
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="metadata-item">
                            <strong>Submitted:</strong> {{ review.date_submitted|date:"F d, Y H:i" }}
                        </div>
                        <div class="metadata-item">
                            <strong>Status:</strong> 
                            <span class="status-badge status-{{ review_request.status }}">
                                {{ review_request.get_status_display }}
                            </span>
                        </div>
                        <div class="metadata-item">
                            <strong>Requested By:</strong> {{ review_request.requested_by.userprofile.full_name }}
                        </div>
                        <div class="metadata-item">
                            <strong>Requested on:</strong> {{ review_request.created_at|date:"F d, Y" }}
                        </div>
                    </div>
                </div>
            </div>

            <!-- Form Responses -->
            {% if form_responses %}
                {% for response in form_responses %}
                <div class="form-response">
                    <h3>{{ response.form.name }}</h3>
                    {% for field_name, field_value in response.response_data.items %}
                    <div class="response-field">
                        <label>{{ field_name }}:</label>
                        <div class="value">
                            {% if field_value|length > 100 %}
                                <pre class="pre-scrollable">{{ field_value }}</pre>
                            {% else %}
                                {{ field_value }}
                            {% endif %}
                        </div>
                    </div>
                    {% endfor %}
                </div>
                {% endfor %}
            {% else %}
                <div class="alert alert-info">
                    No form responses found for this review.
                </div>
            {% endif %}

            <!-- Comments Section -->
            {% if review.comments %}
            <div class="card mt-4">
                <div class="card-header">
                    <h3 class="mb-0">Additional Comments</h3>
                </div>
                <div class="card-body">
                    {{ review.comments|linebreaks }}
                </div>
            </div>
            {% endif %}
        </div>
    </div>

    <!-- Action Buttons -->
    <div class="card">
        <div class="card-body">
            <div class="d-flex justify-content-between">
                <div>
                    {% if is_requester or is_pi %}
                    <a href="{% url 'messaging:compose_message' %}?related_review={{ review.id }}" 
                       class="btn btn-info">
                        <i class="fas fa-envelope"></i> Contact Reviewer
                    </a>
                    {% endif %}
                </div>
                <div>
                    {% if is_pi or is_requester %}
                    <a href="{% url 'submission:download_submission_pdf' submission.id review.submission_version %}" 
                       class="btn btn-secondary">
                        <i class="fas fa-file-pdf"></i> Download Submission Version
                    </a>
                    {% endif %}
                    <a href="{% url 'review:download_review_pdf' review.review_request.id %}" class="btn btn-primary">
                        <i class="fas fa-file-pdf"></i> Download Review PDF
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\__init__.py


# Contents from: .\admin.py
# review/admin.py

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from submission.models import Submission
from .models import ReviewRequest, Review, FormResponse

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['review_id', 'reviewer', 'submission', 'date_submitted']
    search_fields = ['reviewer__username', 'submission__title']
    list_filter = ['date_submitted']

@admin.register(ReviewRequest)
class ReviewRequestAdmin(admin.ModelAdmin):
    list_display = ['submission', 'requested_by', 'requested_to', 'deadline', 'status']
    search_fields = ['submission__title', 'requested_by__username', 'requested_to__username']
    list_filter = ['status', 'deadline']

@admin.register(FormResponse)
class FormResponseAdmin(admin.ModelAdmin):
    list_display = ['review', 'form', 'date_submitted']
    search_fields = ['review__reviewer__username', 'form__name']
    list_filter = ['date_submitted']

# Contents from: .\apps.py
# review/apps.py

from django.apps import AppConfig


class ReviewConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "review"


# Contents from: .\combine.py
import os

def get_files_recursively(directory, extensions):
    """
    Recursively get all files with specified extensions from directory and subdirectories
    """
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_list.append(os.path.join(root, file))
    return file_list

def combine_files(output_file, file_list):
    """
    Combine contents of all files in file_list into output_file
    """
    with open(output_file, 'a', encoding='utf-8') as outfile:
        for fname in file_list:
            # Add a header comment to show which file's contents follow
            outfile.write(f"\n\n# Contents from: {fname}\n")
            try:
                with open(fname, 'r', encoding='utf-8') as infile:
                    for line in infile:
                        outfile.write(line)
            except Exception as e:
                outfile.write(f"# Error reading file {fname}: {str(e)}\n")

def main():
    # Define the base directory (current directory in this case)
    base_directory = "."
    output_file = 'combined.py'
    extensions = ('.py', '.html')

    # Remove output file if it exists
    if os.path.exists(output_file):
        try:
            os.remove(output_file)
        except Exception as e:
            print(f"Error removing existing {output_file}: {str(e)}")
            return

    # Get all files recursively
    all_files = get_files_recursively(base_directory, extensions)
    
    # Sort files by extension and then by name
    all_files.sort(key=lambda x: (os.path.splitext(x)[1], x))

    # Add a header to the output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write("# Combined Python and HTML files\n")
        outfile.write(f"# Generated from directory: {os.path.abspath(base_directory)}\n")
        outfile.write(f"# Total files found: {len(all_files)}\n\n")

    # Combine all files
    combine_files(output_file, all_files)
    
    print(f"Successfully combined {len(all_files)} files into {output_file}")
    print("Files processed:")
    for file in all_files:
        print(f"  - {file}")

if __name__ == "__main__":
    main()

# Contents from: .\forms.py
# review/forms.py

from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from .models import ReviewRequest
from forms_builder.models import DynamicForm
from dal import autocomplete

from django import forms
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.db.models import Q
from .models import ReviewRequest
from forms_builder.models import DynamicForm
from dal import autocomplete

class ReviewRequestForm(forms.ModelForm):
    requested_to = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        widget=forms.Select(attrs={
            'class': 'form-select',
            'data-placeholder': 'Select a reviewer...',
        }),
        label="Select Reviewer",
        help_text="Choose a qualified reviewer for this submission"
    )

    class Meta:
        model = ReviewRequest
        fields = ['requested_to', 'deadline', 'message', 'selected_forms', 'can_forward']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'selected_forms': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'can_forward': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, study_type=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set up reviewer field to show full name
        self.fields['requested_to'].queryset = User.objects.filter(
            is_active=True
        ).select_related('userprofile').order_by('userprofile__full_name')
        
        self.fields['requested_to'].label_from_instance = lambda user: (
            f"{user.get_full_name() or user.username}"
        )

        # Filter forms for Evaluation study type
        form_queryset = DynamicForm.objects.filter(
            study_types__name='Evaluation'
        ).order_by('order', 'name')
            
        self.fields['selected_forms'].queryset = form_queryset
        self.fields['selected_forms'].widget.attrs.update({
            'class': 'form-control',
            'size': min(10, form_queryset.count()),  # Show up to 10 items
            'multiple': 'multiple'  # Enable multiple selection
        })

class ConflictOfInterestForm(forms.Form):
    conflict_of_interest = forms.ChoiceField(
        choices=[('no', 'No'), ('yes', 'Yes')],
        widget=forms.RadioSelect,
        label='Do you have a conflict of interest with this submission?'
    )
    conflict_details = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Provide details (optional)'}),
        required=False,
        label='Conflict Details'
    )

# Contents from: .\management\commands\setup_review_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Creates required groups for review system'

    def handle(self, *args, **kwargs):
        required_groups = [
            'OSAR',
            'IRB Chair',
            'RC Chair',
            'AHARRP Head'
        ]
        
        for group_name in required_groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created {group_name} group')
                )
            else:
                self.stdout.write(f'{group_name} group already exists') 

# Contents from: .\migrations\0001_initial.py
# Generated by Django 5.1.2 on 2024-11-05 18:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        (
            "forms_builder",
            "0002_alter_dynamicform_options_alter_formfield_options_and_more",
        ),
        ("submission", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("submission_version", models.PositiveIntegerField()),
                ("comments", models.TextField()),
                ("date_submitted", models.DateTimeField(auto_now_add=True)),
                (
                    "reviewer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "submission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="submission.submission",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FormResponse",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("response_data", models.JSONField()),
                ("date_submitted", models.DateTimeField(auto_now_add=True)),
                (
                    "form",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="forms_builder.dynamicform",
                    ),
                ),
                (
                    "review",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="review.review"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ReviewRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "submission_version",
                    models.PositiveIntegerField(
                        help_text="Version number of the submission being reviewed"
                    ),
                ),
                ("message", models.TextField(blank=True)),
                ("deadline", models.DateField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("accepted", "Accepted"),
                            ("declined", "Declined"),
                            ("completed", "Completed"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("conflict_of_interest_declared", models.BooleanField(null=True)),
                ("conflict_of_interest_details", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "requested_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="review_requests_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "requested_to",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="review_requests_received",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "selected_forms",
                    models.ManyToManyField(to="forms_builder.dynamicform"),
                ),
                (
                    "submission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="submission.submission",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="review",
            name="review_request",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="review.reviewrequest"
            ),
        ),
    ]


# Contents from: .\migrations\0002_statuschoice_alter_reviewrequest_status.py
# Generated by Django 5.1.2 on 2024-11-05 20:45

import submission.models
from django.db import migrations, models

# Define the review status choices directly in the migration
REVIEW_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('declined', 'Declined'),
    ('completed', 'Completed'),
    ('overdue', 'Overdue'),
    ('extended', 'Extended'),
    ('request_withdrawn', 'Request Withdrawn'),
]

class Migration(migrations.Migration):

    dependencies = [
        ("review", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="StatusChoice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=50, unique=True)),
                ("label", models.CharField(max_length=100)),
                ("is_active", models.BooleanField(default=True)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={
                "verbose_name": "Status Choice",
                "verbose_name_plural": "Status Choices",
                "ordering": ["order"],
            },
        ),
        migrations.AlterField(
            model_name="reviewrequest",
            name="status",
            field=models.CharField(
                choices=REVIEW_STATUS_CHOICES,
                max_length=50,
                default='pending'
            ),
        ),
    ]


# Contents from: .\migrations\0003_review_is_archived_reviewrequest_extension_reason_and_more.py
# Generated by Django 5.1.2 on 2024-11-05 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0002_statuschoice_alter_reviewrequest_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="is_archived",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="reviewrequest",
            name="extension_reason",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="reviewrequest",
            name="extension_requested",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="reviewrequest",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="reviewrequest",
            name="order",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="reviewrequest",
            name="proposed_deadline",
            field=models.DateField(blank=True, null=True),
        ),
    ]


# Contents from: .\migrations\0004_alter_reviewrequest_status.py
# Generated by Django 5.1.2 on 2024-11-05 22:46

import review.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0003_review_is_archived_reviewrequest_extension_reason_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reviewrequest",
            name="status",
            field=models.CharField(
                choices=review.models.get_status_choices,
                default="pending",
                max_length=50,
            ),
        ),
    ]


# Contents from: .\migrations\0005_reviewrequest_can_forward_and_more.py
# Generated by Django 5.1.2 on 2024-11-05 23:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0004_alter_reviewrequest_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="reviewrequest",
            name="can_forward",
            field=models.BooleanField(
                default=False, help_text="Whether this reviewer can forward to others"
            ),
        ),
        migrations.AddField(
            model_name="reviewrequest",
            name="forwarding_chain",
            field=models.JSONField(
                default=list, help_text="List of users who forwarded this request"
            ),
        ),
        migrations.AddField(
            model_name="reviewrequest",
            name="parent_request",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="child_requests",
                to="review.reviewrequest",
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="comments",
            field=models.TextField(blank=True),
        ),
    ]


# Contents from: .\migrations\0006_alter_reviewrequest_submission.py
# Generated by Django 5.1.2 on 2024-11-06 01:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0005_reviewrequest_can_forward_and_more"),
        ("submission", "0005_statuschoice_alter_submission_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reviewrequest",
            name="submission",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="review_requests",
                to="submission.submission",
            ),
        ),
    ]


# Contents from: .\migrations\0007_alter_review_id.py
# Generated by Django 5.1.2 on 2024-11-06 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0006_alter_reviewrequest_submission"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]


# Contents from: .\migrations\0008_rename_id_review_review_id.py
# Generated by Django 5.1.2 on 2024-11-07 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0007_alter_review_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="review",
            old_name="id",
            new_name="review_id",
        ),
    ]


# Contents from: .\migrations\0009_alter_review_options_review_is_completed.py
# Generated by Django 5.1.2 on 2024-11-07 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0008_rename_id_review_review_id"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="review",
            options={"ordering": ["-date_submitted"]},
        ),
        migrations.AddField(
            model_name="review",
            name="is_completed",
            field=models.BooleanField(default=False),
        ),
    ]


# Contents from: .\migrations\0010_alter_review_options_remove_review_is_completed.py
# Generated by Django 5.1.2 on 2024-11-08 00:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0009_alter_review_options_review_is_completed"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="review",
            options={},
        ),
        migrations.RemoveField(
            model_name="review",
            name="is_completed",
        ),
    ]


# Contents from: .\migrations\0011_alter_reviewrequest_status.py
# Generated by Django 5.1.2 on 2024-11-09 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0010_alter_review_options_remove_review_is_completed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reviewrequest",
            name="status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("submitted", "Submitted"),
                    ("under_review", "Under Review"),
                    ("revision_needed", "Unlocked for Revision"),
                    ("accepted", "Accepted"),
                    ("declined", "Declined"),
                    ("suspended", "Suspended"),
                    ("withdrawn", "Withdrawn"),
                    ("expired", "Expired"),
                    ("archived", "Archived"),
                ],
                default="pending",
                max_length=50,
            ),
        ),
    ]


# Contents from: .\migrations\0012_alter_reviewrequest_status.py
# Generated by Django 5.1.2 on 2024-11-09 20:49

import iRN.constants
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0011_alter_reviewrequest_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reviewrequest",
            name="status",
            field=models.CharField(
                choices=iRN.constants.get_status_choices,
                default="pending",
                max_length=50,
            ),
        ),
    ]


# Contents from: .\migrations\0013_alter_review_options.py
# Generated by Django 5.1.3 on 2024-11-30 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0012_alter_reviewrequest_status"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="review",
            options={
                "permissions": [
                    ("view_any_review", "Can view any review regardless of assignment"),
                    ("change_submission_status", "Can change submission status"),
                ]
            },
        ),
    ]


# Contents from: .\migrations\0014_notepadentry.py
# Generated by Django 5.1.3 on 2024-11-30 13:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0013_alter_review_options"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="NotepadEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "notepad_type",
                    models.CharField(
                        choices=[
                            ("OSAR", "OSAR Notepad"),
                            ("IRB", "IRB Notepad"),
                            ("RC", "RC Notepad"),
                        ],
                        max_length=10,
                    ),
                ),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Notepad Entry",
                "verbose_name_plural": "Notepad Entries",
                "ordering": ["-created_at"],
            },
        ),
    ]


# Contents from: .\migrations\0015_delete_notepadentry.py
# Generated by Django 5.1.3 on 2024-11-30 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0014_notepadentry"),
    ]

    operations = [
        migrations.DeleteModel(
            name="NotepadEntry",
        ),
    ]


# Contents from: .\migrations\0016_notepadentry.py
# Generated by Django 5.1.3 on 2024-11-30 14:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0015_delete_notepadentry"),
        ("submission", "0014_submission_show_in_irb_submission_show_in_rc"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="NotepadEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "notepad_type",
                    models.CharField(
                        choices=[("OSAR", "OSAR"), ("IRB", "IRB"), ("RC", "RC")],
                        max_length=10,
                    ),
                ),
                ("text", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "submission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notepad_entries",
                        to="submission.submission",
                    ),
                ),
            ],
            options={
                "verbose_name": "Notepad Entry",
                "verbose_name_plural": "Notepad Entries",
                "ordering": ["-created_at"],
            },
        ),
    ]


# Contents from: .\migrations\0017_notepadentry_read_by_alter_notepadentry_created_by_and_more.py
# Generated by Django 5.1.3 on 2024-12-02 20:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0016_notepadentry"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="notepadentry",
            name="read_by",
            field=models.ManyToManyField(
                blank=True, related_name="read_notes", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="notepadentry",
            name="created_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="created_notes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterModelTable(
            name="notepadentry",
            table="review_notepad_entry",
        ),
    ]


# Contents from: .\migrations\0018_submissiondecision.py
# Generated by Django 5.1.3 on 2024-12-05 21:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0017_notepadentry_read_by_alter_notepadentry_created_by_and_more"),
        ("submission", "0028_alter_submission_options_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="SubmissionDecision",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "decision",
                    models.CharField(
                        choices=[
                            ("revision_requested", "Revision Requested"),
                            ("rejected", "Rejected"),
                            ("accepted", "Accepted"),
                        ],
                        max_length=20,
                    ),
                ),
                ("comments", models.TextField(blank=True)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                (
                    "decided_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "submission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="decisions",
                        to="submission.submission",
                    ),
                ),
            ],
            options={
                "db_table": "review_submission_decision",
                "ordering": ["-date_created"],
            },
        ),
    ]


# Contents from: .\migrations\__init__.py


# Contents from: .\models.py
from django.db import models
from django.contrib.auth.models import User
from submission.models import Submission
from forms_builder.models import DynamicForm
from datetime import datetime
from django.core.cache import cache
from django.utils import timezone
from django.apps import apps
from iRN.constants import get_status_choices

######################
# Status Choice
######################

class StatusChoice(models.Model):
    """Model to store custom status choices."""
    code = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Status Choice'
        verbose_name_plural = 'Status Choices'

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete('review_status_choices')

######################
# Review Request
######################

class ReviewRequest(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE,  related_name='review_requests' )
    submission_version = models.PositiveIntegerField(
        help_text="Version number of the submission being reviewed"
    )
    requested_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='review_requests_created'
    )
    requested_to = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='review_requests_received'
    )
    message = models.TextField(blank=True)
    deadline = models.DateField()
    status = models.CharField(
        max_length=50,
        choices=get_status_choices,
        default='pending'
    )
    selected_forms = models.ManyToManyField(DynamicForm)
    conflict_of_interest_declared = models.BooleanField(null=True)
    conflict_of_interest_details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1)
    extension_requested = models.BooleanField(default=False)
    proposed_deadline = models.DateField(null=True, blank=True)
    extension_reason = models.TextField(null=True, blank=True)
    
    parent_request = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='child_requests'
    )
    forwarding_chain = models.JSONField(
        default=list,
        help_text="List of users who forwarded this request"
    )
    can_forward = models.BooleanField(
        default=False,
        help_text="Whether this reviewer can forward to others"
    )

    @classmethod
    def can_create_review_request(cls, user):
        """Check if the user can create a review request."""
        # Check if the user is in any of the required groups
        return user.groups.filter(name__in=['IRB', 'OSAR', 'RC']).exists()

    @property
    def is_overdue(self):
        return self.deadline < timezone.now().date()

    @property
    def days_until_deadline(self):
        return (self.deadline - timezone.now().date()).days

    @property
    def has_forwarded_requests(self):
        """Check if this review request has any child requests (has been forwarded)"""
        return self.child_requests.exists()

    @property
    def forward_count(self):
        """Return the number of times this request has been forwarded"""
        return self.child_requests.count()

    def save(self, *args, **kwargs):
        # Ensure submission_version is an integer
        if isinstance(self.submission_version, datetime):
            self.submission_version = self.submission.version
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review Request for {self.submission} (Version {self.submission_version})"

######################
# Review
######################

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    review_request = models.ForeignKey(ReviewRequest, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    submission_version = models.PositiveIntegerField()
    comments = models.TextField(blank=True)
    date_submitted = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)

    class Meta:
        permissions = [
            ("view_any_review", "Can view any review regardless of assignment"),
            ("change_submission_status", "Can change submission status"),
        ]

    def __str__(self):
        return f"Review by {self.reviewer} for {self.submission}"

######################
# Form Response
######################

class FormResponse(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    form = models.ForeignKey('forms_builder.DynamicForm', on_delete=models.CASCADE)
    response_data = models.JSONField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to {self.form} for {self.review}"

######################
# Notepad
######################
# models.py

class NotepadEntry(models.Model):
    NOTEPAD_TYPES = [
        ('OSAR', 'OSAR'),
        ('IRB', 'IRB'),
        ('RC', 'RC'),
    ]
    
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='notepad_entries')
    notepad_type = models.CharField(max_length=10, choices=NOTEPAD_TYPES)
    text = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_notes')
    created_at = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(User, related_name='read_notes', blank=True)

    class Meta:
        verbose_name = 'Notepad Entry'
        verbose_name_plural = 'Notepad Entries'
        ordering = ['-created_at']
        db_table = 'review_notepad_entry'


######################
# Submission Decision
######################

class SubmissionDecision(models.Model):
    DECISION_CHOICES = [
        ('revision_requested', 'Revision Requested'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
        ('provisional_approval', 'Provisional Approval'),
        ('suspended', 'Suspended'),
    ]

    submission = models.ForeignKey('submission.Submission', on_delete=models.CASCADE, related_name='decisions')
    decision = models.CharField(max_length=20, choices=DECISION_CHOICES)
    comments = models.TextField(blank=True)
    decided_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']
        db_table = 'review_submission_decision'

    def __str__(self):
        return f"{self.get_decision_display()} for {self.submission}"



# Contents from: .\tasks.py
# tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta

@shared_task
def send_review_reminders():
    upcoming_deadlines = ReviewRequest.objects.filter(
        status='pending',
        deadline__lte=timezone.now() + timedelta(days=2)
    )
    for request in upcoming_deadlines:
        send_reminder_email(request)

# Contents from: .\templatetags\review_extras.py
from django import template
from django.utils import timezone
from datetime import datetime

register = template.Library()

@register.filter
def timesince_in_days(value):
    if not value:
        return 0
    
    if isinstance(value, str):
        value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    
    now = timezone.now()
    diff = now - value
    return diff.days 

# Contents from: .\templatetags\review_tags.py
# review/templatetags/review_tags.py

from django import template
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

register = template.Library()

@register.filter
def get_user_name(user_id):
    """Get user's full name from ID."""
    try:
        user = User.objects.select_related('userprofile').get(id=user_id)
        return user.userprofile.full_name
    except User.DoesNotExist:
        return f"Unknown User ({user_id})"

@register.simple_tag
def get_reviewer_role(user):
    """Get primary role of a reviewer."""
    role_hierarchy = [
        'OSAR',
        'IRB Head',
        'Research Council Head',
        'AHARPP Head',
        'IRB Member',
        'Research Council Member',
        'AHARPP Reviewer'
    ]
    
    for role in role_hierarchy:
        if user.groups.filter(name=role).exists():
            return role
    return 'Unknown Role'

@register.filter
def timesince_in_days(value):
    if not value:
        return 0
    
    if isinstance(value, str):
        value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    
    now = timezone.now()
    diff = now - value
    return diff.days

@register.filter
def intersect(queryset1, queryset2):
    return set(queryset1) & set(queryset2)

@register.filter
def split_string(value, delimiter=','):
    """
    Split a string into a list using the specified delimiter.
    Usage: {{ "a,b,c"|split_string:"," }}
    """
    return value.split(delimiter)

# Contents from: .\tests\__init__.py


# Contents from: .\tests\test_forms.py
from django.test import TestCase
from django.contrib.auth.models import User, Group
from forms_builder.models import DynamicForm
from review.forms import ReviewRequestForm, ConflictOfInterestForm
from django.utils import timezone
from datetime import timedelta

class ReviewFormTests(TestCase):
    def setUp(self):
        self.reviewer = User.objects.create_user('reviewer', 'reviewer@test.com', 'password123')
        self.irb_group = Group.objects.create(name='IRB Member')
        self.reviewer.groups.add(self.irb_group)
        self.test_form = DynamicForm.objects.create(
            name='Test Form',
            description='Test form'
        )

    def test_review_request_form_validation(self):
        form_data = {
            'requested_to': self.reviewer.id,
            'message': 'Please review',
            'deadline': (timezone.now() + timedelta(days=7)).date(),
            'selected_forms': [self.test_form.id],
            'submission_version': 1
        }
        form = ReviewRequestForm(data=form_data)
        self.assertTrue(form.is_valid()) 

# Contents from: .\tests\test_models.py
from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.utils import timezone
from datetime import timedelta
from submission.models import Submission, VersionHistory
from forms_builder.models import DynamicForm, StudyType
from review.models import ReviewRequest, Review

class ReviewModelTests(TestCase):
    def setUp(self):
        # Create test users
        self.reviewer = User.objects.create_user('reviewer', 'reviewer@test.com', 'password123')
        self.admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'password123')
        
        # Create IRB Member group
        self.irb_group = Group.objects.create(name='IRB Member')
        self.reviewer.groups.add(self.irb_group)
        
        # Create test study type and submission
        self.study_type = StudyType.objects.create(name='Test Study')
        self.submission = Submission.objects.create(
            title='Test Submission',
            primary_investigator=self.admin_user,
            study_type=self.study_type,
            status='submitted',
            version=1
        )

    def test_review_request_creation(self):
        review_request = ReviewRequest.objects.create(
            submission=self.submission,
            requested_by=self.admin_user,
            requested_to=self.reviewer,
            submission_version=1,
            deadline=timezone.now().date() + timedelta(days=7),
            status='pending'
        )
        self.assertEqual(review_request.submission_version, 1)
        self.assertEqual(review_request.status, 'pending')

    def test_review_creation(self):
        review_request = ReviewRequest.objects.create(
            submission=self.submission,
            requested_by=self.admin_user,
            requested_to=self.reviewer,
            submission_version=1,
            deadline=timezone.now().date() + timedelta(days=7),
            status='pending'
        )
        
        review = Review.objects.create(
            review_request=review_request,
            reviewer=self.reviewer,
            submission=self.submission,
            submission_version=1,
            comments='Test review comments'
        )
        
        self.assertEqual(review.submission_version, 1)
        self.assertEqual(review.reviewer, self.reviewer)

# Contents from: .\tests\test_pdf_generator.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from io import BytesIO
from django.db.models.signals import post_save
from django.test.utils import override_settings
from ..models import Review, ReviewRequest, Submission
from ..utils.pdf_generator import generate_review_dashboard_pdf
from submission.models import StudyType
from users.models import UserProfile
from users.signals import create_user_profile  # Import the signal handler

class PDFGeneratorTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Disconnect the signal temporarily
        post_save.disconnect(create_user_profile, sender=User)

        try:
            # Create test users without triggering signals
            cls.user = User.objects.create(
                username='testuser',
                email='test@example.com',
            )
            cls.pi_user = User.objects.create(
                username='pi_user',
                email='pi@example.com',
            )
            
            # Create user profiles manually
            UserProfile.objects.create(
                user=cls.user,
                full_name="Test User"
            )
            UserProfile.objects.create(
                user=cls.pi_user,
                full_name="PI User"
            )

            # Create study type
            cls.study_type = StudyType.objects.create(
                name="Test Study",
                description="Test Study Description"
            )

            # Create test submission
            cls.submission = Submission.objects.create(
                title="Test Submission",
                primary_investigator=cls.pi_user,
                study_type=cls.study_type,
                version=1
            )

        finally:
            # Reconnect the signal
            post_save.connect(create_user_profile, sender=User)

    def setUp(self):
        # Create review requests
        self.pending_review = ReviewRequest.objects.create(
            submission=self.submission,
            submission_version=1,
            requested_by=self.pi_user,
            requested_to=self.user,
            deadline=timezone.now().date() + timedelta(days=7),
            status='pending'
        )

        self.completed_review = ReviewRequest.objects.create(
            submission=self.submission,
            submission_version=1,
            requested_by=self.pi_user,
            requested_to=self.user,
            deadline=timezone.now().date() - timedelta(days=7),
            status='completed'
        )

        # Create completed review
        self.review = Review.objects.create(
            review_request=self.completed_review,
            reviewer=self.user,
            submission=self.submission,
            submission_version=1,
            date_submitted=timezone.now()
        )

    def test_generate_pdf_as_buffer(self):
        """Test PDF generation returns a BytesIO buffer"""
        pending_reviews = ReviewRequest.objects.filter(status='pending')
        completed_reviews = Review.objects.all()
        
        pdf_buffer = generate_review_dashboard_pdf(
            pending_reviews,
            completed_reviews,
            self.user,
            as_buffer=True
        )
        
        self.assertIsInstance(pdf_buffer, BytesIO)
        pdf_content = pdf_buffer.getvalue()
        self.assertTrue(pdf_content.startswith(b'%PDF'))

    def test_generate_pdf_as_response(self):
        """Test PDF generation returns an HTTP response"""
        pending_reviews = ReviewRequest.objects.filter(status='pending')
        completed_reviews = Review.objects.all()
        
        response = generate_review_dashboard_pdf(
            pending_reviews,
            completed_reviews,
            self.user,
            as_buffer=False
        )
        
        # Check response properties
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertEqual(
            response['Content-Disposition'],
            'attachment; filename="review_dashboard.pdf"'
        )
        self.assertTrue(response.content.startswith(b'%PDF'))

    def test_pdf_content_structure(self):
        """Test the structure of generated PDF content"""
        pending_reviews = ReviewRequest.objects.filter(status='pending')
        completed_reviews = Review.objects.all()
        
        pdf_buffer = generate_review_dashboard_pdf(
            pending_reviews,
            completed_reviews,
            self.user,
            as_buffer=True
        )
        
        # Convert PDF to text for content checking
        pdf_content = pdf_buffer.getvalue()
        
        # Basic size check
        self.assertGreater(len(pdf_content), 100)  # PDF should have reasonable size

    def test_empty_reviews(self):
        """Test PDF generation with empty review sets"""
        pending_reviews = ReviewRequest.objects.none()
        completed_reviews = Review.objects.none()
        
        pdf_buffer = generate_review_dashboard_pdf(
            pending_reviews,
            completed_reviews,
            self.user,
            as_buffer=True
        )
        
        # Check if PDF is still generated
        self.assertIsInstance(pdf_buffer, BytesIO)
        pdf_content = pdf_buffer.getvalue()
        self.assertTrue(pdf_content.startswith(b'%PDF')) 

# Contents from: .\tests\test_views.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission, Group
from django.utils import timezone
from datetime import timedelta
from submission.models import Submission, VersionHistory
from forms_builder.models import DynamicForm, StudyType
from review.models import ReviewRequest, Review

class ReviewViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test users
        self.reviewer = User.objects.create_user('reviewer', 'reviewer@test.com', 'password123')
        self.admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'password123')
        
        # Create IRB Member group
        self.irb_group = Group.objects.create(name='IRB Member')
        self.reviewer.groups.add(self.irb_group)
        
        # Create test study type and submission
        self.study_type = StudyType.objects.create(name='Test Study')
        self.submission = Submission.objects.create(
            title='Test Submission',
            primary_investigator=self.admin_user,
            study_type=self.study_type,
            status='submitted',
            version=1
        )

    def test_review_dashboard_view(self):
        self.client.login(username='reviewer', password='password123')
        response = self.client.get(reverse('review:review_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_create_review_request_view(self):
        self.client.login(username='admin', password='password123')
        response = self.client.get(
            reverse('review:create_review_request', 
            args=[self.submission.pk])
        )
        self.assertEqual(response.status_code, 200) 

# Contents from: .\urls.py
from django.urls import path
from .views import (
    ReviewDashboardView,
    ReviewSummaryView,
    SubmissionVersionsView,
    ToggleSubmissionVisibilityView,
    UpdateSubmissionStatusView,
    AssignKHCCNumberView,
    ProcessSubmissionDecisionView,
    view_notepad,
    CreateReviewRequestView,
    SubmitReviewView,
    ViewReviewView,
    RequestExtensionView,
    DeclineReviewView,
    download_review_pdf,
    download_action_pdf,
    QualityDashboardView,
    get_dashboard_data,
    check_notes_status,
    process_action,
)
from submission.views import user_autocomplete

app_name = 'review'

urlpatterns = [
    # Single dashboard URL
    path('', ReviewDashboardView.as_view(), name='review_dashboard'),
    
    # Submission Management URLs
    path('submission/<int:submission_id>/summary/', 
         ReviewSummaryView.as_view(), 
         name='review_summary'),
    path('submission/<int:submission_id>/versions/', 
         SubmissionVersionsView.as_view(), 
         name='submission_versions'),
    path('submission/<int:submission_id>/toggle-visibility/', 
         ToggleSubmissionVisibilityView.as_view(), 
         name='toggle_visibility'),
    path('submission/<int:submission_id>/update-status/', 
         UpdateSubmissionStatusView.as_view(), 
         name='update_status'),
    path('submission/<int:submission_id>/assign-irb/', 
         AssignKHCCNumberView.as_view(), 
         name='assign_irb'),
    path('submission/<int:submission_id>/process-decision/', 
         ProcessSubmissionDecisionView.as_view(), 
         name='process_submission_decision'),
    path('submission/<int:submission_id>/notepad/<str:notepad_type>/', 
         view_notepad, 
         name='view_notepad'),

    # Review Process URLs
    path('create/<int:submission_id>/', 
         CreateReviewRequestView.as_view(), 
         name='create_review_request'),
    path('submit/<int:review_request_id>/', 
         SubmitReviewView.as_view(), 
         name='submit_review'),
    path('review/<int:review_request_id>/', 
         ViewReviewView.as_view(), 
         name='view_review'),
    path('review/<int:review_request_id>/extension/', 
         RequestExtensionView.as_view(), 
         name='request_extension'),
    path('review/<int:review_request_id>/decline/', 
         DeclineReviewView.as_view(), 
         name='decline_review'),
    path('review/<int:review_request_id>/pdf/', 
         download_review_pdf, 
         name='download_review_pdf'),
    path('action/<int:action_id>/pdf/', 
         download_action_pdf, 
         name='download_action_pdf'),

    # Utility URLs
    path('user-autocomplete/', 
         user_autocomplete, 
         name='user-autocomplete'),

    path('quality-dashboard/', 
         QualityDashboardView.as_view(), 
         name='quality_dashboard'),  # Notice the underscore
    path('api/dashboard-data/', 
         get_dashboard_data, 
         name='dashboard_data'),
     path('api/notes/<int:submission_id>/<str:notepad_type>/check/',
          check_notes_status,
          name='check_notes_status'),

     path('submission/<int:submission_id>/action/<int:action_id>/process/',
          process_action, 
          name='process_action'),
     ]

# Contents from: .\utils.py
# review/utils.py

from messaging.models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

def send_review_request_notification(review_request):
    sender = review_request.requested_by
    recipient = review_request.requested_to
    submission = review_request.submission
    subject = f"Review Request for '{submission.title}'"
    body = f"""
    Dear {recipient.get_full_name()},

    You have been requested to review the submission titled '{submission.title}' (Version {submission.version}).

    Please log in to the system to proceed with the review.

    Thank you,
    {sender.get_full_name()}
    """

    # Create the message
    message = Message.objects.create(
        sender=sender,
        subject=subject.strip(),
        body=body.strip(),
        related_submission=submission,
    )
    # Add the recipient
    message.recipients.add(recipient)
    message.save()


def send_conflict_of_interest_notification(review_request):
    sender = review_request.requested_to  # The reviewer who declared conflict
    recipient = review_request.requested_by  # The person who requested the review
    submission = review_request.submission
    subject = f"Conflict of Interest Declared for '{submission.title}'"
    body = f"""
    Dear {recipient.get_full_name()},

    The reviewer {sender.get_full_name()} has declared a conflict of interest for the submission titled '{submission.title}'.

    Please assign a new reviewer.

    Conflict Details:
    {review_request.conflict_of_interest_details or 'No additional details provided.'}

    Thank you,
    {sender.get_full_name()}
    """

    # Create the message
    message = Message.objects.create(
        sender=sender,
        subject=subject.strip(),
        body=body.strip(),
        related_submission=submission,
    )
    # Add the recipient
    message.recipients.add(recipient)
    message.save()


def send_review_completion_notification(review_request):
    sender = review_request.requested_to  # The reviewer
    recipient = review_request.requested_by  # The person who requested the review
    submission = review_request.submission
    subject = f"Review Completed for '{submission.title}'"
    body = f"""
    Dear {recipient.get_full_name()},

    The review for the submission titled '{submission.title}' has been completed by {sender.get_full_name()}.

    You can view the review by logging into the system.

    Thank you,
    {sender.get_full_name()}
    """

    # Create the message
    message = Message.objects.create(
        sender=sender,
        subject=subject.strip(),
        body=body.strip(),
        related_submission=submission,
    )
    # Add the recipient
    message.recipients.add(recipient)
    message.save()


def send_decision_notification(submission, action, comments, decided_by):
    """Send notification about submission decision."""
    system_user = get_system_user()
    action_display = action.replace('_', ' ').title()
    
    message_content = f"""
    Your submission "{submission.title}" has been {action_display}.
    
    Decision made by: {decided_by.get_full_name() or decided_by.username}
    Comments: {comments}
    """
    
    # Get all users who need to be notified
    users_to_notify = set([submission.primary_investigator])
    users_to_notify.update(
        submission.research_assistants.filter(can_submit=True).values_list('user', flat=True)
    )
    users_to_notify.update(
        submission.coinvestigators.filter(can_submit=True).values_list('user', flat=True)
    )
    
    # Send notification to each user
    for user in users_to_notify:
        Message.objects.create(
            sender=system_user,
            body=message_content,
            subject=f"Submission {action_display} - {submission.title}",
            related_submission=submission
        ).recipients.set([user])


# Contents from: .\utils\__init__.py


# Contents from: .\utils\notifications.py
from django.utils import timezone
from django.core.files.base import ContentFile
from django.utils.text import slugify
from messaging.models import Message, MessageAttachment
from submission.utils.pdf_generator import generate_submission_pdf
from review.utils.pdf_generator import generate_review_pdf
from users.utils import get_system_user
from django.template.loader import render_to_string


def send_review_request_notification(review_request):
    """Create notification message for new review requests."""
    submission_title = review_request.submission.title
    requester_name = review_request.requested_by.get_full_name()
    reviewer_name = review_request.requested_to.get_full_name()

    # Generate PDF of submission with the current version
    pdf_buffer = generate_submission_pdf(
        submission=review_request.submission,
        version=review_request.submission_version,  # Use the version from review request
        user=get_system_user(),  # Use system user for PDF generation
        as_buffer=True
    )

    message = Message.objects.create(
        sender=get_system_user(),
        subject=f'New Review Request - {submission_title}',
        body=f"""
Dear {reviewer_name},

You have received a new review request.

Submission: {submission_title}
Requested by: {requester_name}
Deadline: {review_request.deadline}

Please find the submission details attached to this message. Log in to the system to submit your review.

Best regards,
iRN System
        """.strip(),
        # study_name=submission_title,
        related_submission=review_request.submission
    )

    # Add recipient
    message.recipients.add(review_request.requested_to)

    # Add CC recipient
    message.cc.add(review_request.requested_by)

    if pdf_buffer:
        try:
            # Create PDF attachment
            submission_title_slug = slugify(submission_title)
            date_str = timezone.now().strftime('%Y_%m_%d')
            filename = f"submission_{submission_title_slug}_{date_str}.pdf"

            MessageAttachment.objects.create(
                message=message,
                file=ContentFile(pdf_buffer.getvalue(), name=filename),
                filename=filename
            )
        finally:
            pdf_buffer.close()

    return message


def send_review_decline_notification(review_request, decliner, reason):
    """Create notification message for declined reviews."""
    message = Message.objects.create(
        sender=get_system_user(),
        subject=f'Review Request Declined - {review_request.submission.title}',
        body=render_to_string('review/decline_notification_email.txt', {
            'requested_by': review_request.requested_by.userprofile.full_name,
            'submission_title': review_request.submission.title,
            'decliner': decliner.userprofile.full_name,
            'reason': reason,
        }),
        # study_name=review_request.submission.title,
        related_submission=review_request.submission
    )
    message.recipients.add(review_request.requested_by)
    return message


def send_extension_request_notification(review_request, new_deadline_date, reason, requester):
    """Create notification message for extension requests."""
    extension_days = (new_deadline_date - review_request.deadline).days
    
    message = Message.objects.create(
        sender=requester,
        subject=f'Extension Request for Review #{review_request.id}',
        body=f"""
Extension Request Details:
-------------------------
Review: {review_request.submission.title}
Current Deadline: {review_request.deadline}
Requested New Deadline: {new_deadline_date}
Extension Days: {extension_days} days
Reason: {reason}

Please review this request and respond accordingly.
        """.strip(),
        # study_name=review_request.submission.title,
        related_submission=review_request.submission
    )
    message.recipients.add(review_request.requested_by)
    return message


def send_review_completion_notification(review, review_request, pdf_buffer):
    """Create notification message for completed reviews."""
    submission_title = review_request.submission.title
    reviewer_name = review.reviewer.get_full_name()
    
    message = Message.objects.create(
        sender=get_system_user(),
        subject=f'Review Completed - {submission_title}',
        body=f"""
Dear {review_request.requested_by.userprofile.full_name},

A review has been completed for this submission.

Submission: {submission_title}
Reviewer: {reviewer_name}
Date Completed: {timezone.now().strftime('%Y-%m-%d %H:%M')}

Please find the detailed review report attached to this message.

Best regards,
iRN System
        """.strip(),
        # study_name=submission_title,
        related_submission=review_request.submission
    )
    
    # Add recipients
    message.recipients.add(review_request.requested_by)
    message.cc.add(review_request.requested_to)
    
    if pdf_buffer:
        # Create PDF attachment
        submission_title_slug = slugify(submission_title)
        reviewer_name_slug = slugify(reviewer_name)
        date_str = timezone.now().strftime('%Y_%m_%d')
        filename = f"review_{submission_title_slug}_{reviewer_name_slug}_{date_str}.pdf"
        
        MessageAttachment.objects.create(
            message=message,
            file=ContentFile(pdf_buffer.getvalue(), name=filename),
            filename=filename
        )
    
    return message



def send_irb_decision_notification(submission, decision, comments):
    system_user = get_system_user()
    decision_display = decision.replace('_', ' ').title()
    
    instructions = {
        'revision_requested': 'Please review the comments and submit a revised version.',
        'accepted': 'Congratulations! Your submission has been accepted.',
        'rejected': 'If you have any questions, please contact the OSAR office.'
    }.get(decision, '')

    # Decision record message
    decision_msg = Message.objects.create(
        sender=system_user,
        subject=f'Submission Decision - {decision_display}',
        body=comments,
        message_type='decision',
        related_submission=submission
    )
    decision_msg.recipients.add(submission.primary_investigator)

    # Notification message 
    notif_body = f"""Dear {submission.primary_investigator.userprofile.full_name},

The OSAR office has made a decision regarding your submission "{submission.title}".

Decision: {decision_display}

Comments:
{comments if comments else 'No additional comments provided.'}

{instructions}

Best regards,
AIDI System""".strip()

    notification = Message.objects.create(
        sender=system_user,
        subject=f'Notification: {submission.title} - {decision_display}',
        body=notif_body,
        message_type='notification', 
        related_submission=submission
    )

    notification.recipients.add(submission.primary_investigator)
    if research_team := submission.get_research_team():
        notification.cc.add(*research_team)

    return decision_msg, notification

# Contents from: .\utils\pdf_generator.py
# review/utils/pdf_generator.py

from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from submission.models import FormDataEntry, StudyAction  # Add this import
from review.models import FormResponse
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, 
    TableStyle, PageBreak
)
from reportlab.lib.utils import simpleSplit
from io import BytesIO
import logging
import json

logger = logging.getLogger(__name__)

class PDFGenerator:
    """Base PDF Generator class with common functionality"""
    def __init__(self, buffer, submission, version, user):
        """Initialize the PDF generator with basic settings"""
        self.buffer = buffer
        self.submission = submission
        self.version = version
        self.user = user
        self.canvas = canvas.Canvas(buffer, pagesize=letter)
        self.y = 750  # Starting y position
        self.line_height = 20
        self.page_width = letter[0]
        self.left_margin = 100
        self.right_margin = 500
        self.min_y = 100  # Minimum y position before new page

    def add_header(self):
        """Add header to the current page"""
        self.canvas.setFont("Helvetica-Bold", 16)
        self.canvas.drawString(self.left_margin, self.y, "Intelligent Research Navigator (iRN) Report")
        self.y -= self.line_height * 1.5
        
        self.canvas.setFont("Helvetica-Bold", 14)
        self.canvas.drawString(self.left_margin, self.y, f"{self.submission.title} - Version {self.version}")
        self.y -= self.line_height * 1.5

    def add_footer(self):
        """Add footer to the current page"""
        footer_text = (
            "iRN is a property of the Artificial Intelligence and Data Innovation (AIDI) office "
            "in collaboration with the Office of Scientific Affairs (OSAR) office @ King Hussein "
            "Cancer Center, Amman - Jordan. Keep this document confidential."
        )
        
        self.canvas.setFont("Helvetica", 8)
        text_object = self.canvas.beginText()
        text_object.setTextOrigin(self.left_margin, 50)
        
        wrapped_text = simpleSplit(footer_text, "Helvetica", 8, self.right_margin - self.left_margin)
        for line in wrapped_text:
            text_object.textLine(line)
        
        self.canvas.drawText(text_object)

    def check_page_break(self):
        """Check if we need a new page and create one if necessary"""
        if self.y < self.min_y:
            self.add_footer()
            self.canvas.showPage()
            self.y = 750
            self.add_header()
            return True
        return False

    def write_wrapped_text(self, text, x_offset=0, bold=False):
        """Write text with word wrapping"""
        if bold:
            self.canvas.setFont("Helvetica-Bold", 10)
        else:
            self.canvas.setFont("Helvetica", 10)
            
        wrapped_text = simpleSplit(str(text), "Helvetica", 10, self.right_margin - (self.left_margin + x_offset))
        for line in wrapped_text:
            self.check_page_break()
            self.canvas.drawString(self.left_margin + x_offset, self.y, line)
            self.y -= self.line_height

    def add_section_header(self, text):
        """Add a section header"""
        self.check_page_break()
        self.y -= self.line_height
        self.canvas.setFont("Helvetica-Bold", 12)
        self.canvas.drawString(self.left_margin, self.y, text)
        self.y -= self.line_height

    def format_field_value(self, value):
        """Format field value, handling special cases like JSON arrays"""
        if value is None:
            return "Not provided"
            
        if isinstance(value, str):
            if value.strip() == "":
                return "Not provided"
            if value.startswith('['):
                try:
                    value_list = json.loads(value)
                    return ", ".join(str(v) for v in value_list)
                except json.JSONDecodeError:
                    return value
        
        return str(value)

class ReviewPDFGenerator(PDFGenerator):
    def __init__(self, buffer, review, submission, form_responses):
        """Initialize the PDF generator for reviews"""
        super().__init__(buffer, submission, review.submission_version, review.reviewer)
        self.review = review
        self.form_responses = form_responses

    def add_header(self):
        """Override header for review PDFs"""
        self.canvas.setFont("Helvetica-Bold", 16)
        self.canvas.drawString(self.left_margin, self.y, "Intelligent Research Navigator (iRN) Review Report")
        self.y -= self.line_height * 1.5
        
        self.canvas.setFont("Helvetica-Bold", 14)
        self.canvas.drawString(self.left_margin, self.y, f"Review for: {self.submission.title}")
        self.y -= self.line_height * 1.5
        
        self.canvas.setFont("Helvetica", 10)
        self.canvas.drawString(self.left_margin, self.y, f"Date of printing: {timezone.now().strftime('%Y-%m-%d %H:%M')}")
        self.y -= self.line_height
        self.canvas.drawString(self.left_margin, self.y, f"Reviewer: {self.review.reviewer.get_full_name()}")
        self.y -= self.line_height * 2

    def add_review_info(self):
        """Add basic review information"""
        self.add_section_header("Review Information")
        
        review_info = [
            f"Submission ID: {self.submission.temporary_id}",
            f"Submission Version: {self.review.submission_version}",
            f"Review Status: {self.review.review_request.get_status_display()}",
            f"Date Submitted: {self.review.date_submitted.strftime('%Y-%m-%d') if self.review.date_submitted else 'Not submitted'}",
            f"Reviewer: {self.review.reviewer.get_full_name()}",
            f"Requested By: {self.review.review_request.requested_by.get_full_name()}"
        ]

        for info in review_info:
            self.write_wrapped_text(info)

    def add_form_responses(self):
        """Add form responses"""
        for response in self.form_responses:
            self.add_section_header(f"Form: {response.form.name}")
            
            for field_name, field_value in response.response_data.items():
                formatted_value = self.format_field_value(field_value)
                self.write_wrapped_text(f"{field_name}:", bold=True)
                self.write_wrapped_text(formatted_value, x_offset=20)
                self.y -= self.line_height/2

    def add_comments(self):
        """Add reviewer comments"""
        if self.review.comments:
            self.add_section_header("Additional Comments")
            self.write_wrapped_text(self.review.comments)

    def generate(self):
        """Generate the complete PDF"""
        try:
            self.add_header()
            self.add_review_info()
            self.add_form_responses()
            self.add_comments()
            self.add_footer()
            self.canvas.save()
        except Exception as e:
            logger.error(f"Error generating review PDF: {str(e)}")
            logger.error("PDF generation error details:", exc_info=True)
            raise

def generate_review_pdf(review, submission, form_responses, as_buffer=False):
    """Generate PDF for a review"""
    try:
        logger.info(f"Generating PDF for review of submission {submission.temporary_id}")
        
        buffer = BytesIO()
        pdf_generator = ReviewPDFGenerator(buffer, review, submission, form_responses)
        pdf_generator.generate()
        
        if as_buffer:
            buffer.seek(0)
            return buffer
            
        buffer.seek(0)
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        filename = f"review_{submission.temporary_id}_v{review.submission_version}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
            
    except Exception as e:
        logger.error(f"Error generating review PDF: {str(e)}")
        logger.error("PDF generation error details:", exc_info=True)
        return None
    

class ActionPDFGenerator(PDFGenerator):
    def __init__(self, buffer, action, submission, form_responses):
        """Initialize PDF generator for study actions"""
        self.action = action
        super().__init__(buffer, submission, action.version, action.performed_by)
        self.form_responses = form_responses

    def add_header(self):
        """Override header for action PDFs"""
        self.canvas.setFont("Helvetica-Bold", 16)
        self.canvas.drawString(self.left_margin, self.y, "Intelligent Research Navigator (iRN) Study Action Report")
        self.y -= self.line_height * 1.5
        
        self.canvas.setFont("Helvetica-Bold", 14)
        self.canvas.drawString(self.left_margin, self.y, f"{self.action.get_action_type_display()}: {self.submission.title}")
        self.y -= self.line_height * 1.5
        
        self.canvas.setFont("Helvetica", 10)
        self.canvas.drawString(self.left_margin, self.y, f"Date of printing: {timezone.now().strftime('%Y-%m-%d %H:%M')}")
        self.y -= self.line_height
        self.canvas.drawString(self.left_margin, self.y, f"Performed by: {self.action.performed_by.get_full_name()}")
        self.y -= self.line_height * 2

    def add_study_action_details(self):
        """Add study action details to the PDF"""
        self.add_section_header("Action Details")
        
        action_info = [
            f"Action Type: {self.action.get_action_type_display()}",
            f"Status: {self.action.get_status_display()}",
            f"Date Created: {self.action.date_created.strftime('%Y-%m-%d %H:%M')}",
            f"Performed By: {self.action.performed_by.get_full_name()}",
            f"Version: {self.action.version}",
        ]
        
        if self.action.notes:
            action_info.append(f"Notes: {self.action.notes}")
            
        for info in action_info:
            self.write_wrapped_text(info)
            
        # Add a space after action details
        self.y -= self.line_height

    def add_form_responses(self):
        """Add form responses to the PDF"""
        if not self.form_responses:
            return

        self.add_section_header("Form Responses")
        
        for form_id, data in self.form_responses.items():
            form = data['form']
            self.write_wrapped_text(f"Form: {form.name}", bold=True)
            self.y -= self.line_height/2
            
            for field_name, value in data['fields'].items():
                # Handle JSON values for checkboxes
                try:
                    if isinstance(value, str) and value.startswith('['):
                        value = ', '.join(json.loads(value))
                except (json.JSONDecodeError, TypeError):
                    pass
                
                self.write_wrapped_text(f"{field_name}:", x_offset=20)
                self.write_wrapped_text(str(value), x_offset=40)
                self.y -= self.line_height/2

            self.y -= self.line_height

    def generate(self):
        """Generate the complete PDF for an action"""
        try:
            self.add_header()
            self.add_study_action_details()
            self.add_form_responses()
            self.add_footer()
            self.canvas.save()
        except Exception as e:
            logger.error(f"Error generating action PDF: {str(e)}")
            logger.error("PDF generation error details:", exc_info=True)
            raise

def generate_action_pdf(submission, study_action, form_entries, user, as_buffer=False):
    """Generate PDF for a study action"""
    try:
        logger.info(f"Generating PDF for action {study_action.id} of submission {submission.temporary_id}")
        
        buffer = BytesIO()
        # Create the PDF generator with all required parameters
        pdf_generator = ActionPDFGenerator(
            buffer=buffer,
            action=study_action,
            submission=submission,
            form_responses=form_entries
        )
        
        # Use the generator's methods to create the PDF
        pdf_generator.generate()  # This will call all necessary methods in the right order
        
        if as_buffer:
            buffer.seek(0)
            return buffer
        
        buffer.seek(0)
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        filename = f"study_action_{study_action.get_action_type_display()}_{study_action.date_created.strftime('%Y%m%d')}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
            
    except Exception as e:
        logger.error(f"Error generating action PDF: {str(e)}")
        logger.error("PDF generation error details:", exc_info=True)
        return None

# Contents from: .\views.py
######################
# Imports
######################
from datetime import datetime, timedelta
import json
import logging

from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.db import transaction
from django.db.models import (
    Q, Count, Avg, F, Prefetch
)
from django.db.models.functions import TruncMonth
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.text import slugify
from django.views import View
from django.views.generic import TemplateView, FormView
from django.views.generic.edit import CreateView

from forms_builder.models import DynamicForm
from iRN.constants import SUBMISSION_STATUS_CHOICES
from messaging.models import Message, MessageAttachment
from submission.models import Submission
from submission.utils.pdf_generator import PDFGenerator, generate_submission_pdf
from users.utils import get_system_user


from .forms import ReviewRequestForm
from .models import ReviewRequest, Review, FormResponse, NotepadEntry
from .utils.notifications import (
    send_review_request_notification,
    send_review_decline_notification,
    send_extension_request_notification,
    send_review_completion_notification,
    send_irb_decision_notification
)
# Models
from submission.models import Submission, StudyAction, FormDataEntry  # Import StudyAction from submission.models
from .models import Review, ReviewRequest, NotepadEntry, SubmissionDecision

# Utils
from users.utils import get_system_user
from .utils.notifications import send_irb_decision_notification
######################
# Review Dashboard
# URL: path('', ReviewDashboardView.as_view(), name='review_dashboard'),
######################



class ReviewDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'review/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get user groups
        is_osar = user.groups.filter(name='OSAR').exists()
        is_irb = user.groups.filter(name='IRB').exists()
        is_rc = user.groups.filter(name='RC').exists()

        # Determine group name for notepad
        group_name = 'OSAR' if is_osar else 'IRB' if is_irb else 'RC' if is_rc else 'general'

        # Base queryset for submissions
        base_submission_qs = Submission.objects.select_related(
            'primary_investigator__userprofile',
            'study_type'
        )

        # Filter submissions based on group
        if is_irb:
            submissions = base_submission_qs.filter(show_in_irb=True)
            review_filter = Q(requested_to__groups__name='IRB') | Q(requested_by__groups__name='IRB')
        elif is_rc:
            submissions = base_submission_qs.filter(show_in_rc=True)
            review_filter = Q(requested_to__groups__name='RC') | Q(requested_by__groups__name='RC')
        else:  # OSAR or other users
            submissions = base_submission_qs.all()
            review_filter = Q()

        # Prefetch review requests with filtering
        submissions = submissions.prefetch_related(
            Prefetch(
                'review_requests',
                queryset=ReviewRequest.objects.filter(review_filter).select_related(
                    'requested_to__userprofile',
                    'requested_by__userprofile'
                )
            )
        )

        # Get review requests based on group filter
        review_requests = ReviewRequest.objects.filter(review_filter) if review_filter else ReviewRequest.objects.all()

        # Get pending and completed reviews
        pending_reviews = review_requests.filter(
            requested_to=user,
            status__in=['pending', 'overdue', 'extended']
        ).select_related(
            'submission__primary_investigator__userprofile',
            'requested_by__userprofile'
        )

        completed_reviews = review_requests.filter(
            requested_to=user,
            status='completed'
        ).select_related(
            'submission__primary_investigator__userprofile',
            'requested_by__userprofile'
        )

        # Check for unread notes for each submission
        for submission in submissions:
            submission.has_unread_notes = NotepadEntry.objects.filter(
                submission=submission,
                notepad_type=group_name
            ).exclude(read_by=user).exists()

        context.update({
            'submissions': submissions,
            'is_osar': is_osar,
            'is_irb': is_irb,
            'is_rc': is_rc,
            'group_name': group_name,
            'review_requests': review_requests,
            'pending_reviews': pending_reviews,
            'completed_reviews': completed_reviews,
            'submission_status_choices': SUBMISSION_STATUS_CHOICES,
        })

        return context

class IRBDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'review/irb_dashboard.html'

    def test_func(self):
        return self.request.user.groups.filter(name='IRB').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get submissions marked for IRB review
        irb_submissions = Submission.objects.filter(
            show_in_irb=True
        ).select_related(
            'primary_investigator__userprofile',
            'study_type'
        )
        context['irb_submissions'] = irb_submissions

        # Get IRB-related review requests
        irb_reviews = ReviewRequest.objects.filter(
            Q(requested_to__groups__name='IRB') | Q(requested_by__groups__name='IRB'),
            Q(requested_to=user) | Q(requested_by=user)
        ).select_related(
            'submission__primary_investigator__userprofile',
            'submission__study_type',
            'requested_by',
            'requested_to'
        ).distinct()
        context['irb_reviews'] = irb_reviews

        return context

class RCDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'review/rc_dashboard.html'

    def test_func(self):
        return self.request.user.groups.filter(name='RC').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get submissions marked for RC review
        rc_submissions = Submission.objects.filter(
            show_in_rc=True
        ).select_related(
            'primary_investigator__userprofile',
            'study_type'
        )
        context['rc_submissions'] = rc_submissions

        # Get RC-related review requests
        rc_reviews = ReviewRequest.objects.filter(
            Q(requested_to__groups__name='RC') | Q(requested_by__groups__name='RC'),
            Q(requested_to=user) | Q(requested_by=user)
        ).select_related(
            'submission__primary_investigator__userprofile',
            'submission__study_type',
            'requested_by',
            'requested_to'
        ).distinct()
        context['rc_reviews'] = rc_reviews

        return context

######################
# Create Review Request
# URL: path('create/<int:submission_id>/', CreateReviewRequestView.as_view(), name='create_review_request'),
######################


class CreateReviewRequestView(LoginRequiredMixin, CreateView):
    model = ReviewRequest
    form_class = ReviewRequestForm
    template_name = 'review/create_review_request.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.submission = get_object_or_404(Submission, pk=kwargs['submission_id'])
        if not ReviewRequest.can_create_review_request(request.user):
            raise PermissionDenied("You don't have permission to create review requests.")
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['deadline'] = timezone.now().date() + timezone.timedelta(days=14)
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.submission = get_object_or_404(Submission, pk=self.kwargs['submission_id'])
        kwargs['study_type'] = self.submission.study_type
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submission'] = self.submission
        return context

    def form_valid(self, form):
        try:
            with transaction.atomic():
                # Set review request fields
                self.object = form.save(commit=False)
                self.object.submission = self.submission
                self.object.requested_by = self.request.user
                self.object.submission_version = self.submission.version
                self.object.save()
                form.save_m2m()

                # Update submission status to 'under_review'
                if self.submission.status == 'submitted':
                    self.submission.status = 'under_review'
                    self.submission.save(update_fields=['status'])

                # Generate the absolute URL for the review
                review_url = self.request.build_absolute_uri(
                    reverse('review:submit_review', args=[self.object.id])
                )

                # Create notification message for the reviewer
                message = Message.objects.create(
                    sender=self.request.user,
                    subject=f'Review Request: {self.submission.title}',
                    body=f"""Dear {self.object.requested_to.userprofile.full_name},

You have been requested to review the submission "{self.submission.title}" (Version {self.submission.version}).

Review Details:
- Deadline: {self.object.deadline.strftime('%B %d, %Y')}
- Forms to Complete: {', '.join(form.name for form in self.object.selected_forms.all())}

Message from requester:
{self.object.message if self.object.message else 'No additional message provided.'}

You can access the review directly by clicking the following link:
{review_url}

Alternatively, you can find this review in the "Reviews" section of your dashboard.

Important Deadlines:
- Review Due Date: {self.object.deadline.strftime('%B %d, %Y')}
- Days Remaining: {(self.object.deadline - timezone.now().date()).days} days

Best regards,
{self.request.user.userprofile.full_name}""",
                    related_submission=self.submission,
                )
                
                # Add the reviewer as recipient
                message.recipients.add(self.object.requested_to)
                
                messages.success(self.request, 'Review request created and notification sent successfully.')
                return redirect('review:review_dashboard')

        except Exception as e:
            messages.error(self.request, f'Error creating review request: {str(e)}')
            return super().form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)
######################
# Decline Review
# URL: path('review/<int:review_request_id>/decline/', DeclineReviewView.as_view(), name='decline_review'),
######################

class DeclineReviewView(LoginRequiredMixin, View):
    template_name = 'review/decline_review.html'

    def dispatch(self, request, *args, **kwargs):
        self.review_request = self.get_review_request(kwargs['review_request_id'], request.user)
        if not self.review_request:
            return redirect('review:review_dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'review_request': self.review_request})

    def post(self, request, *args, **kwargs):
        reason = request.POST.get('reason')
        if not reason:
            messages.error(request, "Please provide a reason for declining the review.")
            return redirect('review:decline_review', review_request_id=self.review_request.id)

        try:
            with transaction.atomic():
                self.review_request.status = 'declined'
                self.review_request.conflict_of_interest_declared = True
                self.review_request.conflict_of_interest_details = reason
                self.review_request.save()

                send_review_decline_notification(self.review_request, request.user, reason)
                messages.success(request, "Review request declined successfully.")
                return redirect('review:review_dashboard')
        except Exception as e:
            messages.error(request, f"Error declining review: {str(e)}")
            return redirect('review:decline_review', review_request_id=self.review_request.id)

    def get_review_request(self, review_request_id, user):
        review_request = get_object_or_404(ReviewRequest, pk=review_request_id)
        if user != review_request.requested_to or review_request.status in ['completed', 'declined']:
            messages.error(self.request, "You don't have permission to decline this review.")
            return None
        return review_request


######################
# Request Extension
# URL: path('review/<int:review_id>/extension/', RequestExtensionView.as_view(), name='request_extension'),
######################

class RequestExtensionView(LoginRequiredMixin, FormView):
    template_name = 'review/request_extension.html'

    def get_review_request(self, review_request_id, user):
        review_request = get_object_or_404(ReviewRequest, pk=review_request_id)
        if user != review_request.requested_to or review_request.status not in ['pending', 'overdue', 'extended']:
            messages.error(self.request, "You don't have permission to request an extension for this review.")
            return None
        return review_request

    def dispatch(self, request, *args, **kwargs):
        self.review_request = self.get_review_request(kwargs['review_request_id'], request.user)
        if not self.review_request:
            return redirect('review:review_dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'review_request': self.review_request})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_request'] = self.review_request
        context['min_date'] = (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        context['max_date'] = (timezone.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        return context

    def post(self, request, *args, **kwargs):
        new_deadline = request.POST.get('new_deadline')
        reason = request.POST.get('reason')
        if not new_deadline or not reason:
            messages.error(request, "Please provide all required fields.")
            return self.form_invalid(None)

        try:
            new_deadline_date = timezone.datetime.strptime(new_deadline, '%Y-%m-%d').date()
            if new_deadline_date <= self.review_request.deadline or new_deadline_date <= timezone.now().date():
                raise ValueError("Invalid new deadline.")

            with transaction.atomic():
                send_extension_request_notification(
                    self.review_request,
                    new_deadline_date,
                    reason,
                    request.user
                )

                self.review_request.extension_requested = True
                self.review_request.proposed_deadline = new_deadline_date
                self.review_request.extension_reason = reason
                self.review_request.save()

                messages.success(request, "Extension request submitted successfully.")
                return redirect('review:review_dashboard')
        except ValueError as e:
            messages.error(request, str(e))
            return self.form_invalid(None)


######################
# Submit Review
# URL: path('submit/<int:review_request_id>/', SubmitReviewView.as_view(), name='submit_review'),
######################

class SubmitReviewView(LoginRequiredMixin, View):
    template_name = 'review/submit_review.html'

    def dispatch(self, request, *args, **kwargs):
        self.review_request = get_object_or_404(
            ReviewRequest.objects.select_related(
                'submission',
                'requested_by__userprofile',
                'submission__primary_investigator'
            ),
            pk=kwargs['review_request_id']
        )
        if not self.can_submit_review(request.user, self.review_request):
            raise PermissionDenied("You don't have permission to submit this review.")
        return super().dispatch(request, *args, **kwargs)

    def can_submit_review(self, user, review_request):
        return user == review_request.requested_to and review_request.status in ['pending', 'overdue', 'extended']

    def get(self, request, *args, **kwargs):
        forms_data = self.get_forms_data()
        context = {
            'review_request': self.review_request,
            'forms_data': forms_data,
            'submission': self.review_request.submission,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', '')
        forms_data = self.get_forms_data(request.POST)
        is_valid = all(form_data['form'].is_valid() for form_data in forms_data)

        if not is_valid:
            messages.error(request, "Please correct the errors in the form.")
            context = {
                'review_request': self.review_request,
                'forms_data': forms_data,
                'submission': self.review_request.submission,
            }
            return render(request, self.template_name, context)

        try:
            with transaction.atomic():
                review, _ = Review.objects.get_or_create(
                    review_request=self.review_request,
                    defaults={
                        'reviewer': request.user,
                        'submission': self.review_request.submission,
                        'submission_version': self.review_request.submission_version
                    }
                )

                for form_data in forms_data:
                    form_template = form_data['template']
                    form_instance = form_data['form']
                    response_data = form_instance.cleaned_data

                    FormResponse.objects.update_or_create(
                        review=review,
                        form=form_template,
                        defaults={'response_data': response_data}
                    )

                comments = request.POST.get('comments', '').strip()
                if comments:
                    review.comments = comments

                if action == 'submit':
                    review.is_completed = True
                    review.completed_at = timezone.now()
                    self.review_request.status = 'completed'
                    self.review_request.save()

                    # Generate PDF and send notification
                    pdf_buffer = generate_review_pdf(review, self.review_request.submission, review.formresponse_set.all())
                    if pdf_buffer:
                        send_review_completion_notification(review, self.review_request, pdf_buffer)
                        pdf_buffer.close()

                    messages.success(request, "Review submitted successfully.")
                else:
                    messages.success(request, "Review saved as draft.")

                review.save()
                return redirect('review:review_dashboard')
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
            context = {
                'review_request': self.review_request,
                'forms_data': forms_data,
                'submission': self.review_request.submission,
            }
            return render(request, self.template_name, context)

    def get_forms_data(self, data=None):
        forms_data = []
        for form_template in self.review_request.selected_forms.all():
            DynamicFormClass = self.generate_django_form(form_template)
            form_instance = DynamicFormClass(
                data=data,
                prefix=f'form_{form_template.id}'
            )
            forms_data.append({
                'template': form_template,
                'form': form_instance
            })
        return forms_data

    def generate_django_form(self, form_template):
        form_fields = {}
        field_map = {
            'text': forms.CharField,
            'email': forms.EmailField,
            'tel': forms.CharField,
            'number': forms.IntegerField,
            'date': forms.DateField,
            'textarea': forms.CharField,
            'checkbox': forms.MultipleChoiceField,
            'radio': forms.ChoiceField,
            'select': forms.ChoiceField,
            'choice': forms.MultipleChoiceField,
            'table': forms.CharField,
        }
        for field in form_template.fields.all():
            field_class = field_map.get(field.field_type, forms.CharField)
            field_kwargs = {
                'label': field.displayed_name,
                'required': field.required,
                'help_text': field.help_text,
                'initial': field.default_value,
            }
            if field.field_type in ['checkbox', 'radio', 'select', 'choice']:
                choices = [(choice.strip(), choice.strip())
                           for choice in field.choices.split(',')
                           if choice.strip()] if field.choices else []
                field_kwargs['choices'] = choices
            if field.max_length:
                field_kwargs['max_length'] = field.max_length
            if field.field_type == 'textarea':
                field_kwargs['widget'] = forms.Textarea(attrs={'rows': field.rows})
            form_fields[field.name] = field_class(**field_kwargs)
        return type(f'DynamicForm_{form_template.id}', (forms.Form,), form_fields)


######################
# View Review
# URL: path('review/<int:review_request_id>/', ViewReviewView.as_view(), name='view_review'),
######################

class ViewReviewView(LoginRequiredMixin, TemplateView):
    template_name = 'review/view_review.html'

    def dispatch(self, request, *args, **kwargs):
        # Get the review request using review_request_id from kwargs
        review_request = get_object_or_404(ReviewRequest, id=kwargs['review_request_id'])
        
        # Then get the associated review
        self.review = get_object_or_404(
            Review.objects.select_related(
                'review_request',
                'reviewer__userprofile',
                'submission',
                'submission__primary_investigator'
            ),
            review_request=review_request
        )
        
        if not self.has_permission(request.user, self.review):
            messages.error(request, "You don't have permission to view this review.")
            return redirect('review:review_dashboard')
        return super().dispatch(request, *args, **kwargs)

    def has_permission(self, user, review):
        return user in [
            review.reviewer,
            review.review_request.requested_by,
            review.submission.primary_investigator
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'review': self.review,
            'review_request': self.review.review_request,
            'submission': self.review.submission,
            'reviewer': self.review.reviewer,
            'form_responses': FormResponse.objects.filter(review=self.review)
        })
        return context


######################
# Review Summary
# URL: path('submission/<int:submission_id>/summary/', ReviewSummaryView.as_view(), name='review_summary'),
######################
from django.shortcuts import render, get_object_or_404
from submission.models import Submission, VersionHistory


class ReviewSummaryView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """View for displaying a comprehensive summary of a submission's reviews"""
    template_name = 'review/review_summary.html'

    def setup(self, request, *args, **kwargs):
        """Initialize common attributes used by multiple methods"""
        super().setup(request, *args, **kwargs)
        self.submission = get_object_or_404(Submission, pk=kwargs.get('submission_id'))
        self.is_osar = request.user.groups.filter(name='OSAR').exists()
        self.is_irb = request.user.groups.filter(name='IRB').exists()
        self.is_rc = request.user.groups.filter(name='RC').exists()

    def test_func(self):
        """Verify user permission to access the submission"""
        user = self.request.user
        
        # Check group permissions
        if user.groups.filter(name__in=['OSAR', 'IRB']).exists():
            return True

        # RC members can view submissions in their department
        if user.groups.filter(name='RC').exists():
            return user.userprofile.department == self.submission.primary_investigator.userprofile.department

        # Check direct involvement
        return any([
            user == self.submission.primary_investigator,
            self.submission.coinvestigators.filter(user=user).exists(),
            self.submission.research_assistants.filter(user=user).exists()
        ])

    def handle_no_permission(self):
        """Route users to appropriate dashboard when access is denied"""
        messages.error(self.request, "You don't have permission to view this submission's details.")
        
        if self.is_osar:
            return redirect('review:osar_dashboard')
        elif self.is_rc:
            return redirect('review:rc_dashboard')
        elif self.is_irb:
            return redirect('review:irb_dashboard')
        return redirect('submission:dashboard')

    def get_review_requests(self):
        """Get filtered review requests based on user group"""
        base_query = self.submission.review_requests.select_related(
            'requested_to__userprofile',
            'requested_by__userprofile'
        ).prefetch_related('review_set')

        if self.is_irb:
            return base_query.filter(
                Q(requested_to__groups__name='IRB') |
                Q(requested_by__groups__name='IRB')
            )
        elif self.is_rc:
            return base_query.filter(
                Q(requested_to__groups__name='RC') |
                Q(requested_by__groups__name='RC')
            )
        return base_query.all()

    def get_version_histories(self):
        """Get submission version history"""
        version_histories = list(self.submission.version_histories.all().order_by('-version'))
        for i, version in enumerate(version_histories):
            if i < len(version_histories) - 1:
                version.next_version = version_histories[i + 1].version
            else:
                version.next_version = None
        return version_histories

    def get_user_permissions(self, user):
        """Determine user-specific permissions"""
        return {
            'can_make_decision': self.is_irb,
            'can_download_pdf': True,
            'can_assign_irb': self.is_irb and not self.submission.khcc_number,
            'is_osar': self.is_osar,
            'is_rc': self.is_rc,
            'is_irb': self.is_irb,
            'can_create_review': any([
                user.groups.filter(name=role).exists() 
                for role in ['OSAR', 'IRB', 'RC']
            ])
        }

    def get_submission_stats(self, review_requests):
        """Calculate submission statistics"""
        submission_date = self.submission.date_submitted or timezone.now()
        days_since = (timezone.now().date() - submission_date.date()).days

        return {
            'total_reviews': review_requests.count(),
            'completed_reviews': review_requests.filter(status='completed').count(),
            'pending_reviews': review_requests.filter(status='pending').count(),
            'days_since_submission': max(0, days_since)
        }

    def prepare_context(self):
        """Prepare all context data"""
        review_requests = self.get_review_requests()
        user_permissions = self.get_user_permissions(self.request.user)
        version_histories = self.get_version_histories()

        # Get study actions
        actions = StudyAction.objects.filter(
            submission=self.submission
        ).select_related(
            'performed_by__userprofile'
        ).prefetch_related(
            'documents'
        ).order_by('-date_created')

        # Format actions for template
        formatted_actions = [{
            'id': action.id,
            'action_type': action.get_action_type_display(),
            'performed_by': action.performed_by.get_full_name(),
            'date_created': action.date_created.strftime('%Y-%m-%d %H:%M'),
            'status': action.status,
            'notes': action.notes,
            'pdf_url': reverse('submission:download_action_pdf', kwargs={
                'submission_id': self.submission.temporary_id,
                'action_id': action.id
            }) if action.documents.exists() else None
        } for action in actions]

        return {
            'submission': self.submission,
            'review_requests': review_requests,
            'version_histories': version_histories,
            'stats': self.get_submission_stats(review_requests),
            'has_active_reviews': review_requests.filter(
                status__in=['pending', 'in_progress']
            ).exists(),
            'has_reviews': review_requests.exists(),
            'study_actions': formatted_actions,
            'can_process_actions': self.request.user.groups.filter(
                name__in=['OSAR', 'IRB', 'RC']
            ).exists(),
            'is_osar': self.is_osar,
            'is_irb': self.is_irb,
            'is_rc': self.is_rc,
            **user_permissions
        }

    def get(self, request, *args, **kwargs):
        """Handle GET requests"""
        if not self.test_func():
            return self.handle_no_permission()
        return render(request, self.template_name, self.prepare_context())

    def post(self, request, *args, **kwargs):
        """Handle POST requests for submission decisions"""
        if not self.test_func():
            return self.handle_no_permission()

        action = request.POST.get('action')
        comments = request.POST.get('comments', '').strip()

        if not comments:
            messages.error(request, "Comments are required for making a decision.")
            return redirect('review:review_summary', submission_id=self.submission.pk)

        try:
            with transaction.atomic():
                # Update submission status and lock state
                if action == 'revision_requested':
                    self.submission.status = 'revision_requested'
                    self.submission.is_locked = False
                elif action in ['rejected', 'accepted']:
                    self.submission.status = action
                    self.submission.is_locked = True
                else:
                    messages.error(request, "Invalid action specified.")
                    return redirect('review:review_summary', submission_id=self.submission.pk)

                self.submission.save()
                send_irb_decision_notification(self.submission, action, comments)
                
                messages.success(
                    request,
                    f"Submission successfully marked as {action.replace('_', ' ').title()}"
                )
                
        except Exception as e:
            messages.error(request, f"Error processing decision: {str(e)}")
        
        return redirect('review:review_summary', submission_id=self.submission.pk)
######################
# Process IRB Decision
# URL: path('submission/<int:submission_id>/decision/', ProcessIRBDecisionView.as_view(), name='process_decision'),
######################

class ProcessIRBDecisionView(LoginRequiredMixin, FormView):
    template_name = 'review/process_decision.html'

    def dispatch(self, request, *args, **kwargs):
        self.submission = get_object_or_404(Submission, pk=kwargs['submission_id'])
        if not request.user.groups.filter(name='IRB Coordinator').exists():
            messages.error(request, "You don't have permission to make IRB decisions.")
            return redirect('submission:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        decision = request.POST.get('decision')
        comments = request.POST.get('comments')

        if decision not in ['approved', 'revision_required', 'rejected']:
            messages.error(request, "Invalid decision.")
            return self.form_invalid(None)

        try:
            with transaction.atomic():
                self.submission.status = decision
                self.submission.save()

                send_irb_decision_notification(self.submission, decision, comments)

                messages.success(request, "Decision recorded and PI has been notified.")
                return redirect('review:review_summary', submission_id=self.submission.id)
        except Exception as e:
            messages.error(request, f"Error processing decision: {str(e)}")
            return self.form_invalid(None)


######################
# Submission Versions
# URL: path('submission/<int:submission_id>/versions/', SubmissionVersionsView.as_view(), name='submission_versions'),
######################

class SubmissionVersionsView(LoginRequiredMixin, TemplateView):
    template_name = 'review/submission_versions.html'

    def get(self, request, *args, **kwargs):
        submission = get_object_or_404(Submission, pk=kwargs['submission_id'])
        histories = submission.version_histories.order_by('-version')
        return render(request, self.template_name, {
            'submission': submission,
            'histories': histories,
        })

@login_required
def download_review_pdf(request, review_request_id):
    """Download PDF of a review with proper permission checks"""
    review_request = get_object_or_404(ReviewRequest.objects.select_related(
        'requested_by',
        'requested_to',
        'submission__primary_investigator'
    ), id=review_request_id)
    
    # Check permissions
    user = request.user
    user_groups = user.groups.all()
    
    # Allow access if user:
    # 1. Is the requester
    # 2. Is the reviewer
    # 3. Is in the same group as the requester (OSAR/IRB/RC)
    has_permission = any([
        user == review_request.requested_by,
        user == review_request.requested_to,
        any(group.name in ['OSAR', 'IRB', 'RC'] 
            for group in user_groups 
            if review_request.requested_by.groups.filter(name=group.name).exists())
    ])
    
    if not has_permission:
        raise PermissionDenied("You don't have permission to download this review.")
    
    review = get_object_or_404(
        Review.objects.select_related(
            'review_request',
            'reviewer__userprofile',
            'submission',
            'submission__primary_investigator'
        ),
        review_request=review_request
    )
    
    submission = review.submission
    form_responses = review.formresponse_set.all()
    
    # Create snake_case filename
    submission_title = slugify(submission.title).replace('-', '_')
    reviewer_name = slugify(review.reviewer.get_full_name()).replace('-', '_')
    date_str = datetime.now().strftime('%Y_%m_%d')
    
    filename = f"{submission_title}_{reviewer_name}_{date_str}.pdf"
    
    buffer = generate_review_pdf(review, submission, form_responses)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.write(buffer.getvalue())
    buffer.close()
    
    return response

class UserAutocompleteView(View):
    def get(self, request):
        term = request.GET.get('term', '')
        user_type = request.GET.get('user_type', '')
        
        if len(term) < 2:
            return JsonResponse([], safe=False)
            
        User = get_user_model()
        users = User.objects.filter(
            Q(first_name__icontains=term) | 
            Q(last_name__icontains=term) |
            Q(email__icontains=term)
        )
        
        # Add any additional filtering for reviewers here
        if user_type == 'reviewer':
            users = users.filter(groups__name='Reviewers')
            
        results = [
            {
                'id': user.id,
                'label': f"{user.get_full_name()} ({user.email})"
            }
            for user in users[:10]  # Limit to 10 results
        ]
        
        return JsonResponse(results, safe=False)


######################
# Assign KHCC #
# URL: path('submission/<int:submission_id>/assign-irb/', AssignKHCCNumberView.as_view(), name='assign_irb'),
######################

class AssignKHCCNumberView(LoginRequiredMixin, View):
    template_name = 'review/assign_khcc_number.html'

    def dispatch(self, request, *args, **kwargs):
        # Update permission check to include IRB members
        if not (request.user.groups.filter(name__in=['OSAR', 'IRB']).exists()):
            messages.error(request, "You don't have permission to assign KHCC #s.")
            return redirect('review:review_dashboard')
        
        self.submission = get_object_or_404(Submission, pk=kwargs['submission_id'])
        if self.submission.khcc_number:
            messages.warning(request, "This submission already has a KHCC #.")
            return redirect('review:review_summary', submission_id=self.submission.id)
            
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            'submission': self.submission,
            'suggested_irb': self._generate_khcc_number()
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        khcc_number = request.POST.get('khcc_number', '').strip()
        
        if not khcc_number:
            messages.error(request, "KHCC # is required.")
            return redirect('review:assign_irb', submission_id=self.submission.temporary_id)

        # Check uniqueness
        if Submission.objects.filter(khcc_number=khcc_number).exists():
            messages.error(request, "This KHCC # is already in use. Please try another.")
            return redirect('review:assign_irb', submission_id=self.submission.temporary_id)

        try:
            with transaction.atomic():
                self.submission.khcc_number = khcc_number
                self.submission.save()

                # Get all users who need to be notified
                users_to_notify = set([self.submission.primary_investigator])
                
                # Add research assistants with submit privilege
                users_to_notify.update(
                    self.submission.research_assistants.filter(
                        can_submit=True
                    ).values_list('user', flat=True)
                )
                
                # Add co-investigators with submit privilege
                users_to_notify.update(
                    self.submission.coinvestigators.filter(
                        can_submit=True
                    ).values_list('user', flat=True)
                )

                # Send notification to each user
                system_user = get_system_user()
                message_content = f"""
                An KHCC # has been assigned to the submission "{self.submission.title}".
                KHCC #: {khcc_number}
                """

                for user in users_to_notify:
                    print("Debug - System User:", system_user)
                    print("Debug - Users to notify:", users_to_notify)
                    print("Debug - Message fields available:", [field.name for field in Message._meta.get_fields()])
                    print("Debug - Message content:", message_content)
                    try:
                        print(f"Debug - Creating message for user: {user}")
                        message = Message.objects.create(
                            sender=system_user,
                            body=message_content,
                            subject=f"KHCC # Assigned - {self.submission.title}",
                            related_submission=self.submission
                        )
                        message.recipients.set([user])  # Use set() method for many-to-many relationship
                        print(f"Debug - Message created successfully: {message}")
                    except Exception as e:
                        print(f"Debug - Message creation error: {str(e)}")
                        print(f"Debug - Error type: {type(e)}")
                        raise  # Re-raise the exception to trigger the outer error handling

                messages.success(request, f"KHCC # {khcc_number} has been assigned successfully.")
                return redirect('review:review_summary', submission_id=self.submission.temporary_id)

        except Exception as e:
            messages.error(request, f"Error assigning KHCC #: {str(e)}")
            return redirect('review:assign_irb', submission_id=self.submission.temporary_id)

    def _generate_khcc_number(self):
        """Generate a suggested KHCC # format: YYYY-XXX"""
        year = timezone.now().year
        
        # Get the highest number for this year
        latest_irb = Submission.objects.filter(
            khcc_number__startswith=f"{year}-"
        ).order_by('-khcc_number').first()

        if latest_irb and latest_irb.khcc_number:
            try:
                number = int(latest_irb.khcc_number.split('-')[1]) + 1
            except (IndexError, ValueError):
                number = 1
        else:
            number = 1

        return f"{year}-{number:03d}"

class ToggleSubmissionVisibilityView(LoginRequiredMixin, View):
    def post(self, request, submission_id):
        try:
            submission = get_object_or_404(Submission, temporary_id=submission_id)
            toggle_type = request.POST.get('toggle_type')
            
            if not toggle_type in ['irb', 'rc']:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid toggle type'
                }, status=400)
            
            # Get the previous state to check if we're turning visibility ON
            previous_state = getattr(submission, f'show_in_{toggle_type}', False)
            
            # Toggle the visibility
            if toggle_type == 'irb':
                submission.show_in_irb = not previous_state
                visible = submission.show_in_irb
            else:  # toggle_type == 'rc'
                submission.show_in_rc = not previous_state
                visible = submission.show_in_rc
            
            submission.save(update_fields=[f'show_in_{toggle_type}'])
            
            # Send notification if visibility was turned ON
            if visible and not previous_state:
                from iRN.constants import irb_coordinator, rc_coordinator
                
                # Determine which coordinators to notify
                if toggle_type == 'irb':
                    coordinator_usernames = irb_coordinator
                else:  # toggle_type == 'rc'
                    coordinator_usernames = [rc_coordinator]
                
                # Convert usernames to User objects
                User = get_user_model()
                coordinator_users = User.objects.filter(username__in=coordinator_usernames)
                
                # Create and send notification message
                message = Message.objects.create(
                    sender=get_system_user(),
                    subject=f'New Submission Visible to {toggle_type.upper()}',
                    body=f"""
Dear {toggle_type.upper()} Coordinator,

A new submission has been shared with the {toggle_type.upper()} office:

Title: {submission.title}
Primary Investigator: {submission.primary_investigator.get_full_name()}
KHCC Number: {submission.khcc_number or 'Not assigned'}

You can view this submission in your dashboard.

Best regards,
OSAR
                    """.strip(),
                    related_submission=submission,
                    message_type='visibility'
                )
                
                # Add all coordinators as recipients
                for coordinator in coordinator_users:
                    message.recipients.add(coordinator)
            
            return JsonResponse({
                'status': 'success',
                'visible': visible,
                'message': f'Successfully toggled {toggle_type.upper()} visibility'
            })
            
        except Submission.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Submission not found'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

class UpdateSubmissionStatusView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name__in=['IRB', 'RC', 'OSAR']).exists()

    def post(self, request, submission_id):
        try:
            submission = get_object_or_404(Submission, temporary_id=submission_id)
            new_status = request.POST.get('status')
            
            if not new_status:
                return JsonResponse({
                    'status': 'error',
                    'message': 'New status not provided'
                }, status=400)
            
            # Get available status choices
            valid_statuses = [choice[0] for choice in submission.get_status_choices()]
            
            if new_status not in valid_statuses:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid status'
                }, status=400)
            
            # Update the status
            submission.status = new_status
            submission.save(update_fields=['status'])
            
            return JsonResponse({
                'status': 'success',
                'message': 'Status updated successfully',
                'new_status': new_status
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

  


@login_required
def irb_dashboard(request):
    if not request.user.groups.filter(name='IRB').exists():
        return redirect('review:review_dashboard')
    
    context = {
        'irb_submissions': Submission.objects.filter(
            status='submitted'
        ).select_related(
            'primary_investigator__userprofile'
        ),
        'pending_irb_decisions': Submission.objects.filter(
            status='pending_irb_decision'
        ).select_related(
            'primary_investigator__userprofile'
        ),
        'irb_reviews': ReviewRequest.objects.filter(
            Q(requested_to__groups__name='IRB') | Q(requested_by__groups__name='IRB'),
            Q(requested_to=request.user) | Q(requested_by=request.user)
        ).select_related(
            'submission__primary_investigator__userprofile',
            'requested_by',
            'requested_to'
        ).distinct(),
    }
    return render(request, 'review/irb_dashboard.html', context)

@login_required
def rc_dashboard(request):
    if not request.user.groups.filter(name='RC').exists():
        return redirect('review:review_dashboard')
    
    context = {
        'rc_submissions': Submission.objects.filter(
            status='submitted'
        ).select_related(
            'primary_investigator__userprofile'
        ),
        'department_submissions': Submission.objects.filter(
            primary_investigator__userprofile__department=request.user.userprofile.department
        ).select_related(
            'primary_investigator__userprofile'
        ),
        'rc_reviews': ReviewRequest.objects.filter(
            Q(requested_to__groups__name='RC') | Q(requested_by__groups__name='RC'),
            Q(requested_to=request.user) | Q(requested_by=request.user)
        ).select_related(
            'submission__primary_investigator__userprofile',
            'requested_by',
            'requested_to'
        ).distinct(),
    }
    return render(request, 'review/rc_dashboard.html', context)



@login_required
def osar_dashboard(request):
    if not request.user.groups.filter(name='OSAR').exists():
        return redirect('review:review_dashboard')
    
    context = {
        'osar_submissions': Submission.objects.all().select_related(
            'primary_investigator__userprofile',
            'study_type'
        ),
        'osar_reviews': ReviewRequest.objects.filter(
            Q(requested_to__groups__name='OSAR') | Q(requested_by__groups__name='OSAR'),
            Q(requested_to=request.user) | Q(requested_by=request.user)
        ).select_related(
            'submission__primary_investigator__userprofile',
            'requested_by',
            'requested_to'
        ).distinct(),
        'submission_status_choices': SUBMISSION_STATUS_CHOICES,
    }
    return render(request, 'review/osar_dashboard.html', context)

@login_required
def view_notepad(request, submission_id, notepad_type):
    """
    View function to handle notepad operations (viewing and adding notes).
    Also handles marking notes as read automatically.
    """
    # Check user permissions
    if not request.user.groups.filter(name=notepad_type).exists():
        messages.error(request, f"You don't have permission to view {notepad_type} notepad.")
        return redirect('review:review_dashboard')
    
    # Get submission or return 404
    submission = get_object_or_404(
        Submission.objects.select_related('primary_investigator__userprofile'),
        pk=submission_id
    )
    
    try:
        # Handle POST request (adding new note)
        if request.method == 'POST':
            note_text = request.POST.get('note_text', '').strip()
            if note_text:
                with transaction.atomic():
                    # Create new note
                    note = NotepadEntry.objects.create(
                        submission=submission,
                        notepad_type=notepad_type,
                        text=note_text,
                        created_by=request.user
                    )
                    # Mark as read by creator
                    note.read_by.add(request.user)
                    messages.success(request, 'Note added successfully.')
            else:
                messages.warning(request, 'Note text cannot be empty.')
            return redirect('review:view_notepad', submission_id=submission_id, notepad_type=notepad_type)

        # Handle GET request (viewing notes)
        with transaction.atomic():
            # Get all notes with related data
            notes = NotepadEntry.objects.filter(
                submission=submission,
                notepad_type=notepad_type
            ).select_related(
                'created_by',
                'created_by__userprofile'
            ).prefetch_related(
                'read_by'
            ).order_by('-created_at')

            # Mark all unread notes as read
            unread_notes = notes.exclude(read_by=request.user)
            for note in unread_notes:
                note.read_by.add(request.user)

            # Prepare context
            context = {
                'submission': submission,
                'notes': notes,
                'notepad_type': notepad_type,
                'can_add_notes': True,  # You might want to add additional permission checks here
                'total_notes': notes.count(),
                'unread_count': unread_notes.count()
            }

            return render(request, 'review/view_notepad.html', context)

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('review:review_dashboard')

# views.py
def has_unread_notes(submission_id, notepad_type, user):
    return NotepadEntry.objects.filter(
        submission_id=submission_id,
        notepad_type=notepad_type
    ).exclude(read_by=user).exists()

# In your dashboard view (ReviewDashboardView)
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    # Add check for unread notes for each submission
    for submission in context['submissions']:
        submission.has_unread_notes = has_unread_notes(
            submission.pk, 
            context['group_name'], 
            self.request.user
        )
    
    return context
# review/views.py
class ProcessSubmissionDecisionView(LoginRequiredMixin, View):
    def post(self, request, submission_id):
        try:
            data = json.loads(request.body)
            action = data.get('action')
            comments = data.get('comments', '').strip()
            
            submission = get_object_or_404(Submission, pk=submission_id)
            
            if not comments:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Comments are required'
                }, status=400)
                
            # Update valid actions list
            if action not in ['revision_requested', 'rejected', 'accepted', 'provisional_approval', 'suspended']:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid action'
                }, status=400)

            with transaction.atomic():
                # Update submission status based on action
                if action == 'suspended':
                    if submission.status != 'accepted':
                        return JsonResponse({
                            'status': 'error',
                            'message': 'Only accepted submissions can be suspended'
                        }, status=400)
                    
                    submission.status = 'suspended'
                    submission.is_locked = True
                elif action == 'revision_requested':
                    submission.status = 'revision_requested'
                    submission.is_locked = False
                elif action == 'provisional_approval':
                    submission.status = 'provisional_approval'
                    submission.is_locked = True
                elif action in ['rejected', 'accepted']:
                    submission.status = action
                    submission.is_locked = True

                submission.save()

                # Create decision record
                SubmissionDecision.objects.create(
                    submission=submission,
                    decision=action,
                    comments=comments,
                    decided_by=request.user
                )

                # Send notification
                if action == 'suspended':
                    message = Message.objects.create(
                        sender=get_system_user(),
                        subject=f'Study Suspended - {submission.title}',
                        body=f"""
Dear {submission.primary_investigator.get_full_name()},

Your study "{submission.title}" has been suspended.

Please refer to the OSAR office for further details and instructions on how to proceed.

Comments from the reviewer:
{comments}

Best regards,
Research Administration System
                        """.strip(),
                        related_submission=submission,
                        message_type='decision'
                    )
                    message.recipients.add(submission.primary_investigator)
                else:
                    send_irb_decision_notification(submission, action, comments)

                return JsonResponse({
                    'status': 'success',
                    'message': f'Submission successfully marked as {action.replace("_", " ").title()}'
                })

        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            print(f"Error processing decision: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

# review/views.py

from django.http import JsonResponse
from django.db.models import Count, Avg, F, Q
from django.db.models.functions import TruncMonth, ExtractDay
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from .models import ReviewRequest, Review
from submission.models import Submission, CoInvestigator
from django.contrib.auth.models import User

@login_required
def get_dashboard_data(request):
    """API endpoint for dashboard data"""
    try:
        print("Starting dashboard data fetch...")
        # Calculate date ranges
        now = timezone.now()
        six_months_ago = now - timedelta(days=180)
        
        # Get submissions excluding drafts
        submissions = Submission.objects.exclude(status='draft')
        total_submissions = submissions.count()
        print(f"Total submissions: {total_submissions}")

        # Get active reviewers
        active_reviewers = ReviewRequest.objects.filter(
            status='pending'
        ).values('requested_to').distinct().count()
        print(f"Active reviewers: {active_reviewers}")

        # Get pending reviews
        pending_reviews = ReviewRequest.objects.filter(
            status='pending'
        ).count()
        print(f"Pending reviews: {pending_reviews}")

        # Calculate average review time
        avg_review_time = 0
        completed_reviews = ReviewRequest.objects.filter(status='completed')
        if completed_reviews.exists():
            avg_time = completed_reviews.aggregate(
                avg_time=Avg(F('updated_at') - F('created_at'))
            )['avg_time']
            if avg_time:
                avg_review_time = avg_time.days
        print(f"Average review time: {avg_review_time}")

        # Get monthly submissions trend
        submission_trends = []
        monthly_data = submissions.filter(
            date_submitted__gte=six_months_ago
        ).annotate(
            month=TruncMonth('date_submitted')
        ).values('month').annotate(
            count=Count('temporary_id')
        ).order_by('month')
        
        for item in monthly_data:
            if item['month']:
                submission_trends.append({
                    'month': item['month'].strftime('%b %Y'),
                    'count': item['count']
                })
        print(f"Submission trends: {len(submission_trends)} months")

        # Get status distribution
        status_dist = submissions.values('status').annotate(
            count=Count('temporary_id')
        ).order_by('-count')
        
        status_distribution = [{
            'status': item['status'].replace('_', ' ').title(),
            'count': item['count']
        } for item in status_dist]
        print(f"Status distribution: {len(status_distribution)} statuses")

        # Get institution distribution
        institution_dist = submissions.select_related(
            'primary_investigator__userprofile'
        ).values(
            'primary_investigator__userprofile__institution'
        ).annotate(
            count=Count('temporary_id')
        ).order_by('-count')

        institutions = [{
            'name': item['primary_investigator__userprofile__institution'] or 'Unknown',
            'count': item['count']
        } for item in institution_dist]
        print(f"Institutions: {len(institutions)} institutions")

        # Get roles distribution
        role_dist = submissions.select_related(
            'primary_investigator__userprofile'
        ).values(
            'primary_investigator__userprofile__role'
        ).annotate(
            count=Count('temporary_id')
        ).order_by('-count')

        role_distribution = [{
            'role': item['primary_investigator__userprofile__role'] or 'Unknown',
            'count': item['count']
        } for item in role_dist]
        print(f"Roles: {len(role_distribution)} roles")

        # Calculate IRB and RC review times
        irb_avg_time = 0
        irb_reviews = ReviewRequest.objects.filter(
            requested_to__groups__name='IRB',
            status='completed'
        )
        if irb_reviews.exists():
            irb_time = irb_reviews.aggregate(
                avg_time=Avg(F('updated_at') - F('created_at'))
            )['avg_time']
            if irb_time:
                irb_avg_time = irb_time.days

        rc_avg_time = 0
        rc_reviews = ReviewRequest.objects.filter(
            requested_to__groups__name='RC',
            status='completed'
        )
        if rc_reviews.exists():
            rc_time = rc_reviews.aggregate(
                avg_time=Avg(F('updated_at') - F('created_at'))
            )['avg_time']
            if rc_time:
                rc_avg_time = rc_time.days

        print(f"IRB avg time: {irb_avg_time}, RC avg time: {rc_avg_time}")

        # Get review time distributions
        irb_time_dist = {}
        for review in irb_reviews:
            days = (review.updated_at - review.created_at).days
            irb_time_dist[days] = irb_time_dist.get(days, 0) + 1

        rc_time_dist = {}
        for review in rc_reviews:
            days = (review.updated_at - review.created_at).days
            rc_time_dist[days] = rc_time_dist.get(days, 0) + 1

        response_data = {
            'totalSubmissions': total_submissions,
            'activeReviewers': active_reviewers,
            'avgReviewTime': avg_review_time,
            'pendingReviews': pending_reviews,
            'irbAvgTime': irb_avg_time,
            'rcAvgTime': rc_avg_time,
            'submissionTrends': submission_trends,
            'roleDistribution': role_distribution,
            'institutions': institutions,
            'statusDistribution': status_distribution,
            'irbTimeDistribution': [
                {'days': days, 'count': count}
                for days, count in sorted(irb_time_dist.items())
            ],
            'rcTimeDistribution': [
                {'days': days, 'count': count}
                for days, count in sorted(rc_time_dist.items())
            ]
        }

        print("Sending response data")
        return JsonResponse(response_data)

    except Exception as e:
        import traceback
        print(f"Error in dashboard data: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({
            'error': str(e),
            'submissionTrends': [],
            'statusDistribution': [],
            'roleDistribution': [],
            'institutions': [],
            'irbTimeDistribution': [],
            'rcTimeDistribution': [],
            'totalSubmissions': 0,
            'activeReviewers': 0,
            'avgReviewTime': 0,
            'pendingReviews': 0,
            'irbAvgTime': 0,
            'rcAvgTime': 0
        }, status=500)# review/views.py

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import reverse

class QualityDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'review/dashboard/quality_dashboard.html'

    def test_func(self):
        return self.request.user.groups.filter(
            name__in=['OSAR', 'IRB', 'RC']
        ).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Quality Dashboard',
        })
        return context
    def handle_no_permission(self):
        messages.error(
            self.request, 
            "You don't have permission to view the Quality Dashboard."
        )
        return redirect('review:review_dashboard')

@login_required
def check_notes_status(request, submission_id, notepad_type):
    """API endpoint to check for unread notes"""
    print(f"Debug: checking notes for submission {submission_id} and type {notepad_type}")  # Add this
    try:
        unread_notes = NotepadEntry.objects.filter(
            submission_id=submission_id,
            notepad_type=notepad_type
        ).exclude(read_by=request.user).exists()
        
        print(f"Debug: found unread notes: {unread_notes}")  # Add this
        
        response_data = {
            'hasNewNotes': unread_notes,
            'submissionId': submission_id,
            'notepadType': notepad_type
        }
        print(f"Debug: sending response: {response_data}")  # Add this
        return JsonResponse(response_data)
    except Exception as e:
        print(f"Debug: Error occurred: {str(e)}")  # Add this
        return JsonResponse({
            'error': str(e)
        }, status=500)
    


@login_required 
def process_action(request, submission_id, action_id):
    """Process a study action (approve/reject) with custom message"""
    submission = get_object_or_404(Submission, pk=submission_id)
    action = get_object_or_404(StudyAction, pk=action_id, submission=submission)

    if not request.user.groups.filter(name__in=['OSAR', 'IRB', 'RC']).exists():
        return JsonResponse({
            'status': 'error',
            'message': 'You do not have permission to process actions'
        }, status=403)

    if request.method == 'POST':
        try:
            decision = request.POST.get('decision')
            comments = request.POST.get('comments', '').strip()
            letter_text = request.POST.get('letter_text', '').strip()
            
            if not comments or not letter_text:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Both comments and letter text are required'
                }, status=400)

            with transaction.atomic():
                # Update action status
                action.status = 'completed' if decision == 'approve' else 'cancelled'
                action.notes = comments
                action.save()

                # Get notification recipients
                recipients = [action.performed_by]  # Person who submitted the action
                if action.performed_by != submission.primary_investigator:
                    recipients.append(submission.primary_investigator)

                # Create notification with customized letter
                message = Message.objects.create(
                    sender=get_system_user(),
                    subject=f'Study Action {decision.title()}d - {submission.title}',
                    body=f"""
Dear {action.performed_by.get_full_name()},

Regarding your {action.get_action_type_display()} request for submission "{submission.title}":

{letter_text}

Additional Comments from Reviewer:
{comments}

Action Details:
- Submission ID: {submission.temporary_id}
- Action Type: {action.get_action_type_display()}
- Decision: {decision.title()}
- Processed by: {request.user.get_full_name()}
- Date: {timezone.now().strftime('%Y-%m-%d %H:%M')}

Best regards,
Office of Scientific Affairs and Research (OSAR)
                    """.strip(),
                    related_submission=submission,
                    message_type='decision'
                )
                
                # Add recipients
                for recipient in recipients:
                    message.recipients.add(recipient)

                # If action was approved, process necessary changes
                if decision == 'approve':
                    if action.action_type == 'closure':
                        submission.status = 'closed'
                        submission.is_locked = True
                    elif action.action_type == 'withdrawal':
                        submission.status = 'withdrawn'
                        submission.is_locked = True
                    submission.save()

                return JsonResponse({
                    'status': 'success',
                    'message': f'Action {decision}d successfully'
                })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=400)



def generate_action_pdf(study_action, form_entries, user, submission, as_buffer=False):
    """Generate PDF for a study action"""
    try:
        logger.info(f"Generating PDF for action {study_action.id}")
        
        buffer = BytesIO()
        pdf_generator = PDFGenerator(
            buffer, 
            submission, 
            study_action.version, 
            user
        )
        
        # Add basic submission info
        pdf_generator.add_header()
        pdf_generator.add_basic_info()
        
        # Add action details
        pdf_generator.add_study_action_details(study_action)
        
        # Add form responses if any
        if form_entries:
            pdf_generator.add_dynamic_forms(form_entries)
        
        # Add footer
        pdf_generator.add_footer()
        pdf_generator.canvas.save()
        
        if as_buffer:
            buffer.seek(0)
            return buffer
        
        buffer.seek(0)
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        filename = f"study_action_{study_action.get_action_type_display()}_{study_action.date_created.strftime('%Y%m%d')}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
            
    except Exception as e:
        logger.error(f"Error generating action PDF: {str(e)}")
        logger.error("PDF generation error details:", exc_info=True)
        return None
    

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from submission.models import StudyAction
from .utils.pdf_generator import generate_action_pdf

@login_required
def download_action_pdf(request, action_id):
    """
    View function to generate and download a PDF for a study action.
    """
    # Get the action with related data
    action = get_object_or_404(StudyAction.objects.select_related(
        'submission',
        'performed_by'
    ), pk=action_id)
    
    # Check permissions
    if not request.user.groups.filter(name__in=['OSAR', 'IRB', 'RC']).exists():
        return HttpResponse('Permission denied', status=403)
    
    # Get form entries related to this specific action
    form_entries = FormDataEntry.objects.filter(
        submission=action.submission,
        study_action=action  # This is the key change - filter by study_action
    ).select_related('form')
    
    # Organize form data by form
    form_data = {}
    for entry in form_entries:
        if entry.form_id not in form_data:
            form_data[entry.form_id] = {
                'form': entry.form,
                'fields': {}
            }
        form_data[entry.form_id]['fields'][entry.field_name] = entry.value
    
    # Generate the PDF
    pdf_response = generate_action_pdf(
        submission=action.submission,
        study_action=action,
        form_entries=form_data,
        user=request.user
    )
    
    if pdf_response is None:
        return HttpResponse('Error generating PDF', status=500)
    
    return pdf_response

