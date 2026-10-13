from django.shortcuts import render, redirect
from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from .models import Repuesto
from .forms import RepuestoForm
from .serializers import RepuestoSerializer, UserRegistroSerializer


# ==============================================================================
# VISTAS WEB TRADICIONALES (HTML)
# ==============================================================================
def inicio(request):
    return render(request, 'paginas/inicio.html')


def listado_repuestos(request):
    repuestos = Repuesto.objects.all()
    data = {'repuestos': repuestos}
    return render(request, 'repuestos/listado.html', data)


def crear_repuesto(request):
    formulario = RepuestoForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('listado_repuestos')
    return render(request, 'repuestos/crear.html', {'formulario': formulario})


def editar_repuesto(request, id):
    repuesto = Repuesto.objects.get(id=id)
    formulario = RepuestoForm(request.POST or None, request.FILES or None, instance=repuesto)
    if formulario.is_valid() and request.method == 'POST':
        formulario.save()
        return redirect('listado_repuestos')
    return render(request, 'repuestos/editar.html', {'formulario': formulario})


def eliminar_repuesto(request, id):
    repuesto = Repuesto.objects.get(id=id)
    repuesto.delete()
    return redirect('listado_repuestos')


# ==============================================================================
# VISTAS API REST - VIEWSETS
# ==============================================================================
class RepuestoViewSet(viewsets.ModelViewSet):
    queryset = Repuesto.objects.all().order_by('id')
    serializer_class = RepuestoSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_destroy(self, instance):
        if instance.imagen:
            instance.imagen.storage.delete(instance.imagen.name)
        instance.delete()

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def estadisticas(self, request):
        total = Repuesto.objects.count()
        bajo_stock = Repuesto.objects.filter(stock__lte=2).count()
        categorias = Repuesto.objects.values_list('categoria', flat=True).distinct()
        return Response({
            'total_repuestos': total,
            'bajo_stock_alerta': bajo_stock,
            'categorias_disponibles': list(categorias),
            'empresa': 'TechParts Limitada'
        }, status=status.HTTP_200_OK)


# ==============================================================================
# VISTAS API REST - GENERICS
# ==============================================================================
class RepuestoListGenericView(generics.ListCreateAPIView):
    queryset = Repuesto.objects.all().order_by('id')
    serializer_class = RepuestoSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RepuestoDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Repuesto.objects.all()
    serializer_class = RepuestoSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ==============================================================================
# VISTAS API REST - FUNCTION BASED VIEWS (@api_view)
# ==============================================================================
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def repuesto_list_fbv(request):
    if request.method == 'GET':
        repuestos = Repuesto.objects.all().order_by('id')
        serializer = RepuestoSerializer(repuestos, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = RepuestoSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def repuesto_detail_fbv(request, pk):
    try:
        repuesto = Repuesto.objects.get(pk=pk)
    except Repuesto.DoesNotExist:
        return Response({'detail': f'Repuesto con id {pk} no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RepuestoSerializer(repuesto, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = RepuestoSerializer(repuesto, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if repuesto.imagen:
            repuesto.imagen.storage.delete(repuesto.imagen.name)
        repuesto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==============================================================================
# VISTA REGISTRO DE USUARIOS
# ==============================================================================
class RegistroUsuarioView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistroSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'mensaje': 'Usuario registrado exitosamente',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                },
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
