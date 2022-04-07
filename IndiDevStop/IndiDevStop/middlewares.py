from IndiDevStop.web.views import ErrorView, Error404View


def handle_exception(get_response):
    def middleware(request):

        response = get_response(request)
        if response.status_code == 404:
            return Error404View.as_view()(request)

        else:
            if response.status_code >= 405:
                return ErrorView.as_view()(request)

        return response

    return middleware
