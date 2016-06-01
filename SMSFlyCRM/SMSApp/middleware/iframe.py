class UserInIframeMiddleware:
    """Intercepts user_id from GET request and puts it into session dict"""
    def process_request(self, request):
        """Set crm_user_id key into session if passed"""
        try:
            request.session['crm_user_id'] = int(request.GET['crm_user_id'])
        except KeyError:
            pass  # Don't reset value if already set
