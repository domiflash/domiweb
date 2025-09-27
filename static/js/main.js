// DomiFlash - JavaScript Principal
// Funcionalidades avanzadas para la interfaz de usuario

class DomiFlashUI {
    constructor() {
        this.cart = {
            items: [],
            total: 0,
            count: 0
        };
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initAnimations();
        this.initSearchAndFilters();
        this.initCartFunctionality();
        console.log('🍕 DomiFlash UI iniciado correctamente');
    }

    setupEventListeners() {
        // Toggle para menú móvil
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const mobileMenu = document.getElementById('mobile-menu');
        
        if (mobileMenuBtn && mobileMenu) {
            mobileMenuBtn.addEventListener('click', () => {
                mobileMenu.classList.toggle('hidden');
                this.animateMenuToggle(mobileMenu);
            });
        }

        // Smooth scroll para enlaces internos
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });

        // Cerrar menú móvil al hacer clic fuera
        document.addEventListener('click', (e) => {
            if (mobileMenu && !mobileMenu.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
                mobileMenu.classList.add('hidden');
            }
        });
    }

    animateMenuToggle(menu) {
        if (!menu.classList.contains('hidden')) {
            menu.style.opacity = '0';
            menu.style.transform = 'translateY(-10px)';
            
            setTimeout(() => {
                menu.style.transition = 'all 0.3s ease-out';
                menu.style.opacity = '1';
                menu.style.transform = 'translateY(0)';
            }, 10);
        }
    }

    initAnimations() {
        // Intersection Observer para animaciones on scroll
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in-up');
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        // Observar elementos con clase 'scroll-animate'
        document.querySelectorAll('.scroll-animate').forEach((el, index) => {
            // Preparar elementos para animación
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = `all 0.6s ease-out ${index * 0.1}s`;
            
            observer.observe(el);
        });

        // Animación de números contadores
        this.animateCounters();

        // Parallax suave en hero section
        this.initParallax();
    }

    animateCounters() {
        const counters = document.querySelectorAll('[data-counter]');
        
        counters.forEach(counter => {
            const target = parseInt(counter.dataset.counter);
            const increment = target / 50;
            let current = 0;
            
            const timer = setInterval(() => {
                current += increment;
                counter.textContent = Math.floor(current);
                
                if (current >= target) {
                    counter.textContent = target;
                    clearInterval(timer);
                }
            }, 30);
        });
    }

    initParallax() {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const parallaxElements = document.querySelectorAll('.parallax');
            
            parallaxElements.forEach(element => {
                const speed = element.dataset.speed || 0.5;
                const yPos = -(scrolled * speed);
                element.style.transform = `translate3d(0, ${yPos}px, 0)`;
            });
        });
    }

    initSearchAndFilters() {
        const searchInput = document.getElementById('search-restaurants');
        const filterBtns = document.querySelectorAll('.filter-btn');
        const sortSelect = document.getElementById('sort-restaurants');
        
        if (searchInput) {
            // Debounce search
            let searchTimeout;
            searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    this.filterRestaurants(e.target.value.toLowerCase());
                }, 300);
            });
        }

        if (filterBtns.length > 0) {
            filterBtns.forEach(btn => {
                btn.addEventListener('click', () => {
                    filterBtns.forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    this.filterByCategory(btn.dataset.filter);
                });
            });
        }

        if (sortSelect) {
            sortSelect.addEventListener('change', (e) => {
                this.sortRestaurants(e.target.value);
            });
        }
    }

    filterRestaurants(searchTerm) {
        const restaurants = document.querySelectorAll('.restaurant-card');
        let visibleCount = 0;
        
        restaurants.forEach(restaurant => {
            const name = restaurant.querySelector('h3').textContent.toLowerCase();
            const isVisible = name.includes(searchTerm);
            
            if (isVisible) {
                restaurant.style.display = 'block';
                this.animateIn(restaurant);
                visibleCount++;
            } else {
                restaurant.style.display = 'none';
            }
        });

        this.updateResultsCount(visibleCount);
        this.toggleNoResults(visibleCount === 0);
    }

    filterByCategory(category) {
        const restaurants = document.querySelectorAll('.restaurant-card');
        let visibleCount = 0;
        
        restaurants.forEach(restaurant => {
            const restaurantCategory = restaurant.dataset.category;
            const isVisible = category === 'all' || restaurantCategory === category;
            
            if (isVisible) {
                restaurant.style.display = 'block';
                this.animateIn(restaurant);
                visibleCount++;
            } else {
                restaurant.style.display = 'none';
            }
        });

        this.updateResultsCount(visibleCount);
        this.toggleNoResults(visibleCount === 0);
    }

    sortRestaurants(sortBy) {
        const container = document.getElementById('restaurants-grid');
        const restaurants = Array.from(container.querySelectorAll('.restaurant-card'));
        
        restaurants.sort((a, b) => {
            switch (sortBy) {
                case 'rating':
                    const ratingA = parseFloat(a.querySelector('.bg-green-500 span:last-child').textContent);
                    const ratingB = parseFloat(b.querySelector('.bg-green-500 span:last-child').textContent);
                    return ratingB - ratingA;
                case 'delivery':
                    const timeA = parseInt(a.querySelector('.bg-domi-yellow span:last-child').textContent);
                    const timeB = parseInt(b.querySelector('.bg-domi-yellow span:last-child').textContent);
                    return timeA - timeB;
                default:
                    return 0;
            }
        });

        // Reorganizar DOM
        restaurants.forEach(restaurant => {
            container.appendChild(restaurant);
        });

        // Animar cambios
        this.staggerAnimation(restaurants);
    }

    updateResultsCount(count) {
        const counter = document.getElementById('results-count');
        if (counter) {
            counter.textContent = count;
        }
    }

    toggleNoResults(show) {
        const noResults = document.getElementById('no-results');
        const grid = document.getElementById('restaurants-grid');
        
        if (noResults && grid) {
            if (show) {
                grid.style.display = 'none';
                noResults.classList.remove('hidden');
            } else {
                grid.style.display = 'grid';
                noResults.classList.add('hidden');
            }
        }
    }

    animateIn(element) {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'all 0.3s ease-out';
        
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, 10);
    }

    staggerAnimation(elements) {
        elements.forEach((el, index) => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                el.style.transition = 'all 0.4s ease-out';
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            }, index * 50);
        });
    }

    initCartFunctionality() {
        // Mejorar formularios de agregar al carrito
        document.querySelectorAll('.add-to-cart-form').forEach(form => {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.addToCartAnimation(form);
                
                // Enviar formulario después de animación
                setTimeout(() => {
                    form.submit();
                }, 800);
            });
        });

        // Actualizar contador del carrito
        this.updateCartCount();
    }

    addToCartAnimation(form) {
        const btn = form.querySelector('button[type="submit"]');
        const originalText = btn.innerHTML;
        
        // Animación del botón
        btn.innerHTML = '<span class="flex items-center justify-center gap-1"><span class="animate-spin">⏳</span><span>Agregando...</span></span>';
        btn.disabled = true;
        btn.classList.add('animate-pulse');
        
        // Simular añadir al carrito
        setTimeout(() => {
            btn.innerHTML = '<span class="flex items-center justify-center gap-1"><span>✅</span><span>¡Agregado!</span></span>';
            btn.classList.remove('animate-pulse');
            btn.classList.add('bg-green-500');
            
            // Mostrar notificación
            this.showToast('¡Producto agregado al carrito!', 'success');
            
            // Restaurar botón
            setTimeout(() => {
                btn.innerHTML = originalText;
                btn.disabled = false;
                btn.classList.remove('bg-green-500');
            }, 1500);
        }, 600);

        // Efecto de "volar" hacia el carrito
        this.flyToCart(btn);
    }

    flyToCart(element) {
        const rect = element.getBoundingClientRect();
        const cartIcon = document.querySelector('[data-cart-icon]');
        
        if (cartIcon) {
            const cartRect = cartIcon.getBoundingClientRect();
            
            // Crear elemento que "vuela"
            const flyingEl = document.createElement('div');
            flyingEl.innerHTML = '🛒';
            flyingEl.style.position = 'fixed';
            flyingEl.style.left = rect.left + 'px';
            flyingEl.style.top = rect.top + 'px';
            flyingEl.style.fontSize = '24px';
            flyingEl.style.zIndex = '9999';
            flyingEl.style.pointerEvents = 'none';
            flyingEl.style.transition = 'all 0.8s cubic-bezier(0.2, 0.9, 0.3, 1)';
            
            document.body.appendChild(flyingEl);
            
            // Animar hacia el carrito
            setTimeout(() => {
                flyingEl.style.left = cartRect.left + 'px';
                flyingEl.style.top = cartRect.top + 'px';
                flyingEl.style.opacity = '0';
                flyingEl.style.transform = 'scale(0.5)';
            }, 10);
            
            // Remover elemento
            setTimeout(() => {
                document.body.removeChild(flyingEl);
            }, 800);
        }
    }

    updateCartCount() {
        // Esta función se llamaría desde el servidor para actualizar el contador
        const cartBadge = document.querySelector('[data-cart-count]');
        if (cartBadge) {
            // Animación del badge cuando cambia
            cartBadge.classList.add('animate-bounce');
            setTimeout(() => {
                cartBadge.classList.remove('animate-bounce');
            }, 600);
        }
    }

    // Función para toggle de productos en menú (compatibilidad)
    toggleProductos(idres) {
        const productosDiv = document.getElementById(`productos-${idres}`);
        if (productosDiv) {
            const isHidden = productosDiv.classList.contains('hidden');
            
            if (isHidden) {
                productosDiv.classList.remove('hidden');
                productosDiv.style.opacity = '0';
                productosDiv.style.transform = 'translateY(-10px)';
                
                setTimeout(() => {
                    productosDiv.style.transition = 'all 0.3s ease-out';
                    productosDiv.style.opacity = '1';
                    productosDiv.style.transform = 'translateY(0)';
                }, 10);
            } else {
                productosDiv.style.opacity = '0';
                productosDiv.style.transform = 'translateY(-10px)';
                
                setTimeout(() => {
                    productosDiv.classList.add('hidden');
                }, 300);
            }
        }
    }

    // Función para mostrar notificaciones toast mejoradas
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };
        
        toast.className = `fixed top-4 right-4 z-50 px-6 py-4 rounded-lg shadow-xl transform translate-x-full transition-all duration-300 ${this.getToastClasses(type)} backdrop-blur-sm`;
        toast.innerHTML = `
            <div class="flex items-center gap-3">
                <span class="text-xl">${icons[type] || icons.info}</span>
                <span class="font-medium">${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-2 text-white hover:text-gray-200 transition-colors">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                    </svg>
                </button>
            </div>
        `;

        document.body.appendChild(toast);

        // Animar entrada
        setTimeout(() => {
            toast.classList.remove('translate-x-full');
        }, 100);

        // Auto-remover después de 4 segundos
        setTimeout(() => {
            toast.classList.add('translate-x-full');
            setTimeout(() => {
                if (document.body.contains(toast)) {
                    document.body.removeChild(toast);
                }
            }, 300);
        }, 4000);
    }

    getToastClasses(type) {
        const classes = {
            success: 'bg-green-500 text-white border-l-4 border-green-600',
            error: 'bg-red-500 text-white border-l-4 border-red-600',
            warning: 'bg-yellow-500 text-white border-l-4 border-yellow-600',
            info: 'bg-blue-500 text-white border-l-4 border-blue-600'
        };
        return classes[type] || classes.info;
    }

    // Función para loading states mejorada
    showLoading(button, duration = 2000) {
        const originalText = button.innerHTML;
        const originalClasses = button.className;
        
        button.innerHTML = `
            <span class="flex items-center justify-center gap-2">
                <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
                <span>Cargando...</span>
            </span>
        `;
        button.disabled = true;
        button.classList.add('opacity-75', 'cursor-not-allowed');
        
        return setTimeout(() => {
            button.innerHTML = originalText;
            button.disabled = false;
            button.className = originalClasses;
        }, duration);
    }
}

