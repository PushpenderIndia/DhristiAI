document.addEventListener('DOMContentLoaded', function() {
    // Get the camera management link
    const cameraManagementLink = document.getElementById('camera-management-link');
    
    if (cameraManagementLink) {
        console.log('Camera Management link found');
        
        // Add click event listener
        cameraManagementLink.addEventListener('click', function(e) {
            console.log('Camera Management link clicked');
            // The default behavior (navigating to /live_feed) will happen automatically
        });
    } else {
        console.log('Camera Management link not found');
    }
}); 