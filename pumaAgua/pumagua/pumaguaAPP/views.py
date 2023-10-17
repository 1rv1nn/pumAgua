from django.shortcuts import render
import folium
from pumaguaAPP.models import bebederos
from django.db.models import Q
from folium.plugins import LocateControl
import json
from folium.plugins import MarkerCluster
 
# Create your views here.
def index(request):
    datosBebederos = bebederos.objects.all()
    m = folium.Map(location=[19.320916010251914, -99.18395683244859], zoom_start=13,height="100%",width="90%",left="5%")
    LocateControl().add_to(m)
    
    html = ''' <h5> Nombre </h5> '''
    html1 = ''' <h5> Ubicacion </h5> '''
    
    
    marker_cluser = MarkerCluster().add_to(m)
    
    
    
    with open('rutasPumaBus.json') as jsonfile:
        paseoRutas = json.load(jsonfile)
    
    fg1 = folium.FeatureGroup(name="Ruta 1",show=False).add_to(m)
    folium.PolyLine(paseoRutas[0]['coordenadas'], tooltip="Ruta 1",color='#2CFF2C',stroke=True).add_to(fg1)
    
    
    fg3 = folium.FeatureGroup(name="Ruta 3",show=False).add_to(m)
    folium.PolyLine(paseoRutas[2]['coordenadas'], tooltip="Ruta 3",color='#005E00',stroke=True).add_to(fg3)
       
    folium.LayerControl().add_to(m)    
        
    
    
    if 'q' in request.GET:
        q = request.GET['q']
        multiple_q = Q(Q(nombre__icontains=q)| Q(ubicacion__icontains=q)| Q(institucion__icontains=q)| Q(palabras_clave__icontains=q))
        data = bebederos.objects.filter(multiple_q)
        
        for coordenada in data:
            datos = (coordenada.latitud, coordenada.longitud)
            folium.Marker(datos, tooltip= 'Info', popup=html + coordenada.nombre + "\n" + html1 + coordenada.ubicacion + "\n",icon=folium.Icon(icon="glyphicon glyphicon-tint")).add_to(m)
    else:    
        for coordenada in datosBebederos:
            datos = (coordenada.latitud, coordenada.longitud)
            folium.Marker(datos, tooltip= 'Info', popup=html + coordenada.nombre + "\n" +  html1 + coordenada.ubicacion + "\n", icon=folium.Icon(icon="glyphicon glyphicon-tint"),name="Bebederos").add_to(marker_cluser)
    contexto = {'map': m._repr_html_()}
    
    return render(request, "index.html", contexto)
