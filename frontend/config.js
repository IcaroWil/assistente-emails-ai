(() => {
    const params = new URLSearchParams(location.search);
    const apiFromQuery = params.get('api');
    const isLocal = location.hostname === 'localhost' || location.hostname === '127.0.0.1';
    window.API_BASE_URL = (apiFromQuery || (isLocal ? 'http://localhost:8000' : '/api')).replace(/\/$/, '');
})();