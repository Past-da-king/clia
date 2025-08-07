

let messagesContainer;
let messageInput;
let sendBtn;
let attachedFilesContainer;

let attachedFiles = [];
let ws;
let currentAgentMessageParagraph = null; // Global to track the <p> element for streaming
let rawMarkdownBuffer = ""; // Buffer to accumulate raw Markdown for streaming

// Load marked.js for Markdown rendering
const markedScript = document.createElement('script');
markedScript.src = "https://cdn.jsdelivr.net/npm/marked/marked.min.js";
markedScript.onload = () => {
    // Configure marked.js if needed
    marked.setOptions({
        gfm: true, // Use GitHub Flavored Markdown
        breaks: true, // Convert \n to <br>
    });
};
document.head.appendChild(markedScript);

function connectWebSocket() {
    try {
        ws = new WebSocket(`ws://${window.location.host}/ws`);
        console.log('WebSocket object after creation:', ws);
    } catch (error) {
        console.error('Error creating WebSocket:', error);
        ws = null; // Ensure ws is null if creation fails
    }

    console.log('ws before onopen assignment:', ws);
    ws.onopen = (event) => {
        console.log("WebSocket opened:", event);
    };

    ws.onmessage = (event) => {
        const message = JSON.parse(event.data);
        console.log("Received message:", message);
        
        // Reset currentAgentMessageParagraph and rawMarkdownBuffer for new non-streaming messages
        if (message.type !== 'agent_message_stream' && message.type !== 'thoughts') {
            currentAgentMessageParagraph = null;
            rawMarkdownBuffer = "";
        }

        if (message.type === 'agent_message') {
            addAgentResponse(message.content, message.tool_info);
        } else if (message.type === 'agent_message_stream') {
            appendAgentResponse(message.content);
        } else if (message.type === 'thoughts') {
            addThoughts(message.content);
        } else if (message.type === 'tool_call') {
            addToolCall(message.tool_name, message.tool_args);
        } else if (message.type === 'tool_result') {
            addToolResult(message.tool_name, message.result);
        } else if (message.type === 'typing_indicator') {
            if (message.status === 'start') {
                showTypingIndicator();
            } else {
                hideTypingIndicator();
            }
        } else if (message.type === 'error') {
            addErrorMessage(message.content);
        } else if (message.type === 'permission_request') {
            showPermissionPrompt(message.tool_name, message.tool_args);
        }
    };

    ws.onclose = (event) => {
        console.log("WebSocket closed:", event);
        // Attempt to reconnect after a delay
        setTimeout(connectWebSocket, 1000);
    };

    ws.onerror = (event) => {
        console.error("WebSocket error:", event);
    };
}

function getFileIcon(fileType) {
    if (fileType.startsWith('image/')) return 'fa-solid fa-file-image';
    if (fileType.startsWith('video/')) return 'fa-solid fa-file-video';
    if (fileType.startsWith('audio/')) return 'fa-solid fa-file-audio';
    if (fileType.startsWith('application/pdf')) return 'fa-solid fa-file-pdf';
    if (fileType.startsWith('text/')) return 'fa-solid fa-file-lines';
    return 'fa-solid fa-file';
}

function handleFileUpload(input) {
    if (input.files.length > 0) {
        Array.from(input.files).forEach(file => {
            if (!attachedFiles.some(f => f.name === file.name && f.size === file.size)) {
                 attachedFiles.push(file);
            }
        });
        updateAttachedFiles();
    }
    input.value = ''; // Reset the input value to allow re-selecting the same file
}

function updateAttachedFiles() {
    attachedFilesContainer.innerHTML = '';
    attachedFiles.forEach((file, index) => {
        const fileDiv = document.createElement('div');
        fileDiv.className = 'flex items-center gap-2 px-3 py-1.5 text-sm rounded-full bg-cli-surface border border-cli-border text-cli-text-secondary';
        fileDiv.innerHTML = `
            <i class="${getFileIcon(file.type)}"></i>
            <span class="font-mono">${file.name}</span>
            <button class="text-red-400 hover:text-red-300" onclick="removeFile(${index})"><i class="fa-solid fa-times-circle"></i></button>
        `;
        attachedFilesContainer.appendChild(fileDiv);
    });
    updateSendButtonState();
}

