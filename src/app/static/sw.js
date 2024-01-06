self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open('connect_pwa').then(function(cache) {
            return cache.addAll([
                '/',
                '/static/vendor/bootstrap/css/bootstrap.min.css',
                '/static/vendor/bootstrap/js/bootstrap.min.js',
                '/static/vendor/jquery/js/jquery.min.js',
                '/static/vendor/popper/js/popper.min.js',
                '/static/vendor/fontawesome/css/fontawesome.min.css',
                '/static/vendor/fontawesome/css/solid.min.css',
                '/static/vendor/fontawesome/css/brands.min.css',
                '/static/vendor/aos/js/aos.js',
                '/static/vendor/aos/css/aos.css',
                '/static/js/main.js',
                '/static/js/inbox.js'
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