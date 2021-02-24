from django.db import models


class Session(models.Model):
    date = models.DateField()
    description = models.TextField()
    students = models.ManyToManyField("Student")


class Student(models.Model):
    firstname = models.TextField()
    lastname = models.TextField()
    mail = models.EmailField()


class Skill(models.Model):
    session = models.ForeignKey("Session", on_delete=models.CASCADE)
    description = models.TextField()
    order = models.IntegerField()
    parent = models.ForeignKey("Skill", on_delete=models.CASCADE)


class CaseStudy(models.Model):
    date = models.DateField()
    evaluator = models.TextField()  # TODO: change to user and One-to-Many
    students = models.ManyToManyField(Student, through="Evaluation")


class Evaluation(models.Model):
    student = models.ForeignKey(CaseStudy, on_delete=models.CASCADE)
    case_study = models.ForeignKey(Student, on_delete=models.CASCADE)
    comment = models.TextField()
    skills = models.ManyToManyField(Skill, through="SkillEvaluation")


class SkillEvaluation(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    grade = models.TextField(choices=[
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D')
    ])
    has_been_evaluated = models.BooleanField()
