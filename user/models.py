from django.db import models
# Create your models here.


class Team(models.Model):
    name = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    score = models.IntegerField(default=0)
    member = models.IntegerField(
        default=0, verbose_name='how many people in this team')
    admin = models.CharField(default='', unique=True, max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "团队"


class User(models.Model):
    gender = (
        ('male', '男'),
        ('famale', '女'),
    )
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    # auto_now_add 自动设置为创建这个model的时间
    creat_time = models.DateTimeField(auto_now_add=True)
    student_id = models.CharField(
        max_length=20, verbose_name='The student id of the user', default=0, null=True)
    mark = models.IntegerField(default=0)
    # team
    team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    issuperuser = models.BooleanField(
        default=False, verbose_name='is it a team manager')

    def __str__(self):
        return self.name  # 可读化显示

    class Meta:
        ordering = ["-creat_time"]  # 按时间降序
        verbose_name = "用户"  # 模型名称
        verbose_name_plural = "用户们"  # 模型复数名


class ApplyMessage(models.Model):
    '''
    申请加入团队时向选中的团队的管理员发送信息
    receiver: the admin receive this message
    sender: the user send the apply
    apply_date: the time the sender applied
    '''
    state=(('approved','通过'),('denied','拒绝'),('unchecked','待审核'))
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='appliesreceived')
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='appliessent')
    apply_date = models.DateTimeField(auto_now_add=True)
    apply_state=models.CharField(max_length=20,choices=state,default='unchecked')
    team=models.CharField(max_length=20,default='',verbose_name='desired team')
    def __str__(self):
        return self.sender.name
