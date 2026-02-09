/**
 * Document Viewer JavaScript - PSID LAB Edition
 * Features: Source view toggle, Frontmatter header, PDF/MD export, Comments, Highlights
 */

document.addEventListener('DOMContentLoaded', () => {
    initViewer();
    initViewModeToggle();
    initFrontmatterHeader();
    loadComments();
    buildTableOfContents();
    initHighlighting();
});

// ============ Core Viewer Init ============
function initViewer() {
    // Favorite button
    const favoriteBtn = document.getElementById('favorite-btn');
    if (favoriteBtn) {
        favoriteBtn.addEventListener('click', toggleFavorite);
    }

    // TOC toggle
    const tocToggle = document.getElementById('toc-toggle-btn');
    const tocSidebar = document.getElementById('toc-sidebar');
    
    if (tocToggle && tocSidebar) {
        tocToggle.addEventListener('click', () => tocSidebar.classList.toggle('active'));
        document.getElementById('toc-close')?.addEventListener('click', () => tocSidebar.classList.remove('active'));
    }

    // Comments toggle
    const commentsToggle = document.getElementById('comments-toggle');
    const commentsSidebar = document.getElementById('comments-sidebar');
    
    if (commentsToggle && commentsSidebar) {
        commentsToggle.addEventListener('click', () => commentsSidebar.classList.toggle('active'));
        document.getElementById('comments-close')?.addEventListener('click', () => commentsSidebar.classList.remove('active'));
    }

    initFontSize();
    initMoreActions();
    initHighlightColors();
    initDeleteModal();
}

// ============ View Mode Toggle (Rendered / Source / Split) ============
function initViewModeToggle() {
    const renderedBtn = document.getElementById('rendered-view-btn');
    const sourceBtn = document.getElementById('source-view-btn');
    const splitBtn = document.getElementById('split-view-btn');
    const documentContent = document.getElementById('document-content');
    const sourceView = document.getElementById('source-view');
    const viewerMain = document.getElementById('viewer-main');

    if (!renderedBtn || !sourceBtn || !splitBtn) return;

    function setViewMode(mode) {
        // Remove all active states
        [renderedBtn, sourceBtn, splitBtn].forEach(b => b.classList.remove('active'));
        viewerMain.classList.remove('split-view');
        
        switch (mode) {
            case 'rendered':
                renderedBtn.classList.add('active');
                documentContent.style.display = '';
                sourceView.style.display = 'none';
                break;
            case 'source':
                sourceBtn.classList.add('active');
                documentContent.style.display = 'none';
                sourceView.style.display = '';
                break;
            case 'split':
                splitBtn.classList.add('active');
                documentContent.style.display = '';
                sourceView.style.display = '';
                viewerMain.classList.add('split-view');
                break;
        }
        
        localStorage.setItem('viewer-mode', mode);
    }

    renderedBtn.addEventListener('click', () => setViewMode('rendered'));
    sourceBtn.addEventListener('click', () => setViewMode('source'));
    splitBtn.addEventListener('click', () => setViewMode('split'));

    // Source view actions
    const copySourceBtn = document.getElementById('copy-source-btn');
    if (copySourceBtn) {
        copySourceBtn.addEventListener('click', () => {
            const sourceContent = document.getElementById('source-content');
            if (sourceContent) {
                navigator.clipboard.writeText(sourceContent.textContent).then(() => {
                    toast.success('원문이 클립보드에 복사되었습니다');
                }).catch(() => {
                    toast.error('복사에 실패했습니다');
                });
            }
        });
    }

    const wrapSourceBtn = document.getElementById('wrap-source-btn');
    if (wrapSourceBtn) {
        wrapSourceBtn.addEventListener('click', () => {
            const sourceContent = document.getElementById('source-content');
            if (sourceContent) {
                sourceContent.classList.toggle('nowrap');
                wrapSourceBtn.classList.toggle('active');
            }
        });
    }

    // Restore saved mode
    const savedMode = localStorage.getItem('viewer-mode') || 'rendered';
    setViewMode(savedMode);
}

// ============ Frontmatter Header ============
function initFrontmatterHeader() {
    const collapseBtn = document.getElementById('fm-collapse-btn');
    const fmBody = document.getElementById('fm-body');
    
    if (!collapseBtn || !fmBody) return;
    
    // Restore saved collapse state
    const isCollapsed = localStorage.getItem('fm-collapsed') === 'true';
    if (isCollapsed) {
        fmBody.classList.add('collapsed');
        collapseBtn.classList.add('collapsed');
    }
    
    collapseBtn.addEventListener('click', () => {
        fmBody.classList.toggle('collapsed');
        collapseBtn.classList.toggle('collapsed');
        localStorage.setItem('fm-collapsed', fmBody.classList.contains('collapsed'));
    });
}

