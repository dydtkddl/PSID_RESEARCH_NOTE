/**
 * Research Platform - Main Application JavaScript
 * Core functionality for the enterprise platform
 */

// ============ API Client ============
class APIClient {
    constructor() {
        // ✅ ROOT_PATH가 없으면 빈 문자열 (로컬 개발용)
        const rootPath = window.ROOT_PATH || '';
        this.baseURL = `${rootPath}/api/v1`;
        this.rootPath = rootPath;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        const token = localStorage.getItem('access_token');
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(url, {
                ...options,
                headers,
                credentials: 'include'
            });

            if (response.status === 401) {
                const refreshed = await this.refreshToken();
                if (refreshed) {
                    return this.request(endpoint, options);
                } else {
                    window.location.href = `${this.rootPath}/login`;
                    return null;
                }
            }

            if (!response.ok) {
                const error = await response.json().catch(() => ({}));
                throw new Error(error.detail || `HTTP ${response.status}`);
            }

            return response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    async refreshToken() {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) return false;

        try {
            const response = await fetch(`${this.baseURL}/auth/refresh`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh_token: refreshToken }),
                credentials: 'include'
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('refresh_token', data.refresh_token);
                return true;
            }
        } catch (error) {
            console.error('Token refresh failed:', error);
        }
        return false;
    }

    get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }

    post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
}

// ============ Toast Notifications ============
class ToastManager {
    constructor() {
        this.container = document.getElementById('toast-container');
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.id = 'toast-container';
            this.container.className = 'toast-container';
            document.body.appendChild(this.container);
        }
    }

    show(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;

        const icons = {
            success: 'ri-check-line',
            error: 'ri-error-warning-line',
            warning: 'ri-alert-line',
            info: 'ri-information-line'
        };

        toast.innerHTML = `
            <i class="toast-icon ${icons[type] || icons.info}"></i>
            <span class="toast-message">${message}</span>
        `;

        this.container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }

    success(message) { this.show(message, 'success'); }
    error(message) { this.show(message, 'error'); }
    warning(message) { this.show(message, 'warning'); }
    info(message) { this.show(message, 'info'); }
}

// ============ Theme Manager ============
class ThemeManager {
    constructor() {
        this.theme = localStorage.getItem('theme') || 'dark';
        this.apply();
    }

    apply() {
        document.documentElement.setAttribute('data-theme', this.theme);
        this.updateIcons();
    }

    toggle() {
        this.theme = this.theme === 'dark' ? 'light' : 'dark';
        localStorage.setItem('theme', this.theme);
        this.apply();
    }

    updateIcons() {
        const btn = document.getElementById('theme-toggle');
        if (btn) {
            const icon = btn.querySelector('i');
            icon.className = this.theme === 'dark' ? 'ri-moon-line' : 'ri-sun-line';
        }
    }
}

// ============ Helper: prefix 붙인 경로 ============
// ✅ 모든 페이지 이동에서 사용
function appUrl(path) {
    const root = window.ROOT_PATH || '';
    return `${root}${path}`;
}

// ============ Command Palette ============
class CommandPalette {
    constructor(api) {
        this.api = api;
        this.modal = document.getElementById('command-palette');
        this.input = document.getElementById('command-input');
        this.results = document.getElementById('command-results');
        this.isOpen = false;

        if (this.modal) {
            this.init();
        }
    }