function removeFile(index) {
    attachedFiles.splice(index, 1);
    updateAttachedFiles();
}

async function sendMessage() {
    const message = messageInput.value.trim();
    if (message || attachedFiles.length > 0) {
        addUserMessage(message, attachedFiles);
        
        const filesToSend = await Promise.all(attachedFiles.map(async file => {
            return new Promise((resolve) => {
                const reader = new FileReader();
                reader.onload = (e) => {
                    resolve({
                        filename: file.name,
                        content_base64: e.target.result.split(',')[1], // Get base64 part
                        mime_type: file.type
                    });
                };
                reader.readAsDataURL(file);
            });
        }));

        ws.send(JSON.stringify({
            type: "user_message",
            text: message,
            files: filesToSend
        }));

        messageInput.value = '';
        messageInput.style.height = 'auto'; // Reset height
        attachedFiles = [];
        updateAttachedFiles();
    }
}

function addUserMessage(text, files) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'flex justify-end message user fade-in-up';
    
    let contentHTML = '';
    if (text) {
        contentHTML += `<div class="p-4 rounded-lg rounded-tr-none bg-cli-accent-dark text-white">${marked.parse(text)}</div>`;
    }

    if (files.length > 0) {
        const filesHTML = files.map(file => {
            const url = URL.createObjectURL(file);
            if (file.type.startsWith('image/')) {
                return `<div class="mt-2 overflow-hidden border rounded-md border-cli-border"><img src="${url}" alt="Uploaded image" class="block w-full h-auto max-w-xs"></div>`;
            }
            if (file.type.startsWith('video/')) {
                return `<div class="mt-2 overflow-hidden border rounded-md border-cli-border"><video controls src="${url}" class="block w-full h-auto max-w-xs"></video></div>`;
            }
            if (file.type.startsWith('audio/')) {
                return `<div class="mt-2"><audio controls src="${url}" class="w-full max-w-xs"></audio></div>`;
            }
            return `<div class="mt-2 p-3 text-sm rounded-md bg-cli-surface flex items-center gap-3"><i class="${getFileIcon(file.type)} text-cli-text-secondary"></i><span class="font-mono">${file.name}</span></div>`;
        }).join('');
        contentHTML += `<div class="flex flex-col gap-2 mt-2">${filesHTML}</div>`;
    }

    messageDiv.innerHTML = `<div class="max-w-md">${contentHTML}</div>`;
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

function addAgentResponse(text, toolInfo = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'flex items-start gap-4 message agent fade-in-up';

    let toolInfoHtml = '';
    if (toolInfo) {
        toolInfoHtml = `
            <div class="p-3 mt-1 text-sm border-l-4 rounded bg-cli-green/10 border-cli-green font-mono">
                <p class="font-semibold text-cli-green">${toolInfo.title}</p>
                <p class="text-cli-text-secondary">${toolInfo.details}</p>
            </div>
        `;
    }

    messageDiv.innerHTML = `
        <div class="w-8 h-8 text-lg flex-shrink-0 bg-cli-surface border border-cli-border rounded-full flex items-center justify-center text-cli-accent">
            <i class="fa-solid fa-robot"></i>
        </div>
        <div class="flex flex-col flex-1 gap-2">
            <div class="flex items-start gap-3 font-mono">
                 <span class="mt-0.5 text-cli-text-secondary">></span>
                 <p class="flex-1 text-cli-text"></p> <!-- Empty p tag for streaming -->
            </div>
            ${toolInfoHtml}
        </div>
    `;
    messagesContainer.appendChild(messageDiv);
    currentAgentMessageParagraph = messageDiv.querySelector('.flex-1.text-cli-text');
    rawMarkdownBuffer = text; // Initialize buffer with the first chunk
    renderAgentMessage(); // Render the first chunk
    scrollToBottom();
}

