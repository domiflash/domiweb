// DomiFlash - Sistema de Gestión de Delivery
// Archivo JavaScript principal - versión corregida

class DomiFlashUI {
    constructor() {
        this.init();
    }

    init() {
        document.addEventListener('DOMContentLoaded', () => {
            this.initTheme();
            this.initNavigation();
            this.initSearch();
            this.initFilters();
            this.initAnimations();
            this.initFormValidation();
            this.initTooltips();
            this.initModals();
            this.initServiceWorker();
        });
    }

    // Sistema de temas
    initTheme() {
        const themeToggle = document.getElementById('theme-toggle');
        const htmlElement = document.documentElement;
        
        // Cargar tema guardado
        const savedTheme = localStorage.getItem('domi-theme') || 'light';
        htmlElement.setAttribute('data-theme', savedTheme);
        
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                const currentTheme = htmlElement.getAttribute('data-theme');
                const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
                
                htmlElement.setAttribute('data-theme', newTheme);
                localStorage.setItem('domi-theme', newTheme);
                
                this.showToast(`Tema ${newTheme === 'dark' ? 'oscuro' : 'claro'} activado`, 'success');
            });
        }
    }

    // Navegación
    initNavigation() {
        const navToggle = document.getElementById('nav-toggle');
        const navMobile = document.getElementById('nav-mobile');
        const navClose = document.getElementById('nav-close');
        
        if (navToggle && navMobile) {
            navToggle.addEventListener('click', () => {
                navMobile.classList.toggle('hidden');
            });
        }
        
        if (navClose && navMobile) {
            navClose.addEventListener('click', () => {
                navMobile.classList.add('hidden');
            });
        }
        
        // Cerrar navegación al hacer click fuera
        document.addEventListener('click', (e) => {
            if (navMobile && !navMobile.contains(e.target) && !navToggle?.contains(e.target)) {
                navMobile.classList.add('hidden');
            }
        });
    }

    // Sistema de búsqueda
    initSearch() {
        const searchInput = document.getElementById('search-restaurants');
        const searchButton = document.getElementById('search-button');
        
        if (searchInput) {
            let searchTimeout;
            
            searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    this.filterRestaurants(e.target.value);
                }, 300);
            });
            
            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    this.filterRestaurants(e.target.value);
                }
            });
        }
        
        if (searchButton) {
            searchButton.addEventListener('click', () => {
                if (searchInput) {
                    this.filterRestaurants(searchInput.value);
                }
            });
        }
    }

    // Filtros de restaurantes
    initFilters() {
        const filterButtons = document.querySelectorAll('.filter-btn');
        
        filterButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                // Remover clase activa de todos los botones
                filterButtons.forEach(b => b.classList.remove('active'));
                // Agregar clase activa al botón clickeado
                btn.classList.add('active');
                
                const category = btn.dataset.category;
                this.filterByCategory(category);
            });
        });
    }

    filterRestaurants(searchTerm) {
        const restaurants = document.querySelectorAll('.restaurant-card');
        const searchLower = searchTerm.toLowerCase();
        
        restaurants.forEach(restaurant => {
            const name = restaurant.dataset.name?.toLowerCase() || '';
            const cuisine = restaurant.dataset.cuisine?.toLowerCase() || '';
            
            if (name.includes(searchLower) || cuisine.includes(searchLower)) {
                restaurant.style.display = 'block';
                restaurant.classList.remove('hidden');
            } else {
                restaurant.style.display = 'none';
                restaurant.classList.add('hidden');
            }
        });
    }

    filterByCategory(category) {
        const restaurants = document.querySelectorAll('.restaurant-card');
        
        restaurants.forEach(restaurant => {
            const restaurantCategory = restaurant.dataset.category;
            
            if (category === 'all' || restaurantCategory === category) {
                restaurant.style.display = 'block';
                restaurant.classList.remove('hidden');
            } else {
                restaurant.style.display = 'none';
                restaurant.classList.add('hidden');
            }
        });
    }

    // Animaciones
    initAnimations() {
        // Observador de intersección para animaciones
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fadeIn');
                }
            });
        });

        // Observar elementos con animación
        document.querySelectorAll('.animate-on-scroll').forEach(el => {
            observer.observe(el);
        });
    }

    // Validación de formularios
    initFormValidation() {
        const forms = document.querySelectorAll('form[data-validate]');
        
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!this.validateForm(form)) {
                    e.preventDefault();
                }
            });
        });
    }

    validateForm(form) {
        let isValid = true;
        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                this.showFieldError(input, 'Este campo es obligatorio');
                isValid = false;
            } else {
                this.clearFieldError(input);
            }
        });
        
        // Validar email
        const emailInputs = form.querySelectorAll('input[type="email"]');
        emailInputs.forEach(input => {
            if (input.value && !this.isValidEmail(input.value)) {
                this.showFieldError(input, 'Email no válido');
                isValid = false;
            }
        });
        
        return isValid;
    }

    showFieldError(input, message) {
        this.clearFieldError(input);
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error text-red-500 text-sm mt-1';
        errorDiv.textContent = message;
        
        input.parentNode.appendChild(errorDiv);
        input.classList.add('border-red-500');
    }

    clearFieldError(input) {
        const existingError = input.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
        input.classList.remove('border-red-500');
    }

    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Tooltips
    initTooltips() {
        const tooltipElements = document.querySelectorAll('[data-tooltip]');
        
        tooltipElements.forEach(element => {
            element.addEventListener('mouseenter', (e) => {
                this.showTooltip(e.target);
            });
            
            element.addEventListener('mouseleave', (e) => {
                this.hideTooltip(e.target);
            });
        });
    }

    showTooltip(element) {
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip absolute bg-gray-800 text-white text-sm px-2 py-1 rounded shadow-lg z-50';
        tooltip.textContent = element.dataset.tooltip;
        
        document.body.appendChild(tooltip);
        
        const rect = element.getBoundingClientRect();
        tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
        tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
        
        element._tooltip = tooltip;
    }

    hideTooltip(element) {
        if (element._tooltip) {
            document.body.removeChild(element._tooltip);
            delete element._tooltip;
        }
    }

    // Modales
    initModals() {
        const modalTriggers = document.querySelectorAll('[data-modal]');
        const modalCloses = document.querySelectorAll('[data-modal-close]');
        
        modalTriggers.forEach(trigger => {
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                const modalId = trigger.dataset.modal;
                this.openModal(modalId);
            });
        });
        
        modalCloses.forEach(close => {
            close.addEventListener('click', () => {
                const modal = close.closest('.modal');
                this.closeModal(modal);
            });
        });
        
        // Cerrar modal al hacer click en el overlay
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal-overlay')) {
                this.closeModal(e.target.closest('.modal'));
            }
        });
    }

    openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('hidden');
            document.body.classList.add('modal-open');
        }
    }

    closeModal(modal) {
        if (modal) {
            modal.classList.add('hidden');
            document.body.classList.remove('modal-open');
        }
    }

    // Service Worker
    initServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/static/sw.js')
                .then(registration => {
                    console.log('SW registrado:', registration);
                })
                .catch(error => {
                    console.log('SW error:', error);
                });
        }
    }

    // Función para mostrar productos
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

    // Función para mostrar notificaciones toast
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };
        
        toast.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 transition-all duration-300 transform translate-x-full opacity-0 ${this.getToastClasses(type)}`;
        toast.innerHTML = `
            <div class="flex items-center gap-3">
                <span class="text-xl">${icons[type] || icons.info}</span>
                <span class="font-medium">${message}</span>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        // Animación de entrada
        setTimeout(() => {
            toast.classList.remove('translate-x-full', 'opacity-0');
        }, 100);
        
        // Auto-remover después de 4 segundos
        setTimeout(() => {
            toast.classList.add('translate-x-full', 'opacity-0');
            setTimeout(() => {
                if (toast.parentNode) {
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

    // Función para loading states
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

// Funciones globales para el carrito
function updateQuantity(productId, newQuantity) {
    if (newQuantity <= 0) {
        removeItem(productId);
        return;
    }
    
    const formData = new FormData();
    formData.append('producto_id', productId);
    formData.append('cantidad', newQuantity);
    
    fetch('/cliente/carrito/actualizar', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            location.reload();
        } else {
            alert('Error al actualizar la cantidad');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error de conexión');
    });
}

function removeItem(productId) {
    if (confirm('¿Estás seguro de eliminar este producto del carrito?')) {
        const formData = new FormData();
        formData.append('producto_id', productId);
        
        fetch('/cliente/carrito/eliminar', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            } else {
                alert('Error al eliminar el producto');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error de conexión');
        });
    }
}

function clearCart() {
    if (confirm('¿Estás seguro de vaciar todo el carrito?')) {
        fetch('/cliente/carrito/vaciar', {
            method: 'POST'
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            } else {
                alert('Error al vaciar el carrito');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error de conexión');
        });
    }
}

function clearFilters() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    filterBtns.forEach(btn => btn.classList.remove('active'));
    filterBtns[0]?.classList.add('active'); // Activar "Todos"
    
    const restaurantCards = document.querySelectorAll('.restaurant-card');
    restaurantCards.forEach(card => {
        card.style.display = 'block';
    });
    
    const searchInput = document.getElementById('search-restaurants');
    if (searchInput) {
        searchInput.value = '';
    }
}

// Función global para toggle de productos (compatibilidad)
function toggleProductos(idres) {
    if (window.domiUI) {
        window.domiUI.toggleProductos(idres);
    }
}

// Función para generar PDF
function generatePDF() {
    window.print();
}

// Inicializar la aplicación
window.domiUI = new DomiFlashUI();