    init() {
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                this.toggle();
            }
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });

        const backdrop = this.modal.querySelector('.command-palette-backdrop');
        if (backdrop) {
            backdrop.addEventListener('click', () => this.close());
        }

        if (this.input) {
            this.input.addEventListener('input', () => this.search());
        }
    }

    toggle() {
        this.isOpen ? this.close() : this.open();
    }

    open() {
        this.isOpen = true;
        this.modal.classList.add('active');
        this.input.focus();
        this.showDefaultCommands();
    }

    close() {
        this.isOpen = false;
        this.modal.classList.remove('active');
        this.input.value = '';
        this.results.innerHTML = '';
    }

    showDefaultCommands() {
        // ✅ appUrl() 사용
        const commands = [
            { icon: 'ri-add-line', label: '새 문서 만들기', action: () => this.createDocument() },
            { icon: 'ri-search-line', label: '문서 검색', action: () => window.location.href = appUrl('/search') },
            { icon: 'ri-settings-3-line', label: '설정', action: () => window.location.href = appUrl('/settings') },
            { icon: 'ri-logout-box-line', label: '로그아웃', action: () => this.logout() }
        ];

        this.renderResults(commands);
    }

    async search() {
        const query = this.input.value.trim();
        if (!query) {
            this.showDefaultCommands();
            return;
        }

        try {
            const data = await this.api.get(`/documents?search=${encodeURIComponent(query)}&limit=10`);
            const items = Array.isArray(data) ? data : (data?.items || []);
            // ✅ appUrl() 사용
            const results = items.map(doc => ({
                icon: 'ri-file-text-line',
                label: doc.title,
                sublabel: doc.workspace_name || '',
                action: () => window.location.href = appUrl(`/documents/${doc.id}`)
            }));

            this.renderResults(results);
        } catch (error) {
            console.error('Search error:', error);
            this.results.innerHTML = '<div class="no-results">검색 중 오류 발생</div>';
        }
    }

    renderResults(items) {
        if (!items.length) {
            this.results.innerHTML = '<div class="no-results">결과 없음</div>';
            return;
        }

        this.results.innerHTML = items.map((item, i) => `
            <button class="command-item" data-index="${i}">
                <i class="${item.icon}"></i>
                <span class="command-label">${item.label}</span>
                ${item.sublabel ? `<span class="command-sublabel">${item.sublabel}</span>` : ''}
            </button>
        `).join('');

        this.results.querySelectorAll('.command-item').forEach((el, i) => {
            el.addEventListener('click', () => {
                items[i].action();
                this.close();
            });
        });
    }

    createDocument() {
        document.getElementById('new-doc-modal')?.classList.add('active');
        this.close();
    }

    async logout() {
        try {
            await this.api.post('/auth/logout', {});
        } catch (error) {
            console.error('Logout error:', error);
        }
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        // ✅ appUrl() 사용
        window.location.href = appUrl('/login');
    }
}

// ============ Sidebar Manager ============
class SidebarManager {
    constructor() {
        this.sidebar = document.getElementById('sidebar');
        this.toggle = document.getElementById('sidebar-toggle');
        this.mobileToggle = document.getElementById('mobile-menu-toggle');

        if (this.sidebar) {
            this.init();
        }
    }

    init() {
        // Create overlay for mobile
        this.overlay = document.createElement('div');
        this.overlay.className = 'sidebar-overlay';
        this.overlay.id = 'sidebar-overlay';
        document.body.appendChild(this.overlay);
        this.overlay.addEventListener('click', () => this.closeMobile());

        if (this.toggle) {
            this.toggle.addEventListener('click', () => this.toggleCollapse());
        }

        if (this.mobileToggle) {
            this.mobileToggle.addEventListener('click', () => this.toggleMobile());
        }

        const collapsed = localStorage.getItem('sidebar-collapsed') === 'true';
        if (collapsed && window.innerWidth > 1024) {
            this.sidebar.classList.add('collapsed');
        }
    }

    toggleCollapse() {
        this.sidebar.classList.toggle('collapsed');
        localStorage.setItem('sidebar-collapsed', this.sidebar.classList.contains('collapsed'));
    }

    toggleMobile() {
        const isOpen = this.sidebar.classList.contains('mobile-open');
        if (isOpen) { this.closeMobile(); } else { this.openMobile(); }
    }

