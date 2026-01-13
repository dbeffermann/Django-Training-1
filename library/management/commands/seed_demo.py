"""
Custom management command to seed demo data into the library database.

Usage:
    python manage.py seed_demo

This command creates:
- 2 Authors
- 4 Books (with FK to authors)
- 2 Members
- 2 Member Profiles (OneToOne)
- 2 Tags
- 4 BookTag relationships (ManyToMany through table)
- 1 Active Loan (today)
- 1 Returned Loan (completed)
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from library.models import Author, Book, Member, MemberProfile, Tag, BookTag, Loan


class Command(BaseCommand):
    help = 'Seeds the database with demo data for the library system'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        # Clear existing data (optional, comment out if you want to append)
        # Loan.objects.all().delete()
        # BookTag.objects.all().delete()
        # MemberProfile.objects.all().delete()
        # Tag.objects.all().delete()
        # Book.objects.all().delete()
        # Member.objects.all().delete()
        # Author.objects.all().delete()

        # =====================
        # 1. Create Authors
        # =====================
        author1, created = Author.objects.get_or_create(
            name="J.K. Rowling",
            defaults={"country": "United Kingdom"}
        )
        if created:
            self.stdout.write(f'  ✓ Created Author: {author1.name}')
        else:
            self.stdout.write(f'  ℹ Author exists: {author1.name}')

        author2, created = Author.objects.get_or_create(
            name="George R.R. Martin",
            defaults={"country": "United States"}
        )
        if created:
            self.stdout.write(f'  ✓ Created Author: {author2.name}')
        else:
            self.stdout.write(f'  ℹ Author exists: {author2.name}')

        # =====================
        # 2. Create Books
        # =====================
        book1, created = Book.objects.get_or_create(
            isbn="978-0439136969",
            defaults={
                "title": "Harry Potter and the Philosopher's Stone",
                "author": author1,
                "status": "AVAILABLE"
            }
        )
        if created:
            self.stdout.write(f'  ✓ Created Book: {book1.title}')
        else:
            self.stdout.write(f'  ℹ Book exists: {book1.title}')

        book2, created = Book.objects.get_or_create(
            isbn="978-0439136983",
            defaults={
                "title": "Harry Potter and the Chamber of Secrets",
                "author": author1,
                "status": "AVAILABLE"
            }
        )
        if created:
            self.stdout.write(f'  ✓ Created Book: {book2.title}')
        else:
            self.stdout.write(f'  ℹ Book exists: {book2.title}')

        book3, created = Book.objects.get_or_create(
            isbn="978-0553103540",
            defaults={
                "title": "A Game of Thrones",
                "author": author2,
                "status": "AVAILABLE"
            }
        )
        if created:
            self.stdout.write(f'  ✓ Created Book: {book3.title}')
        else:
            self.stdout.write(f'  ℹ Book exists: {book3.title}')

        book4, created = Book.objects.get_or_create(
            isbn="978-0553108034",
            defaults={
                "title": "A Clash of Kings",
                "author": author2,
                "status": "AVAILABLE"
            }
        )
        if created:
            self.stdout.write(f'  ✓ Created Book: {book4.title}')
        else:
            self.stdout.write(f'  ℹ Book exists: {book4.title}')

        # =====================
        # 3. Create Members
        # =====================
        member1, created = Member.objects.get_or_create(
            email="alice@example.com",
            defaults={"full_name": "Alice Johnson"}
        )
        if created:
            self.stdout.write(f'  ✓ Created Member: {member1.full_name}')
        else:
            self.stdout.write(f'  ℹ Member exists: {member1.full_name}')

        member2, created = Member.objects.get_or_create(
            email="bob@example.com",
            defaults={"full_name": "Bob Smith"}
        )
        if created:
            self.stdout.write(f'  ✓ Created Member: {member2.full_name}')
        else:
            self.stdout.write(f'  ℹ Member exists: {member2.full_name}')

        # =====================
        # 4. Create Member Profiles (1:1)
        # =====================
        profile1, created = MemberProfile.objects.get_or_create(
            member=member1,
            defaults={
                "nickname": "Ally",
                "risk_level": "LOW"
            }
        )
        if created:
            self.stdout.write(f'  ✓ Created MemberProfile for: {profile1.member.full_name}')
        else:
            self.stdout.write(f'  ℹ MemberProfile exists for: {profile1.member.full_name}')

        profile2, created = MemberProfile.objects.get_or_create(
            member=member2,
            defaults={
                "nickname": "Bobby",
                "risk_level": "MED"
            }
        )
        if created:
            self.stdout.write(f'  ✓ Created MemberProfile for: {profile2.member.full_name}')
        else:
            self.stdout.write(f'  ℹ MemberProfile exists for: {profile2.member.full_name}')

        # =====================
        # 5. Create Tags
        # =====================
        tag1, created = Tag.objects.get_or_create(
            name="Fantasy",
            defaults={"description": "Fantasy and magical worlds"}
        )
        if created:
            self.stdout.write(f'  ✓ Created Tag: {tag1.name}')
        else:
            self.stdout.write(f'  ℹ Tag exists: {tag1.name}')

        tag2, created = Tag.objects.get_or_create(
            name="Epic",
            defaults={"description": "Epic and grand-scale stories"}
        )
        if created:
            self.stdout.write(f'  ✓ Created Tag: {tag2.name}')
        else:
            self.stdout.write(f'  ℹ Tag exists: {tag2.name}')

        # =====================
        # 6. Create BookTag relationships (M2M)
        # =====================
        booktag1, created = BookTag.objects.get_or_create(
            book=book1,
            tag=tag1
        )
        if created:
            self.stdout.write(f'  ✓ Tagged "{book1.title}" with "{tag1.name}"')

        booktag2, created = BookTag.objects.get_or_create(
            book=book2,
            tag=tag1
        )
        if created:
            self.stdout.write(f'  ✓ Tagged "{book2.title}" with "{tag1.name}"')

        booktag3, created = BookTag.objects.get_or_create(
            book=book3,
            tag=tag1
        )
        if created:
            self.stdout.write(f'  ✓ Tagged "{book3.title}" with "{tag1.name}"')

        booktag4, created = BookTag.objects.get_or_create(
            book=book3,
            tag=tag2
        )
        if created:
            self.stdout.write(f'  ✓ Tagged "{book3.title}" with "{tag2.name}"')

        # =====================
        # 7. Create Loans
        # =====================
        # Active Loan (returned_at is NULL)
        now = timezone.now()
        due_date_active = now + timedelta(days=14)

        # Try to create active loan, skip if constraint fails
        try:
            active_loan, created = Loan.objects.get_or_create(
                book=book1,
                member=member1,
                defaults={
                    "loaned_at": now,
                    "due_at": due_date_active,
                    "returned_at": None
                }
            )
            if created:
                self.stdout.write(f'  ✓ Created Active Loan: {book1.title} → {member1.full_name}')
            else:
                self.stdout.write(f'  ℹ Active Loan exists: {book1.title} → {member1.full_name}')
        except Exception as e:
            self.stdout.write(f'  ⚠ Could not create active loan (may already exist): {str(e)}')

        # Returned Loan (returned_at is set)
        past_date = now - timedelta(days=30)
        return_date = past_date + timedelta(days=7)

        try:
            returned_loan, created = Loan.objects.get_or_create(
                book=book3,
                member=member2,
                defaults={
                    "loaned_at": past_date,
                    "due_at": return_date,
                    "returned_at": return_date
                }
            )
            if created:
                self.stdout.write(f'  ✓ Created Returned Loan: {book3.title} → {member2.full_name}')
            else:
                self.stdout.write(f'  ℹ Returned Loan exists: {book3.title} → {member2.full_name}')
        except Exception as e:
            self.stdout.write(f'  ⚠ Could not create returned loan: {str(e)}')

        self.stdout.write(self.style.SUCCESS('\n✓ Seeding completed successfully!'))
        self.stdout.write('\nDatabase summary:')
        self.stdout.write(f'  Authors: {Author.objects.count()}')
        self.stdout.write(f'  Books: {Book.objects.count()}')
        self.stdout.write(f'  Members: {Member.objects.count()}')
        self.stdout.write(f'  Member Profiles: {MemberProfile.objects.count()}')
        self.stdout.write(f'  Tags: {Tag.objects.count()}')
        self.stdout.write(f'  Book Tags: {BookTag.objects.count()}')
        self.stdout.write(f'  Loans: {Loan.objects.count()}')
