/**
 * Sistema de Supermercado - JavaScript Principal
 * Contém funções utilitárias e interações globais
 */

// ==================== VARIÁVEIS GLOBAIS ====================
let isLoading = false;

// ==================== INICIALIZAÇÃO ====================
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Inicializa a aplicação
 */
function initializeApp() {
    // Configurar tooltips do Bootstrap
    initializeTooltips();
    
    // Configurar validação de formulários
    initializeFormValidation();
    
    // Configurar atalhos de teclado
    initializeKeyboardShortcuts();
    
    // Configurar notificações
    initializeNotifications();
    
    console.log('Sistema de Supermercado inicializado com sucesso!');
}

// ==================== FUNÇÕES DE LOADING ====================

/**
 * Exibe o spinner de carregamento
 */
function showLoading() {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.classList.remove('d-none');
        isLoading = true;
    }
}

/**
 * Oculta o spinner de carregamento
 */
function hideLoading() {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.classList.add('d-none');
        isLoading = false;
    }
}

// ==================== FUNÇÕES DE NOTIFICAÇÃO ====================

/**
 * Exibe uma notificação de sucesso
 * @param {string} title - Título da notificação
 * @param {string} message - Mensagem da notificação
 */
function showSuccess(title, message = '') {
    Swal.fire({
        icon: 'success',
        title: title,
        text: message,
        timer: 3000,
        timerProgressBar: true,
        showConfirmButton: false,
        toast: true,
        position: 'top-end'
    });
}

/**
 * Exibe uma notificação de erro
 * @param {string} title - Título da notificação
 * @param {string} message - Mensagem da notificação
 */
function showError(title, message = '') {
    Swal.fire({
        icon: 'error',
        title: title,
        text: message,
        confirmButtonText: 'OK'
    });
}

/**
 * Exibe uma notificação de aviso
 * @param {string} title - Título da notificação
 * @param {string} message - Mensagem da notificação
 */
function showWarning(title, message = '') {
    Swal.fire({
        icon: 'warning',
        title: title,
        text: message,
        confirmButtonText: 'OK'
    });
}

/**
 * Exibe uma notificação de informação
 * @param {string} title - Título da notificação
 * @param {string} message - Mensagem da notificação
 */
function showInfo(title, message = '') {
    Swal.fire({
        icon: 'info',
        title: title,
        text: message,
        confirmButtonText: 'OK'
    });
}

/**
 * Exibe um diálogo de confirmação
 * @param {string} title - Título do diálogo
 * @param {string} message - Mensagem do diálogo
 * @param {string} confirmText - Texto do botão de confirmação
 * @param {string} cancelText - Texto do botão de cancelamento
 * @returns {Promise<boolean>} - Resultado da confirmação
 */
async function showConfirmation(title, message, confirmText = 'Sim', cancelText = 'Não') {
    const result = await Swal.fire({
        title: title,
        text: message,
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: confirmText,
        cancelButtonText: cancelText,
        confirmButtonColor: '#198754',
        cancelButtonColor: '#6c757d'
    });
    
    return result.isConfirmed;
}

// ==================== FUNÇÕES DE VALIDAÇÃO ====================

/**
 * Valida se um email é válido
 * @param {string} email - Email a ser validado
 * @returns {boolean} - True se válido
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Valida se um CPF é válido (formato básico)
 * @param {string} cpf - CPF a ser validado
 * @returns {boolean} - True se válido
 */
function isValidCPF(cpf) {
    cpf = cpf.replace(/[^\d]/g, '');
    return cpf.length === 11;
}

/**
 * Valida se um valor monetário é válido
 * @param {string|number} value - Valor a ser validado
 * @returns {boolean} - True se válido
 */
function isValidMoney(value) {
    const num = parseFloat(value);
    return !isNaN(num) && num >= 0;
}

/**
 * Valida se um código de barras é válido (formato básico)
 * @param {string} barcode - Código de barras a ser validado
 * @returns {boolean} - True se válido
 */
function isValidBarcode(barcode) {
    return barcode && barcode.length >= 8 && /^\d+$/.test(barcode);
}

// ==================== FUNÇÕES DE FORMATAÇÃO ====================

/**
 * Formata um valor monetário
 * @param {number} value - Valor a ser formatado
 * @returns {string} - Valor formatado
 */
function formatMoney(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

/**
 * Formata uma data
 * @param {Date|string} date - Data a ser formatada
 * @returns {string} - Data formatada
 */
function formatDate(date) {
    if (typeof date === 'string') {
        date = new Date(date);
    }
    
    return new Intl.DateTimeFormat('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    }).format(date);
}

/**
 * Formata data e hora
 * @param {Date|string} date - Data a ser formatada
 * @returns {string} - Data e hora formatadas
 */
function formatDateTime(date) {
    if (typeof date === 'string') {
        date = new Date(date);
    }
    
    return new Intl.DateTimeFormat('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(date);
}

/**
 * Formata um número com separadores de milhares
 * @param {number} num - Número a ser formatado
 * @returns {string} - Número formatado
 */
function formatNumber(num) {
    return new Intl.NumberFormat('pt-BR').format(num);
}

// ==================== FUNÇÕES DE REQUISIÇÃO HTTP ====================

/**
 * Faz uma requisição GET
 * @param {string} url - URL da requisição
 * @returns {Promise<any>} - Resposta da requisição
 */
async function httpGet(url) {
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Erro na requisição GET:', error);
        throw error;
    }
}

/**
 * Faz uma requisição POST
 * @param {string} url - URL da requisição
 * @param {object} data - Dados a serem enviados
 * @returns {Promise<any>} - Resposta da requisição
 */
async function httpPost(url, data) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Erro na requisição POST:', error);
        throw error;
    }
}

