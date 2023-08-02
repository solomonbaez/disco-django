from rest_framework.decorators import api_view
from rest_framework.response import Response


# restrict requests
@api_view(
    [
        "GET",
    ]
)
def getRoutes(request):
    routes = [
        "GET /api",
        "GET /api/rooms",
        "GET /api/rooms/:id",
    ]
    # restrict to python
    return Response(routes)