// Funciones globales para compatibilidad con templates existentes
function toggleProductos(idres) {
    if (window.domiUI) {
        window.domiUI.toggleProductos(idres);
    }
}

function clearFilters() {
    const searchInput = document.getElementById('search-restaurants');
    const allFilter = document.querySelector('.filter-btn[data-filter="all"]');
    const sortSelect = document.getElementById('sort-restaurants');
    
    if (searchInput) searchInput.value = '';
    if (allFilter) {
        document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
        allFilter.classList.add('active');
    }
    if (sortSelect) sortSelect.value = 'popular';
    
    // Mostrar todos los restaurantes
    document.querySelectorAll('.restaurant-card').forEach(card => {
        card.style.display = 'block';
    });
    
    document.getElementById('no-results')?.classList.add('hidden');
    document.getElementById('restaurants-grid')?.style.setProperty('display', 'grid');
}

// ===============================================
// WEEK 4 - PREMIUM FEATURES
// ===============================================

// Sistema de Dark Mode
class DarkModeManager {
    constructor() {
        this.isDark = localStorage.getItem('domiflash-theme') === 'dark' || 
                     (localStorage.getItem('domiflash-theme') === null && 
                      window.matchMedia('(prefers-color-scheme: dark)').matches);
        this.init();
    }