    openMobile() {
        this.sidebar.classList.add('mobile-open');
        this.overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    closeMobile() {
        this.sidebar.classList.remove('mobile-open');
        this.overlay.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// ============ User Menu ============
class UserMenu {
    constructor(api) {
        this.api = api;
        this.trigger = document.getElementById('user-menu');
        this.dropdown = document.getElementById('user-dropdown');
        this.logoutBtn = document.getElementById('logout-btn');

        if (this.trigger) {
            this.init();
        }
    }

    init() {
        this.trigger.addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggle();
        });

        document.addEventListener('click', () => this.close());

        if (this.logoutBtn) {
            this.logoutBtn.addEventListener('click', () => this.logout());
        }
    }

    toggle() {
        if (this.dropdown.style.display === 'none') {
            this.open();
        } else {
            this.close();
        }
    }

    open() {
        const rect = this.trigger.getBoundingClientRect();
        this.dropdown.style.display = 'block';
        this.dropdown.style.bottom = `${window.innerHeight - rect.top + 8}px`;
        this.dropdown.style.left = `${rect.left}px`;
        this.dropdown.classList.add('show');
    }

    close() {
        this.dropdown.style.display = 'none';
        this.dropdown.classList.remove('show');
    }

    async logout() {
        try {
            await this.api.post('/auth/logout', {});
        } catch (error) {
            console.error('Logout error:', error);
        }
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        // ✅ appUrl() 사용
        window.location.href = appUrl('/login');
    }
}

// ============ Dropdown Manager ============
class DropdownManager {
    constructor() {
        this.init();
    }

    init() {
        document.querySelectorAll('.dropdown-trigger').forEach(trigger => {
            trigger.addEventListener('click', (e) => {
                e.stopPropagation();
                const menu = trigger.nextElementSibling;
                if (menu && menu.classList.contains('dropdown-menu')) {
                    menu.classList.toggle('show');
                }
            });
        });

        document.addEventListener('click', () => {
            document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                menu.classList.remove('show');
            });
        });
    }
}

// ============ Modal Manager ============
class ModalManager {
    constructor() {
        this.init();
    }

    init() {
        document.querySelectorAll('.modal-close, [id^="close-"], [id^="cancel-"]').forEach(btn => {
            btn.addEventListener('click', () => {
                const modal = btn.closest('.modal');
                if (modal) this.close(modal);
            });
        });

        document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
            backdrop.addEventListener('click', () => {
                const modal = backdrop.closest('.modal');
                if (modal) this.close(modal);
            });
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                const openModal = document.querySelector('.modal.active');
                if (openModal) this.close(openModal);
            }
        });
    }

    open(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('active');
        }
    }

    close(modal) {
        if (typeof modal === 'string') {
            modal = document.getElementById(modal);
        }
        if (modal) {
            modal.classList.remove('active');
        }
    }
}

// ============ Global Instances ============
const api = new APIClient();
const toast = new ToastManager();
const theme = new ThemeManager();
const commandPalette = new CommandPalette(api);
const sidebar = new SidebarManager();
const userMenu = new UserMenu(api);
const dropdowns = new DropdownManager();
const modals = new ModalManager();

// ============ Initialize ============
document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', () => theme.toggle());
    }

    const globalSearch = document.getElementById('global-search');
    if (globalSearch) {
        globalSearch.addEventListener('focus', () => commandPalette.open());
    }

    loadWorkspaces();
    initCreateWorkspace();
    loadNotificationCount();
    initNotifications();
});

// ============ Create Workspace ============
function initCreateWorkspace() {
    const btn = document.getElementById('create-workspace-btn');
    if (!btn) return;

    btn.addEventListener('click', (e) => {
        e.preventDefault();
        showCreateWorkspaceModal();
    });
}

