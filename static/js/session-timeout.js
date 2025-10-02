/**
 * 🕐 Sistema de Gestión de Timeout de Sesión
 * Maneja automáticamente:
 * - Verificación periódica de sesión
 * - Alertas de sesión próxima a expirar
 * - Renovación automática de sesión
 * - Logout automático por timeout
 */

class SessionTimeoutManager {
    constructor(options = {}) {
        this.config = {
            checkInterval: options.checkInterval || 60000, // Verificar cada minuto
            warningTime: options.warningTime || 5, // Alertar 5 minutos antes
            heartbeatInterval: options.heartbeatInterval || 300000, // Heartbeat cada 5 minutos
            autoExtend: options.autoExtend || false, // Auto-extender en actividad
            showModal: options.showModal !== false, // Mostrar modal de advertencia
            ...options
        };
        
        this.timers = {
            check: null,
            heartbeat: null,
            warning: null
        };
        
        this.state = {
            isActive: false,
            lastWarning: null,
            modalShown: false
        };
        
        this.init();
    }
    
    init() {
        console.log('🕐 Iniciando gestor de timeout de sesión...');
        
        // Verificar si hay sesión activa
        this.checkSession().then(active => {
            if (active) {
                this.startMonitoring();
                this.setupEventListeners();
            }
        });
    }
    
    async checkSession() {
        try {
            const response = await fetch('/session/status');
            const data = await response.json();
            
            this.state.isActive = data.authenticated;
            
            if (data.authenticated) {
                this.handleSessionData(data);
                return true;
            } else {
                this.stopMonitoring();
                return false;
            }
        } catch (error) {
            console.error('❌ Error verificando sesión:', error);
            return false;
        }
    }
    
    handleSessionData(data) {
        const timeRemaining = data.time_until_timeout;
        
        // Si la sesión ha expirado
        if (data.is_expired) {
            this.handleSessionExpired();
            return;
        }
        
        // Si necesita advertencia
        if (data.needs_warning && !this.state.modalShown) {
            this.showTimeoutWarning(timeRemaining);
        }
        
        // Actualizar indicador de sesión si existe
        this.updateSessionIndicator(timeRemaining, data.needs_warning);
    }
    
    handleSessionExpired() {
        console.log('⏰ Sesión expirada - redirigiendo...');
        this.stopMonitoring();
        
        // Mostrar notificación
        this.showNotification('Tu sesión ha expirado por inactividad', 'warning');
        
        // Redireccionar después de un momento
        setTimeout(() => {
            window.location.href = '/session/logout-timeout';
        }, 2000);
    }
    
    showTimeoutWarning(timeRemaining) {
        this.state.modalShown = true;
        const minutes = Math.ceil(timeRemaining);
        
        if (this.config.showModal) {
            this.showWarningModal(minutes);
        } else {
            this.showNotification(`Tu sesión expirará en ${minutes} minutos`, 'warning');
        }
    }
    
    showWarningModal(minutes) {
        // Crear modal de advertencia si no existe
        let modal = document.getElementById('session-timeout-modal');
        if (!modal) {
            modal = this.createWarningModal();
            document.body.appendChild(modal);
        }
        
        // Actualizar contenido
        const messageEl = modal.querySelector('.timeout-message');
        messageEl.textContent = `Tu sesión expirará en ${minutes} minutos. ¿Deseas extenderla?`;
        
        // Mostrar modal
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        
        // Configurar botones
        const extendBtn = modal.querySelector('.extend-session-btn');
        const logoutBtn = modal.querySelector('.logout-session-btn');
        
        extendBtn.onclick = () => this.extendSession();
        logoutBtn.onclick = () => this.manualLogout();
    }
    
