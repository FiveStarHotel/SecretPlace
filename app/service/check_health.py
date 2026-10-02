from fastapi import Response


def check_health():
    return Response(status_code=200)