async function showCreateWorkspaceModal() {
    document.querySelector('.create-ws-modal')?.remove();

    let orgs = [];
    try {
        orgs = await api.get('/organizations');
    } catch (e) {
        toast.error('조직 정보를 불러올 수 없습니다');
        return;
    }

    const modal = document.createElement('div');
    modal.className = 'modal active create-ws-modal';
    modal.innerHTML = `
        <div class="modal-backdrop"></div>
        <div class="modal-content" style="max-width:400px">
            <div class="modal-header">
                <h3>새 워크스페이스</h3>
                <button class="btn-icon modal-close"><i class="ri-close-line"></i></button>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <label>이름</label>
                    <input type="text" id="ws-name" class="form-input" placeholder="워크스페이스 이름" autofocus>
                </div>
                <div class="form-group">
                    <label>설명 (선택)</label>
                    <textarea id="ws-desc" class="form-input" rows="2" placeholder="워크스페이스 설명"></textarea>
                </div>
                <div class="form-group">
                    <label>아이콘</label>
                    <div class="icon-select" id="ws-icon-select">
                        ${['📁','📂','🔬','💻','📊','📚','🎯','🚀','💡','⚙️'].map(e => `<span class="icon-opt ${e === '📁' ? 'selected' : ''}" data-icon="${e}">${e}</span>`).join('')}
                    </div>
                </div>
                ${orgs.length > 1 ? `
                <div class="form-group">
                    <label>조직</label>
                    <select id="ws-org" class="form-input">
                        ${orgs.map(o => `<option value="${o.id}">${o.name}</option>`).join('')}
                    </select>
                </div>
                ` : `<input type="hidden" id="ws-org" value="${orgs[0]?.id || ''}">`}
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary modal-close">취소</button>
                <button class="btn btn-primary" id="ws-create-btn">생성</button>
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    let selectedIcon = '📁';
    modal.querySelectorAll('.icon-opt').forEach(opt => {
        opt.addEventListener('click', () => {
            modal.querySelectorAll('.icon-opt').forEach(o => o.classList.remove('selected'));
            opt.classList.add('selected');
            selectedIcon = opt.dataset.icon;
        });
    });

    modal.querySelectorAll('.modal-close, .modal-backdrop').forEach(el => {
        el.addEventListener('click', () => modal.remove());
    });

    modal.querySelector('#ws-create-btn').addEventListener('click', async () => {
        const name = modal.querySelector('#ws-name').value.trim();
        const description = modal.querySelector('#ws-desc').value.trim();
        const orgId = modal.querySelector('#ws-org').value;

        if (!name) {
            toast.error('이름을 입력하세요');
            return;
        }

        try {
            const ws = await api.post(`/workspaces?org_id=${orgId}`, {
                name,
                description,
                icon: selectedIcon
            });
            toast.success('워크스페이스가 생성되었습니다');
            modal.remove();
            loadWorkspaces();
            // ✅ appUrl() 사용
            window.location.href = appUrl(`/workspaces/${ws.id}`);
        } catch (error) {
            toast.error('생성 실패: ' + (error.message || '알 수 없는 오류'));
        }
    });

    setTimeout(() => modal.querySelector('#ws-name').focus(), 100);
}

// ============ Notifications ============
async function loadNotificationCount() {
    try {
        const data = await api.get('/notifications/count');
        const badge = document.getElementById('notification-badge');
        if (badge && data.count > 0) {
            badge.textContent = data.count > 9 ? '9+' : data.count;
            badge.style.display = 'flex';
        } else if (badge) {
            badge.style.display = 'none';
        }
    } catch (e) {
        console.log('Failed to load notification count');
    }
}

function initNotifications() {
    const btn = document.getElementById('notifications-btn');
    const dropdown = document.getElementById('notification-dropdown');
    const markAllBtn = document.getElementById('mark-all-read');

    if (!btn || !dropdown) return;

    btn.addEventListener('click', async (e) => {
        e.stopPropagation();
        dropdown.classList.toggle('active');
        if (dropdown.classList.contains('active')) {
            await loadNotifications();
        }
    });

    document.addEventListener('click', (e) => {
        if (!dropdown.contains(e.target) && !btn.contains(e.target)) {
            dropdown.classList.remove('active');
        }
    });

    if (markAllBtn) {
        markAllBtn.addEventListener('click', async () => {
            try {
                await api.post('/notifications/read-all');
                loadNotificationCount();
                loadNotifications();
                toast.success('모든 알림을 읽었습니다');
            } catch (e) {
                console.error('Failed to mark all read');
            }
        });
    }
}

async function loadNotifications() {
    const list = document.getElementById('notification-list');
    if (!list) return;

    try {
        const notifications = await api.get('/notifications?limit=10');

        if (notifications.length === 0) {
            list.innerHTML = '<div class="notification-empty">알림이 없습니다</div>';
            return;
        }

        list.innerHTML = notifications.map(n => `
            <div class="notification-item ${n.is_read ? 'read' : ''}" data-id="${n.id}" data-link="${n.link || ''}">
                <div class="notification-icon">
                    <i class="ri-${getNotificationIcon(n.type)}-line"></i>
                </div>
                <div class="notification-content">
                    <div class="notification-title">${escapeHtml(n.title)}</div>
                    <div class="notification-message">${escapeHtml(n.message)}</div>
                    <div class="notification-time">${formatRelativeTime(n.created_at)}</div>
                </div>
            </div>
        `).join('');

        list.querySelectorAll('.notification-item').forEach(item => {
            item.addEventListener('click', async () => {
                const id = item.dataset.id;
                const link = item.dataset.link;

                try {
                    await api.post(`/notifications/${id}/read`);
                    loadNotificationCount();
                } catch (e) {}

                if (link) {
                    window.location.href = link;
                }
            });
        });
    } catch (e) {
        console.error('Failed to load notifications');
        list.innerHTML = '<div class="notification-empty">로드 실패</div>';
    }
}

function getNotificationIcon(type) {
    const icons = {
        invite: 'user-add',
        mention: 'at',
        comment: 'chat-3',
        share: 'share',
        system: 'notification-3'
    };
    return icons[type] || 'notification-3';
}

function formatRelativeTime(dateStr) {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = now - date;
    if (diff < 60000) return '방금';
    if (diff < 3600000) return `${Math.floor(diff / 60000)}분 전`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}시간 전`;
    if (diff < 604800000) return `${Math.floor(diff / 86400000)}일 전`;
    return date.toLocaleDateString('ko-KR');
}

