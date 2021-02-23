from django.contrib import admin

from .models import Poll, Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice

    def get_max_num(self, request, obj=None, **kwargs):
        max_num = 15

        if obj:
            if obj.type == 'WA':
                self.show_change_link = False
                return 0

        self.show_change_link = True
        return max_num


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True


class PollAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'updated_at',
                    'end_date', 'visible']
    list_display_links = ['pk', 'title']
    list_editable = ['visible', 'end_date']
    search_fields = ['title', 'description']
    list_filter = ['visible']
    sortable_by = ['updated_at', 'end_date']

    inlines = [QuestionInline]


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'type']
    list_display_links = ['pk', 'title']
    search_fields = ['text', 'title']

    inlines = [ChoiceInline]


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
