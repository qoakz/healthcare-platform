from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import AuditLog
from users.permissions import IsAdmin


class AuditLogListView(generics.ListAPIView):
    """
    List audit logs (admin only)
    """
    queryset = AuditLog.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['actor', 'action', 'entity', 'entity_id']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']
    
    def get_queryset(self):
        return AuditLog.objects.all()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsAdmin])
def audit_stats(request):
    """
    Get audit log statistics (admin only)
    """
    total_logs = AuditLog.objects.count()
    
    # Logs by action
    by_action = {}
    for choice in AuditLog.ACTION_CHOICES:
        count = AuditLog.objects.filter(action=choice[0]).count()
        by_action[choice[0]] = count
    
    # Logs by entity
    by_entity = {}
    for choice in AuditLog.ENTITY_CHOICES:
        count = AuditLog.objects.filter(entity=choice[0]).count()
        by_entity[choice[0]] = count
    
    # Recent activity
    recent_logs = AuditLog.objects.order_by('-timestamp')[:10]
    
    return Response({
        'total_logs': total_logs,
        'by_action': by_action,
        'by_entity': by_entity,
        'recent_logs': [
            {
                'id': log.id,
                'actor': log.actor.get_full_name() if log.actor else 'System',
                'action': log.action,
                'entity': log.entity,
                'entity_id': log.entity_id,
                'timestamp': log.timestamp
            }
            for log in recent_logs
        ]
    })
