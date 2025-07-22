document.addEventListener('DOMContentLoaded', function() {
    // Modal elements
    const deleteModal = document.getElementById('delete-confirm-modal');
    const deleteForm = document.getElementById('delete-form');
    const closeModalBtn = deleteModal.querySelector('.close-modal');
    const cancelDeleteBtn = document.getElementById('cancel-delete');
    const allDeleteButtons = document.querySelectorAll('.delete-btn');
    
    // Function to show the delete confirmation modal
    const showDeleteModal = (cameraId, cameraUrl) => {
        // Set the URL in the modal for user confirmation
        deleteModal.querySelector('.camera-url').textContent = cameraUrl;
        
        // Set the form's action to the correct deletion URL
        const deleteUrl = `/delete_camera/${cameraId}`;
        deleteForm.setAttribute('action', deleteUrl);
        
        // Show the modal
        deleteModal.classList.add('show');
    };
    
    // Function to hide the delete confirmation modal
    const hideDeleteModal = () => {
        deleteModal.classList.remove('show');
    };

    // Add click event listeners to all delete buttons
    allDeleteButtons.forEach(button => {
        button.addEventListener('click', () => {
            const cameraId = button.dataset.cameraId;
            const cameraUrl = button.dataset.cameraUrl;
            showDeleteModal(cameraId, cameraUrl);
        });
    });

    // Modal event listeners
    closeModalBtn.addEventListener('click', hideDeleteModal);
    cancelDeleteBtn.addEventListener('click', hideDeleteModal);

    // Mobile navigation toggle
    const mobileNavToggle = document.getElementById('mobile-nav-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (mobileNavToggle && sidebar) {
        mobileNavToggle.addEventListener('click', () => {
            sidebar.classList.toggle('show');
        });
    }
});