from django.db import models

# === ВЖЕ ІСНУЄ ===
class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    student_card_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    group = models.ForeignKey('StudentGroup', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class StudentGroup(models.Model):
    group_number = models.CharField(max_length=10, unique=True)
    slogan = models.CharField(max_length=100)
    meeting_room = models.CharField(max_length=30)

    def __str__(self):
        return self.group_number

# === 1. OneToOne: Student ↔ Profile ===
class Profile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return f"Profile of {self.student}"

# === 2. OneToMany: StudentGroup → Course ===
class Course(models.Model):
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=100)
    teacher = models.CharField(max_length=100)
    credit_hours = models.IntegerField()

    def __str__(self):
        return f"{self.name} for {self.group}"

# === 3. ManyToMany: Student ↔ Club ===
class Club(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    members = models.ManyToManyField(Student, related_name='clubs')

    def __str__(self):
        return self.name

# === Інші моделі ===
class LibraryCard(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    issue_date = models.DateField()
    expiration_date = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    card_id = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"Card {self.card_id} for {self.student}"

class Literature(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    publish_date = models.DateField()
    publication_year = models.IntegerField()
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.title

class BookBorrowing(models.Model):
    library_card = models.ForeignKey(LibraryCard, on_delete=models.CASCADE)
    literature = models.ForeignKey(Literature, on_delete=models.CASCADE)
    borrowed_date = models.DateField()
    librarian_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.literature.title} borrowed by {self.library_card.student}"
