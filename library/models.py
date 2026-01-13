from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Author(models.Model):
    """
    Author model for the Library system.
    Demonstrates basic model with optional field.
    """
    name = models.CharField(max_length=200, help_text="Author's full name")
    country = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Country of origin (optional)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Authors"

    def __str__(self):
        if self.country:
            return f"{self.name} ({self.country})"
        return self.name


class Book(models.Model):
    """
    Book model with Foreign Key relationship to Author.
    Demonstrates ON_DELETE=PROTECT (cannot delete author with books).
    """
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('LOANED', 'Loaned'),
        ('LOST', 'Lost'),
    ]

    title = models.CharField(max_length=300, help_text="Book title")
    isbn = models.CharField(
        max_length=20,
        unique=True,
        help_text="ISBN code (unique)"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,  # Cannot delete author if books exist
        related_name='books',
        help_text="Author of the book"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='AVAILABLE',
        help_text="Current status of the book"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['isbn']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.title} by {self.author.name}"

    @property
    def is_available(self):
        """Check if book is available for lending."""
        return self.status == 'AVAILABLE'

    def mark_lost(self):
        """Mark the book as lost."""
        self.status = 'LOST'
        self.save()


class Member(models.Model):
    """
    Library Member model.
    Demonstrates DateTimeField with auto_now_add.
    """
    full_name = models.CharField(max_length=200, help_text="Member's full name")
    email = models.EmailField(unique=True, help_text="Member's email (unique)")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class Loan(models.Model):
    """
    Loan model linking Book and Member.
    Demonstrates:
    - FK with ON_DELETE=PROTECT (book)
    - FK with ON_DELETE=CASCADE (member)
    - Constraint on unique active loans
    - Model validation in clean()
    """
    book = models.ForeignKey(
        Book,
        on_delete=models.PROTECT,  # Cannot delete book with active loan
        related_name='loans',
        help_text="Book being loaned"
    )
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,  # Loans deleted when member is deleted
        related_name='loans',
        help_text="Member borrowing the book"
    )
    loaned_at = models.DateTimeField(auto_now_add=True)
    due_at = models.DateTimeField(help_text="Expected return date")
    returned_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Actual return date (null if not returned)"
    )

    class Meta:
        ordering = ['-loaned_at']
        constraints = [
            models.UniqueConstraint(
                fields=['book'],
                condition=models.Q(returned_at__isnull=True),
                name='unique_active_loan_per_book',
                violation_error_message='This book already has an active loan'
            ),
        ]

    def __str__(self):
        status = "Active" if not self.returned_at else "Returned"
        return f"{self.book.title} to {self.member.full_name} ({status})"

    def clean(self):
        """Validate loan before saving."""
        # Check if book is available
        if self.book.status != 'AVAILABLE':
            raise ValidationError(
                f"Book '{self.book.title}' is not available (status: {self.book.status})"
            )

        # Check if due_at is after loaned_at
        # Note: loaned_at is auto_now_add, so it may be None during creation
        # Use timezone.now() as fallback for validation
        base_time = self.loaned_at or timezone.now()
        if self.due_at <= base_time:
            raise ValidationError(
                "Due date must be after the loan date"
            )

    def save(self, *args, **kwargs):
        """Save and update book status."""
        self.full_clean()  # Run validations
        if not self.returned_at:
            self.book.status = 'LOANED'
            self.book.save()
        super().save(*args, **kwargs)

    def return_book(self):
        """Record the book return and update status."""
        self.returned_at = timezone.now()
        self.book.status = 'AVAILABLE'
        self.book.save()
        self.save()

    @property
    def is_overdue(self):
        """Check if loan is overdue."""
        if self.returned_at:
            return False
        return timezone.now() > self.due_at


# ============================================================================
# FASE 2: Extended Models (OneToOne, ManyToMany with through)
# ============================================================================


class MemberProfile(models.Model):
    """
    Member profile model demonstrating OneToOne relationship.
    Shows CASCADE deletion: if member is deleted, profile is deleted too.
    """
    RISK_LEVEL_CHOICES = [
        ('LOW', 'Low Risk'),
        ('MED', 'Medium Risk'),
        ('HIGH', 'High Risk'),
    ]

    member = models.OneToOneField(
        Member,
        on_delete=models.CASCADE,
        related_name='profile',
        help_text="Member profile (1:1 relationship, CASCADE deletion)"
    )
    nickname = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Member's nickname (optional)"
    )
    risk_level = models.CharField(
        max_length=10,
        choices=RISK_LEVEL_CHOICES,
        default='LOW',
        help_text="Risk level based on loan history"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Member Profiles"

    def __str__(self):
        nickname_text = f" ({self.nickname})" if self.nickname else ""
        return f"Profile of {self.member.full_name}{nickname_text} - Risk: {self.get_risk_level_display()}"


class Tag(models.Model):
    """
    Tag model for categorizing books.
    Demonstrates ManyToMany relationship through intermediate model.
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="Tag name (e.g., 'Fiction', 'Mystery', 'Science Fiction')"
    )
    description = models.TextField(
        blank=True,
        help_text="Description of the tag"
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class BookTag(models.Model):
    """
    Through model for Book-Tag ManyToMany relationship.
    Shows explicit control over the intermediate table.
    """
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='book_tags',
        help_text="Book being tagged"
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='book_tags',
        help_text="Tag applied to book"
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('book', 'tag')
        ordering = ['book', 'tag']
        verbose_name = "Book Tag"
        verbose_name_plural = "Book Tags"

    def __str__(self):
        return f"{self.book.title} -> {self.tag.name}"
