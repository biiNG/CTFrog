from django.db import models

# Create your models here.

class User(models.Model):

    gender=(
        ('male','男'),
        ('famale','女'),
    )

    name=models.CharField(max_length=128,unique=True)
    password=models.CharField(max_length=256)
    email=models.EmailField(unique=True)
    sex=models.CharField(max_length=32,choices=gender,default='男')
    creat_time=models.DateTimeField(auto_now_add=True) #auto_now_add 自动设置为创建这个model的时间
    student_id=models.CharField(max_length=20,verbose_name='The student id of the user')
    # 暂时不加入team

    def __str__(self):
        return self.name #可读化显示

    class Meta:
        ordering=["-creat_time"] #按时间降序
        verbose_name="用户" #模型名称
        verbose_name_plural="用户们" #模型复数名

