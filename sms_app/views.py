
# Create your views here.
from .models import Student
from .forms import StudentForm, StudentProfileForm
from .models import Attendance, Marks, Fees
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from reportlab.pdfgen import canvas




User = get_user_model()
def login_page(request):

    if request.method == 'POST':

        username = request.POST['username']

        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.role == 'ADMIN':
                return redirect('/admin-dashboard/')

            elif user.role == 'TEACHER':
                return redirect('/teacher-dashboard/')

            elif user.role == 'STUDENT':
                return redirect('/student-dashboard/')

    return render(request, 'login.html')




from django.db.models import Sum
import json

def dashboard(request):
    if not request.session.get('admin_logged_in'):
        return redirect('/admin-login/')
    total_students = Student.objects.count()

    total_courses = Student.objects.values(
        'course'
    ).distinct().count()

    fees = Fees.objects.all()

    total_fees = 0

    for fee in fees:
        total_fees += fee.paid_fee

    students = Student.objects.order_by('-id')[:3]
    total_attendance = Attendance.objects.count()

    present_attendance = Attendance.objects.filter(
        status='Present'
    ).count()

    attendance_percentage = 0

    if total_attendance > 0:
        attendance_percentage = int(
            (present_attendance / total_attendance) * 100
        )

    # ================= STUDENT GROWTH =================

    monthly_students = []

    for month in range(1, 13):

        count = Student.objects.filter(
            created_at__month=month
        ).count()

        monthly_students.append(count)

    # ================= ATTENDANCE REPORT =================

    present_count = Attendance.objects.filter(
        status='Present'
    ).count()

    absent_count = Attendance.objects.filter(
        status='Absent'
    ).count()

    context = {

        'total_students': total_students,
        'total_courses': total_courses,
        'total_fees': total_fees,
        'students': students,
        'attendance_percentage': attendance_percentage,

        # charts data
        'monthly_students': json.dumps(monthly_students),

        'present_count': present_count,
        'absent_count': absent_count,

    }

    return render(
        request,
        'dashboard.html',
        context
    )



def add_student(request):

    if request.method == 'POST':

        form = StudentForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            password = form.cleaned_data['password']

            email = form.cleaned_data['email']

            # CREATE LOGIN USER

            user = User.objects.create_user(

                username=email,

                email=email,

                password=password,

                role='student'
            )

            # CREATE STUDENT

            student = form.save(commit=False)

            student.user = user

            student.is_approved = True

            student.save()

            return redirect('students')

    else:

        form = StudentForm()

    return render(
        request,
        'add_student.html',
        {'form': form}
    )


from django.db.models import Q


def students(request):

        query = request.GET.get('q')

        students = Student.objects.filter(is_approved=True)

        if query:
            students = students.filter(
                Q(name__icontains=query) |
                Q(course__icontains=query)
            )

        return render(
            request,
            'students.html',
            {'students': students}
        )
def delete_student(request, id):
    student = Student.objects.get(id=id)
    student.delete()

    return redirect('students')


def attendance(request):

    students = Student.objects.all()

    attendance_data = Attendance.objects.all()

    if request.method == "POST":

        student_id = request.POST.get('student')

        student = Student.objects.get(id=student_id)

        Attendance.objects.create(

            student=student,

            from_date=request.POST['from_date'],
            to_date = request.POST['to_date'],

            total_classes=request.POST.get('total_classes'),

            attended_classes=request.POST.get('attended_classes'),

            status=request.POST.get('status')

        )

        return redirect('/attendance/')

    context = {

        'students': students,

        'attendance_data': attendance_data

    }

    return render(

        request,

        'attendance.html',

        context

    )




def fees(request):

    fees_data = Fees.objects.all()

    return render(request,
                  'fees.html',
                  {'fees_data': fees_data})

def courses(request):

    student_courses = Student.objects.values_list('course',
                                                  flat=True).distinct()

    return render(request,
                  'courses.html',
                  {'courses': student_courses})

@login_required
def admin_dashboard(request):

    return render(
        request,
        'admin_dashboard.html'
    )




def teacher_dashboard(request):

    total_students = Student.objects.count()

    total_attendance = Attendance.objects.count()

    present_attendance = Attendance.objects.filter(
        status='Present'
    ).count()

    attendance_percentage = 0

    if total_attendance > 0:
        attendance_percentage = int(
            (present_attendance / total_attendance) * 100
        )

    students_with_marks = Marks.objects.values_list(
        'student',
        flat=True
    ).distinct()

    pending_results = Student.objects.exclude(
        id__in=students_with_marks
    ).count()

    context = {

        'total_students': total_students,
        'attendance_percentage': attendance_percentage,
        'pending_results': pending_results,

    }

    return render(request,
                  'teacher_dashboard.html',
                  context)

