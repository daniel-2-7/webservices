from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Professor (models.Model):
    professor_id = models.CharField(max_length=10, primary_key=True)
    professor_name = models.CharField(max_length=30)

    def __str__(self):
        return self.professor_name


class Course (models.Model):
    module_code = models.CharField(max_length=10, primary_key=True)
    module_name = models.CharField(max_length=30)

    def __str__(self):
        return self.module_name


class ModuleInstance (models.Model):
    SemesterYear = [('semester1', 'Semester 1'), ('semester2', 'Semester 2')]
    semester = models.CharField(max_length=10, choices=SemesterYear)
    year = models.IntegerField()
    professors = models.ManyToManyField(Professor)
    modules = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.modules.module_name + " " + self.semester + " " + str(self.year)


class Rating (models.Model):
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    module_instance = models.ForeignKey(ModuleInstance, on_delete=models.CASCADE)

    def __str__(self):
        return self.professor.professor_name + ", Rating: " + str(self.rating) + " (" + self.module_instance.modules.module_name + ")"