// ============ Favorite Toggle ============
async function toggleFavorite() {
    const btn = document.getElementById('favorite-btn');
    const isFavorited = btn.dataset.favorited === 'true';
    
    try {
        if (isFavorited) {
            await api.delete(`/documents/${DOCUMENT_ID}/favorite`);
            btn.dataset.favorited = 'false';
            btn.querySelector('i').className = 'ri-star-line';
            toast.success('즐겨찾기에서 제거되었습니다');
        } else {
            await api.post(`/documents/${DOCUMENT_ID}/favorite`, {});
            btn.dataset.favorited = 'true';
            btn.querySelector('i').className = 'ri-star-fill';
            toast.success('즐겨찾기에 추가되었습니다');
        }
        btn.classList.toggle('active');
    } catch (error) {
        toast.error('오류가 발생했습니다');
    }
}

// ============ Font Size ============
function initFontSize() {
    let fontSize = parseInt(localStorage.getItem('viewer-font-size')) || 100;
    updateFontSize(fontSize);

    document.getElementById('font-decrease')?.addEventListener('click', () => {
        fontSize = Math.max(75, fontSize - 10);
        updateFontSize(fontSize);
    });

    document.getElementById('font-increase')?.addEventListener('click', () => {
        fontSize = Math.min(150, fontSize + 10);
        updateFontSize(fontSize);
    });
}

function updateFontSize(size) {
    localStorage.setItem('viewer-font-size', size);
    document.getElementById('font-size-value').textContent = `${size}%`;
    document.getElementById('document-content').style.fontSize = `${size}%`;
    const sourceContent = document.getElementById('source-content');
    if (sourceContent) {
        sourceContent.style.fontSize = `${Math.max(11, 13 * size / 100)}px`;
    }
}

// ============ Table of Contents ============
function buildTableOfContents() {
    const content = document.getElementById('document-content');
    const tocContent = document.getElementById('toc-content');
    if (!content || !tocContent) return;

    const headings = content.querySelectorAll('h1, h2, h3');
    if (headings.length === 0) {
        tocContent.innerHTML = '<p class="toc-empty">목차가 없습니다</p>';
        return;
    }

    let html = '';
    headings.forEach((heading, i) => {
        const id = `heading-${i}`;
        heading.id = id;
        const level = heading.tagName.toLowerCase();
        html += `<a href="#${id}" class="toc-link toc-link-${level}">${heading.textContent}</a>`;
    });

    tocContent.innerHTML = html;

    tocContent.querySelectorAll('.toc-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = document.querySelector(link.getAttribute('href'));
            if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    });
}

// ============ Comments ============
async function loadComments() {
    const container = document.getElementById('comments-list');
    const countBadge = document.getElementById('comments-count');
    if (!container) return;

    try {
        const comments = await api.get(`/documents/${DOCUMENT_ID}/comments`);
        countBadge.textContent = comments.length;

        if (comments.length === 0) {
            container.innerHTML = '<div class="comments-empty">댓글이 없습니다</div>';
            return;
        }

        container.innerHTML = comments.map(comment => `
            <div class="comment-item" data-id="${comment.id}" ${comment.anchor_text ? `data-anchor="${escapeHtml(comment.anchor_text)}"` : ''}>
                ${comment.anchor_text ? `<div class="comment-quote">"${escapeHtml(comment.anchor_text.substring(0, 100))}${comment.anchor_text.length > 100 ? '...' : ''}"</div>` : ''}
                <div class="comment-author">
                    <div class="comment-avatar">${(comment.author_name || 'U')[0].toUpperCase()}</div>
                    <span class="comment-name">${escapeHtml(comment.author_name || 'Unknown')}</span>
                    <span class="comment-time">${formatDate(comment.created_at)}</span>
                </div>
                <div class="comment-text">${escapeHtml(comment.content)}</div>
            </div>
        `).join('');
        
        container.querySelectorAll('.comment-item[data-anchor]').forEach(item => {
            item.addEventListener('mouseenter', () => highlightTextInDocument(item.dataset.anchor, true));
            item.addEventListener('mouseleave', () => clearDocumentHighlights());
            item.addEventListener('click', () => scrollToTextInDocument(item.dataset.anchor));
        });
        
        applyPersistentHighlights(comments);
    } catch (error) {
        console.error('Failed to load comments:', error);
    }
}

