"""
Django Admin configuration for the Library app.

Shows how to register models and customize the admin interface.
Good reference for seeing the data and testing relationships.
"""

from django.contrib import admin
from .models import Author, Book, Member, MemberProfile, Loan, Tag, BookTag


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Admin interface for Author model."""
    list_display = ('name', 'country', 'created_at')
    list_filter = ('country', 'created_at')
    search_fields = ('name', 'country')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Author Information', {
            'fields': ('name', 'country')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin interface for Book model."""
    list_display = ('title', 'author', 'isbn', 'status', 'is_available', 'created_at')
    list_filter = ('status', 'author', 'created_at')
    search_fields = ('title', 'isbn', 'author__name')
    readonly_fields = ('created_at', 'is_available')

    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'isbn', 'author', 'status')
        }),
        ('Status', {
            'fields': ('is_available',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_available', 'mark_as_lost']

    def mark_as_available(self, request, queryset):
        """Admin action to mark books as available."""
        updated = queryset.update(status='AVAILABLE')
        self.message_user(request, f'{updated} books marked as available.')

    def mark_as_lost(self, request, queryset):
        """Admin action to mark books as lost."""
        updated = queryset.update(status='LOST')
        self.message_user(request, f'{updated} books marked as lost.')

    mark_as_available.short_description = "Mark selected books as available"
    mark_as_lost.short_description = "Mark selected books as lost"


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """Admin interface for Member model."""
    list_display = ('full_name', 'email', 'joined_at', 'loan_count')
    list_filter = ('joined_at',)
    search_fields = ('full_name', 'email')
    readonly_fields = ('joined_at', 'loan_count')

    fieldsets = (
        ('Member Information', {
            'fields': ('full_name', 'email')
        }),
        ('Statistics', {
            'fields': ('loan_count',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('joined_at',),
            'classes': ('collapse',)
        }),
    )

    def loan_count(self, obj):
        """Display total number of loans for the member."""
        return obj.loans.count()

    loan_count.short_description = "Total Loans"


@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    """Admin interface for MemberProfile model."""
    list_display = ('member', 'nickname', 'risk_level', 'updated_at')
    list_filter = ('risk_level', 'updated_at')
    search_fields = ('member__full_name', 'nickname')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Profile Information', {
            'fields': ('member', 'nickname', 'risk_level')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class BookTagInline(admin.TabularInline):
    """Inline admin for BookTag relationships."""
    model = BookTag
    extra = 1
    readonly_fields = ('added_at',)


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    """Admin interface for Loan model."""
    list_display = ('book', 'member', 'loaned_at', 'due_at', 'is_active', 'is_overdue')
    list_filter = ('loaned_at', 'due_at', 'returned_at')
    search_fields = ('book__title', 'member__full_name')
    readonly_fields = ('loaned_at', 'is_active', 'is_overdue')

    fieldsets = (
        ('Loan Information', {
            'fields': ('book', 'member')
        }),
        ('Dates', {
            'fields': ('loaned_at', 'due_at', 'returned_at')
        }),
        ('Status', {
            'fields': ('is_active', 'is_overdue'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_returned']

    def is_active(self, obj):
        """Show if loan is active (not returned)."""
        return obj.returned_at is None

    is_active.boolean = True
    is_active.short_description = "Is Active"

    def is_overdue(self, obj):
        """Show if loan is overdue."""
        return obj.is_overdue

    is_overdue.boolean = True
    is_overdue.short_description = "Is Overdue"

    def mark_as_returned(self, request, queryset):
        """Admin action to mark loans as returned."""
        count = 0
        for loan in queryset.filter(returned_at__isnull=True):
            loan.return_book()
            count += 1
        self.message_user(request, f'{count} loans marked as returned.')

    mark_as_returned.short_description = "Mark selected loans as returned"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin interface for Tag model."""
    list_display = ('name', 'book_count')
    search_fields = ('name', 'description')
    readonly_fields = ('book_count',)

    fieldsets = (
        ('Tag Information', {
            'fields': ('name', 'description')
        }),
        ('Statistics', {
            'fields': ('book_count',),
            'classes': ('collapse',)
        }),
    )

    def book_count(self, obj):
        """Display number of books with this tag."""
        return obj.book_tags.count()

    book_count.short_description = "Number of Books"


@admin.register(BookTag)
class BookTagAdmin(admin.ModelAdmin):
    """Admin interface for BookTag model (through table)."""
    list_display = ('book', 'tag', 'added_at')
    list_filter = ('tag', 'added_at')
    search_fields = ('book__title', 'tag__name')
    readonly_fields = ('added_at',)

    fieldsets = (
        ('Relationship', {
            'fields': ('book', 'tag')
        }),
        ('Metadata', {
            'fields': ('added_at',),
            'classes': ('collapse',)
        }),
    )
