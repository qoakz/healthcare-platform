import json
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from .models import AuditLog


class AuditMiddleware(MiddlewareMixin):
    """
    Middleware to automatically log user actions
    """
    
    def process_request(self, request):
        # Skip audit logging for certain paths
        skip_paths = [
            '/admin/jsi18n/',
            '/static/',
            '/media/',
            '/favicon.ico',
            '/health/',
        ]
        
        if any(request.path.startswith(path) for path in skip_paths):
            return None
        
        # Store request info for later use
        request._audit_info = {
            'ip': self.get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'path': request.path,
            'method': request.method,
        }
    
    def process_response(self, request, response):
        # Only log for authenticated users and certain actions
        if (hasattr(request, '_audit_info') and 
            hasattr(request, 'user') and 
            request.user != AnonymousUser() and
            request.method in ['POST', 'PUT', 'PATCH', 'DELETE']):
            
            self.log_action(request, response)
        
        return response
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def log_action(self, request, response):
        """Log the action to audit trail"""
        try:
            # Determine action type based on HTTP method
            action_map = {
                'POST': 'create',
                'PUT': 'update',
                'PATCH': 'update',
                'DELETE': 'delete',
            }
            
            action = action_map.get(request.method, 'read')
            
            # Create audit log entry
            AuditLog.objects.create(
                actor=request.user,
                actor_ip=request._audit_info['ip'],
                actor_user_agent=request._audit_info['user_agent'],
                action=action,
                description=f"{request.method} {request.path}",
                metadata={
                    'path': request._audit_info['path'],
                    'method': request._audit_info['method'],
                    'status_code': response.status_code,
                }
            )
        except Exception as e:
            # Don't let audit logging break the request
            pass
