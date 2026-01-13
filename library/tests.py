"""
Tests for the library app.

Example test structure for the models.
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from library.models import Author, Book, Member, MemberProfile, Loan, Tag, BookTag


class AuthorModelTest(TestCase):
    """Test cases for Author model."""

    def setUp(self):
        self.author = Author.objects.create(
            name="Isaac Asimov",
            country="USA"
        )

    def test_author_creation(self):
        """Test that an author can be created."""
        self.assertEqual(self.author.name, "Isaac Asimov")
        self.assertEqual(self.author.country, "USA")

    def test_author_string_representation(self):
        """Test __str__ method."""
        self.assertEqual(str(self.author), "Isaac Asimov (USA)")


class BookModelTest(TestCase):
    """Test cases for Book model."""

    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            isbn="123-456-789",
            author=self.author,
            status="AVAILABLE"
        )

    def test_book_creation(self):
        """Test that a book can be created."""
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.author, self.author)

    def test_book_is_available_property(self):
        """Test is_available property."""
        self.assertTrue(self.book.is_available)
        self.book.status = "LOANED"
        self.assertFalse(self.book.is_available)

    def test_book_mark_lost(self):
        """Test mark_lost method."""
        self.book.mark_lost()
        self.book.refresh_from_db()
        self.assertEqual(self.book.status, "LOST")

    def test_isbn_unique(self):
        """Test that ISBN must be unique."""
        with self.assertRaises(Exception):
            Book.objects.create(
                title="Another Book",
                isbn=self.book.isbn,  # Same ISBN
                author=self.author
            )


class MemberModelTest(TestCase):
    """Test cases for Member model."""

    def setUp(self):
        self.member = Member.objects.create(
            full_name="John Doe",
            email="john@example.com"
        )

    def test_member_creation(self):
        """Test that a member can be created."""
        self.assertEqual(self.member.full_name, "John Doe")

    def test_email_unique(self):
        """Test that email must be unique."""
        with self.assertRaises(Exception):
            Member.objects.create(
                full_name="Jane Doe",
                email=self.member.email  # Same email
            )


class LoanModelTest(TestCase):
    """Test cases for Loan model."""

    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            isbn="123-456-789",
            author=self.author
        )
        self.member = Member.objects.create(
            full_name="Test Member",
            email="test@example.com"
        )

    def test_loan_creation(self):
        """Test that a loan can be created."""
        now = timezone.now()
        due = now + timedelta(days=14)
        
        loan = Loan.objects.create(
            book=self.book,
            member=self.member,
            loaned_at=now,
            due_at=due
        )
        
        self.assertEqual(loan.book, self.book)
        self.assertEqual(loan.member, self.member)

    def test_loan_status_change(self):
        """Test that book status changes when loaned."""
        now = timezone.now()
        due = now + timedelta(days=14)
        
        self.assertTrue(self.book.is_available)
        
        Loan.objects.create(
            book=self.book,
            member=self.member,
            loaned_at=now,
            due_at=due
        )
        
        self.book.refresh_from_db()
        self.assertEqual(self.book.status, "LOANED")

    def test_return_book(self):
        """Test return_book method."""
        now = timezone.now()
        due = now + timedelta(days=14)
        
        loan = Loan.objects.create(
            book=self.book,
            member=self.member,
            loaned_at=now,
            due_at=due
        )
        
        loan.return_book()
        
        self.book.refresh_from_db()
        self.assertEqual(self.book.status, "AVAILABLE")
        self.assertIsNotNone(loan.returned_at)

    def test_unique_active_loan_constraint(self):
        """Test that only one active loan per book is allowed."""
        now = timezone.now()
        due = now + timedelta(days=14)
        
        # Create first loan
        loan1 = Loan.objects.create(
            book=self.book,
            member=self.member,
            loaned_at=now,
            due_at=due
        )
        
        # Try to create second active loan (should fail)
        member2 = Member.objects.create(
            full_name="Another Member",
            email="another@example.com"
        )
        
        with self.assertRaises(Exception):
            Loan.objects.create(
                book=self.book,
                member=member2,
                loaned_at=now,
                due_at=due
            )

    def test_loan_validation(self):
        """Test loan.clean() validation."""
        now = timezone.now()
        past = now - timedelta(days=1)  # Before loan date
        
        # Test: due_at before loaned_at should fail
        with self.assertRaises(ValidationError):
            loan = Loan(
                book=self.book,
                member=self.member,
                loaned_at=now,
                due_at=past
            )
            loan.full_clean()

    def test_loaned_book_cannot_be_loaned(self):
        """Test that a loaned book cannot be loaned again."""
        now = timezone.now()
        due = now + timedelta(days=14)
        
        # First loan
        Loan.objects.create(
            book=self.book,
            member=self.member,
            loaned_at=now,
            due_at=due
        )
        
        # Book is now LOANED
        self.book.refresh_from_db()
        self.assertEqual(self.book.status, "LOANED")
        
        # Try to create another loan (should fail in validation)
        member2 = Member.objects.create(
            full_name="Another Member",
            email="another@example.com"
        )
        
        with self.assertRaises(ValidationError):
            loan2 = Loan(
                book=self.book,
                member=member2,
                loaned_at=now,
                due_at=due
            )
            loan2.full_clean()


class MemberProfileModelTest(TestCase):
    """Test cases for MemberProfile model."""

    def setUp(self):
        self.member = Member.objects.create(
            full_name="Test Member",
            email="test@example.com"
        )
        self.profile = MemberProfile.objects.create(
            member=self.member,
            nickname="TestNick",
            risk_level="LOW"
        )

    def test_profile_creation(self):
        """Test that a profile can be created."""
        self.assertEqual(self.profile.member, self.member)
        self.assertEqual(self.profile.nickname, "TestNick")

    def test_profile_cascade_delete(self):
        """Test that profile is deleted when member is deleted."""
        member_id = self.member.id
        self.member.delete()
        
        with self.assertRaises(MemberProfile.DoesNotExist):
            MemberProfile.objects.get(id=self.profile.id)


class BookTagModelTest(TestCase):
    """Test cases for BookTag model (ManyToMany through table)."""

    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            isbn="123-456-789",
            author=self.author
        )
        self.tag = Tag.objects.create(
            name="Fiction",
            description="Fictional works"
        )

    def test_booktag_creation(self):
        """Test that a BookTag relationship can be created."""
        booktag = BookTag.objects.create(
            book=self.book,
            tag=self.tag
        )
        
        self.assertEqual(booktag.book, self.book)
        self.assertEqual(booktag.tag, self.tag)

    def test_booktag_unique_together(self):
        """Test that book-tag combination must be unique."""
        BookTag.objects.create(book=self.book, tag=self.tag)
        
        with self.assertRaises(Exception):
            BookTag.objects.create(book=self.book, tag=self.tag)
