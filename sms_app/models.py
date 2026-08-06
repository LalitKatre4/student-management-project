from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

class CustomUser(AbstractUser):

    ROLE_CHOICES = (

        ('ADMIN', 'Admin'),

        ('TEACHER', 'Teacher'),

        ('STUDENT', 'Student'),

    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )
class Student(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)

    email = models.EmailField(null=True,
                              blank=True)

    contact = models.CharField(max_length=15,
                               null=True,
                               blank=True)

    course = models.CharField(max_length=100,
                              null=True,
                              blank=True)

    address = models.TextField(null=True,
                               blank=True)

    photo = models.ImageField(upload_to='students/', null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    gender = models.CharField(
        max_length=10,
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')],null=True,
    blank=True)

    created_at = models.DateTimeField(auto_now_add=True,
                                      null=True,
                                      blank=True)

    def __str__(self):
        return self.name
class Attendance(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )
    from_date = models.DateField()
    to_date = models.DateField()

    total_classes = models.IntegerField(default=0)

    attended_classes = models.IntegerField(default=0)

    status = models.CharField(
        max_length=20,
        default='Present'
    )

    def __str__(self):
        return self.student.name
class Marks(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    subject = models.CharField(
        max_length=100
    )

    marks = models.IntegerField()

    total_marks = models.IntegerField(
        default=100
    )

    def __str__(self):
        return self.student.name
class Fees(models.Model):

    student = models.ForeignKey(Student,
                                on_delete=models.CASCADE)

    total_fee = models.FloatField()

    paid_fee = models.FloatField()

    due_fee = models.FloatField()

    def __str__(self):
        return self.student.name

