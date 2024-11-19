import logging
from functools import wraps


logger = logging.getLogger('main')


def log_user_action(text_for_logging):
    def decorator(method):
        
        @wraps(method)
        def inner(request, *args, **kwargs):
            logger.info(f'User id({request.user.id}) - {text_for_logging}')
            return method(request, *args, **kwargs)
        return inner
    return decorator

def log_user_action_cls(text_for_logging): 
    def decorator(method): 
        @wraps(method) 
        def inner(self, *args, **kwargs): 
            user_id = self.request.user.id
            logger.info(f'User id({user_id}) - {text_for_logging}') 
            return method(self, *args, **kwargs) 
        return inner 
    return decorator