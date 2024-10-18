from django.shortcuts import render
from django.db.models import Q
from .models import *

# Create your views here.

def index(request):
    return render(request,'index.html')

def listar_libros(request):
    libros = Libro.objects.select_related("biblioteca").prefetch_related("autores")
    libros = libros.all()
    return render(request, 'libro/lista.html',{"libros_mostrar":libros})

def dame_libro(request,id_libro):
    libro = Libro.objects.select_related("biblioteca").prefetch_related("autores").get(id=id_libro)
    return render(request, 'libro/libro.html',{"libro":libro})

def dame_libros_fecha(request,anyo_libro,mes_libro):
    libros = Libro.objects.select_related("biblioteca").prefetch_related("autores")
    libros = libros.filter(fecha_publicacion__year=anyo_libro,fecha_publicacion__month=mes_libro)
    return render(request, 'libro/lista.html',{"libros_mostrar":libros})

def dame_libros_idioma(request,tipo):
    libros = Libro.objects.select_related("biblioteca").prefetch_related("autores")
    libros = libros.filter(Q(tipo=tipo) | Q(tipo="ES")).order_by("fecha_publicacion")
    return render(request, 'libro/lista.html',{"libros_mostrar":libros})

def dame_libros_biblioteca(request,id_biblioteca,descripcion):
    libros = Libro.objects.select_related("biblioteca").prefetch_related("autores")
    libros = libros.filter(biblioteca=id_biblioteca).filter(descripcion__contains=descripcion).order_by("-nombre")
    return render(request,'libro/lista.html',{"libros_mostrar":libros})

def dame_ultimo_cliente_libro(request,libro):
    cliente = Cliente.objects.filter(libros_prestamos=libro).order_by("-prestamos__fecha_prestamo")[:1].get()
    return render(request,'cliente/cliente.html',{"cliente":cliente})

def libros_no_prestados(request):
    libros = Libro.objects.select_related("biblioteca").prefetch_related("autores")
    libros = libros.filter(prestamos=None)
    return render(request,'libro/lista.html',{"libros_mostrar":libros})