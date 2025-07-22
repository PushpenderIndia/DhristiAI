document.addEventListener('DOMContentLoaded', function() {
    // Camera management functionality
    const cameraUrlInput = document.getElementById('camera-url');
    const addCameraBtn = document.getElementById('add-camera');
    const feedsContainer = document.getElementById('feeds-container');
    const camerasStatusEl = document.getElementById('cameras-status');
    const activeCamerasCountEl = document.getElementById('active-cameras-count');
    
    // Modal elements
    const deleteModal = document.getElementById('delete-confirm-modal');
    const closeModalBtn = document.querySelector('.close-modal');
    const cancelDeleteBtn = document.getElementById('cancel-delete');
    const confirmDeleteBtn = document.getElementById('confirm-delete');
    let cameraToDelete = null;
    
    // Local storage key for camera data
    const CAMERAS_STORAGE_KEY = 'dhristiAI_cameras';
    
    // Get cameras from local storage
    const getCameras = () => {
        const camerasJson = localStorage.getItem(CAMERAS_STORAGE_KEY);
        return camerasJson ? JSON.parse(camerasJson) : [];
    };
    
    // Save cameras to local storage
    const saveCameras = (cameras) => {
        localStorage.setItem(CAMERAS_STORAGE_KEY, JSON.stringify(cameras));
    };
    
    // Format camera URL to ensure it has the correct format
    const formatCameraUrl = (url) => {
        let formattedUrl = url.trim();
        
        // Ensure URL has http:// prefix
        if (!formattedUrl.startsWith('http://') && !formattedUrl.startsWith('https://')) {
            formattedUrl = 'http://' + formattedUrl;
        }
        
        // Remove trailing slash if present
        if (formattedUrl.endsWith('/')) {
            formattedUrl = formattedUrl.slice(0, -1);
        }
        
        return formattedUrl;
    };
    
    // Generate a video URL from a camera base URL
    const getVideoUrl = (cameraUrl) => {
        return `${cameraUrl}/video`;
    };
    
    // No longer needed - sidebar camera list has been removed
    
    // Create a camera feed card
    const createCameraFeedCard = (camera) => {
        const card = document.createElement('div');
        card.className = 'glass-card feed-card';
        card.dataset.id = camera.id;
        
        const videoContainer = document.createElement('div');
        videoContainer.className = 'feed-video';
        
        // Create iframe to display camera feed
        const videoElement = document.createElement('iframe');
        videoElement.src = getVideoUrl(camera.url);
        videoElement.width = '100%';
        videoElement.height = '100%';
        videoElement.setAttribute('allowfullscreen', '');
        videoElement.setAttribute('frameborder', '0');
        
        videoContainer.appendChild(videoElement);
        
        const infoContainer = document.createElement('div');
        infoContainer.className = 'feed-info';
        
        const titleContainer = document.createElement('div');
        titleContainer.className = 'feed-title';
        
        const title = document.createElement('h3');
        title.textContent = `Camera ${camera.id.substring(0, 6)}`;
        
        const status = document.createElement('span');
        status.className = 'feed-status';
        status.textContent = 'Online';
        
        titleContainer.appendChild(title);
        titleContainer.appendChild(status);
        
        const address = document.createElement('p');
        address.textContent = camera.url;
        
        const actionsContainer = document.createElement('div');
        actionsContainer.className = 'feed-actions';
        
        const monitorBtn = document.createElement('button');
        monitorBtn.className = 'btn-primary btn-sm';
        monitorBtn.style.flex = '1';
        monitorBtn.innerHTML = '<i class="fas fa-chart-line"></i> View Stats';
        monitorBtn.addEventListener('click', () => {
            window.location.href = `/dashboard?camera=${camera.id}`;
        });
        
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'btn-secondary btn-sm';
        deleteBtn.innerHTML = '<i class="fas fa-trash"></i>';
        deleteBtn.addEventListener('click', () => {
            showDeleteModal(camera);
        });
        
        actionsContainer.appendChild(monitorBtn);
        actionsContainer.appendChild(deleteBtn);
        
        infoContainer.appendChild(titleContainer);
        infoContainer.appendChild(address);
        infoContainer.appendChild(actionsContainer);
        
        card.appendChild(videoContainer);
        card.appendChild(infoContainer);
        
        return card;
    };
    
    // Show delete confirmation modal
    const showDeleteModal = (camera) => {
        cameraToDelete = camera;
        deleteModal.querySelector('.camera-url').textContent = camera.url;
        deleteModal.classList.add('show');
    };
    
    // Hide delete confirmation modal
    const hideDeleteModal = () => {
        deleteModal.classList.remove('show');
        cameraToDelete = null;
    };
    
    // Delete a camera
    const deleteCamera = (cameraId) => {
        let cameras = getCameras();
        cameras = cameras.filter(camera => camera.id !== cameraId);
        saveCameras(cameras);
        renderCameras();
        updateCameraCount(cameras.length);
    };
    
    // Add a new camera
    const addCamera = () => {
        const url = cameraUrlInput.value.trim();
        
        if (!url) {
            alert('Please enter a camera URL');
            return;
        }
        
        const formattedUrl = formatCameraUrl(url);
        
        // Check if camera already exists
        const cameras = getCameras();
        const existingCamera = cameras.find(c => c.url === formattedUrl);
        
        if (existingCamera) {
            alert('This camera is already added');
            return;
        }
        
        // Create new camera
        const newCamera = {
            id: Date.now().toString(36) + Math.random().toString(36).substring(2, 7),
            url: formattedUrl,
            dateAdded: new Date().toISOString()
        };
        
        // Add to storage and render
        cameras.push(newCamera);
        saveCameras(cameras);
        cameraUrlInput.value = '';
        renderCameras();
        updateCameraCount(cameras.length);
    };
    
    // Update camera count display
    const updateCameraCount = (count) => {
        camerasStatusEl.textContent = `${count} Camera${count !== 1 ? 's' : ''} Online`;
        
        // Update dashboard counter if on the same page
        if (activeCamerasCountEl) {
            activeCamerasCountEl.textContent = count;
        }
    };
    
    // Render cameras in sidebar list and main grid
    const renderCameras = () => {
        const cameras = getCameras();
        
            // Don't need to clear camera list items in sidebar anymore, as the camera list has been removed
    // from the sidebar
        
        // Clear existing feed cards
        if (feedsContainer) {
            while (feedsContainer.firstChild) {
                feedsContainer.removeChild(feedsContainer.firstChild);
            }
        }
        
        if (cameras.length === 0) {
            // Show empty state in feed container
            if (feedsContainer) {
                const emptyState = document.createElement('div');
                emptyState.className = 'glass-card feed-card empty-state';
                emptyState.innerHTML = `
                    <div class="feed-video">
                        <div class="video-placeholder">
                            <i class="fas fa-video-slash"></i>
                            <p>No cameras added</p>
                        </div>
                    </div>
                    <div class="feed-info">
                        <div class="feed-title">
                            <h3>Add your first camera</h3>
                            <span class="feed-status offline">Offline</span>
                        </div>
                        <p>Use the form above to add a new camera feed</p>
                    </div>
                `;
                feedsContainer.appendChild(emptyState);
            }
        } else {
            // Add camera feed cards to grid
            if (feedsContainer) {
                cameras.forEach(camera => {
                    feedsContainer.appendChild(createCameraFeedCard(camera));
                });
            }
        }
    };
    
    // Event Listeners
    addCameraBtn.addEventListener('click', addCamera);
    
    cameraUrlInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            addCamera();
        }
    });
    
    // Modal event listeners
    closeModalBtn.addEventListener('click', hideDeleteModal);
    cancelDeleteBtn.addEventListener('click', hideDeleteModal);
    
    confirmDeleteBtn.addEventListener('click', () => {
        if (cameraToDelete) {
            deleteCamera(cameraToDelete.id);
            hideDeleteModal();
        }
    });
    
    // Mobile navigation toggle
    const mobileNavToggle = document.getElementById('mobile-nav-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    mobileNavToggle.addEventListener('click', () => {
        sidebar.classList.toggle('show');
    });
    
    // Initialize camera list
    renderCameras();
    updateCameraCount(getCameras().length);
}); 