    init() {
        this.applyTheme();
        this.createToggle();
        this.setupSystemListener();
    }

    createToggle() {
        const nav = document.querySelector('nav, header');
        if (!nav || document.getElementById('dark-toggle')) return;

        const toggleHTML = `
            <button id="dark-toggle" 
                    class="p-2 rounded-lg transition-all duration-300 hover:bg-gray-200 dark:hover:bg-gray-700 ml-4"
                    title="Cambiar tema">
                <span class="text-xl">${this.isDark ? '☀️' : '🌙'}</span>
            </button>
        `;

        nav.insertAdjacentHTML('beforeend', toggleHTML);
        
        document.getElementById('dark-toggle').addEventListener('click', () => {
            this.toggle();
        });
    }

    toggle() {
        this.isDark = !this.isDark;
        this.applyTheme();
        localStorage.setItem('domiflash-theme', this.isDark ? 'dark' : 'light');
        
        const toggle = document.getElementById('dark-toggle');
        if (toggle) {
            toggle.querySelector('span').textContent = this.isDark ? '☀️' : '🌙';
        }

        if (window.domiUI) {
            window.domiUI.showToast(`Modo ${this.isDark ? 'oscuro' : 'claro'} activado`, 'info');
        }
    }

    applyTheme() {
        const html = document.documentElement;
        
        if (this.isDark) {
            html.classList.add('dark');
            html.style.colorScheme = 'dark';
        } else {
            html.classList.remove('dark');
            html.style.colorScheme = 'light';
        }
    }

