#-*- encoding: utf-8 -*-
from django.contrib.auth.decorators   import login_required
from django.views.generic.list_detail import object_list
from django.shortcuts  import render_to_response
from dpro.bilet.models import Sefer, Koltuk, Bilet, BiletForm, BiletFormD
from django.http import HttpResponseRedirect, HttpResponse
from django.db   import transaction
import csv
#from reportlab.pdfgen import canvas

@login_required
def index(request):
    user     = request.user
    if user.username == 'OZLEM':
        seferler = Sefer.objects.all()
    else:
        seferler = Sefer.objects.filter(sorumlu=user.id)
    dict = {'seferler': seferler,
            'user': user
    }
    return render_to_response('index.html', dict)

@login_required
def listele(request, p_seferid):
    user     = request.user
    sefer    = Sefer.objects.get(id=p_seferid)
    biletler = Bilet.objects.filter(koltuk__sefer__id=p_seferid)
    return object_list(request, 
                       queryset=biletler, 
                       template_name='listele.html', 
                       template_object_name='bilet', 
                       extra_context={'sefer': sefer, 'user': user})
    
@login_required
def ara(request):
    user = request.user
    if request.POST:
        if user.username == 'OZLEM':
            biletler = Bilet.objects.filter(kimlik_no__icontains=request.POST['p_kimlikno'],
                                            yolcu_adi__icontains=request.POST['p_yolcuadi'],
                                            yolcu_soyadi__icontains=request.POST['p_yolcusoyadi']).order_by('koltuk_no')
        else:
            biletler = Bilet.objects.filter(koltuk__sefer__sorumlu=user, 
                                            kimlik_no__icontains=request.POST['p_kimlikno'],
                                            yolcu_adi__icontains=request.POST['p_yolcuadi'],
                                            yolcu_soyadi__icontains=request.POST['p_yolcusoyadi']).order_by('bilet_bilet__koltuk__sefer.sefer_tarihi')
        return object_list(request, queryset=biletler, template_name='listele2.html', template_object_name='bilet', extra_context={'user': user})        
    dict = {'user': user}
    return render_to_response('arama.html', dict)

@login_required
def degistir(request, p_koltukid):
    user  = request.user
    bilet = Bilet.objects.get(koltuk__id=p_koltukid)
    if request.method == 'POST':
        form = BiletFormD(data=request.POST, instance=bilet)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/bilet/biletlistele/%s' % bilet.koltuk.sefer.id)
    else:
        form = BiletFormD(instance=bilet)
    dict = {'bilet': bilet,
            'form':  form, 
            'user': user
    }
    return render_to_response('degistir.html', dict)

@login_required
def sil(request, p_biletid):
    user  = request.user
    bilet = Bilet.objects.get(id=p_biletid)
    if request.POST:
        bilet.delete()
        return HttpResponseRedirect('/bilet/biletlistele/%s' % bilet.koltuk.sefer.id)
    return render_to_response('sil.html', locals())

@login_required
@transaction.commit_manually
def doldur(request, p_secim, p_seferid):
    user      = request.user
    sefer     = Sefer.objects.get(id=p_seferid)
    koltukall = Koltuk.objects.filter(sefer=sefer)
    tmplist   = []
    kollist   = []
    sayac     = 0
    uyari     = ''
    kimlik    = "0"
    tmpkoltuk = 0
    tmpkimlik = ''
    for i in range(12):
        for j in range(4):
            try:
                tmplist.append(koltukall[sayac])
            except IndexError:
                tmplist.append('BOS')
            sayac += 1
        kollist.append(tmplist)
        tmplist = []
    kolsay = koltukall.filter(rezerve_eh=p_secim).count()
    if request.method == 'POST':
        form   = BiletForm(request.POST)
        kimlik = request.GET['kimlik']
        tmpkoltuk = int(request.POST['koltuk_no'])
        tmpkimlik = request.POST['vat_no']
        if kimlik == "1":
            if Bilet.objects.filter(kimlik_no=tmpkimlik).count() > 0:
                uyari = u'Bu kişi daha önce geziye katılmış'
        else:
            if form.is_valid():
                try:
                    yenibilet = form.save(commit=False)
                    yenibilet.koltuk = Koltuk.objects.get(sefer=sefer, koltuk_no=request.POST['koltuk_no'])
                    yenibilet.koltuk_no = yenibilet.koltuk.koltuk_no
                    yenibilet.kimlik_no = request.POST['vat_no']
                    yenibilet.save()
                    transaction.commit()
                    return HttpResponseRedirect('/bilet/biletdoldur/%s/%s' % (p_secim, p_seferid))            
                except:
                    transaction.rollback()
                    raise

    else:        
        form   = BiletForm()
    dict = {'sefer':     sefer,
            'form':      form,
            'kollist':   kollist,
            'secim':     p_secim,
            'user':      user,
            'kolsay':    kolsay,
            'kimlik':    kimlik,
            'uyari':     uyari,
            'tmpkoltuk': tmpkoltuk,
            'tmpkimlik': tmpkimlik
    }
    return render_to_response('doldur.html', dict)

#def csvdeneme(request):
#    response = HttpResponse(mimetype='text/csv')
#    response['Content-Disposition'] = 'attachment; filename=somefilename.csv'
#    writer = csv.writer(response)
#    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
#    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quo,teİıŞÜĞ"])
#    return response
#    response = HttpResponse(mimetype='application/pdf')
#    response['Content-Disposition'] = 'filename=somefilename.pdf'
#    p = canvas.Canvas(response)
#    p.drawString(-10, -10, "Hello world.")
#    p.showPage()
#    p.save()
#    return response
