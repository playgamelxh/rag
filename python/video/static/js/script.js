// 异步提交表单
document.getElementById('textForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const textInput = document.getElementById('textInput');
    const text = textInput.value.trim();
    if (!text) return;

    // 添加用户输入到对话历史
    addToHistory('user', text);
    textInput.value = '';

    try {
        // 1. 首先获取生成的文字
        const textResponse = await fetch('/generate-text', {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: `text=${encodeURIComponent(text)}`
        });
        const { generated_text, request_id } = await textResponse.json();

        // 添加AI生成文字到对话历史
        addToHistory('ai', generated_text);

        // 2. 然后异步生成视频
        await fetch('/generate-video', {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: `text=${encodeURIComponent(generated_text)}&request_id=${request_id}`
        });
    } catch (error) {
        addToHistory('error', '请求失败，请重试');
        console.error('Error:', error);
    }
});

// 添加消息到对话历史
function addToHistory(sender, content) {
    const historyElement = document.getElementById('conversationHistory');
    const messageDiv = document.createElement('div');
    messageDiv.className = `mb-3 ${sender === 'user' ? 'text-end' : 'text-start'}`;
    messageDiv.innerHTML = `
        <div class="d-inline-block p-2 rounded-3 ${sender === 'user' ? 'bg-primary text-white' : 'bg-light text-dark'}">
            ${content}
        </div>
    `;
    historyElement.appendChild(messageDiv);
    historyElement.scrollTop = historyElement.scrollHeight;
}

// 定时刷新视频文件列表（每5秒）
const VIDEO_REFRESH_INTERVAL = 5000; // 5秒刷新一次
let lastVideoList = [];

// 请求视频文件列表并更新UI
function refreshVideoFiles() {
    fetch('/api/get_video_files')
        .then(response => response.json())
        .then(currentFiles => {
            // 仅在文件列表变化时更新UI
            if (!arraysEqual(currentFiles, lastVideoList)) {
                updateVideoListUI(currentFiles);
                lastVideoList = [...currentFiles];
            }
        })
        .catch(error => console.error('获取视频列表失败:', error));
}

// 比较两个数组是否相等
function arraysEqual(a, b) {
    return a.length === b.length && a.every((val, index) => val === b[index]);
}

// 更新视频列表UI（匹配模板样式）
function updateVideoListUI(files) {
    const container = document.getElementById('videoContainer');
    const emptyState = document.getElementById('emptyState');

    // 隐藏/显示空状态
    if (emptyState)
        emptyState.style.display = files.length > 0 ? 'none' : 'block';

    if (files.length > 0) {
        // 生成符合模板风格的视频网格
        container.innerHTML = `
            <div class="row g-3 p-3">
                ${files.map(file => `
                    <div class="col-md-6">
                        <div class="card h-100 border-0 shadow-sm">
                            <div class="ratio ratio-16x9">
                                <video controls class="rounded-top w-100">
                                    <source src="/static/videos/${file}" type="video/mp4">
                                    您的浏览器不支持视频播放
                                </video>
                            </div>
                            <div class="card-body p-3">
                                <h5 class="card-title fs-6 text-truncate">${file}</h5>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }
}

// 初始加载并启动定时器
window.addEventListener('load', () => {
    refreshVideoFiles(); // 立即加载一次
    setInterval(refreshVideoFiles, VIDEO_REFRESH_INTERVAL);
});

// 格式化文件大小（需要后端配合或简化实现）
function formatFileSize(filePath) {
    // 前端简化版：实际项目建议由后端返回文件大小
    return '未知大小';
}