/**
 * Faz uma requisição PUT
 * @param {string} url - URL da requisição
 * @param {object} data - Dados a serem enviados
 * @returns {Promise<any>} - Resposta da requisição
 */
async function httpPut(url, data) {
    try {
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Erro na requisição PUT:', error);
        throw error;
    }
}

/**
 * Faz uma requisição DELETE
 * @param {string} url - URL da requisição
 * @returns {Promise<any>} - Resposta da requisição
 */
async function httpDelete(url) {
    try {
        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Erro na requisição DELETE:', error);
        throw error;
    }
}

// ==================== FUNÇÕES DE UTILITÁRIOS ====================

/**
 * Debounce - Atrasa a execução de uma função
 * @param {Function} func - Função a ser executada
 * @param {number} wait - Tempo de espera em ms
 * @returns {Function} - Função com debounce
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Throttle - Limita a execução de uma função
 * @param {Function} func - Função a ser executada
 * @param {number} limit - Limite de tempo em ms
 * @returns {Function} - Função com throttle
 */
function throttle(func, limit) {
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
}

/**
 * Copia texto para a área de transferência
 * @param {string} text - Texto a ser copiado
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showSuccess('Copiado!', 'Texto copiado para a área de transferência');
    } catch (err) {
        console.error('Erro ao copiar texto:', err);
        showError('Erro', 'Não foi possível copiar o texto');
    }
}

/**
 * Gera um ID único
 * @returns {string} - ID único
 */
function generateUniqueId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

/**
 * Converte string para slug (URL amigável)
 * @param {string} str - String a ser convertida
 * @returns {string} - Slug gerado
 */
function stringToSlug(str) {
    return str
        .toLowerCase()
        .trim()
        .replace(/[^\w\s-]/g, '')
        .replace(/[\s_-]+/g, '-')
        .replace(/^-+|-+$/g, '');
}

// ==================== INICIALIZAÇÃO DE COMPONENTES ====================

/**
 * Inicializa tooltips do Bootstrap
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Inicializa validação de formulários
 */
function initializeFormValidation() {
    // Adicionar validação customizada aos formulários
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * Inicializa atalhos de teclado
 */
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl + K para busca rápida (se existir)
        if (e.ctrlKey && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('#searchInput, #barcodeInput');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // ESC para fechar modais
        if (e.key === 'Escape') {
            const openModals = document.querySelectorAll('.modal.show');
            openModals.forEach(modal => {
                const modalInstance = bootstrap.Modal.getInstance(modal);
                if (modalInstance) {
                    modalInstance.hide();
                }
            });
        }
    });
}

/**
 * Inicializa sistema de notificações
 */
function initializeNotifications() {
    // Configurar SweetAlert2 padrões
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer);
            toast.addEventListener('mouseleave', Swal.resumeTimer);
        }
    });
    
    // Tornar Toast disponível globalmente
    window.Toast = Toast;
}

// ==================== FUNÇÕES DE ANIMAÇÃO ====================

/**
 * Anima um elemento com efeito de shake
 * @param {HTMLElement} element - Elemento a ser animado
 */
function shakeElement(element) {
    element.classList.add('animate__animated', 'animate__shakeX');
    setTimeout(() => {
        element.classList.remove('animate__animated', 'animate__shakeX');
    }, 1000);
}

/**
 * Anima um elemento com efeito de pulse
 * @param {HTMLElement} element - Elemento a ser animado
 */
function pulseElement(element) {
    element.classList.add('animate__animated', 'animate__pulse');
    setTimeout(() => {
        element.classList.remove('animate__animated', 'animate__pulse');
    }, 1000);
}

// ==================== FUNÇÕES DE ARMAZENAMENTO LOCAL ====================

/**
 * Salva dados no localStorage
 * @param {string} key - Chave para armazenamento
 * @param {any} data - Dados a serem salvos
 */
function saveToLocalStorage(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
    } catch (error) {
        console.error('Erro ao salvar no localStorage:', error);
    }
}

/**
 * Carrega dados do localStorage
 * @param {string} key - Chave dos dados
 * @returns {any} - Dados carregados ou null
 */
function loadFromLocalStorage(key) {
    try {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    } catch (error) {
        console.error('Erro ao carregar do localStorage:', error);
        return null;
    }
}

/**
 * Remove dados do localStorage
 * @param {string} key - Chave dos dados a serem removidos
 */
function removeFromLocalStorage(key) {
    try {
        localStorage.removeItem(key);
    } catch (error) {
        console.error('Erro ao remover do localStorage:', error);
    }
}

// ==================== EXPORTAR FUNÇÕES GLOBAIS ====================

// Tornar funções principais disponíveis globalmente
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.showSuccess = showSuccess;
window.showError = showError;
window.showWarning = showWarning;
window.showInfo = showInfo;
window.showConfirmation = showConfirmation;
window.formatMoney = formatMoney;
window.formatDate = formatDate;
window.formatDateTime = formatDateTime;
window.formatNumber = formatNumber;
window.httpGet = httpGet;
window.httpPost = httpPost;
window.httpPut = httpPut;
window.httpDelete = httpDelete;
window.debounce = debounce;
window.throttle = throttle;
window.copyToClipboard = copyToClipboard;
window.generateUniqueId = generateUniqueId;
window.stringToSlug = stringToSlug;

console.log('JavaScript principal carregado com sucesso!');