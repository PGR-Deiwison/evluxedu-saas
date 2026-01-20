// ====================================
// ANIMAÇÕES E INTERATIVIDADE
// ====================================

document.addEventListener('DOMContentLoaded', function() {
    
    // Suavização do scroll para links de navegação
    const navLinks = document.querySelectorAll('a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            
            const element = document.querySelector(href);
            if (element) {
                e.preventDefault();
                element.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Animação de entrada dos cards
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'slideIn 0.6s ease forwards';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observar cards de features
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.animationDelay = `${index * 0.1}s`;
        observer.observe(card);
    });

    // Observar cards de preços
    const pricingCards = document.querySelectorAll('.pricing-card');
    pricingCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.animationDelay = `${index * 0.1}s`;
        observer.observe(card);
    });

    // Observar itens de vantagens
    const advantages = document.querySelectorAll('.advantage-item');
    advantages.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.animationDelay = `${index * 0.1}s`;
        observer.observe(item);
    });

    // Adicionar efeito de clique nos botões
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Efeito ripple
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);

            // Feedback visual
            console.log('Clicado:', this.textContent);
        });
    });

    // Animação de scroll do header
    let lastScrollTop = 0;
    const header = document.querySelector('.header');

    window.addEventListener('scroll', function() {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        if (scrollTop > 100) {
            header.style.boxShadow = '0 0 40px rgba(0, 255, 255, 0.3)';
        } else {
            header.style.boxShadow = '0 0 30px rgba(0, 255, 255, 0.2)';
        }

        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    });

    // Contador de números para seções
    const counterElements = document.querySelectorAll('[data-count]');
    counterElements.forEach(element => {
        const targetCount = parseInt(element.getAttribute('data-count'));
        const duration = 2000;
        let currentCount = 0;
        const increment = targetCount / (duration / 16);

        const counter = setInterval(() => {
            currentCount += increment;
            if (currentCount >= targetCount) {
                element.textContent = targetCount + (element.hasAttribute('data-suffix') ? element.getAttribute('data-suffix') : '');
                clearInterval(counter);
            } else {
                element.textContent = Math.floor(currentCount) + (element.hasAttribute('data-suffix') ? element.getAttribute('data-suffix') : '');
            }
        }, 16);
    });

    // Efeito de hover nos cards de preço
    pricingCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            pricingCards.forEach(c => {
                if (c !== this) {
                    c.style.opacity = '0.7';
                }
            });
        });

        card.addEventListener('mouseleave', function() {
            pricingCards.forEach(c => {
                c.style.opacity = '1';
            });
        });
    });

    // Validação de formulário (se houver)
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Formulário enviado com sucesso!');
            this.reset();
        });
    });

    // Efeito de parallax no background
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const starsBackground = document.querySelector('.stars-background');
        if (starsBackground) {
            starsBackground.style.transform = `translateY(${scrolled * 0.5}px)`;
        }
    });

    // Inicializar Intersection Observer para animações de entrada
    function handleIntersection(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }

    const animationObserver = new IntersectionObserver(handleIntersection, {
        threshold: 0.1
    });

    document.querySelectorAll('.feature-card, .pricing-card, .advantage-item').forEach(el => {
        animationObserver.observe(el);
    });
});

// ====================================
// FUNÇÕES DE AÇÃO DOS BOTÕES
// ====================================

function iniciarTeste() {
    alert('Bem-vindo ao teste gratuito de 30 dias!\nEntraremos em contato em breve.');
}

function verDemo() {
    alert('Agendando demo para você...\nUm de nossos especialistas entrará em contato.');
}

function escolherPlano(nomePlano) {
    alert(`Você selecionou o plano ${nomePlano}.\nProsseguindo para checkout...`);
}

function solicitarDemo() {
    alert('Sua solicitação de demo foi registrada.\nEntraremos em contato em até 24 horas.');
}

// ====================================
// ADIÇÃO DE ESTILO DE RIPPLE
// ====================================

const style = document.createElement('style');
style.textContent = `
    .btn {
        position: relative;
        overflow: hidden;
    }

    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }

    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .visible {
        animation: slideIn 0.6s ease forwards;
    }
`;

document.head.appendChild(style);

// ====================================
// SUPORTE A TEMAS (OPCIONAL)
// ====================================

function alternarTema() {
    const root = document.documentElement;
    const temaAtual = root.getAttribute('data-tema') || 'claro';
    
    if (temaAtual === 'claro') {
        root.setAttribute('data-tema', 'escuro');
        localStorage.setItem('tema', 'escuro');
    } else {
        root.setAttribute('data-tema', 'claro');
        localStorage.setItem('tema', 'claro');
    }
}

// Carregar tema salvo
window.addEventListener('load', function() {
    const temaSalvo = localStorage.getItem('tema') || 'claro';
    document.documentElement.setAttribute('data-tema', temaSalvo);
});

// ====================================
// OTIMIZAÇÕES DE PERFORMANCE
// ====================================

// Lazy loading de imagens (se usadas)
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.add('loaded');
                observer.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => imageObserver.observe(img));
}

// Preload de fontes críticas
if (window.preloadFont) {
    window.preloadFont('Segoe UI', { style: 'normal', weight: 400 });
}

console.log('🚀 EVLuxEduca - Script carregado com sucesso!');
console.log('✨ Bem-vindo ao Gestor Educacional do futuro!');
