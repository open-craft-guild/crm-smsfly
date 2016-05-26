class UserInIframeMiddleware:
    """Intercepts user_id from GET request and puts it into session dict"""
    def process_request(self, request):
        """Set crm_user_id key into session. Fallback to -1"""
        request.session['crm_user_id'] = request.GET.get('crm_user_id', -1)
