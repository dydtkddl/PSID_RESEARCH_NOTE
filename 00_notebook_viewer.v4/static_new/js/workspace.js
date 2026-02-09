/**
 * Workspace Page JavaScript
 */

let currentView = 'list';
let currentFilter = 'all';
let currentSort = 'updated_at';
let documents = [];

document.addEventListener('DOMContentLoaded', () => {
    // Set initial view to list
    const container = document.getElementById('documents-grid');
    if (container) container.classList.add('list-view');
    document.querySelector('.view-btn[data-view="list"]')?.classList.add('active');
    document.querySelector('.view-btn[data-view="grid"]')?.classList.remove('active');
    
    loadDocuments();
    initViewToggle();
    initFilters();
    initSort();
    initSearch();
    initNewDocModal();
    initWorkspaceSettings();
    initDropdowns();
});

async function loadDocuments() {
    const container = document.getElementById('documents-grid');
    
    try {
        const data = await api.get(`/documents?workspace_id=${WORKSPACE_ID}&sort=${currentSort}`);
        documents = data.items || [];
        
        renderDocuments();
    } catch (error) {
        container.innerHTML = `
            <div class="error-state">
                <i class="ri-error-warning-line"></i>
                <p>문서를 불러올 수 없습니다</p>
            </div>
        `;
    }
}

function renderDocuments() {
    const container = document.getElementById('documents-grid');
    
    let filtered = documents.filter(doc => {
        if (currentFilter === 'all') return true;
        return doc.status === currentFilter;
    });

    if (filtered.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="ri-file-text-line"></i>
                <p>문서가 없습니다</p>
                <button class="btn btn-primary" id="create-first">첫 문서 만들기</button>
            </div>
        `;
        document.getElementById('create-first')?.addEventListener('click', () => {
            document.getElementById('new-doc-modal')?.classList.add('active');
        });
        return;
    }

    container.innerHTML = filtered.map(doc => `
        <a href="${window.ROOT_PATH || ''}/documents/${doc.id}" class="document-card" data-id="${doc.id}">
            <div class="card-header">
                <span class="card-icon">${doc.icon || '📄'}</span>
                <div class="card-actions">
                    <button class="btn btn-icon btn-sm favorite-btn" 
                            data-id="${doc.id}" data-favorited="${doc.is_favorited}">
                        <i class="${doc.is_favorited ? 'ri-star-fill' : 'ri-star-line'}"></i>
                    </button>
                </div>
            </div>
            <div class="card-body">
                <h3 class="card-title">${escapeHtml(doc.title)}</h3>
                <p class="card-summary">${doc.summary || ''}</p>
            </div>
            <div class="card-footer">
                <span class="card-status ${doc.status}">${getStatusLabel(doc.status)}</span>
                <span class="card-date">${formatDate(doc.updated_at)}</span>
            </div>
        </a>
    `).join('');

    // Favorite buttons
    container.querySelectorAll('.favorite-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            e.stopPropagation();
            await toggleDocFavorite(btn);
        });
    });
}

async function toggleDocFavorite(btn) {
    const id = btn.dataset.id;
    const isFavorited = btn.dataset.favorited === 'true';
    
    try {
        if (isFavorited) {
            await api.delete(`/documents/${id}/favorite`);
            btn.dataset.favorited = 'false';
            btn.querySelector('i').className = 'ri-star-line';
        } else {
            await api.post(`/documents/${id}/favorite`, {});
            btn.dataset.favorited = 'true';
            btn.querySelector('i').className = 'ri-star-fill';
        }
    } catch (error) {
        toast.error('오류가 발생했습니다');
    }
}

function getStatusLabel(status) {
    const labels = {
        draft: '초안',
        published: '게시됨',
        archived: '보관됨'
    };
    return labels[status] || status;
}

function initViewToggle() {
    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentView = btn.dataset.view;
            const grid = document.getElementById('documents-grid');
            if (grid) {
                if (currentView === 'list') {
                    grid.classList.add('list-view');
                } else {
                    grid.classList.remove('list-view');
                }
            }
        });
    });
}

function initDropdowns() {
    document.querySelectorAll('.dropdown-trigger').forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            e.stopPropagation();
            const menu = trigger.nextElementSibling;
            if (menu && menu.classList.contains('dropdown-menu')) {
                // Close all other dropdowns
                document.querySelectorAll('.dropdown-menu.show').forEach(m => {
                    if (m !== menu) m.classList.remove('show');
                });
                menu.classList.toggle('show');
            }
        });
    });
    
    // Close dropdowns on click outside
    document.addEventListener('click', () => {
        document.querySelectorAll('.dropdown-menu.show').forEach(m => m.classList.remove('show'));
    });
}

function initFilters() {
    document.querySelectorAll('.filter-dropdown .dropdown-item').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.filter-dropdown .dropdown-item').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            renderDocuments();
        });
    });
}

function initSort() {
    document.querySelectorAll('.sort-dropdown .dropdown-item').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.sort-dropdown .dropdown-item').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentSort = btn.dataset.sort;
            loadDocuments();
        });
    });
}

function initSearch() {
    const searchInput = document.getElementById('doc-search');
    if (!searchInput) return;

    searchInput.addEventListener('input', debounce(() => {
        const query = searchInput.value.toLowerCase();
        
        const filtered = documents.filter(doc => 
            doc.title.toLowerCase().includes(query)
        );
        
        const temp = documents;
        documents = filtered;
        renderDocuments();
        documents = temp;
    }, 300));
}

function initNewDocModal() {
    const btn = document.getElementById('new-doc-btn');
    const modal = document.getElementById('new-doc-modal');
    const form = document.getElementById('new-doc-form');

    btn?.addEventListener('click', () => modal?.classList.add('active'));
    
    document.getElementById('close-new-doc')?.addEventListener('click', () => modal?.classList.remove('active'));
    document.getElementById('cancel-new-doc')?.addEventListener('click', () => modal?.classList.remove('active'));

    document.querySelectorAll('.template-option').forEach(opt => {
        opt.addEventListener('click', () => {
            document.querySelectorAll('.template-option').forEach(o => o.classList.remove('selected'));
            opt.classList.add('selected');
        });
    });

    form?.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const title = document.getElementById('doc-title')?.value;
        const template = form.querySelector('input[name="template"]:checked')?.value || 'blank';
        
        if (!title) {
            toast.error('제목을 입력해주세요');
            return;
        }

        try {
            const doc = await api.post('/documents', {
                title,
                workspace_id: WORKSPACE_ID,
                content: getTemplateContent(template)
            });
            
            toast.success('문서가 생성되었습니다');
            window.location.href = `${window.ROOT_PATH || ''}/documents/${doc.id}/edit`;
        } catch (error) {
            toast.error('문서 생성에 실패했습니다');
        }
    });
}

function getTemplateContent(template) {
    const templates = {
        blank: '',
        meeting: `# 회의록\n\n## 참석자\n\n## 안건\n\n## 결정사항\n`,
        experiment: `# 실험 노트\n\n## 목적\n\n## 방법\n\n## 결과\n\n## 결론\n`
    };
    return templates[template] || '';
}

