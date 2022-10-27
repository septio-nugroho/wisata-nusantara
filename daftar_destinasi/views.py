from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Destinasi
from django.core import serializers

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.
def show_json(request):
  data = Destinasi.objects.all()
  return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def daftar_destinasi(request):
  data = Destinasi.objects.all()

  context = {
    'data': data
  }

  return render(request, 'daftar-destinasi.html', context)

def destinasi_by_id(request, id):
  destinasi = Destinasi.objects.get(pk=id)

  context = {
    'nama': destinasi.nama,
    'deskripsi': destinasi.deskripsi,
    'lokasi': destinasi.lokasi,
    'kategori': destinasi.kategori,
    'foto_thumbnail_url': destinasi.foto_thumbnail_url,
    'foto_cover_url': destinasi.foto_cover_url,
    'maps_url': destinasi.maps_url,
    'suka': destinasi.suka,
  }

  return render(request, 'destinasi-by-id.html', context)

@csrf_exempt
def tambah_destinasi(request):
  if (request.method == 'POST'):
    nama = request.POST.get('nama')
    deskripsi = request.POST.get('deskripsi')
    lokasi = request.POST.get('lokasi')
    kategori = request.POST.get('kategori')
    foto_thumbnail_url = request.POST.get('foto_thumbnail_url')
    foto_cover_url = request.POST.get('foto_cover_url')
    maps_url = request.POST.get('maps_url')

    destinasi = Destinasi(
      nama=nama,
      deskripsi=deskripsi,
      lokasi=lokasi,
      kategori=kategori,
      foto_thumbnail_url=foto_thumbnail_url,
      foto_cover_url=foto_cover_url,
      maps_url=maps_url
    )
    destinasi.save()

    context = {
      'nama': destinasi.nama,
      'description': destinasi.deskripsi,
      'location': destinasi.lokasi,
      'category': destinasi.kategori
    }

    print(context)

    return JsonResponse({"header": "Destinasi Ditambahkan"}, status=200)

  return render(request, 'tambah-destinasi.html')

@csrf_exempt
@login_required(login_url='/auth/login')
def hapus_destinasi(request):
  data = Destinasi.objects.all()

  context = {
    'data': data
  }

  return render(request, 'hapus-destinasi.html', context)
  
@csrf_exempt
@login_required(login_url='/auth/login')
def hapus_destinasi_by_id(request, id):
  if (request.user.username == "eugenius.mario"): # hanya user dengan username ini yg bisa hapus destination
    task = Destinasi.objects.get(pk=id)
    task.delete()
  return HttpResponseRedirect("/destination/delete")