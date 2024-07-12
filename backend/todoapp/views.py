from django.shortcuts import get_object_or_404, render
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def todo_list(request):
    if request.method == "GET":
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)



@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def todo_detail(request, pk=None):
    try:
        todo = get_object_or_404(Todo, pk=pk)

        if request.method == 'GET':
            serializer = TodoSerializer(todo)
            return Response(serializer.data)

        elif request.method in ['PUT', 'PATCH']:
            serializer = TodoSerializer(todo, data=request.data, partial=request.method == 'PATCH')
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)

        elif request.method == 'DELETE':
            todo.delete()
            return Response({"message": "Todo deleted successfully"}, status=204)

    except Todo.MultipleObjectsReturned:
        return Response({"error": "Multiple Todo objects found for the given pk"}, status=500)
    except Todo.DoesNotExist:
        return Response({"error": "Todo not found"}, status=404)
    
    