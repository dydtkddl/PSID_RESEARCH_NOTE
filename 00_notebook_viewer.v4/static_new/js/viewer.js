/**
 * Document Viewer JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
    initViewer();
    loadComments();
    buildTableOfContents();
    initHighlighting();
});

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
}

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
        
        // Add hover interaction for anchor text highlighting
        container.querySelectorAll('.comment-item[data-anchor]').forEach(item => {
            item.addEventListener('mouseenter', () => {
                const anchorText = item.dataset.anchor;
                highlightTextInDocument(anchorText, true);
            });
            item.addEventListener('mouseleave', () => {
                clearDocumentHighlights();
            });
            item.addEventListener('click', () => {
                const anchorText = item.dataset.anchor;
                scrollToTextInDocument(anchorText);
            });
        });
        
        // Apply persistent highlights for all comments with anchor_text
        applyPersistentHighlights(comments);
    } catch (error) {
        console.error('Failed to load comments:', error);
    }
}

// Apply persistent highlights that stay on page load
function applyPersistentHighlights(comments) {
    console.log('[Highlights] Starting applyPersistentHighlights with', comments.length, 'comments');
    const content = document.getElementById('document-content');
    if (!content) {
        console.log('[Highlights] No document-content element found!');
        return;
    }
    
    // Get all comments with anchor_text
    const anchors = comments.filter(c => c.anchor_text).map(c => ({
        id: c.id,
        text: c.anchor_text
    }));
    
    console.log('[Highlights] Found', anchors.length, 'comments with anchor_text');
    if (anchors.length === 0) return;
    
    // Find and mark all anchor texts
    anchors.forEach(anchor => {
        const searchText = anchor.text.substring(0, 80); // Use first 80 chars for matching
        console.log('[Highlights] Searching for:', searchText.substring(0, 30) + '...');
        const walker = document.createTreeWalker(content, NodeFilter.SHOW_TEXT, null, false);
        let node;
        let found = false;
        
        while (node = walker.nextNode()) {
            const index = node.textContent.indexOf(searchText);
            if (index !== -1) {
                found = true;
                console.log('[Highlights] FOUND match, creating highlight');
                try {
                    const range = document.createRange();
                    range.setStart(node, index);
                    range.setEnd(node, Math.min(index + anchor.text.length, node.textContent.length));
                    
                    const mark = document.createElement('mark');
                    mark.className = 'comment-highlight-permanent';
                    mark.dataset.commentId = anchor.id;
                    
                    range.surroundContents(mark);
                    console.log('[Highlights] Mark element created successfully');
                    
                    // Add click handler to scroll to comment in sidebar
                    mark.addEventListener('click', () => {
                        const commentItem = document.querySelector(`.comment-item[data-id="${anchor.id}"]`);
                        if (commentItem) {
                            commentItem.scrollIntoView({ behavior: 'smooth', block: 'center' });
                            commentItem.classList.add('comment-highlight-active');
                            setTimeout(() => commentItem.classList.remove('comment-highlight-active'), 2000);
                        }
                    });
                } catch (e) {
                    console.log('[Highlights] Error creating mark:', e.message);
                }
                break;
            }
        }
        if (!found) {
            console.log('[Highlights] NOT FOUND in document');
        }
    });
}

// Highlight text in document when hovering over comment
function highlightTextInDocument(text, highlight) {
    const content = document.getElementById('document-content');
    if (!content || !text) return;
    
    // Remove existing temp highlights
    clearDocumentHighlights();
    
    if (!highlight) return;
    
    // Find and highlight matching text
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
            mark.style.cssText = 'background: rgba(255, 200, 0, 0.5); border-radius: 2px; transition: background 0.2s;';
            
            try {
                range.surroundContents(mark);
                mark.scrollIntoView({ behavior: 'smooth', block: 'center' });
            } catch (e) {
                // Range spans multiple nodes, skip
            }
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

// Global variable to store pending anchor text for comment
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
        pendingAnchorText = null;  // Clear after submission
        loadComments();
        toast.success('댓글이 추가되었습니다');
    } catch (error) {
        toast.error('댓글 추가에 실패했습니다');
    }
});

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
            // Selection spans multiple nodes, can't wrap
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

    // Add comment button - opens comments sidebar
    document.getElementById('add-comment')?.addEventListener('click', () => {
        const commentsSidebar = document.getElementById('comments-sidebar');
        if (commentsSidebar) {
            commentsSidebar.classList.add('active');
            const commentInput = document.getElementById('new-comment');
            if (selection) {
                pendingAnchorText = selection.text;  // Store full text for anchor
                if (commentInput) {
                    commentInput.value = `"${selection.text.substring(0, 50)}${selection.text.length > 50 ? '...' : ''}" - `;
                    commentInput.focus();
                }
            }
        }
        popup.style.display = 'none';
    });
}

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
        toast.success('링크가 복사되었습니다');
    });

    document.getElementById('print-btn')?.addEventListener('click', () => window.print());
}

// ============ Delete Document Modal ============
function initDeleteModal() {
    const deleteBtn = document.getElementById('delete-doc-btn');
    const modal = document.getElementById('delete-doc-modal');
    
    if (!deleteBtn || !modal) return;
    
    // Open modal
    deleteBtn.addEventListener('click', () => {
        document.getElementById('more-actions-menu')?.classList.remove('show');
        modal.classList.add('active');
    });
    
    // Close modal
    document.getElementById('close-delete-doc')?.addEventListener('click', () => {
        modal.classList.remove('active');
    });
    document.getElementById('cancel-delete-doc')?.addEventListener('click', () => {
        modal.classList.remove('active');
    });
    
    // Confirm delete
    document.getElementById('confirm-delete-doc')?.addEventListener('click', async () => {
        try {
            await api.delete(`/documents/${DOCUMENT_ID}`);
            toast.success('문서가 삭제되었습니다');
            // Go back to workspace
            window.history.back();
        } catch (error) {
            toast.error('삭제에 실패했습니다');
            modal.classList.remove('active');
        }
    });
}