    setupSystemListener() {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('domiflash-theme')) {
                this.isDark = e.matches;
                this.applyTheme();
            }
        });
    }
}

// PWA Service Worker Manager
class PWAManager {
    constructor() {
        this.init();
    }

    async init() {
        if ('serviceWorker' in navigator) {
            try {
                await this.registerServiceWorker();
                this.setupInstallPrompt();
                this.setupUpdateNotifications();
                console.log('🔥 PWA capabilities initialized');
            } catch (error) {
                console.warn('PWA initialization failed:', error);
            }
        }
    }

    async registerServiceWorker() {
        const registration = await navigator.serviceWorker.register('/static/sw.js');
        
        registration.addEventListener('updatefound', () => {
            const newWorker = registration.installing;
            newWorker.addEventListener('statechange', () => {
                if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                    this.showUpdateNotification();
                }
            });
        });
    }

    setupInstallPrompt() {
        let deferredPrompt;

        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            this.showInstallBanner();
        });

        window.addEventListener('appinstalled', () => {
            if (window.domiUI) {
                window.domiUI.showToast('🎉 ¡DomiFlash instalado exitosamente!', 'success');
            }
            this.hideInstallBanner();
        });
    }

    showInstallBanner() {
        const banner = document.createElement('div');
        banner.id = 'install-banner';
        banner.className = 'fixed bottom-4 left-4 right-4 bg-domi-orange text-white p-4 rounded-lg shadow-lg z-50 flex items-center justify-between transform translate-y-full transition-all duration-300';
        banner.innerHTML = `
            <div class="flex items-center gap-3">
                <span class="text-2xl">📱</span>
                <div>
                    <p class="font-bold">¡Instala DomiFlash!</p>
                    <p class="text-sm opacity-90">Acceso rápido desde tu pantalla de inicio</p>
                </div>
            </div>
            <div class="flex gap-2">
                <button id="install-app" class="bg-white text-domi-orange px-4 py-2 rounded-lg font-medium hover:bg-gray-100 transition-colors">
                    Instalar
                </button>
                <button id="dismiss-install" class="text-white hover:text-gray-200">
                    ✕
                </button>
            </div>
        `;

        document.body.appendChild(banner);
        
        setTimeout(() => {
            banner.classList.remove('translate-y-full');
        }, 100);

        document.getElementById('install-app').addEventListener('click', async () => {
            const deferredPrompt = window.deferredPrompt;
            if (deferredPrompt) {
                deferredPrompt.prompt();
                const { outcome } = await deferredPrompt.userChoice;
                console.log('Install prompt outcome:', outcome);
                window.deferredPrompt = null;
            }
            this.hideInstallBanner();
        });

        document.getElementById('dismiss-install').addEventListener('click', () => {
            this.hideInstallBanner();
        });
    }

    hideInstallBanner() {
        const banner = document.getElementById('install-banner');
        if (banner) {
            banner.classList.add('translate-y-full');
            setTimeout(() => banner.remove(), 300);
        }
    }

    showUpdateNotification() {
        if (window.domiUI) {
            const updateToast = document.createElement('div');
            updateToast.className = 'fixed top-4 right-4 z-50 bg-blue-500 text-white p-4 rounded-lg shadow-lg max-w-sm';
            updateToast.innerHTML = `
                <div class="flex items-center gap-3">
                    <span class="text-xl">🔄</span>
                    <div class="flex-1">
                        <p class="font-bold">Nueva versión disponible</p>
                        <p class="text-sm opacity-90">Reinicia para actualizar</p>
                    </div>
                    <button onclick="window.location.reload()" 
                            class="bg-white text-blue-500 px-3 py-1 rounded text-sm font-medium hover:bg-gray-100">
                        Actualizar
                    </button>
                </div>
            `;
            document.body.appendChild(updateToast);

            setTimeout(() => {
                updateToast.remove();
            }, 10000);
        }
    }
}

