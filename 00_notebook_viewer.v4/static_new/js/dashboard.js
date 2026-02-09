/**
 * Dashboard JavaScript - All buttons functional
 */

document.addEventListener('DOMContentLoaded', () => {
    loadDashboardData();
    initNewDocModal();
    initImportModal();
    initFeedbackModal();
    initShortcutsModal();
});

// ============ Dashboard Data ============

async function loadDashboardData() {
    // Load stats
    try {
        const stats = await api.get('/users/me/stats');
        document.getElementById('stat-documents').textContent = stats.documents || 0;
        document.getElementById('stat-workspaces').textContent = stats.workspaces || 0;
        document.getElementById('stat-favorites').textContent = stats.favorites || 0;
        document.getElementById('stat-collaborators').textContent = stats.collaborators || 0;
    } catch (e) { console.error('Stats failed:', e); }

    // Load recent documents
    try {
        const recent = await api.get('/users/me/recent?limit=5');
        const container = document.getElementById('recent-documents');
        if (recent && recent.length > 0) {
            container.innerHTML = recent.map(doc => `
                <a href="${appUrl('/documents/' + doc.id)}" class="doc-list-item">
                    <span class="doc-icon">${doc.icon || '📄'}</span>
                    <span class="doc-title">${escapeHtml(doc.title || 'Untitled')}</span>
                    <span class="doc-date">${formatDate(doc.updated_at)}</span>
                </a>
            `).join('');
        }
    } catch (e) { console.error('Recent failed:', e); }

    // Load favorites
    try {
        const favs = await api.get('/users/me/favorites?limit=5');
        const container = document.getElementById('favorite-documents');
        if (favs && favs.length > 0) {
            container.innerHTML = favs.map(doc => `
                <a href="${appUrl('/documents/' + doc.id)}" class="doc-list-item">
                    <span class="doc-icon">${doc.icon || '⭐'}</span>
                    <span class="doc-title">${escapeHtml(doc.title || 'Untitled')}</span>
                    <span class="doc-date">${formatDate(doc.updated_at)}</span>
                </a>
            `).join('');
        }
    } catch (e) { console.error('Favorites failed:', e); }

    // Load activity
    try {
        const activities = await api.get('/users/me/activity?limit=10');
        const container = document.getElementById('activity-feed');
        if (activities && activities.length > 0) {
            container.innerHTML = activities.map(act => `
                <div class="activity-item">
                    <div class="activity-icon"><i class="${getActivityIcon(act.action)}"></i></div>
                    <span class="activity-text">${escapeHtml(act.description || act.action)}</span>
                    <span class="activity-time">${formatDate(act.timestamp)}</span>
                </div>
            `).join('');
        }
    } catch (e) { console.error('Activity failed:', e); }
}

function getActivityIcon(action) {
    const icons = {
        'doc_created': 'ri-file-add-line',
        'doc_updated': 'ri-edit-line',
        'doc_deleted': 'ri-delete-bin-line',
        'doc_published': 'ri-send-plane-line',
        'comment_added': 'ri-chat-1-line',
        'login': 'ri-login-box-line',
        'logout': 'ri-logout-box-line',
    };
    return icons[action] || 'ri-time-line';
}

// ============ New Document Modal ============

async function initNewDocModal() {
    const modal = document.getElementById('new-doc-modal');
    const btn = document.getElementById('new-doc-btn');
    const createBtn = document.getElementById('create-doc-btn');
    const wsSelect = document.getElementById('doc-workspace');

    btn?.addEventListener('click', async () => {
        modal.classList.add('active');
        await loadWorkspaceOptions(wsSelect);
        document.getElementById('doc-title')?.focus();
    });

    createBtn?.addEventListener('click', async () => {
        const title = document.getElementById('doc-title')?.value || 'Untitled';
        const workspace_id = wsSelect?.value;
        const template = document.querySelector('input[name="template"]:checked')?.value || 'blank';

        if (!workspace_id) {
            toast.error('Please select a workspace');
            return;
        }

        const templates = {
            blank: '',
            meeting: `# Meeting Notes\n\n**Date:** ${new Date().toISOString().split('T')[0]}\n**Participants:** \n\n## Agenda\n\n1. \n\n## Discussion\n\n\n## Action Items\n\n- [ ] \n`,
            experiment: `# Experiment: ${title}\n\n**Date:** ${new Date().toISOString().split('T')[0]}\n**Researcher:** \n\n## Objective\n\n\n## Materials & Methods\n\n\n## Results\n\n\n## Analysis\n\n\n## Conclusion\n\n`,
        };

        try {
            createBtn.disabled = true;
            createBtn.textContent = 'Creating...';
            const doc = await api.post('/documents', {
                title,
                workspace_id,
                content: templates[template] || '',
            });
            toast.success('Document created');
            window.location.href = appUrl(`/documents/${doc.id}/edit`);
        } catch (e) {
            toast.error('Failed to create document');
            createBtn.disabled = false;
            createBtn.textContent = 'Create';
        }
    });

    // Close modal on backdrop click
    modal?.querySelector('.modal-backdrop')?.addEventListener('click', () => modal.classList.remove('active'));
}

// ============ Import Modal (Functional) ============