function appendAgentResponse(text) {
    if (currentAgentMessageParagraph) {
        rawMarkdownBuffer += text; // Append to raw buffer
        renderAgentMessage(); // Re-render the whole buffer
        scrollToBottom();
    } else {
        // Fallback if for some reason currentAgentMessageParagraph is not set
        addAgentResponse(text);
    }
}

function renderAgentMessage() {
    if (currentAgentMessageParagraph) {
        currentAgentMessageParagraph.innerHTML = marked.parse(rawMarkdownBuffer);
    }
}

function addThoughts(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'flex items-start gap-4 message agent fade-in-up'; // Re-using agent styling for now

    messageDiv.innerHTML = `
        <div class="w-8 h-8 text-lg flex-shrink-0 bg-cli-surface border border-cli-border rounded-full flex items-center justify-center text-cli-accent">
            <i class="fa-solid fa-brain"></i>
        </div>
        <div class="flex flex-col flex-1 gap-2">
            <div class="p-3 mt-1 text-sm border-l-4 rounded bg-cyan-900/50 border-cli-accent font-mono">
                <p class="font-semibold text-cli-accent">[Thoughts]</p>
                <p class="text-cli-text-secondary">${marked.parse(text)}</p>
            </div>
        </div>
    `;
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

function addToolCall(toolName, toolArgs) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'flex items-start gap-4 message agent fade-in-up'; // Re-using agent styling for now

    messageDiv.innerHTML = `
        <div class="w-8 h-8 text-lg flex-shrink-0 bg-cli-surface border border-cli-border rounded-full flex items-center justify-center text-cli-accent">
            <i class="fa-solid fa-tools"></i>
        </div>
        <div class="flex flex-col flex-1 gap-2">
            <div class="p-3 mt-1 text-sm border-l-4 rounded bg-purple-900/50 border-purple-500 font-mono">
                <p class="font-semibold text-purple-400">[Tool Call]</p>
                <p class="text-cli-text-secondary break-words">Calling tool <code>${toolName}</code> with arguments: <code>${toolArgs}</code></p>
            </div>
        </div>
    `;
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

function addToolResult(toolName, result) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'flex items-start gap-4 message agent fade-in-up'; // Re-using agent styling for now

    messageDiv.innerHTML = `
        <div class="w-8 h-8 text-lg flex-shrink-0 bg-cli-surface border border-cli-border rounded-full flex items-center justify-center text-cli-accent">
            <i class="fa-solid fa-check-circle"></i>
        </div>
        <div class="flex flex-col flex-1 gap-2">
            <div class="p-3 mt-1 text-sm border-l-4 rounded bg-green-900/50 border-green-500 font-mono">
                <p class="font-semibold text-green-400">[Tool Result]</p>
                <p class="text-cli-text-secondary break-words"><pre class="whitespace-pre-wrap">${result}</pre></p>
            </div>
        </div>
    `;
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

function addErrorMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'flex items-start gap-4 message agent fade-in-up'; // Re-using agent styling for now

    messageDiv.innerHTML = `
        <div class="w-8 h-8 text-lg flex-shrink-0 bg-cli-surface border border-cli-border rounded-full flex items-center justify-center text-red-500">
            <i class="fa-solid fa-exclamation-triangle"></i>
        </div>
        <div class="flex flex-col flex-1 gap-2">
            <div class="p-3 mt-1 text-sm border-l-4 rounded bg-red-900/50 border-red-500 font-mono">
                <p class="font-semibold text-red-400">[Error]</p>
                <p class="text-cli-text-secondary">${marked.parse(text)}</p>
            </div>
        </div>
    `;
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

function showPermissionPrompt(toolName, toolArgs) {
    const permissionModal = document.createElement('div');
    permissionModal.id = 'permissionModal';
    permissionModal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center';
    permissionModal.innerHTML = `
        <div class="bg-cli-surface p-6 rounded-lg shadow-lg text-white max-w-md w-full">
            <h2 class="text-xl font-bold mb-4">Permission Request</h2>
            <p class="mb-4">The AI wants to run the tool: <strong>${toolName}</strong></p>
            <p class="mb-4">With arguments: <code>${toolArgs}</code></p>
            <div class="flex justify-end gap-4">
                <button id="denyBtn" class="px-4 py-2 rounded bg-red-500 hover:bg-red-600">Deny</button>
                <button id="allowOnceBtn" class="px-4 py-2 rounded bg-gray-500 hover:bg-gray-600">Allow Once</button>
                <button id="allowAlwaysBtn" class="px-4 py-2 rounded bg-green-500 hover:bg-green-600">Always Allow</button>
            </div>
        </div>
    `;
    document.body.appendChild(permissionModal);

    document.getElementById('denyBtn').onclick = () => {
        ws.send(JSON.stringify({ type: 'permission_response', allow: false }));
        document.body.removeChild(permissionModal);
    };

    document.getElementById('allowOnceBtn').onclick = () => {
        ws.send(JSON.stringify({ type: 'permission_response', allow: true }));
        document.body.removeChild(permissionModal);
    };

    document.getElementById('allowAlwaysBtn').onclick = () => {
        ws.send(JSON.stringify({ type: 'permission_response', allow: 'always' }));
        document.body.removeChild(permissionModal);
    };
}


function showTypingIndicator() {
    let typingIndicator = document.getElementById('typingIndicator');
    if (!typingIndicator) {
        typingIndicator = document.createElement('div');
        typingIndicator.id = 'typingIndicator';
        typingIndicator.className = 'flex items-start gap-4 fade-in-up';
        typingIndicator.innerHTML = `
            <div class="w-8 h-8 text-lg flex-shrink-0 bg-cli-surface border border-cli-border rounded-full flex items-center justify-center text-cli-accent">
                <i class="fa-solid fa-robot"></i>
            </div>
            <div class="flex items-start flex-1 gap-3 font-mono">
                <span class="mt-0.5 text-cli-text-secondary">></span>
                <span class="text-cli-text-secondary">Agent is typing<span class="inline-block w-1 ml-1 font-bold cursor-blink">_</span></span>
            </div>
        `;
        messagesContainer.appendChild(typingIndicator);
        scrollToBottom();
    }
}

function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function updateSendButtonState() {
    sendBtn.disabled = messageInput.value.trim().length === 0 && attachedFiles.length === 0;
}

// --- Event Listeners ---
// This part needs to be integrated with the actual file input elements
// For example, if you have an input with id="fileUpload":
// document.getElementById('fileUpload').addEventListener('change', function(event) {
//     handleFileUpload(event.target.files);
// });
// Make sure to call updateAttachedFiles() after files are added/removed.
// The current HTML has inline onclicks, which is less ideal but works.
// The handleFileUpload function needs to be globally accessible or attached to window.
window.handleFileUpload = handleFileUpload;
window.removeFile = removeFile;

document.addEventListener('DOMContentLoaded', () => {
    messagesContainer = document.getElementById('messages');
    messageInput = document.getElementById('messageInput');
    sendBtn = document.getElementById('sendBtn');
    attachedFilesContainer = document.getElementById('attachedFiles');

    console.log('messagesContainer:', messagesContainer);
    console.log('messageInput:', messageInput);
    console.log('sendBtn:', sendBtn);
    console.log('attachedFilesContainer:', attachedFilesContainer);

    // Attach event listeners after elements are available
        // Attach event listeners after elements are available
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    messageInput.addEventListener('input', () => {
        // Auto-resize textarea
        const maxHeight = 160; // 10rem
        messageInput.style.height = 'auto';
        messageInput.style.height = `${Math.min(messageInput.scrollHeight, maxHeight)}px`;
        updateSendButtonState();
    });

    sendBtn.addEventListener('click', sendMessage); // Attach sendMessage to button click

    updateSendButtonState();
    connectWebSocket();
});

