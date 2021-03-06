from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class TrainingSession(models.Model):
    date = models.DateField()
    description = models.TextField()
    students = models.ManyToManyField("Student", blank=True)
    case_study_group_size = models.IntegerField(default=2)

    class Meta:
        verbose_name = _("training session")
        verbose_name_plural = _("training sessions")


class Student(models.Model):
    firstname = models.TextField()
    lastname = models.TextField()
    mail = models.EmailField()

    def __str__(self):
        return f"{self.firstname} {self.lastname.upper()}"

    class Meta:
        verbose_name = _("student")
        verbose_name_plural = _("students")


class Skill(models.Model):
    training_session = models.ForeignKey(
        "TrainingSession", on_delete=models.CASCADE, related_name="skills"
    )
    description = models.TextField()
    order = models.IntegerField()
    parent = models.ForeignKey("Skill", on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def full_clean(self, exclude=None, validate_unique=True):
        if self.training_session.case_studies.count() > 0:
            raise ValidationError(
                _(
                    "Cannot change skills when there are already case studies in the training session"
                )
            )
        return super().full_clean(exclude=exclude, validate_unique=validate_unique)

    def __str__(self):
        return f"{self.order}. {self.description}"

    class Meta:
        verbose_name = _("skill")
        verbose_name_plural = _("skills")


class CaseStudy(models.Model):
    training_session = models.ForeignKey(
        TrainingSession, on_delete=models.CASCADE, related_name="case_studies"
    )
    date = models.DateField()
    subject = models.TextField()
    evaluator = models.TextField()  # TODO: change to user and One-to-Many
    students = models.ManyToManyField(Student, through="Evaluation")

    class Meta:
        verbose_name = _("case study")
        verbose_name_plural = _("case studies")


class Evaluation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    skills = models.ManyToManyField(Skill, through="SkillEvaluation")

    def save(self, *args, **kwargs):
        is_new = self.id is None

        # Save needed before Many-to-Many manipulation: an id is needed
        super().save(*args, **kwargs)

        # If new, the session skills are automatically linked to the Evaluation
        if is_new:
            for session_skill in self.case_study.training_session.skills.all():
                skill_evaluation = SkillEvaluation(skill=session_skill, evaluation=self)
                skill_evaluation.save()

    class Meta:
        verbose_name = _("evaluation")
        verbose_name_plural = _("evaluations")


class SkillEvaluation(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    grade = models.TextField(
        choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")], blank=True
    )
    has_been_evaluated = models.BooleanField(default=False)
