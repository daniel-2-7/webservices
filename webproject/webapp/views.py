from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import ModuleInstance, Professor, Rating, Course
from django.db.models import Avg


# Create your views here.
def home(request):
    return HttpResponse("Hello, Django!")


@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password or not email:
        return Response({"Error : All fields are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({"Error : Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
    

    try:
        user = User.objects.create_user(username=username, password=password, email=email)
        return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "message": "Login successful"}, status=status.HTTP_200_OK)

    return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_user(request):
    logout(request._request)
    return Response({"Success : Logged Out Successfully!"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def modules_list(request):
    modules = ModuleInstance.objects.prefetch_related('professors').select_related('modules')

    if not modules.exists():
        return Response({"error": "No modules found"}, status=status.HTTP_404_NOT_FOUND)
    
    data = []  
    for module in modules:
        professors_list = [
            f"{professor.professor_id}, {professor.professor_name}"
            for professor in module.professors.all()
        ]
        
        print(f"Module: {module.modules.module_name}, Professors: {professors_list}")

        data.append({  
            "module_code": module.modules.module_code,  
            "module_name": module.modules.module_name,  
            "year": module.year,
            "semester": module.get_semester_display(),  
            "professors": professors_list
        })

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def view_ratings(request):
    professors = Professor.objects.all()
    data = [
        {
            "professor_id": professor.professor_id,
            "professor_name": professor.professor_name,
            "average_rating": round(professor.rating_set.aggregate(Avg('rating'))['rating__avg'] or 0)
        }
        for professor in professors
    ]

    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def rate_professor(request):
    professor_id = request.data.get("professor_id")
    module_code = request.data.get("module_code")
    year = request.data.get("year")
    semester = request.data.get("semester")
    rating_value = request.data.get("rating")

   
    if not rating_value or not (1 <= int(rating_value) <= 5):
        return Response({"error": "Rating must be between 1 and 5"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        professor = Professor.objects.get(professor_id=professor_id)
        module_instance = ModuleInstance.objects.get(
            modules__module_code=module_code, year=year, semester=semester
        )
    except Professor.DoesNotExist:
        return Response({"error": "Professor not found"}, status=status.HTTP_404_NOT_FOUND)
    except ModuleInstance.DoesNotExist:
        return Response({"error": "Module instance not found"}, status=status.HTTP_404_NOT_FOUND)

   
    if not module_instance.professors.filter(professor_id=professor_id).exists():
        return Response(
            {"error": "This professor does not teach this module instance"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    Rating.objects.create(
        professor=professor,
        module_instance=module_instance,
        rating=rating_value
    )

    return Response({"message": "Rating submitted successfully"}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def view_prof_module_ratings(request, professor_id, module_code):
    try:
        professor = Professor.objects.get(professor_id=professor_id)
        module = Course.objects.get(module_code=module_code)
    except Professor.DoesNotExist:
        return Response({"error": "Professor not found"}, status=status.HTTP_404_NOT_FOUND)
    except Course.DoesNotExist:
        return Response({"error": "Module not found"}, status=status.HTTP_404_NOT_FOUND)

    avg_rating = Rating.objects.filter(professor=professor, module_instance__modules=module).aggregate(Avg('rating'))['rating__avg']
    
    avg_rating = round(avg_rating) if avg_rating else 0

    return Response({
        "professor_id": professor.professor_id,
        "professor_name": professor.professor_name,
        "module_code": module.module_code,
        "module_name": module.module_name,
        "average_rating": avg_rating
    }, status=status.HTTP_200_OK)