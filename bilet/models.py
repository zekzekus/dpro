#-*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.newforms import ModelForm

class Dernek(models.Model):
    dernek_adi    = models.CharField(max_length=50, verbose_name=u'Dernek Adı')
    dernek_adresi = models.CharField(max_length=500, verbose_name=u'Dernek Adresi')

    def __unicode__(self):
        return self.dernek_adi

    class Admin:
        list_display  = ('dernek_adi', 'dernek_adresi')
        search_fields = ('dernek_adi', 'dernek_adresi')
        
    class Meta:
        verbose_name        = 'Dernek'
        verbose_name_plural = 'Dernekler'

class Gezi(models.Model):
    gezi_adi = models.CharField(max_length=50, verbose_name=u'Gezi Adı')
    ilktarih = models.DateField(verbose_name=u'Başlangıç Tarihi')
    sontarih = models.DateField(verbose_name=u'Bitiş Tarihi')

    def __unicode__(self):
        return self.gezi_adi

    class Admin:
        list_display  = ('gezi_adi', 'ilktarih', 'sontarih')
        search_fields = ('gezi_adi', 'ilktarih', 'sontarih')
        
    class Meta:
        verbose_name        = 'Gezi'
        verbose_name_plural = 'Geziler'

class Sefer(models.Model):
    sefer_adi     = models.CharField(max_length=50, verbose_name=u'Sefer Adı')
    sefer_tarihi  = models.DateField(verbose_name=u'Sefer Tarihi')
    koltuk_sayisi = models.IntegerField(verbose_name=u'Koltuk Sayısı')
    kalkis_yeri   = models.CharField(max_length=50, verbose_name=u'Kalkış Yeri')
    kalkis_saati  = models.CharField(max_length=5, verbose_name=u'Kalkış Saati')
    onrezerv1     = models.IntegerField(verbose_name=u'Ön Rezerv 1')
    onrezerv2     = models.IntegerField(verbose_name=u'Ön Rezerv 2')
    dernek        = models.ForeignKey(Dernek, blank=True, null=True, verbose_name=u'Dernek')
    sorumlu       = models.ForeignKey(User, verbose_name=u'Sorumlu Kullanıcı')
    gezi          = models.ForeignKey(Gezi, verbose_name=u'Bağlı Gezi')
#    hsayi         = models.IntegerField()

    def __unicode__(self):
        return '%s - %s' % (self.sefer_adi, self.sefer_tarihi)

    class Admin:
        list_display  = ('sefer_adi', 'sefer_tarihi', 'dernek', 'sorumlu', 'gezi')
        search_fields = ('sefer_adi', 'sefer_tarihi', 'dernek', 'sorumlu', 'gezi')
        list_filter   = ('dernek', 'sorumlu', 'gezi')

    class Meta:
        verbose_name        = 'Sefer'
        verbose_name_plural = 'Seferler'
        ordering            = ["sefer_tarihi"]

class Koltuk(models.Model):
    koltuk_no  = models.IntegerField(verbose_name=u'Koltuk Numarası')
    rezerve_eh = models.CharField(max_length=1, verbose_name=u'Rezervasyon Durumu')
    sefer      = models.ForeignKey(Sefer, verbose_name=u'Bağlı Sefer')

    def __unicode__(self):
        return '%s - %s' % (self.sefer.sefer_adi, self.koltuk_no)
    
#    class Admin:
#        list_display = ('sefer', 'koltuk_no')
#        list_filter  = ('sefer',)

    class Meta:
        verbose_name        = 'Koltuk'
        verbose_name_plural = 'Koltuklar'
        ordering            = ["koltuk_no"]

CINSIYET_CHOICES = (
    ('E', 'Erkek'),
    ('K', 'Bayan'),
)
OZURLU_CHOICES = (
    ('E', u'Evet'),
    ('H', u'Hayır'),
)

class  Bilet(models.Model):
    koltuk       = models.ForeignKey(Koltuk, verbose_name='Koltuk No')
    kimlik_no    = models.CharField(max_length=11, blank=True, null=True, verbose_name=u'Vatandaşlık No')
    yolcu_adi    = models.CharField(max_length=50, verbose_name=u'Yolcu Adı')
    yolcu_soyadi = models.CharField(max_length=50, verbose_name=u'Yolcu Soyadı')
    cinsiyet     = models.CharField(max_length=1, choices=CINSIYET_CHOICES, verbose_name=u'Cinsiyet')
    ozurlu_eh    = models.CharField(max_length=1, choices=OZURLU_CHOICES, blank=True, null=True, default='H', verbose_name=u'Özürlü?')
    baba_adi     = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'Baba Adı')
    anne_adi     = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'Doğum Yeri')
    tel_no       = models.CharField(max_length=12, blank=True, null=True, verbose_name=u'Telefon No')
    gsm_no       = models.CharField(max_length=12, blank=True, null=True, verbose_name=u'Cep Telefonu')
    eposta       = models.EmailField(blank=True, null=True, verbose_name=u'E-Posta')
    mahalle      = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'Mahalle')
    cadde        = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'Cadde')
    sokak        = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'Sokak')
    bina_no      = models.CharField(max_length=5,  blank=True, null=True, verbose_name=u'Bina No')
    daire_no     = models.CharField(max_length=5,  blank=True, null=True, verbose_name=u'Daire No')
    il           = models.CharField(max_length=30, blank=True, null=True, verbose_name=u'İl', default='Küçükçekmece')
    ilce         = models.CharField(max_length=30, blank=True, null=True, verbose_name=u'İlçe', default='İstanbul')
    koltuk_no    = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return '%s - %s' % (self.koltuk.sefer.sefer_adi, self.koltuk.koltuk_no)

    class Admin:
        list_display  = ('yolcu_adi', 'yolcu_soyadi', 'kimlik_no', 'cinsiyet', 'mahalle')
        search_fields = ('kimlik_no', 'yolcu_adi', 'yolcu_soyadi', 'cinsiyet', 'mahalle')
        list_filter   = ('cinsiyet', 'mahalle')

    class Meta:
        verbose_name        = 'Bilet'
        verbose_name_plural = 'Biletler'
        ordering            = ["koltuk_no"]

class BiletForm(ModelForm):
    class Meta:
        model   = Bilet
        exclude = ('koltuk', 'koltuk_no', 'kimlik_no', 'bina_no', 'daire_no')

class BiletFormD(ModelForm):
    class Meta:
        model   = Bilet
        exclude = ('koltuk', 'koltuk_no', 'bina_no', 'daire_no', 'cinsiyet')
    
