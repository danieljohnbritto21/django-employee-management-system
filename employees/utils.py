"""
Utility functions for employees app
"""
from django.contrib import messages


def add_form_errors_to_messages(request, form):
    """
    Add all form errors to Django messages for display.
    Reduces code duplication across views.
    
    Args:
        request: The request object
        form: The Django form object with errors
    """
    if not form.errors:
        return
    
    # Add non-field errors
    for error in form.non_field_errors():
        messages.error(request, error)
    
    # Add field-specific errors
    for field, errors in form.errors.items():
        if field != '__all__':  # Skip non-field errors (already added)
            for error in errors:
                messages.error(request, f'{field}: {error}')


def add_success_message(request, message):
    """
    Add a success message to the request.
    
    Args:
        request: The request object
        message: The message string
    """
    messages.success(request, message)


def add_error_message(request, message):
    """
    Add an error message to the request.
    
    Args:
        request: The request object
        message: The message string
    """
    messages.error(request, message)
