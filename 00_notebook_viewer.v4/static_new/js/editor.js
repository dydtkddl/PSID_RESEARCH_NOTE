/**
 * Document Editor JavaScript
 */

let saveTimeout = null;
let lastSavedContent = '';
let isUnsaved = false;

document.addEventListener('DOMContentLoaded', () => {
    initEditor();
    initToolbar();
    initPreview();
    initModals();
    
    // Initialize last saved content
    lastSavedContent = document.getElementById('markdown-editor')?.value || '';
});

function initEditor() {
    const editor = document.getElementById('markdown-editor');
    const titleInput = document.getElementById('document-title');
    
    if (!editor) return;

    // Auto-save on content change
    editor.addEventListener('input', () => {
        markUnsaved();
        scheduleAutoSave();
        updateCounts();
        updatePreview();
    });

    // Title change
    titleInput?.addEventListener('input', () => {
        markUnsaved();
        scheduleAutoSave();
    });

    // Keyboard shortcuts
    editor.addEventListener('keydown', handleKeyboard);

    // Update counts initially
    updateCounts();

    // Cursor position
    editor.addEventListener('keyup', updateCursorPosition);
    editor.addEventListener('click', updateCursorPosition);

    // Drag and drop file support on editor
    editor.addEventListener('dragover', (e) => {
        e.preventDefault();
        editor.style.borderColor = 'var(--accent-primary)';
    });
    editor.addEventListener('dragleave', () => {
        editor.style.borderColor = '';
    });
    editor.addEventListener('drop', async (e) => {
        e.preventDefault();
        editor.style.borderColor = '';
        const files = e.dataTransfer.files;
        for (const file of files) {
            await uploadImage(file);
        }
    });

    // Complete button - save before navigating
    const completeBtn = document.getElementById('complete-btn');
    if (completeBtn) {
        completeBtn.addEventListener('click', async () => {
            // Force save before leaving
            const content = editor?.value || '';
            const title = titleInput?.value || 'Untitled';
            
            try {
                completeBtn.disabled = true;
                completeBtn.innerHTML = '<i class="ri-loader-4-line"></i><span>저장 중...</span>';
                
                await api.put(`/documents/${DOCUMENT_ID}`, { title, content });
                markSaved();
                
                // Navigate to viewer after save
                window.location.href = completeBtn.dataset.href;
            } catch (error) {
                toast.error('저장에 실패했습니다. 다시 시도해주세요.');
                completeBtn.disabled = false;
                completeBtn.innerHTML = '<i class="ri-check-line"></i><span>완료</span>';
            }
        });
    }
}

function markUnsaved() {
    isUnsaved = true;
    const status = document.getElementById('save-status');
    if (status) {
        status.innerHTML = '<i class="ri-loader-4-line"></i><span>저장 중...</span>';
        status.className = 'save-status saving';
    }
}

function markSaved() {
    isUnsaved = false;
    const status = document.getElementById('save-status');
    if (status) {
        status.innerHTML = '<i class="ri-check-line"></i><span>저장됨</span>';
        status.className = 'save-status';
    }
}

function scheduleAutoSave() {
    if (saveTimeout) clearTimeout(saveTimeout);
    saveTimeout = setTimeout(saveDocument, 2000);
}

async function saveDocument() {
    const editor = document.getElementById('markdown-editor');
    const titleInput = document.getElementById('document-title');
    
    const content = editor?.value || '';
    const title = titleInput?.value || 'Untitled';

    if (content === lastSavedContent && !isUnsaved) return;

    try {
        await api.put(`/documents/${DOCUMENT_ID}`, { title, content });
        lastSavedContent = content;
        markSaved();
    } catch (error) {
        const status = document.getElementById('save-status');
        if (status) {
            status.innerHTML = '<i class="ri-error-warning-line"></i><span>저장 실패</span>';
            status.className = 'save-status error';
        }
        toast.error('저장에 실패했습니다');
    }
}

function updateCounts() {
    const editor = document.getElementById('markdown-editor');
    const content = editor?.value || '';
    
    // Word count (Korean-aware)
    const words = content.trim().split(/\s+/).filter(w => w.length > 0).length;
    document.getElementById('word-count').textContent = words;
    
    // Character count
    document.getElementById('char-count').textContent = content.length;
}

function updateCursorPosition() {
    const editor = document.getElementById('markdown-editor');
    if (!editor) return;

    const text = editor.value.substring(0, editor.selectionStart);
    const lines = text.split('\n');
    const lineNum = lines.length;
    const colNum = lines[lines.length - 1].length + 1;

    document.getElementById('line-num').textContent = lineNum;
    document.getElementById('col-num').textContent = colNum;
}

function handleKeyboard(e) {
    const editor = e.target;

    // Tab for indentation
    if (e.key === 'Tab') {
        e.preventDefault();
        insertText(editor, '    ');
    }

    // Ctrl+B for bold
    if (e.ctrlKey && e.key === 'b') {
        e.preventDefault();
        wrapSelection(editor, '**', '**');
    }

    // Ctrl+I for italic
    if (e.ctrlKey && e.key === 'i') {
        e.preventDefault();
        wrapSelection(editor, '_', '_');
    }

    // Ctrl+K for link
    if (e.ctrlKey && e.key === 'k') {
        e.preventDefault();
        document.getElementById('link-modal')?.classList.add('active');
    }

    // Ctrl+S for save
    if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        saveDocument();
    }
}

function insertText(editor, text) {
    const start = editor.selectionStart;
    const end = editor.selectionEnd;
    const value = editor.value;
    
    editor.value = value.substring(0, start) + text + value.substring(end);
    editor.selectionStart = editor.selectionEnd = start + text.length;
    editor.dispatchEvent(new Event('input'));
}

