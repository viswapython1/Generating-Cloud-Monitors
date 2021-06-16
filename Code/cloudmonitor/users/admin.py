from django.contrib import admin
from users.models import Contact,Account,ContactSource,ContactStatus,ActivityStatus,Activity,CloudUsersModel,UserFileModel


# Register your models here.

admin.site.register(Contact)
admin.site.register(Account)
admin.site.register(ContactSource)
admin.site.register(ContactStatus)
admin.site.register(ActivityStatus)
admin.site.register(Activity)
admin.site.register(CloudUsersModel)
admin.site.register(UserFileModel)
