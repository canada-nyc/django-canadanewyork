def add_to_middleware(MIDDLEWARE_CLASSES, middleware, prepend=False):
    if middleware not in MIDDLEWARE_CLASSES:
        if prepend:
            return (middleware,) + MIDDLEWARE_CLASSES
        else:
            return MIDDLEWARE_CLASSES + (middleware,)
    else:
        return MIDDLEWARE_CLASSES
