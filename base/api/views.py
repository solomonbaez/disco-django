from django.http import JsonResponse


def getRoutes(request):
    routes = [
        "GET /api",
        "GET /api/rooms",
        "GET /api/rooms/:id",
    ]
    # restrict to python
    return JsonResponse(routes, safe=False)
