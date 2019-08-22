from django.db import models
# from django.utils.timezone import now

# Create your models here.

class Yado(models.Model):
    
    #オプションの第一引数に名前を入れることで、項目欄が平仮名表記なる
    name = models.CharField("宿名",max_length=50,blank=True, null=True, unique=True)
    yado_area = models.CharField('エリア',max_length=50,blank=True, null=True, unique=True)
    
    
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "yado"
        verbose_name = verbose_name_plural = '宿名'



class reviews(models.Model):
    
    #blank=Trueはフォーム入力の項目が空でもOK null=True,データベースに項目が空でも
    yado_name = models.CharField(max_length=50,blank=True, null=True, verbose_name='名前')
    name = models.ForeignKey(Yado,null=True, blank=True, on_delete=models.SET_NULL, verbose_name='紐付け(名前)')
    area = models.CharField('エリア',max_length=50,blank=True, null=True)
    rank = models.IntegerField('掲載順位',blank=True,null=True)
    review＿number  = models.IntegerField('口コミ数',blank=True,null=True)
    total_review  = models.FloatField('総合得点',blank=True,null=True)
    room_score  = models.FloatField('部屋',blank=True,null=True)
    bath_score  = models.FloatField('風呂',blank=True,null=True)
    breakfast_score  = models.FloatField('朝食',blank=True,null=True)
    dinner_score  = models.FloatField('夕食',blank=True,null=True,default='')
    service_score  = models.FloatField('サービス',blank=True,null=True)
    beautiful_score  = models.FloatField('清潔感',blank=True,null=True)
    
    dinner_breakfast_lowest_price = models.PositiveIntegerField('1泊2食最安値',blank=True,null=True)
    stay_overnight_lowest_price = models.PositiveIntegerField('素泊まり最安値',blank=True,null=True)
    created_at = models.DateTimeField(verbose_name='投稿日時', blank=True,null=True)
    
    
    def __str__(self):
        return self.yado_name
    
    class Meta:
        db_table = "review"
        verbose_name = verbose_name_plural = '口コミ'
        
        
