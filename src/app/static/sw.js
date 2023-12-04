self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open('connect_pwa').then(function(cache) {
            return cache.addAll([
                '/',
                '/static/vendor/bootstrap/css/boostrap.min.css',
                '/static/js/main.js'
            ]);
        })
    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request).then(function(response) {
            return response || fetch(event.request);
        })
    );
});