function initImportModal() {
    const modal = document.getElementById('import-modal');
    const btn = document.getElementById('import-btn');
    const zone = document.getElementById('import-zone');
    const fileInput = document.getElementById('import-file');
    const wsSelect = document.getElementById('import-workspace');

    btn?.addEventListener('click', async () => {
        modal.classList.add('active');
        await loadWorkspaceOptions(wsSelect);
    });

    zone?.addEventListener('click', () => fileInput?.click());
    zone?.addEventListener('dragover', (e) => {
        e.preventDefault();
        zone.style.borderColor = 'var(--accent-primary)';
        zone.style.background = 'var(--accent-primary-light)';
    });
    zone?.addEventListener('dragleave', () => {
        zone.style.borderColor = 'var(--border-color)';
        zone.style.background = '';
    });
    zone?.addEventListener('drop', (e) => {
        e.preventDefault();
        zone.style.borderColor = 'var(--border-color)';
        zone.style.background = '';
        const files = e.dataTransfer.files;
        if (files.length > 0) importFiles(files, wsSelect?.value);
    });

    fileInput?.addEventListener('change', (e) => {
        const files = e.target.files;
        if (files.length > 0) importFiles(files, wsSelect?.value);
    });

    modal?.querySelector('.modal-backdrop')?.addEventListener('click', () => modal.classList.remove('active'));
}

async function importFiles(files, workspace_id) {
    if (!workspace_id) {
        toast.error('Please select a workspace first');
        return;
    }

    let imported = 0;
    for (const file of files) {
        try {
            const content = await file.text();
            const title = file.name.replace(/\.(md|txt|markdown)$/i, '');
            await api.post('/documents', { title, workspace_id, content });
            imported++;
        } catch (e) {
            toast.error(`Failed to import: ${file.name}`);
        }
    }

    if (imported > 0) {
        toast.success(`${imported} document(s) imported`);
        document.getElementById('import-modal').classList.remove('active');
        setTimeout(() => loadDashboardData(), 500);
    }
}

// ============ Feedback Modal (Functional) ============

function initFeedbackModal() {
    const modal = document.getElementById('feedback-modal');
    const link = document.getElementById('feedback-link');
    const submitBtn = document.getElementById('submit-feedback-btn');
    let selectedType = 'general';

    link?.addEventListener('click', () => modal.classList.add('active'));

    // Type selection
    document.querySelectorAll('.feedback-type-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.feedback-type-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            selectedType = btn.dataset.type;
        });
    });

    submitBtn?.addEventListener('click', async () => {
        const title = document.getElementById('feedback-title')?.value?.trim();
        const message = document.getElementById('feedback-message')?.value?.trim();

        if (!title || !message) {
            toast.error('Please fill in all fields');
            return;
        }

        try {
            submitBtn.disabled = true;
            submitBtn.textContent = 'Sending...';
            await api.post('/feedback', { type: selectedType, title, message });
            toast.success('Thank you for your feedback!');
            modal.classList.remove('active');
            document.getElementById('feedback-title').value = '';
            document.getElementById('feedback-message').value = '';
        } catch (e) {
            toast.error('Failed to send feedback');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Send Feedback';
        }
    });

    modal?.querySelector('.modal-backdrop')?.addEventListener('click', () => modal.classList.remove('active'));
}

// ============ Shortcuts Modal (Functional) ============

function initShortcutsModal() {
    const modal = document.getElementById('shortcuts-modal');
    const link = document.getElementById('shortcuts-link');
    const grid = document.getElementById('shortcuts-grid');

    const shortcuts = [
        { keys: ['Ctrl', 'B'], desc: 'Bold' },
        { keys: ['Ctrl', 'I'], desc: 'Italic' },
        { keys: ['Ctrl', 'K'], desc: 'Insert Link / Command Palette' },
        { keys: ['Ctrl', 'S'], desc: 'Save' },
        { keys: ['Ctrl', 'Z'], desc: 'Undo' },
        { keys: ['Ctrl', 'Shift', 'Z'], desc: 'Redo' },
        { keys: ['Tab'], desc: 'Indent' },
        { keys: ['Ctrl', '/'], desc: 'Toggle Preview' },
        { keys: ['Ctrl', 'Shift', 'E'], desc: 'Export PDF' },
    ];

    if (grid) {
        grid.innerHTML = shortcuts.map(s => `
            <div class="shortcut-item">
                <span>${s.desc}</span>
                <span class="shortcut-keys">${s.keys.map(k => `<span class="kbd">${k}</span>`).join('+')}</span>
            </div>
        `).join('');
    }

    link?.addEventListener('click', () => modal.classList.add('active'));
    modal?.querySelector('.modal-backdrop')?.addEventListener('click', () => modal.classList.remove('active'));
}

// ============ Helpers ============

async function loadWorkspaceOptions(selectEl) {
    if (!selectEl) return;
    try {
        const orgs = await api.get('/organizations');
        let options = '';
        for (const org of orgs) {
            try {
                const workspaces = await api.get(`/organizations/${org.id}/workspaces`);
                for (const ws of workspaces) {
                    options += `<option value="${ws.id}">${ws.icon || '📁'} ${escapeHtml(ws.name)}</option>`;
                }
            } catch (e) {}
        }
        selectEl.innerHTML = options || '<option value="">No workspaces available</option>';
    } catch (e) {
        selectEl.innerHTML = '<option value="">Failed to load workspaces</option>';
    }
}
