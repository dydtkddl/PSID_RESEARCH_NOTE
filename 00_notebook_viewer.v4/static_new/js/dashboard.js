/**
 * Dashboard Page JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
    loadDashboardData();
    initNewDocModal();
    initImportButton();
});

// ============ Load Dashboard Data ============
async function loadDashboardData() {
    loadStats();
    loadRecentDocuments();
    loadFavorites();
    loadActivity();
}

// ============ Stats ============
async function loadStats() {
    try {
        const stats = await api.get('/users/me/stats');
        document.getElementById('stat-documents').textContent = stats.documents || 0;
        document.getElementById('stat-workspaces').textContent = stats.workspaces || 0;
        document.getElementById('stat-favorites').textContent = stats.favorites || 0;
        document.getElementById('stat-collaborators').textContent = stats.collaborators || 0;
    } catch (error) {
        console.error('Failed to load stats:', error);
        document.getElementById('stat-documents').textContent = '0';
        document.getElementById('stat-workspaces').textContent = '0';
        document.getElementById('stat-favorites').textContent = '0';
        document.getElementById('stat-collaborators').textContent = '0';
    }
}

// ============ Recent Documents ============
async function loadRecentDocuments() {
    const container = document.getElementById('recent-documents');
    if (!container) return;

    try {
        const documents = await api.get('/users/me/recent?limit=5');
        
        if (!documents || documents.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="ri-file-text-line"></i>
                    <p>최근 문서가 없습니다</p>
                </div>
            `;
            return;
        }

        container.innerHTML = documents.map(doc => `
            <a href="${window.ROOT_PATH || ''}/documents/${doc.id}" class="document-item">
                <span class="doc-icon">${doc.icon || '📄'}</span>
                <div class="doc-info">
                    <div class="doc-title">${escapeHtml(doc.title)}</div>
                    <div class="doc-meta">${formatDate(doc.updated_at)}</div>
                </div>
                <span class="doc-status ${doc.status}">${getStatusLabel(doc.status)}</span>
            </a>
        `).join('');
    } catch (error) {
        console.error('Failed to load recent documents:', error);
        container.innerHTML = `
            <div class="empty-state">
                <i class="ri-file-text-line"></i>
                <p>문서를 불러올 수 없습니다</p>
            </div>
        `;
    }
}

// ============ Favorites ============
async function loadFavorites() {
    const container = document.getElementById('favorite-documents');
    if (!container) return;

    try {
        const documents = await api.get('/users/me/favorites?limit=5');
        
        if (!documents || documents.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="ri-star-line"></i>
                    <p>즐겨찾기한 문서가 없습니다</p>
                </div>
            `;
            return;
        }

        container.innerHTML = documents.map(doc => `
            <a href="${window.ROOT_PATH || ''}/documents/${doc.id}" class="document-item">
                <span class="doc-icon">${doc.icon || '📄'}</span>
                <div class="doc-info">
                    <div class="doc-title">${escapeHtml(doc.title)}</div>
                    <div class="doc-meta">${formatDate(doc.updated_at)}</div>
                </div>
                <i class="ri-star-fill" style="color: var(--accent-warning);"></i>
            </a>
        `).join('');
    } catch (error) {
        console.error('Failed to load favorites:', error);
        container.innerHTML = `
            <div class="empty-state">
                <i class="ri-star-line"></i>
                <p>즐겨찾기를 불러올 수 없습니다</p>
            </div>
        `;
    }
}

// ============ Activity Feed ============
async function loadActivity() {
    const container = document.getElementById('activity-feed');
    if (!container) return;

    try {
        const activities = await api.get('/users/me/activity?limit=10');
        
        if (!activities || activities.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="ri-pulse-line"></i>
                    <p>최근 활동이 없습니다</p>
                </div>
            `;
            return;
        }

        container.innerHTML = activities.map(act => `
            <div class="activity-item">
                <div class="activity-icon ${act.type}">
                    <i class="${getActivityIcon(act.type)}"></i>
                </div>
                <div class="activity-content">
                    <span class="activity-user">${escapeHtml(act.user)}</span>님이 
                    <span class="activity-action">${getActivityAction(act.action)}</span>
                    ${act.resource_name ? `<a href="${getActivityLink(act)}" class="activity-doc">${escapeHtml(act.resource_name)}</a>` : ''}
                </div>
                <div class="activity-time">${formatRelativeTime(act.timestamp)}</div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load activity:', error);
        container.innerHTML = `
            <div class="empty-state">
                <i class="ri-pulse-line"></i>
                <p>활동을 불러올 수 없습니다</p>
            </div>
        `;
    }
}

function getActivityIcon(type) {
    const icons = {
        edit: 'ri-edit-line',
        comment: 'ri-chat-1-line',
        create: 'ri-add-line',
        delete: 'ri-delete-bin-line',
        login: 'ri-login-box-line'
    };
    return icons[type] || 'ri-file-text-line';
}

function getActivityAction(action) {
    const actions = {
        'document_created': '문서를 생성했습니다:',
        'document_updated': '문서를 수정했습니다:',
        'document_deleted': '문서를 삭제했습니다:',
        'document_published': '문서를 게시했습니다:',
        'comment_created': '댓글을 남겼습니다:',
        'workspace_created': '워크스페이스를 생성했습니다:',
        'login': '로그인했습니다'
    };
    return actions[action] || action;
}

function getActivityLink(act) {
    if (act.resource_type === 'document' && act.resource_id) {
        return `${window.ROOT_PATH || ''}/documents/${act.resource_id}`;
    }
    if (act.resource_type === 'workspace' && act.resource_id) {
        return `${window.ROOT_PATH || ''}/workspaces/${act.resource_id}`;
    }
    return '#';
}

function formatRelativeTime(isoString) {
    if (!isoString) return '';
    
    const date = new Date(isoString);
    const now = new Date();
    const diff = now - date;
    
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);
    
    if (minutes < 1) return '방금 전';
    if (minutes < 60) return `${minutes}분 전`;
    if (hours < 24) return `${hours}시간 전`;
    if (days < 7) return `${days}일 전`;
    
    return date.toLocaleDateString('ko-KR');
}

function getStatusLabel(status) {
    const labels = {
        draft: '초안',
        published: '게시됨',
        archived: '보관됨'
    };
    return labels[status] || status;
}

// ============ New Document Modal ============
function initNewDocModal() {
    const btn = document.getElementById('new-doc-btn');
    const modal = document.getElementById('new-doc-modal');
    const form = document.getElementById('new-doc-form');
    const closeBtn = document.getElementById('close-new-doc-modal');
    const cancelBtn = document.getElementById('cancel-new-doc');

    if (btn && modal) {
        btn.addEventListener('click', () => {
            modal.classList.add('active');
            loadWorkspaceOptions();
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', () => modal.classList.remove('active'));
    }

    if (cancelBtn) {
        cancelBtn.addEventListener('click', () => modal.classList.remove('active'));
    }

    // Template selection
    document.querySelectorAll('.template-option').forEach(opt => {
        opt.addEventListener('click', () => {
            document.querySelectorAll('.template-option').forEach(o => o.classList.remove('selected'));
            opt.classList.add('selected');
        });
    });

    // Form submit
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            await createDocument(form);
        });
    }
}

async function loadWorkspaceOptions() {
    const select = document.getElementById('doc-workspace');
    if (!select) return;

    try {
        const orgs = await api.get('/organizations');
        let options = '<option value="">워크스페이스 선택</option>';

        for (const org of orgs) {
            const workspaces = await api.get(`/organizations/${org.id}/workspaces`);
            for (const ws of workspaces) {
                options += `<option value="${ws.id}">${org.name} / ${ws.name}</option>`;
            }
        }

        select.innerHTML = options;
    } catch (error) {
        console.error('Failed to load workspaces:', error);
    }
}

async function createDocument(form) {
    const title = document.getElementById('doc-title').value;
    const workspaceId = document.getElementById('doc-workspace').value;
    const template = form.querySelector('input[name="template"]:checked')?.value || 'blank';

    if (!title || !workspaceId) {
        toast.error('제목과 워크스페이스를 입력해주세요');
        return;
    }

    const content = getTemplateContent(template);

    try {
        const doc = await api.post('/documents', {
            title,
            workspace_id: workspaceId,
            content
        });

        toast.success('문서가 생성되었습니다');
        window.location.href = `${window.ROOT_PATH || ''}/documents/${doc.id}/edit`;
    } catch (error) {
        toast.error('문서 생성에 실패했습니다: ' + error.message);
    }
}

function getTemplateContent(template) {
    const templates = {
        blank: '',
        meeting: `# 회의록

## 회의 정보
- **날짜**: ${new Date().toLocaleDateString('ko-KR')}
- **참석자**: 
- **장소**: 

## 안건

### 1. 

## 결정 사항

## 액션 아이템
- [ ] 
`,
        experiment: `# 실험 노트

## 실험 목적

## 가설

## 재료 및 방법

## 결과

## 분석

## 결론

## 참고 문헌
`,
        report: `# 보고서

## 개요

## 배경

## 분석

## 결론

## 권장 사항

## 부록
`
    };

    return templates[template] || templates.blank;
}

// ============ Dashboard Styles ============
const dashboardStyles = `
<style>
.dashboard {
    max-width: 1400px;
    margin: 0 auto;
}

.dashboard-welcome {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 32px;
    background: var(--gradient-primary);
    border-radius: var(--radius-xl);
    margin-bottom: 24px;
    color: white;
}

.welcome-content h1 {
    font-size: 1.75rem;
    margin-bottom: 8px;
}

.welcome-content p {
    opacity: 0.9;
}

.welcome-actions {
    display: flex;
    gap: 12px;
}

.welcome-actions .btn {
    background: rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: white;
}

.welcome-actions .btn:hover {
    background: rgba(255, 255, 255, 0.3);
}

.dashboard-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 32px;
}

.stat-card {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
}

.stat-icon {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--stat-color, var(--accent-primary));
    opacity: 0.15;
    border-radius: var(--radius-md);
    font-size: 1.5rem;
    color: var(--stat-color, var(--accent-primary));
}

.stat-icon i {
    opacity: 1;
    color: var(--stat-color);
}

.stat-value {
    font-size: 1.5rem;
    font-weight: 700;
}

.stat-label {
    color: var(--text-secondary);
    font-size: 0.875rem;
}

.dashboard-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 24px;
}

.dashboard-section {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    overflow: hidden;
}

.section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 20px;
    border-bottom: 1px solid var(--border-color);
}

.section-header h2 {
    font-size: 1rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 8px;
}

.section-header h2 i {
    color: var(--text-secondary);
}

.section-link {
    font-size: 0.8125rem;
    color: var(--accent-primary);
    display: flex;
    align-items: center;
    gap: 4px;
}

.document-list {
    padding: 12px;
}

.document-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    border-radius: var(--radius-md);
    transition: background var(--transition-fast);
    color: var(--text-primary);
}

.document-item:hover {
    background: var(--bg-hover);
}

.doc-icon {
    font-size: 1.25rem;
}

.doc-info {
    flex: 1;
    min-width: 0;
}

.doc-title {
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.doc-meta {
    font-size: 0.75rem;
    color: var(--text-tertiary);
}

.doc-status {
    font-size: 0.6875rem;
    padding: 2px 8px;
    border-radius: var(--radius-sm);
    background: var(--bg-tertiary);
    color: var(--text-secondary);
}

.doc-status.published {
    background: rgba(34, 197, 94, 0.1);
    color: var(--accent-success);
}

.activity-feed {
    padding: 12px;
}

.activity-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 10px;
}

.activity-icon {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg-tertiary);
    border-radius: var(--radius-full);
    font-size: 0.875rem;
}

.activity-icon.edit { color: var(--accent-primary); }
.activity-icon.comment { color: var(--accent-info); }
.activity-icon.create { color: var(--accent-success); }

.activity-content {
    flex: 1;
    font-size: 0.875rem;
}

.activity-user {
    font-weight: 500;
}

.activity-doc {
    color: var(--accent-primary);
}

.activity-time {
    font-size: 0.6875rem;
    color: var(--text-muted);
}

.quick-link-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
    padding: 12px;
}

.quick-link-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px;
    background: var(--bg-tertiary);
    border-radius: var(--radius-md);
    color: var(--text-secondary);
    font-size: 0.8125rem;
    transition: all var(--transition-fast);
}

.quick-link-item:hover {
    background: var(--bg-hover);
    color: var(--text-primary);
}

.quick-link-item i {
    font-size: 1.125rem;
}

.template-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
}

.template-option {
    cursor: pointer;
}

.template-option input {
    display: none;
}

.template-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    padding: 16px;
    background: var(--bg-tertiary);
    border: 2px solid var(--border-color);
    border-radius: var(--radius-md);
    transition: all var(--transition-fast);
}

.template-option.selected .template-card,
.template-option:hover .template-card {
    border-color: var(--accent-primary);
    background: var(--accent-primary-light);
}

.template-card i {
    font-size: 1.5rem;
    color: var(--text-secondary);
}

.template-card span {
    font-size: 0.8125rem;
}

.empty-state {
    text-align: center;
    padding: 32px;
    color: var(--text-tertiary);
}

.empty-state i {
    font-size: 2.5rem;
    margin-bottom: 12px;
    opacity: 0.5;
}

@media (max-width: 1024px) {
    .dashboard-stats {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .dashboard-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 640px) {
    .dashboard-welcome {
        flex-direction: column;
        text-align: center;
        gap: 16px;
    }
    
    .dashboard-stats {
        grid-template-columns: 1fr;
    }
    
    .template-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}
</style>
`;

// ============ Import Button ============
function initImportButton() {
    const importBtn = document.getElementById('import-btn');
    if (!importBtn) return;
    
    // Create import modal if it doesn't exist
    if (!document.getElementById('import-modal')) {
        const modalHtml = `
            <div class="modal" id="import-modal">
                <div class="modal-backdrop"></div>
                <div class="modal-content">
                    <div class="modal-header">
                        <h3>마크다운 파일 가져오기</h3>
                        <button class="modal-close" id="close-import-modal">
                            <i class="ri-close-line"></i>
                        </button>
                    </div>
                    <div class="modal-body">
                        <div class="form-group">
                            <label>워크스페이스 선택</label>
                            <select id="import-workspace" required>
                                <option value="">워크스페이스를 선택하세요</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>마크다운 파일 (.md)</label>
                            <div class="file-upload-area" id="file-upload-area">
                                <i class="ri-upload-cloud-2-line" style="font-size: 2rem; color: var(--text-muted);"></i>
                                <p>파일을 드래그하거나 클릭하여 선택</p>
                                <input type="file" id="import-file" accept=".md,.markdown" hidden>
                            </div>
                            <p id="selected-file-name" style="margin-top: 8px; color: var(--text-secondary);"></p>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-ghost" id="cancel-import">취소</button>
                        <button class="btn btn-primary" id="submit-import">가져오기</button>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        
        // Add styles for file upload area
        const styles = document.createElement('style');
        styles.textContent = `
            .file-upload-area {
                border: 2px dashed var(--border-color);
                border-radius: var(--radius-md);
                padding: 32px;
                text-align: center;
                cursor: pointer;
                transition: border-color 0.2s, background 0.2s;
            }
            .file-upload-area:hover {
                border-color: var(--accent-primary);
                background: var(--bg-hover);
            }
            .file-upload-area.dragover {
                border-color: var(--accent-primary);
                background: rgba(99, 102, 241, 0.1);
            }
        `;
        document.head.appendChild(styles);
    }
    
    const modal = document.getElementById('import-modal');
    const fileInput = document.getElementById('import-file');
    const uploadArea = document.getElementById('file-upload-area');
    const selectedFileName = document.getElementById('selected-file-name');
    const workspaceSelect = document.getElementById('import-workspace');
    
    // Open modal
    importBtn.addEventListener('click', async () => {
        modal.classList.add('active');
        // Load workspaces
        try {
            const workspaces = await api.get('/workspaces');
            workspaceSelect.innerHTML = '<option value="">워크스페이스를 선택하세요</option>' + 
                workspaces.map(ws => `<option value="${ws.id}">${ws.icon || '📁'} ${escapeHtml(ws.name)}</option>`).join('');
        } catch (error) {
            console.error('Failed to load workspaces:', error);
        }
    });
    
    // Close modal
    document.getElementById('close-import-modal')?.addEventListener('click', () => modal.classList.remove('active'));
    document.getElementById('cancel-import')?.addEventListener('click', () => modal.classList.remove('active'));
    
    // File upload area click
    uploadArea?.addEventListener('click', () => fileInput?.click());
    
    // File selection
    fileInput?.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            selectedFileName.textContent = `선택된 파일: ${fileInput.files[0].name}`;
        }
    });
    
    // Drag and drop
    uploadArea?.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    uploadArea?.addEventListener('dragleave', () => uploadArea.classList.remove('dragover'));
    uploadArea?.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0 && e.dataTransfer.files[0].name.endsWith('.md')) {
            fileInput.files = e.dataTransfer.files;
            selectedFileName.textContent = `선택된 파일: ${e.dataTransfer.files[0].name}`;
        }
    });
    
    // Submit import
    document.getElementById('submit-import')?.addEventListener('click', async () => {
        const workspaceId = workspaceSelect.value;
        const file = fileInput?.files[0];
        
        if (!workspaceId) {
            toast.error('워크스페이스를 선택하세요');
            return;
        }
        if (!file) {
            toast.error('파일을 선택하세요');
            return;
        }
        
        try {
            const content = await file.text();
            const title = file.name.replace(/\.md$/i, '').replace(/\.markdown$/i, '');
            
            const doc = await api.post('/documents', {
                workspace_id: workspaceId,
                title: title,
                content: content
            });
            
            toast.success('문서를 가져왔습니다');
            modal.classList.remove('active');
            window.location.href = `${window.ROOT_PATH || ''}/documents/${doc.id}`;
        } catch (error) {
            toast.error('가져오기에 실패했습니다');
        }
    });
}

// Inject styles
document.head.insertAdjacentHTML('beforeend', dashboardStyles);

