def ctx(*args, **kwargs):
    context = {}
    for ctx_dict in args:
        context.update(ctx_dict)

    context.update(kwargs)
    return context