function applyPersistentHighlights(comments) {
    const content = document.getElementById('document-content');
    if (!content) return;
    
    const anchors = comments.filter(c => c.anchor_text).map(c => ({ id: c.id, text: c.anchor_text }));
    if (anchors.length === 0) return;
    
    anchors.forEach(anchor => {
        const searchText = anchor.text.substring(0, 80);
        const walker = document.createTreeWalker(content, NodeFilter.SHOW_TEXT, null, false);
        let node;
        
        while (node = walker.nextNode()) {
            const index = node.textContent.indexOf(searchText);
            if (index !== -1) {
                try {
                    const range = document.createRange();
                    range.setStart(node, index);
                    range.setEnd(node, Math.min(index + anchor.text.length, node.textContent.length));
                    
                    const mark = document.createElement('mark');
                    mark.className = 'comment-highlight-permanent';
                    mark.dataset.commentId = anchor.id;
                    range.surroundContents(mark);
                    
                    mark.addEventListener('click', () => {
                        const commentItem = document.querySelector(`.comment-item[data-id="${anchor.id}"]`);
                        if (commentItem) {
                            commentItem.scrollIntoView({ behavior: 'smooth', block: 'center' });
                            commentItem.classList.add('comment-highlight-active');
                            setTimeout(() => commentItem.classList.remove('comment-highlight-active'), 2000);
                        }
                    });
                } catch (e) {
                    // Range spans multiple nodes
                }
                break;
            }
        }
    });
}

function highlightTextInDocument(text, highlight) {
    const content = document.getElementById('document-content');
    if (!content || !text) return;
    clearDocumentHighlights();
    if (!highlight) return;
    
    const walker = document.createTreeWalker(content, NodeFilter.SHOW_TEXT, null, false);
    let node;
    
    while (node = walker.nextNode()) {
        const index = node.textContent.indexOf(text.substring(0, 50));
        if (index !== -1) {
            const range = document.createRange();
            range.setStart(node, index);
            range.setEnd(node, Math.min(index + text.length, node.textContent.length));
            
            const mark = document.createElement('mark');
            mark.className = 'comment-highlight-temp';
            
            try {
                range.surroundContents(mark);
                mark.scrollIntoView({ behavior: 'smooth', block: 'center' });
            } catch (e) {}
            break;
        }
    }
}

function clearDocumentHighlights() {
    document.querySelectorAll('.comment-highlight-temp').forEach(mark => {
        const parent = mark.parentNode;
        parent.replaceChild(document.createTextNode(mark.textContent), mark);
        parent.normalize();
    });
}

function scrollToTextInDocument(text) {
    highlightTextInDocument(text, true);
}

// ============ Comment Submission ============
let pendingAnchorText = null;

document.getElementById('submit-comment')?.addEventListener('click', async () => {
    const textarea = document.getElementById('new-comment');
    const content = textarea.value.trim();
    if (!content) return;

    try {
        await api.post(`/documents/${DOCUMENT_ID}/comments`, { 
            content,
            anchor_text: pendingAnchorText || null
        });
        textarea.value = '';
        pendingAnchorText = null;
        loadComments();
        toast.success('댓글이 추가되었습니다');
    } catch (error) {
        toast.error('댓글 추가에 실패했습니다');
    }
});

// ============ Highlight Colors ============
let selectedColor = '#fff59d';

function initHighlightColors() {
    document.querySelectorAll('.highlight-color').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.highlight-color').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            selectedColor = btn.dataset.color;
        });
    });
}

// ============ Highlighting ============
function initHighlighting() {
    const content = document.getElementById('document-content');
    const popup = document.getElementById('highlight-popup');
    if (!content || !popup || !CAN_EDIT) return;

    let selection = null;

    content.addEventListener('mouseup', (e) => {
        const sel = window.getSelection();
        if (sel.toString().trim().length > 0) {
            selection = { text: sel.toString(), range: sel.getRangeAt(0) };
            popup.style.display = 'flex';
            popup.style.left = `${e.pageX - 40}px`;
            popup.style.top = `${e.pageY - 45}px`;
        } else {
            popup.style.display = 'none';
        }
    });

    document.getElementById('add-highlight')?.addEventListener('click', async () => {
        if (!selection) return;
        try {
            const span = document.createElement('span');
            span.className = 'highlight-text';
            span.style.background = selectedColor;
            selection.range.surroundContents(span);
            toast.success('하이라이트가 추가되었습니다');
        } catch (e) {
            toast.error('선택 범위가 너무 복잡합니다. 더 짧은 텍스트를 선택해주세요.');
        }
        popup.style.display = 'none';
    });

    document.getElementById('copy-text')?.addEventListener('click', () => {
        if (selection) {
            navigator.clipboard.writeText(selection.text);
            toast.success('클립보드에 복사되었습니다');
        }
        popup.style.display = 'none';
    });

    document.getElementById('add-comment')?.addEventListener('click', () => {
        const commentsSidebar = document.getElementById('comments-sidebar');
        if (commentsSidebar) {
            commentsSidebar.classList.add('active');
            const commentInput = document.getElementById('new-comment');
            if (selection) {
                pendingAnchorText = selection.text;
                if (commentInput) {
                    commentInput.value = `"${selection.text.substring(0, 50)}${selection.text.length > 50 ? '...' : ''}" - `;
                    commentInput.focus();
                }
            }
        }
        popup.style.display = 'none';
    });
}

