from django.contrib import admin
from .models import BloodAnalysis, Diagnosis, CholesterolAnalysis, Conclusion

admin.site.register(BloodAnalysis)
admin.site.register(Diagnosis)
admin.site.register(CholesterolAnalysis)
admin.site.register(Conclusion)
