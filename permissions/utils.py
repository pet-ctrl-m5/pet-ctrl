def verify_request_kwargs(request, model):
    pk = request.parser_context["kwargs"]["pk"]

    user = model.objects.get(pk=pk)

    return user
