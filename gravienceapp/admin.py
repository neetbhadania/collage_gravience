from django.contrib import admin
from .models import Grievance

@admin.register(Grievance)
class GrievanceAdmin(admin.ModelAdmin):
    # Columns shown in the admin grievance list
    list_display = ('id', 'student_name', 'email', 'subject', 'created_at')

    # Make some fields clickable
    list_display_links = ('student_name', 'subject')

    # Filters on sidebar
    list_filter = ('created_at',)

    # Search box fields
    search_fields = ('student_name', 'email', 'subject', 'description')

    # Arrange fields in the edit page
    fieldsets = (
        ('Student Info', {
            'fields': ('student', 'student_name', 'email')
        }),
        ('Grievance Details', {
            'fields': ('subject', 'description')
        }),
        ('Date Info', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    # Read-only field so it doesn’t change accidentally
    readonly_fields = ('created_at',)

    # Default ordering (latest first)
    ordering = ('-created_at',)

# Customize admin site titles
admin.site.site_header = "Student Grievance Admin Panel"
admin.site.site_title = "Student Grievance Portal"
admin.site.index_title = "Manage Student Grievances"
