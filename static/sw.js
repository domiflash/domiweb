// DomiFlash Service Worker - PWA Support
const CACHE_NAME = 'domiflash-v1.0.0';
const OFFLINE_URL = '/offline';

// Recursos para cachear
const urlsToCache = [
    '/',
    '/static/css/tailwind.min.css',
    '/static/js/main.js',
    '/static/img/brand/logo.png',
    '/static/img/brand/favicon.ico',
    '/static/js/tailwind.config.js',
    '/offline'
];

// Instalación del Service Worker
self.addEventListener('install', event => {
    console.log('🔧 DomiFlash Service Worker installing...');
    
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('📦 Caching app resources');
                return cache.addAll(urlsToCache);
            })
            .then(() => {
                console.log('✅ Service Worker installation complete');
                return self.skipWaiting();
            })
            .catch(error => {
                console.error('❌ Service Worker installation failed:', error);
            })
    );
});

// Activación del Service Worker
self.addEventListener('activate', event => {
    console.log('🚀 DomiFlash Service Worker activating...');
    
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('🗑️ Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => {
            console.log('✅ Service Worker activation complete');
            return self.clients.claim();
        })
    );
});

// Estrategia de fetch - Cache First para assets, Network First para API
self.addEventListener('fetch', event => {
    const request = event.request;
    
    // Skip cross-origin requests
    if (!request.url.startsWith(self.location.origin)) {
        return;
    }
    
    // Skip chrome-extension and other schemes
    if (!request.url.startsWith('http')) {
        return;
    }

    event.respondWith(
        (async () => {
            // Estrategia para diferentes tipos de requests
            if (isStaticAsset(request.url)) {
                // Cache First para assets estáticos
                return cacheFirst(request);
            } else if (isAPIRequest(request.url)) {
                // Network First para API calls
                return networkFirst(request);
            } else {
                // Network First con fallback para páginas
                return networkFirstWithFallback(request);
            }
        })()
    );
});

// Cache First Strategy
async function cacheFirst(request) {
    const cached = await caches.match(request);
    if (cached) {
        console.log('📦 Served from cache:', request.url);
        return cached;
    }
    
    try {
        const response = await fetch(request);
        if (response.ok) {
            const cache = await caches.open(CACHE_NAME);
            cache.put(request, response.clone());
        }
        return response;
    } catch (error) {
        console.error('🔥 Cache first failed:', error);
        throw error;
    }
}

// Network First Strategy
async function networkFirst(request) {
    try {
        const response = await fetch(request);
        if (response.ok) {
            const cache = await caches.open(CACHE_NAME);
            cache.put(request, response.clone());
        }
        return response;
    } catch (error) {
        console.log('📦 Network failed, trying cache:', request.url);
        const cached = await caches.match(request);
        if (cached) {
            return cached;
        }
        throw error;
    }
}

// Network First with Offline Fallback
async function networkFirstWithFallback(request) {
    try {
        const response = await fetch(request);
        if (response.ok) {
            const cache = await caches.open(CACHE_NAME);
            cache.put(request, response.clone());
        }
        return response;
    } catch (error) {
        console.log('🔍 Network failed, checking cache:', request.url);
        const cached = await caches.match(request);
        if (cached) {
            return cached;
        }
        
        // Fallback para navegación offline
        if (request.mode === 'navigate') {
            const offlinePage = await caches.match(OFFLINE_URL);
            if (offlinePage) {
                return offlinePage;
            }
        }
        
        throw error;
    }
}

// Helpers
function isStaticAsset(url) {
    return url.includes('/static/') || 
           url.includes('.css') || 
           url.includes('.js') || 
           url.includes('.png') || 
           url.includes('.jpg') || 
           url.includes('.ico') || 
           url.includes('.svg') ||
           url.includes('.woff') ||
           url.includes('.woff2');
}

function isAPIRequest(url) {
    return url.includes('/api/') || 
           url.includes('/ajax/') ||
           url.includes('application/json');
}

// Background Sync para pedidos offline
self.addEventListener('sync', event => {
    if (event.tag === 'background-sync-orders') {
        console.log('🔄 Processing background sync for orders');
        event.waitUntil(processOfflineOrders());
    }
});

async function processOfflineOrders() {
    try {
        // Aquí procesarías pedidos guardados offline
        console.log('📝 Processing offline orders...');
        
        // Obtener datos del IndexedDB o localStorage
        const offlineOrders = await getOfflineOrders();
        
        for (const order of offlineOrders) {
            try {
                const response = await fetch('/api/orders', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(order)
                });
                
                if (response.ok) {
                    await removeOfflineOrder(order.id);
                    console.log('✅ Offline order processed:', order.id);
                }
            } catch (error) {
                console.error('❌ Failed to process offline order:', error);
            }
        }
    } catch (error) {
        console.error('❌ Background sync failed:', error);
    }
}

// Push notifications
self.addEventListener('push', event => {
    if (!event.data) return;
    
    const data = event.data.json();
    console.log('🔔 Push notification received:', data);
    
    const options = {
        body: data.body || 'Tu pedido ha sido actualizado',
        icon: '/static/img/brand/logo.png',
        badge: '/static/img/brand/favicon.ico',
        vibrate: [200, 100, 200],
        data: {
            url: data.url || '/',
            orderId: data.orderId
        },
        actions: [
            {
                action: 'view',
                title: 'Ver pedido',
                icon: '/static/icons/view.png'
            },
            {
                action: 'dismiss',
                title: 'Cerrar',
                icon: '/static/icons/close.png'
            }
        ]
    };
    
    event.waitUntil(
        self.registration.showNotification(data.title || 'DomiFlash', options)
    );
});

// Handle notification clicks
self.addEventListener('notificationclick', event => {
    event.notification.close();
    
    if (event.action === 'view') {
        const url = event.notification.data.url;
        event.waitUntil(
            self.clients.matchAll().then(clients => {
                // Si ya hay una ventana abierta, enfocarla
                for (const client of clients) {
                    if (client.url === url && 'focus' in client) {
                        return client.focus();
                    }
                }
                // Si no, abrir nueva ventana
                if (self.clients.openWindow) {
                    return self.clients.openWindow(url);
                }
            })
        );
    }
});

// Utility functions para offline storage
async function getOfflineOrders() {
    // Implementar con IndexedDB
    return [];
}

async function removeOfflineOrder(orderId) {
    // Implementar con IndexedDB
    console.log('Removing offline order:', orderId);
}

console.log('🎉 DomiFlash Service Worker loaded successfully');