// ============ Workspace Settings ============
function initWorkspaceSettings() {
    const settingsBtn = document.getElementById('workspace-settings-btn');
    const modal = document.getElementById('workspace-settings-modal');
    const form = document.getElementById('ws-settings-form');
    const deleteBtn = document.getElementById('delete-workspace-btn');
    const deleteModal = document.getElementById('delete-confirm-modal');
    
    // Open settings modal
    settingsBtn?.addEventListener('click', () => {
        modal?.classList.add('active');
    });
    
    // Close settings modal
    document.getElementById('close-ws-settings')?.addEventListener('click', () => {
        modal?.classList.remove('active');
    });
    document.getElementById('cancel-ws-settings')?.addEventListener('click', () => {
        modal?.classList.remove('active');
    });
    
    // Save settings
    form?.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const name = document.getElementById('ws-name')?.value;
        const description = document.getElementById('ws-description')?.value;
        const icon = document.getElementById('ws-icon')?.value;
        
        try {
            await api.put(`/workspaces/${WORKSPACE_ID}`, {
                name,
                description,
                icon
            });
            
            toast.success('설정이 저장되었습니다');
            modal?.classList.remove('active');
            // Reload page to reflect changes
            window.location.reload();
        } catch (error) {
            toast.error('설정 저장에 실패했습니다');
        }
    });
    
    // Delete workspace button
    deleteBtn?.addEventListener('click', () => {
        modal?.classList.remove('active');
        deleteModal?.classList.add('active');
    });
    
    // Close delete modal
    document.getElementById('close-delete-confirm')?.addEventListener('click', () => {
        deleteModal?.classList.remove('active');
    });
    document.getElementById('cancel-delete')?.addEventListener('click', () => {
        deleteModal?.classList.remove('active');
    });
    
    // Confirm delete
    document.getElementById('confirm-delete')?.addEventListener('click', async () => {
        try {
            await api.delete(`/workspaces/${WORKSPACE_ID}`);
            toast.success('워크스페이스가 삭제되었습니다');
            window.location.href = '/';
        } catch (error) {
            toast.error('삭제에 실패했습니다');
            deleteModal?.classList.remove('active');
        }
    });
}

