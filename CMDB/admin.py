from django.contrib import admin
from .models import cmdb
from import_export.admin import ImportExportModelAdmin


@admin.register(cmdb)

class cmdb(ImportExportModelAdmin):

    list_display = ('id', '日期','月份', '花费地', '小类别','购买渠道','明细','金额','发票类型','报销申请','财务打款')