@login_required


def student_dashboard(request):



    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return HttpResponse("Student profile not found")
    attendance = Attendance.objects.filter(
        student=student
    )

    marks = Marks.objects.filter(
        student=student
    )
    fees = Fees.objects.filter(
        student=student
    ).first()

    total_classes = 0
    attended_classes = 0

    for a in attendance:

        total_classes += a.total_classes
        attended_classes += a.attended_classes

    attendance_percentage = 0
    if total_classes > 0:
        attendance_percentage = int(
            (attended_classes / total_classes) * 100
        )
    pending_fee = 0

    if fees:
        pending_fee = fees.due_fee




    context = {

        'student': student,
        'attendance_percentage': attendance_percentage,
        'marks': marks,
        'fees': fees,
        'pending_fee': pending_fee,

    }

    return render(request,
                  'student_dashboard.html',
                  context)

def home(request):
    return render(request, 'home.html')



def teacher_login(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('/teacher-dashboard/')

    return render(request, 'teacher_login.html')


def student_login(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('/student-dashboard/')

    return render(request, 'student_login.html')




def marks(request):

    students = Student.objects.all()

    marks_data = Marks.objects.all()

    if request.method == "POST":

        student_id = request.POST.get('student')

        student = Student.objects.get(id=student_id)

        Marks.objects.create(

            student=student,

            subject=request.POST.get('subject'),

            marks=request.POST.get('marks'),

            total_marks=request.POST.get('total_marks')

        )

        return redirect('/marks/')

    context = {

        'students': students,

        'marks_data': marks_data

    }

    return render(

        request,

        'marks.html',

        context

    )

def edit_attendance(request, id):

    attendance = Attendance.objects.get(id=id)

    if request.method == 'POST':

        attendance.total_classes = request.POST['total']
        attendance.attended_classes = request.POST['attended']
        attendance.status = request.POST['status']

        attendance.save()

        return redirect('attendance')

    return render(request,
                  'edit_attendance.html',
                  {'attendance': attendance})

def delete_attendance(request, id):

    attendance = Attendance.objects.get(id=id)

    attendance.delete()

    return redirect('attendance')

def edit_marks(request, id):

    mark = Marks.objects.get(id=id)

    if request.method == 'POST':

        mark.subject = request.POST['subject']
        mark.marks = request.POST['marks']
        mark.total_marks = request.POST['total_marks']

        mark.save()

        return redirect('marks')

    return render(request,
                  'edit_marks.html',
                  {'mark': mark})


def delete_marks(request, id):

    mark = Marks.objects.get(id=id)

    mark.delete()

    return redirect('marks')




# ================= STUDENT REGISTER =================


# ================= TEACHER REGISTER =================

def teacher_register(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')

            else:
                User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    role='TEACHER'
                )

                messages.success(request, 'Teacher Registration Successful')

                return redirect('teacher_login')

        else:
            messages.error(request, 'Passwords do not match')

    return render(request, 'teacher_register.html')




def admin_login(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        if username == "admin" and password == "admin123":

            request.session['admin_logged_in'] = True

            return redirect('/dashboard/')

        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, 'admin_login.html')

def download_report(request, id):

    student = Student.objects.get(id=id)

    marks = Marks.objects.filter(student=student)

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = f'attachment; filename="{student.name}_report.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 18)

    p.drawString(180, 800, "Student Report Card")

    p.setFont("Helvetica", 12)

    p.drawString(50, 760, f"Student Name : {student.name}")

    p.drawString(50, 740, f"Email : {student.email}")

    p.drawString(50, 720, f"Course : {student.course}")

    y = 660

    p.setFont("Helvetica-Bold", 13)

    p.drawString(50, y, "Subject")
    p.drawString(250, y, "Marks")
    p.drawString(350, y, "Total")
    p.drawString(450, y, "Percentage")

    y -= 30

    p.setFont("Helvetica", 12)

    for m in marks:

        percentage = (m.marks / m.total_marks) * 100

        p.drawString(50, y, str(m.subject))
        p.drawString(250, y, str(m.marks))
        p.drawString(350, y, str(m.total_marks))
        p.drawString(450, y, f"{percentage:.1f}%")

        y -= 25

    p.save()

    return response

def edit_student_profile(request):

    student = Student.objects.get(
        user=request.user
    )

    if request.method == 'POST':

        form = StudentProfileForm(

            request.POST,

            request.FILES,

            instance=student
        )

        if form.is_valid():

            form.save()

            return redirect(
                'student_dashboard'
            )

    else:

        form = StudentProfileForm(
            instance=student
        )

    return render(

        request,

        'edit_student_profile.html',

        {'form': form}
    )