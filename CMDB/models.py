from django.db import models

class cmdb(models.Model):
    日期 = models.DateField(null=True, blank=True)
    月份 =models.IntegerField(null=True, blank=True)
    花费地 = models.CharField(max_length=255,null=True, blank=True)
    USE_choices =(
        ('名片印制','名片印制'),
        ('日常办公','日常办公'),
        ('员工福利','员工福利')
    )
    小类别 = models.CharField(max_length=255,choices=USE_choices,null=True, blank=True)
    channel_type =(
        ('京东','京东'),
        ('淘宝','淘宝'),
        ('拼多多','拼多多'),
        ('闪送','闪送')
    )
    购买渠道 =models.CharField(max_length=255,choices=channel_type,null=True, blank=True)
    明细 = models.TextField()
    金额 = models.FloatField()
    bill_type = (
        ('截图','截图'),
        ('发票','发票'),
        ('截图+发票','截图+发票')
    )
    发票类型 =  models.CharField(max_length=255,choices=bill_type,null=True, blank=True)
    CHOICES = (
        ('yes','是'),
        ('no','否')
    )
    报销申请 = models.CharField(max_length=255,choices=CHOICES,null=True, blank=True)
    财务打款 = models.CharField(max_length=255,choices=CHOICES,null=True, blank=True)

    def __str__(self):
        return f"{self.id}"

