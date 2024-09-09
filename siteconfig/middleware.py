import logging
import time

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('django.request')

    def __call__(self, request):
        # Captura o tempo de início da requisição
        start_time = time.time()
        
        # Adiciona informações iniciais ao log
        self.logger.info('Request received', extra={
            'client_ip': self.get_client_ip(request),
            'method': request.method,
            'url': request.get_full_path(),
            'user': str(request.user) if request.user.is_authenticated else 'Anonymous',
            'headers': dict(request.headers),  # Converte os cabeçalhos para um dicionário para uma visualização mais limpa
        })
        
        # Processa a requisição
        response = self.get_response(request)

        # Captura o tempo de resposta
        response_time = time.time() - start_time
        
        # Adiciona informações da resposta ao log
        self.logger.info('Response generated', extra={
            'client_ip': self.get_client_ip(request),
            'method': request.method,
            'url': request.get_full_path(),
            'status_code': response.status_code,
            'response_time': f'{response_time:.2f}s',
        })
        
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