    createWarningModal() {
        const modal = document.createElement('div');
        modal.id = 'session-timeout-modal';
        modal.className = 'hidden fixed inset-0 bg-black bg-opacity-50 items-center justify-center z-50';
        
        modal.innerHTML = `
            <div class="bg-white rounded-lg p-8 max-w-md mx-4 shadow-2xl">
                <div class="text-center">
                    <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-yellow-100 mb-4">
                        🕐
                    </div>
                    <h3 class="text-lg font-medium text-gray-900 mb-4">
                        Sesión Próxima a Expirar
                    </h3>
                    <p class="timeout-message text-sm text-gray-500 mb-6">
                        Tu sesión expirará pronto...
                    </p>
                    <div class="flex space-x-3">
                        <button class="extend-session-btn flex-1 bg-orange-600 hover:bg-orange-700 text-white font-medium py-2 px-4 rounded-lg transition duration-300">
                            ⏰ Extender Sesión
                        </button>
                        <button class="logout-session-btn flex-1 bg-gray-600 hover:bg-gray-700 text-white font-medium py-2 px-4 rounded-lg transition duration-300">
                            🚪 Cerrar Sesión
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        return modal;
    }
    
    async extendSession() {
        try {
            const response = await fetch('/session/extend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.hideWarningModal();
                this.showNotification('Sesión extendida exitosamente', 'success');
                this.state.modalShown = false;
            }
        } catch (error) {
            console.error('❌ Error extendiendo sesión:', error);
            this.showNotification('Error al extender la sesión', 'error');
        }
    }
    
    manualLogout() {
        this.stopMonitoring();
        window.location.href = '/auth/logout';
    }
    
    hideWarningModal() {
        const modal = document.getElementById('session-timeout-modal');
        if (modal) {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        }
    }
    
    async sendHeartbeat() {
        try {
            const response = await fetch('/session/heartbeat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (!data.authenticated) {
                this.handleSessionExpired();
            }
        } catch (error) {
            console.error('❌ Error enviando heartbeat:', error);
        }
    }
    
    updateSessionIndicator(timeRemaining, needsWarning) {
        // Actualizar indicador visual si existe
        const indicator = document.getElementById('session-indicator');
        if (indicator) {
            const minutes = Math.ceil(timeRemaining);
            indicator.textContent = `Sesión: ${minutes}m`;
            
            if (needsWarning) {
                indicator.className = 'session-indicator warning';
            } else {
                indicator.className = 'session-indicator active';
            }
        }
    }
    
    showNotification(message, type = 'info') {
        // Crear notificación toast
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${this.getNotificationClasses(type)}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Auto-remover después de 5 segundos
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
    }
    
    getNotificationClasses(type) {
        const classes = {
            success: 'bg-green-500 text-white',
            warning: 'bg-yellow-500 text-white',
            error: 'bg-red-500 text-white',
            info: 'bg-blue-500 text-white'
        };
        return classes[type] || classes.info;
    }
    
    setupEventListeners() {
        // Renovar sesión en actividad del usuario si está configurado
        if (this.config.autoExtend) {
            const events = ['click', 'keypress', 'scroll', 'mousemove'];
            events.forEach(event => {
                document.addEventListener(event, this.throttle(() => {
                    this.refreshSession();
                }, 60000)); // Máximo una vez por minuto
            });
        }
    }
    
    async refreshSession() {
        try {
            const response = await fetch('/session/refresh', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                console.log('🔄 Sesión renovada automáticamente');
            }
        } catch (error) {
            console.error('❌ Error renovando sesión:', error);
        }
    }
    
    startMonitoring() {
        console.log('🟢 Iniciando monitoreo de sesión...');
        
        // Timer principal de verificación
        this.timers.check = setInterval(() => {
            this.checkSession();
        }, this.config.checkInterval);
        
        // Timer de heartbeat
        this.timers.heartbeat = setInterval(() => {
            this.sendHeartbeat();
        }, this.config.heartbeatInterval);
    }
    
    stopMonitoring() {
        console.log('🔴 Deteniendo monitoreo de sesión...');
        
        Object.values(this.timers).forEach(timer => {
            if (timer) clearInterval(timer);
        });
        
        this.state.isActive = false;
        this.hideWarningModal();
    }
    
    // Utility function
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    }
}

// Inicializar automáticamente cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    // Solo inicializar si hay elementos que indican sesión activa
    if (document.body.classList.contains('authenticated') || 
        document.querySelector('[data-user-role]')) {
        
        window.sessionManager = new SessionTimeoutManager({
            checkInterval: 60000,      // Verificar cada minuto
            warningTime: 5,            // Advertir 5 minutos antes
            heartbeatInterval: 300000, // Heartbeat cada 5 minutos
            autoExtend: true,          // Auto-extender en actividad
            showModal: true            // Mostrar modal de advertencia
        });
    }
});