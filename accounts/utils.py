"""
Utility functions for accounts app
"""
from django.contrib import messages


def add_form_errors_to_messages(request, form):
    """
    Add all form errors to Django messages for display.
    
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
        if field != '__all__':
            for error in errors:
                messages.error(request, f'{field}: {error}')