function wrapSelection(editor, before, after) {
    const start = editor.selectionStart;
    const end = editor.selectionEnd;
    const value = editor.value;
    const selected = value.substring(start, end);
    
    editor.value = value.substring(0, start) + before + selected + after + value.substring(end);
    editor.selectionStart = start + before.length;
    editor.selectionEnd = end + before.length;
    editor.dispatchEvent(new Event('input'));
}

// Toolbar actions
function initToolbar() {
    document.querySelectorAll('.toolbar-btn[data-action]').forEach(btn => {
        btn.addEventListener('click', () => handleToolbarAction(btn.dataset.action));
    });
}

function handleToolbarAction(action) {
    const editor = document.getElementById('markdown-editor');
    if (!editor) return;

    const actions = {
        bold: () => wrapSelection(editor, '**', '**'),
        italic: () => wrapSelection(editor, '_', '_'),
        strikethrough: () => wrapSelection(editor, '~~', '~~'),
        code: () => wrapSelection(editor, '`', '`'),
        h1: () => insertLine(editor, '# '),
        h2: () => insertLine(editor, '## '),
        h3: () => insertLine(editor, '### '),
        ul: () => insertLine(editor, '- '),
        ol: () => insertLine(editor, '1. '),
        task: () => insertLine(editor, '- [ ] '),
        quote: () => insertLine(editor, '> '),
        link: () => document.getElementById('link-modal')?.classList.add('active'),
        image: () => document.getElementById('image-modal')?.classList.add('active'),
        table: () => insertText(editor, '\n| Header | Header |\n| ------ | ------ |\n| Cell   | Cell   |\n'),
        codeblock: () => wrapSelection(editor, '\n```\n', '\n```\n'),
        math: () => wrapSelection(editor, '$', '$'),
        hr: () => insertText(editor, '\n---\n'),
        undo: () => document.execCommand('undo'),
        redo: () => document.execCommand('redo')
    };

    if (actions[action]) actions[action]();
}

function insertLine(editor, prefix) {
    const start = editor.selectionStart;
    const value = editor.value;
    
    // Find line start
    let lineStart = start;
    while (lineStart > 0 && value[lineStart - 1] !== '\n') lineStart--;
    
    editor.value = value.substring(0, lineStart) + prefix + value.substring(lineStart);
    editor.selectionStart = editor.selectionEnd = start + prefix.length;
    editor.dispatchEvent(new Event('input'));
}

// Preview
function initPreview() {
    const toggle = document.getElementById('preview-toggle');
    const main = document.getElementById('editor-main');
    
    toggle?.addEventListener('click', () => {
        main?.classList.toggle('split');
        updatePreview();
    });
}

function updatePreview() {
    const editor = document.getElementById('markdown-editor');
    const preview = document.getElementById('preview-content');
    
    if (!editor || !preview) return;
    
    // Simple markdown rendering (in production use marked.js)
    let html = editor.value
        .replace(/^### (.*$)/gm, '<h3>$1</h3>')
        .replace(/^## (.*$)/gm, '<h2>$1</h2>')
        .replace(/^# (.*$)/gm, '<h1>$1</h1>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`(.*?)`/g, '<code>$1</code>')
        .replace(/\n/g, '<br>');
    
    preview.innerHTML = html;
    
    // Re-render MathJax if available
    if (typeof MathJax !== 'undefined') {
        MathJax.typesetPromise?.([preview]);
    }
}

// Modals
function initModals() {
    // Link modal
    document.getElementById('insert-link')?.addEventListener('click', () => {
        const text = document.getElementById('link-text')?.value || 'Link';
        const url = document.getElementById('link-url')?.value || '';
        
        if (url) {
            const editor = document.getElementById('markdown-editor');
            insertText(editor, `[${text}](${url})`);
            document.getElementById('link-modal')?.classList.remove('active');
        }
    });

    // Image modal
    const uploadZone = document.getElementById('upload-zone');
    const imageUpload = document.getElementById('image-upload');
    
    uploadZone?.addEventListener('click', () => imageUpload?.click());
    
    imageUpload?.addEventListener('change', async (e) => {
        const file = e.target.files?.[0];
        if (file) await uploadImage(file);
    });

    document.getElementById('insert-image')?.addEventListener('click', () => {
        const url = document.getElementById('image-url')?.value;
        if (url) {
            const editor = document.getElementById('markdown-editor');
            insertText(editor, `![Image](${url})`);
            document.getElementById('image-modal')?.classList.remove('active');
        }
    });
}

async function uploadImage(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
        const rootPath = window.ROOT_PATH || '';
        const response = await fetch(`${rootPath}/api/v1/documents/${DOCUMENT_ID}/upload`, {
            method: 'POST',
            body: formData,
            credentials: 'include',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });

        if (response.ok) {
            const data = await response.json();
            const editor = document.getElementById('markdown-editor');
            
            if (data.is_image) {
                insertText(editor, `![${file.name}](${data.url})`);
            } else {
                // For non-image files, insert as a download link
                const sizeStr = data.size > 1024*1024 ? 
                    `${(data.size/1024/1024).toFixed(1)}MB` : 
                    `${(data.size/1024).toFixed(1)}KB`;
                insertText(editor, `[📎 ${file.name} (${sizeStr})](${data.url})`);
            }
            
            document.getElementById('image-modal')?.classList.remove('active');
            toast.success(`File uploaded: ${file.name}`);
        } else {
            const err = await response.json().catch(() => ({}));
            toast.error(err.detail || 'Upload failed');
        }
    } catch (error) {
        toast.error('File upload failed');
    }
}

// Warn before leaving with unsaved changes
window.addEventListener('beforeunload', (e) => {
    if (isUnsaved) {
        e.preventDefault();
        e.returnValue = '';
    }
});