// Performance Monitor
class PerformanceMonitor {
    constructor() {
        this.metrics = {
            loadTime: 0,
            interactions: 0,
            errors: 0,
            memoryUsage: 0
        };
        this.init();
    }

    init() {
        this.measureLoadTime();
        this.setupErrorTracking();
        this.setupPerformanceObserver();
        this.startMemoryMonitoring();
    }

    measureLoadTime() {
        window.addEventListener('load', () => {
            const loadTime = performance.now();
            this.metrics.loadTime = loadTime;
            
            // Mostrar métricas en desarrollo
            if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
                console.log(`🚀 Page loaded in ${Math.round(loadTime)}ms`);
                this.showPerformanceIndicator(loadTime);
            }
        });
    }

    setupErrorTracking() {
        window.addEventListener('error', (e) => {
            this.metrics.errors++;
            console.error('DomiFlash Error:', e.error);
        });

        window.addEventListener('unhandledrejection', (e) => {
            this.metrics.errors++;
            console.error('Unhandled Promise Rejection:', e.reason);
        });
    }

    setupPerformanceObserver() {
        if ('PerformanceObserver' in window) {
            const observer = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    if (entry.entryType === 'largest-contentful-paint') {
                        console.log(`📊 LCP: ${Math.round(entry.startTime)}ms`);
                    }
                }
            });
            observer.observe({ entryTypes: ['largest-contentful-paint'] });
        }
    }

    startMemoryMonitoring() {
        if ('memory' in performance) {
            setInterval(() => {
                const memory = performance.memory;
                this.metrics.memoryUsage = memory.usedJSHeapSize;
                
                // Alertar si el uso de memoria es alto
                if (memory.usedJSHeapSize / memory.jsHeapSizeLimit > 0.8) {
                    console.warn('⚠️ High memory usage detected');
                }
            }, 30000);
        }
    }

    showPerformanceIndicator(loadTime) {
        const indicator = document.createElement('div');
        indicator.className = 'fixed bottom-4 right-4 bg-green-500 text-white px-3 py-2 rounded-lg text-sm font-medium z-50';
        indicator.textContent = `⚡ ${Math.round(loadTime)}ms`;
        
        document.body.appendChild(indicator);
        
        setTimeout(() => {
            indicator.style.opacity = '0';
            setTimeout(() => indicator.remove(), 300);
        }, 3000);
    }
}

// Offline Mode Manager
class OfflineManager {
    constructor() {
        this.isOnline = navigator.onLine;
        this.init();
    }

    init() {
        this.setupConnectionListeners();
        this.setupOfflineUI();
    }

    setupConnectionListeners() {
        window.addEventListener('online', () => {
            this.isOnline = true;
            this.hideOfflineBanner();
            if (window.domiUI) {
                window.domiUI.showToast('🌐 Conexión restaurada', 'success');
            }
        });

        window.addEventListener('offline', () => {
            this.isOnline = false;
            this.showOfflineBanner();
        });
    }