// Styles
const workspaceStyles = `
<style>
.workspace-page {
    max-width: 1400px;
    margin: 0 auto;
}

.workspace-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 24px;
}

.workspace-info {
    display: flex;
    align-items: center;
    gap: 16px;
}

.workspace-icon {
    font-size: 2.5rem;
}

.workspace-info h1 {
    font-size: 1.5rem;
}

.workspace-description {
    color: var(--text-secondary);
    font-size: 0.875rem;
}

.workspace-actions {
    display: flex;
    gap: 8px;
}

.workspace-toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 16px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    margin-bottom: 24px;
}

.toolbar-left, .toolbar-right {
    display: flex;
    align-items: center;
    gap: 12px;
}

.view-toggle {
    display: flex;
    background: var(--bg-tertiary);
    border-radius: var(--radius-md);
    padding: 4px;
}

.view-btn {
    padding: 6px 10px;
    background: none;
    border: none;
    color: var(--text-secondary);
    border-radius: var(--radius-sm);
    cursor: pointer;
}

.view-btn.active {
    background: var(--bg-elevated);
    color: var(--text-primary);
}

.documents-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 16px;
}

.document-card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    overflow: hidden;
    transition: all var(--transition-fast);
    color: var(--text-primary);
}

.document-card:hover {
    border-color: var(--accent-primary);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.document-card .card-header {
    display: flex;
    justify-content: space-between;
    padding: 16px 16px 0;
}

.card-icon {
    font-size: 1.5rem;
}

.document-card .card-body {
    padding: 12px 16px;
}

.card-title {
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 8px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.card-summary {
    font-size: 0.8125rem;
    color: var(--text-secondary);
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.document-card .card-footer {
    display: flex;
    justify-content: space-between;
    padding: 12px 16px;
    border-top: 1px solid var(--border-color);
    font-size: 0.75rem;
}

.card-status {
    padding: 2px 8px;
    border-radius: var(--radius-sm);
    background: var(--bg-tertiary);
}

.card-status.published {
    background: rgba(34, 197, 94, 0.1);
    color: var(--accent-success);
}

.card-date {
    color: var(--text-muted);
}

.empty-state, .error-state {
    grid-column: 1 / -1;
    text-align: center;
    padding: 64px 32px;
    color: var(--text-tertiary);
}

.empty-state i, .error-state i {
    font-size: 3rem;
    margin-bottom: 16px;
}

.loading-state {
    grid-column: 1 / -1;
    text-align: center;
    padding: 64px;
}

/* List view styles */
.documents-grid.list-view {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.documents-grid.list-view .document-card {
    flex-direction: row;
    padding: 12px 16px;
    align-items: center;
}

.documents-grid.list-view .card-header {
    padding: 0;
    border-bottom: none;
    flex-shrink: 0;
}

.documents-grid.list-view .card-body {
    flex: 1;
    padding: 0 16px;
}

.documents-grid.list-view .card-body h3 {
    margin-bottom: 4px;
    font-size: 0.9375rem;
}

.documents-grid.list-view .card-summary {
    display: none;
}

.documents-grid.list-view .card-footer {
    border-top: none;
    padding: 0;
    flex-shrink: 0;
}

/* Dropdown menu styles */
.dropdown-menu {
    display: none;
    position: absolute;
    top: 100%;
    right: 0;
    min-width: 150px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-lg);
    z-index: 100;
    margin-top: 4px;
}

.dropdown-menu.show {
    display: block;
}

.filter-dropdown,
.sort-dropdown {
    position: relative;
}
</style>
`;

document.head.insertAdjacentHTML('beforeend', workspaceStyles);

