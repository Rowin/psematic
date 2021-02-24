from django.contrib import admin

from .models import TrainingSession, Student, Skill, CaseStudy, Evaluation


class EvaluationInline(admin.TabularInline):
    model = Evaluation


class CaseStudyAdmin(admin.ModelAdmin):
    inlines = (EvaluationInline,)


admin.site.register(TrainingSession)
admin.site.register(Student)
admin.site.register(Skill)
admin.site.register(CaseStudy, CaseStudyAdmin)
admin.site.register(Evaluation)