    showOfflineBanner() {
        if (document.getElementById('offline-banner')) return;

        const banner = document.createElement('div');
        banner.id = 'offline-banner';
        banner.className = 'fixed top-0 left-0 right-0 bg-red-500 text-white p-3 text-center z-50 transform -translate-y-full transition-transform duration-300';
        banner.innerHTML = `
            <div class="flex items-center justify-center gap-2">
                <span>📡</span>
                <span class="font-medium">Sin conexión - Algunas funciones pueden no estar disponibles</span>
            </div>
        `;

        document.body.appendChild(banner);
        
        setTimeout(() => {
            banner.classList.remove('-translate-y-full');
        }, 100);
    }

    hideOfflineBanner() {
        const banner = document.getElementById('offline-banner');
        if (banner) {
            banner.classList.add('-translate-y-full');
            setTimeout(() => banner.remove(), 300);
        }
    }

    setupOfflineUI() {
        // Deshabilitar botones de envío cuando esté offline
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!this.isOnline) {
                    e.preventDefault();
                    if (window.domiUI) {
                        window.domiUI.showToast('❌ Sin conexión - No se puede enviar el formulario', 'error');
                    }
                }
            });
        });
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    // Inicializar UI principal
    window.domiUI = new DomiFlashUI();
    
    // Inicializar características premium de Week 4
    window.darkMode = new DarkModeManager();
    window.pwaManager = new PWAManager();
    window.performanceMonitor = new PerformanceMonitor();
    window.offlineManager = new OfflineManager();
    
    console.log('🎉 DomiFlash Premium Features activadas');
    
    // Easter egg - Konami code
    let konamiCode = [];
    const targetCode = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65];
    
    document.addEventListener('keydown', (e) => {
        konamiCode.push(e.keyCode);
        if (konamiCode.length > targetCode.length) {
            konamiCode.shift();
        }
        
        if (konamiCode.length === targetCode.length && 
            konamiCode.every((code, index) => code === targetCode[index])) {
            window.domiUI.showToast('🎉 ¡Código secreto activado! ¡Envío gratis en tu próximo pedido!', 'success');
            document.body.style.filter = 'hue-rotate(45deg)';
            setTimeout(() => {
                document.body.style.filter = '';
            }, 3000);
        }
    });
    
    // Accessibility features
    setupAccessibilityFeatures();
    
    // Preload critical resources
    preloadCriticalResources();
});

// Función global para mostrar notificaciones desde Flask
window.showToast = function(message, type) {
    if (window.domiUI) {
        window.domiUI.showToast(message, type);
    }
};

// Funciones de accesibilidad
function setupAccessibilityFeatures() {
    // Navegación por teclado mejorada
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-navigation');
        }
    });
    
    document.addEventListener('mousedown', () => {
        document.body.classList.remove('keyboard-navigation');
    });

    // Skip links para navegación
    if (!document.querySelector('.skip-link')) {
        const skipLink = document.createElement('a');
        skipLink.className = 'skip-link absolute -top-10 left-0 bg-domi-orange text-white p-2 z-50 transition-all focus:top-0';
        skipLink.href = '#main-content';
        skipLink.textContent = 'Saltar al contenido principal';
        document.body.insertBefore(skipLink, document.body.firstChild);
    }

    // Mejorar contraste automáticamente en dark mode
    const contrastObserver = new MutationObserver(() => {
        if (document.documentElement.classList.contains('dark')) {
            document.body.style.setProperty('--text-contrast', '1.2');
        } else {
            document.body.style.setProperty('--text-contrast', '1');
        }
    });

    contrastObserver.observe(document.documentElement, {
        attributes: true,
        attributeFilter: ['class']
    });
}

// Preload recursos críticos
function preloadCriticalResources() {
    // Precargar imágenes críticas
    const criticalImages = [
        '/static/img/brand/logo.png',
        '/static/img/food/pizza.jpg',
        '/static/img/food/burger.jpg'
    ];

    criticalImages.forEach(src => {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.as = 'image';
        link.href = src;
        document.head.appendChild(link);
    });

    // Precargar fuentes importantes
    const fontLink = document.createElement('link');
    fontLink.rel = 'preload';
    fontLink.as = 'font';
    fontLink.type = 'font/woff2';
    fontLink.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap';
    fontLink.crossOrigin = 'anonymous';
    document.head.appendChild(fontLink);

    console.log('🚀 Recursos críticos precargados');
}

// Utility functions para performance
window.debounce = function(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

window.throttle = function(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
};

// Analytics tracking (opcional)
window.trackEvent = function(category, action, label = null) {
    if (window.gtag) {
        window.gtag('event', action, {
            event_category: category,
            event_label: label
        });
    }
    
    console.log(`📊 Event tracked: ${category} - ${action}`, label);
};