// ============ Load Workspaces ============
async function loadWorkspaces() {
    const container = document.getElementById('workspace-list');
    if (!container) return;

    try {
        const orgs = await api.get('/organizations');
        if (!orgs || !Array.isArray(orgs)) {
            container.innerHTML = '<p class="nav-empty">워크스페이스 없음</p>';
            return;
        }

        let workspaceData = [];

        for (const org of orgs) {
            try {
                const workspaces = await api.get(`/organizations/${org.id}/workspaces`);
                if (workspaces && Array.isArray(workspaces)) {
                    workspaceData.push(...workspaces);
                }
            } catch (wsError) {
                console.warn(`Failed to load workspaces for org ${org.id}:`, wsError);
            }
        }

        workspaceData.sort((a, b) => (a.position || 0) - (b.position || 0));

        if (workspaceData.length === 0) {
            container.innerHTML = '<p class="nav-empty">워크스페이스 없음</p>';
            return;
        }

        // ✅ appUrl() 사용
        container.innerHTML = workspaceData.map(ws => `
            <div class="nav-item workspace-item" draggable="true" data-ws-id="${ws.id}">
                <span class="workspace-icon" data-ws-id="${ws.id}" title="아이콘 변경">${ws.icon || '📁'}</span>
                <a href="${appUrl(`/workspaces/${ws.id}`)}" class="workspace-link">${escapeHtml(ws.name)}</a>
                <span class="drag-handle" title="드래그하여 순서 변경"><i class="ri-draggable"></i></span>
            </div>
        `).join('');

        initWorkspaceDragDrop(container);
        initWorkspaceIconPicker(container);
    } catch (error) {
        console.error('Failed to load workspaces:', error);
        container.innerHTML = '<p class="nav-empty">로드 실패</p>';
    }
}

function initWorkspaceDragDrop(container) {
    let draggedItem = null;

    container.querySelectorAll('.workspace-item').forEach(item => {
        item.addEventListener('dragstart', (e) => {
            draggedItem = item;
            item.classList.add('dragging');
            e.dataTransfer.effectAllowed = 'move';
        });

        item.addEventListener('dragend', () => {
            item.classList.remove('dragging');
            draggedItem = null;
            saveWorkspaceOrder(container);
        });

        item.addEventListener('dragover', (e) => {
            e.preventDefault();
            if (draggedItem && draggedItem !== item) {
                const rect = item.getBoundingClientRect();
                const midY = rect.top + rect.height / 2;
                if (e.clientY < midY) {
                    container.insertBefore(draggedItem, item);
                } else {
                    container.insertBefore(draggedItem, item.nextSibling);
                }
            }
        });
    });
}

async function saveWorkspaceOrder(container) {
    const items = container.querySelectorAll('.workspace-item');
    const ids = Array.from(items).map(item => item.dataset.wsId);

    try {
        await api.post('/workspaces/reorder', ids);
        toast.success('순서가 저장되었습니다');
    } catch (error) {
        console.error('Failed to save order:', error);
    }
}

