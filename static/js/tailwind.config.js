// Configuración personalizada de Tailwind para DomiFlash - Premium Version
tailwind.config = {
  darkMode: 'class', // Habilitar dark mode por clase
  content: ['./templates/**/*.html', './static/**/*.js'],
  theme: {
    extend: {
      colors: {
        // Paleta de colores DomiFlash
        'domi-orange': '#FF6B35',
        'domi-red': '#E63946',
        'domi-yellow': '#FFD23F',
        'domi-dark': '#1A1A1A',
        'domi-light': '#F8FAFC',
        
        // Colores organizados (compatible con versión anterior)
        'domi': {
          'orange': '#FF6B35',
          'red': '#E63946', 
          'yellow': '#FFD23F',
          'dark': '#1A1A1A',
          'success': '#38A169'
        },
        
        // Dark mode colors
        'dark-bg': {
          primary: '#1a1a1a',
          secondary: '#2d2d2d',
          tertiary: '#404040'
        },
        'dark-text': {
          primary: '#ffffff',
          secondary: '#b3b3b3',
          tertiary: '#8a8a8a'
        }
      },
      
      backgroundImage: {
        // Gradientes mejorados
        'domi-gradient': 'linear-gradient(135deg, #FF6B35 0%, #E63946 100%)',
        'domi-gradient-reverse': 'linear-gradient(135deg, #E63946 0%, #FF6B35 100%)',
        'domi-gradient-light': 'linear-gradient(135deg, #FFF5F0 0%, #FFEBEE 50%, #FFFBF0 100%)',
        'hero-pattern': 'url("data:image/svg+xml,%3Csvg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"%3E%3Cg fill="none" fill-rule="evenodd"%3E%3Cg fill="%23FF6B35" fill-opacity="0.1"%3E%3Ccircle cx="30" cy="30" r="3"/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")',
        'hero-pattern-dark': 'radial-gradient(circle at 25% 25%, #FF6B35 0%, transparent 50%), radial-gradient(circle at 75% 75%, #E63946 0%, transparent 50%)'
      },
      
      fontFamily: {
        'inter': ['Inter', 'system-ui', 'sans-serif'],
        'display': ['Inter', 'system-ui', 'sans-serif'],
        'body': ['Inter', 'system-ui', 'sans-serif']
      },
      
      animation: {
        // Animaciones existentes
        'food-bounce': 'foodBounce 3s ease-in-out infinite',
        'slide-in-right': 'slideInRight 0.3s ease-out',
        'slide-in-left': 'slideInLeft 0.3s ease-out',
        'fade-in-up': 'fadeInUp 0.5s ease-out',
        'pulse-slow': 'pulse 3s infinite',
        'float': 'float 6s ease-in-out infinite',
        
        // Nuevas animaciones premium
        'fade-in': 'fadeIn 0.6s ease-out',
        'fade-in-down': 'fadeInDown 0.6s ease-out',
        'bounce-gentle': 'bounceGentle 2s infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'spin-slow': 'spin 3s linear infinite',
        'wiggle': 'wiggle 1s ease-in-out infinite',
        'gradient-shift': 'gradientShift 3s ease infinite',
        'scale-up': 'scaleUp 0.3s ease-out',
        'theme-transition': 'themeTransition 0.3s ease'
      },
      
      keyframes: {
        // Keyframes existentes
        foodBounce: {
          '0%, 100%': { 
            transform: 'translateY(0px) rotate(0deg)',
            animationTimingFunction: 'cubic-bezier(0.8, 0, 1, 1)'
          },
          '50%': { 
            transform: 'translateY(-25px) rotate(5deg)',
            animationTimingFunction: 'cubic-bezier(0, 0, 0.2, 1)'
          }
        },
        slideInRight: {
          '0%': { transform: 'translateX(100%)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' }
        },
        slideInLeft: {
          '0%': { transform: 'translateX(-100%)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' }
        },
        fadeInUp: {
          '0%': { transform: 'translateY(30px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' }
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' }
        },
        
        // Nuevos keyframes premium
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' }
        },
        fadeInDown: {
          '0%': { opacity: '0', transform: 'translateY(-30px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        },
        bounceGentle: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' }
        },
        glow: {
          '0%': { boxShadow: '0 0 5px rgba(255, 107, 53, 0.2)' },
          '100%': { boxShadow: '0 0 20px rgba(255, 107, 53, 0.4)' }
        },
        wiggle: {
          '0%, 100%': { transform: 'rotate(-3deg)' },
          '50%': { transform: 'rotate(3deg)' }
        },
        gradientShift: {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' }
        },
        scaleUp: {
          '0%': { transform: 'scale(0.95)' },
          '100%': { transform: 'scale(1)' }
        },
        themeTransition: {
          '0%': { opacity: '0.8' },
          '100%': { opacity: '1' }
        }
      },
      
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '112': '28rem'
      },
      
      borderRadius: {
        'xl': '1rem',
        '2xl': '1.5rem',
        '3xl': '2rem'
      },
      
      backdropBlur: {
        'xs': '2px'
      },
      
      boxShadow: {
        // Sombras existentes
        'domi': '0 10px 25px -5px rgba(255, 107, 53, 0.3)',
        'domi-lg': '0 20px 40px -10px rgba(255, 107, 53, 0.4)',
        'card': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'card-hover': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        
        // Nuevas sombras premium
        'glow-sm': '0 0 10px rgba(255, 107, 53, 0.3)',
        'glow-md': '0 0 20px rgba(255, 107, 53, 0.4)',
        'glow-lg': '0 0 30px rgba(255, 107, 53, 0.5)',
        'inner-glow': 'inset 0 0 10px rgba(255, 107, 53, 0.2)',
        'dark-sm': '0 1px 2px 0 rgba(0, 0, 0, 0.3)',
        'dark-md': '0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2)',
        'dark-lg': '0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.2)'
      },
      
      screens: {
        'xs': '475px',
        '3xl': '1600px'
      },
      
      zIndex: {
        '60': '60',
        '70': '70',
        '80': '80',
        '90': '90',
        '100': '100'
      }
    }
  },
  
  plugins: [
    // Plugin personalizado para utilidades dark mode y componentes premium
    function({ addUtilities, addComponents, theme }) {
      const darkUtilities = {
        '.dark-card': {
          '@apply bg-white dark:bg-dark-bg-secondary border border-gray-200 dark:border-dark-bg-tertiary': {},
        },
        '.dark-text': {
          '@apply text-gray-900 dark:text-dark-text-primary': {},
        },
        '.dark-text-secondary': {
          '@apply text-gray-600 dark:text-dark-text-secondary': {},
        },
        '.dark-border': {
          '@apply border-gray-200 dark:border-dark-bg-tertiary': {},
        },
        '.dark-bg': {
          '@apply bg-gray-50 dark:bg-dark-bg-primary': {},
        },
        '.dark-bg-secondary': {
          '@apply bg-white dark:bg-dark-bg-secondary': {},
        },
        '.dark-hover': {
          '@apply hover:bg-gray-100 dark:hover:bg-dark-bg-tertiary': {},
        }
      };
      
      const premiumComponents = {
        '.btn-primary': {
          '@apply bg-domi-gradient text-white font-semibold py-3 px-6 rounded-lg hover:shadow-glow-md transition-all duration-200 transform hover:scale-105': {},
        },
        '.btn-secondary': {
          '@apply bg-white dark:bg-dark-bg-secondary text-domi-orange border-2 border-domi-orange font-semibold py-3 px-6 rounded-lg hover:bg-domi-orange hover:text-white transition-all duration-200': {},
        },
        '.card': {
          '@apply dark-card rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105': {},
        },
        '.input': {
          '@apply w-full px-4 py-3 border dark-border rounded-lg focus:ring-2 focus:ring-domi-orange focus:border-transparent dark-bg dark-text transition-all duration-200': {},
        },
        '.toast': {
          '@apply fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg backdrop-blur-sm transform transition-all duration-300': {},
        }
      };
      
      addUtilities(darkUtilities);
      addComponents(premiumComponents);
    }
  ]
};