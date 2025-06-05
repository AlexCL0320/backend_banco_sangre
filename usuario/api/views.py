from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser,IsAuthenticated
from usuario.models import Usuario
from usuario.api.serializer import UsuarioSerializer
#Agregado por dalia para obtener los datos del usuario logeado
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from usuario.api.permissions import IsOwnerOrAdmin # <-- ESTO ESTÁ CORRECTO
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response



class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    def get_permissions(self):
        if self.action == 'create':  # Permitir POST para crear usuario
            return [AllowAny()]  # Permite que cualquiera cree un usuario
        elif self.action == 'list':  # Permitir GET para ver todos los usuarios
            return [AllowAny()]  # Permite que cualquiera vea los usuarios
        elif self.action == 'retrieve':  # Permitir GET para ver un usuario específico
            return [AllowAny()]  # Permite que cualquiera vea un usuario específico
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [IsAdminUser()]  # Requiere ser admin para los demás métodos (update, destroy, etc.) <

#para el usuario logeado
class UsuarioAutenticadoView(APIView):
    # Configuramos para permitir solo acceso con un token válido
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        # Obtener el usuario actual desde el token
        user = request.user
        
        # Obtener detalles del usuario
        user_data = {
            'id': user.id,
            'nombre_usuario': user.nombre_usuario,
            'correo': user.correo,
            'rol': user.rol.nombre,
        }
        
        return Response(user_data)

class RegistroView(APIView):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rol_repo = DjangoRolRepository()
        self.user_repo = DjangoUsuarioRepository(self.rol_repo)
        self.crear_usuario_uc = CrearUsuarioUseCase(self.user_repo, self.rol_repo)

    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                rol_id = data.get('rol_id')
                password = data.get('password')

                usuario_creado = self.crear_usuario_uc.execute(
                    nombre_usuario=data['nombre_usuario'],
                    correo=data['correo'],
                    sexo=data['sexo'],
                    password=password,
                    rol_id=rol_id
                )
                response_serializer = UsuarioSerializer(usuario_creado)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except EmailAlreadyExistsException as e:
                return Response({'correo': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except RolNotFoundException as e:
                return Response({'rol_id': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'detail': 'Error interno en el registro', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