// ============ More Actions (Export, History, etc.) ============
function initMoreActions() {
    const btn = document.getElementById('more-actions-btn');
    const menu = document.getElementById('more-actions-menu');
    
    if (btn && menu) {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            menu.classList.toggle('show');
        });
        document.addEventListener('click', () => menu.classList.remove('show'));
    }

    document.getElementById('copy-link-btn')?.addEventListener('click', () => {
        navigator.clipboard.writeText(window.location.href);
        toast.success('링크가 클립보드에 복사되었습니다');
    });

    document.getElementById('print-btn')?.addEventListener('click', () => window.print());

    // PDF Export
    document.getElementById('export-pdf-btn')?.addEventListener('click', async () => {
        toast.info('PDF를 생성하고 있습니다...');
        try {
            const rootPath = window.ROOT_PATH || '';
            const response = await fetch(`${rootPath}/api/v1/export/documents/${DOCUMENT_ID}/pdf`, {
                headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
                credentials: 'include'
            });
            if (!response.ok) throw new Error('PDF generation failed');
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = (document.getElementById('document-title')?.textContent || 'document') + '.pdf';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            toast.success('PDF 다운로드가 완료되었습니다');
        } catch (e) {
            toast.error('PDF 내보내기 실패: ' + e.message);
        }
    });

    // Markdown Download
    document.getElementById('export-md-btn')?.addEventListener('click', async () => {
        try {
            const rootPath = window.ROOT_PATH || '';
            const response = await fetch(`${rootPath}/api/v1/export/documents/${DOCUMENT_ID}/markdown`, {
                headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
                credentials: 'include'
            });
            if (!response.ok) throw new Error('Download failed');
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = (document.getElementById('document-title')?.textContent || 'document') + '.md';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            toast.success('마크다운 다운로드가 완료되었습니다');
        } catch (e) {
            toast.error('다운로드 실패: ' + e.message);
        }
    });

    // Version History
    document.getElementById('history-btn')?.addEventListener('click', async () => {
        const modal = document.getElementById('history-modal');
        const list = document.getElementById('version-list');
        if (!modal || !list) return;
        
        modal.classList.add('active');
        list.innerHTML = '<div class="loading-state"><div class="loading-spinner"></div></div>';
        
        try {
            const versions = await api.get(`/documents/${DOCUMENT_ID}/versions`);
            if (versions.length === 0) {
                list.innerHTML = '<div class="empty-state"><i class="ri-history-line"></i><span>버전 기록이 없습니다</span></div>';
                return;
            }
            list.innerHTML = versions.map(v => `
                <div class="doc-list-item" style="padding: 12px;">
                    <span class="doc-icon"><i class="ri-history-line"></i></span>
                    <div style="flex:1;">
                        <div style="font-weight:500;">v${v.version_number} - ${escapeHtml(v.title || 'Untitled')}</div>
                        <div style="font-size:var(--font-size-xs);color:var(--text-muted);">${v.word_count || 0} words${v.change_summary ? ' - ' + escapeHtml(v.change_summary) : ''}</div>
                    </div>
                    <span class="doc-date">${formatDate(v.created_at)}</span>
                </div>
            `).join('');
        } catch (e) {
            list.innerHTML = '<div class="empty-state"><span>버전 목록을 불러올 수 없습니다</span></div>';
        }
    });

    document.getElementById('close-history-modal')?.addEventListener('click', () => {
        document.getElementById('history-modal')?.classList.remove('active');
    });
}

// ============ Delete Document Modal ============
function initDeleteModal() {
    const deleteBtn = document.getElementById('delete-doc-btn');
    const modal = document.getElementById('delete-doc-modal');
    
    if (!deleteBtn || !modal) return;
    
    deleteBtn.addEventListener('click', () => {
        document.getElementById('more-actions-menu')?.classList.remove('show');
        modal.classList.add('active');
    });
    
    document.getElementById('close-delete-doc')?.addEventListener('click', () => {
        modal.classList.remove('active');
    });
    document.getElementById('cancel-delete-doc')?.addEventListener('click', () => {
        modal.classList.remove('active');
    });
    
    document.getElementById('confirm-delete-doc')?.addEventListener('click', async () => {
        try {
            await api.delete(`/documents/${DOCUMENT_ID}`);
            toast.success('문서가 삭제되었습니다');
            window.history.back();
        } catch (error) {
            toast.error('삭제에 실패했습니다');
            modal.classList.remove('active');
        }
    });
}