function initWorkspaceIconPicker(container) {
    const emojis = [
        '📁', '📂', '🗂️', '📑', '📄', '📃', '📋', '📝', '🗃️', '🗄️',
        '🔬', '🧪', '⚗️', '🔭', '🧬', '🧫', '🧲', '🔋', '⚛️', '🦠',
        '💻', '🖥️', '⌨️', '🖱️', '💾', '📀', '🔧', '🔩', '⚙️', '🛠️',
        '📊', '📈', '📉', '📆', '📅', '🗓️', '📇', '🎛️', '🗺️', '📍',
        '📚', '📖', '📕', '📗', '📘', '📙', '📓', '📔', '🎓', '🏫',
        '🎨', '🖌️', '🖍️', '✏️', '🎭', '🎪', '🎬', '🎦', '📷', '📸',
        '🎵', '🎶', '🎼', '🎧', '🎤', '🎹', '🥁', '🎸', '🎺', '🎻',
        '💼', '📧', '📨', '📩', '✉️', '📮', '📬', '📥', '📤', '💰',
        '🌱', '🌿', '🍀', '🌳', '🌲', '🌴', '🌵', '🌾', '🌻', '🌸',
        '🚀', '🛸', '🌍', '🌎', '🌏', '🌕', '⭐', '🌟', '💫', '✨',
        '💡', '🔔', '🔕', '🔆', '🔅', '💎', '🏆', '🎯', '🎖️', '🏅',
        '❤️', '💛', '💚', '💙', '💜', '🤍', '🖤', '🧡', '💗', '💖'
    ];

    container.querySelectorAll('.workspace-icon').forEach(icon => {
        icon.style.cursor = 'pointer';
        icon.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            showIconPicker(icon, emojis);
        });
    });
}

function showIconPicker(iconEl, emojis) {
    document.querySelector('.icon-picker')?.remove();

    const picker = document.createElement('div');
    picker.className = 'icon-picker';
    picker.innerHTML = `
        <div class="icon-picker-header">
            <span>아이콘 선택</span>
            <button class="icon-picker-close"><i class="ri-close-line"></i></button>
        </div>
        <div class="icon-picker-grid">
            ${emojis.map(e => `<span class="icon-option">${e}</span>`).join('')}
        </div>
    `;

    const rect = iconEl.getBoundingClientRect();
    picker.style.cssText = `
        position: fixed;
        left: ${rect.right + 8}px;
        top: ${Math.min(rect.top, window.innerHeight - 320)}px;
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        z-index: 1000;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        width: 260px;
    `;

    document.body.appendChild(picker);

    picker.querySelector('.icon-picker-close').addEventListener('click', () => picker.remove());

    picker.querySelectorAll('.icon-option').forEach(opt => {
        opt.style.cssText = 'cursor: pointer; padding: 4px; border-radius: 4px; text-align: center;';
        opt.addEventListener('mouseenter', () => opt.style.background = 'var(--bg-hover)');
        opt.addEventListener('mouseleave', () => opt.style.background = 'transparent');
        opt.addEventListener('click', async () => {
            const wsId = iconEl.dataset.wsId;
            try {
                await api.put(`/workspaces/${wsId}`, { icon: opt.textContent });
                iconEl.textContent = opt.textContent;
                toast.success('아이콘이 변경되었습니다');
            } catch (error) {
                toast.error('아이콘 변경 실패');
            }
            picker.remove();
        });
    });

    setTimeout(() => {
        document.addEventListener('click', function closeHandler(e) {
            if (!picker.contains(e.target)) {
                picker.remove();
                document.removeEventListener('click', closeHandler);
            }
        });
    }, 100);
}

// ============ Utility Functions ============
function formatDate(dateStr) {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = now - date;

    if (diff < 60000) return '방금';
    if (diff < 3600000) return `${Math.floor(diff / 60000)}분 전`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}시간 전`;
    if (diff < 604800000) return `${Math.floor(diff / 86400000)}일 전`;

    return date.toLocaleDateString('ko-KR', { year: 'numeric', month: 'short', day: 'numeric' });
}

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

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
