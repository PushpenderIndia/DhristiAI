// Dashboard JavaScript for DhristiAI

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const uploadVideoBtn = document.getElementById('upload-video');
    const analyzeVideoBtn = document.getElementById('analyze-video');
    const frameSkipSlider = document.getElementById('frame-skip');
    const maxWorkersSlider = document.getElementById('max-workers');
    const videoPlaceholder = document.querySelector('.video-placeholder');
    const chartContainer = document.getElementById('density-chart');
    const aiRecommendations = document.getElementById('ai-recommendations');
    const aiLoading = document.getElementById('ai-loading');
    const heatmapContainer = document.getElementById('crowd-heatmap');
    const sidebarLinks = document.querySelectorAll('.sidebar-nav a');
    const sidebar = document.querySelector('.sidebar');
    const mobileNavToggle = document.getElementById('mobile-nav-toggle');
    
    // Get AI server URL from hidden input
    const aiServerUrl = document.getElementById('ai-server-url').value;
    
    // Global variables
    let uploadedVideo = null;
    let videoElement = null;
    let chart = null;
    let isProcessing = false;
    
    // Initialize tooltips, popovers, etc. (if needed)
    initDashboard();
    
    // Initialize event listeners
    initEventListeners();
    
    // Dashboard initialization
    function initDashboard() {
        // Any initialization code for the dashboard
        console.log('Dashboard initialized');
        console.log('AI Server URL:', aiServerUrl);
        
        // Create placeholders for data visualizations
        createPlaceholderChart();

        // Update range value displays
        updateRangeValueDisplays();
    }
    
    // Update the value displays for range inputs
    function updateRangeValueDisplays() {
        // Get all range inputs
        const rangeInputs = document.querySelectorAll('input[type="range"]');
        
        // Update value displays
        rangeInputs.forEach(input => {
            // Find the corresponding value display element
            const valueDisplay = input.nextElementSibling;
            if (valueDisplay && valueDisplay.classList.contains('range-value')) {
                // Set initial value
                valueDisplay.textContent = input.value;
                
                // Update on input change
                input.addEventListener('input', function() {
                    valueDisplay.textContent = this.value;
                });
            }
        });
    }

    // Initialize sidebar navigation
    function initSidebarNavigation() {
        // Add click event to sidebar links
        sidebarLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Get the target section ID
                const targetId = this.getAttribute('href');
                const targetSection = document.querySelector(targetId);
                
                if (targetSection) {
                    // Smooth scroll to section
                    window.scrollTo({
                        top: targetSection.offsetTop - 20,
                        behavior: 'smooth'
                    });
                    
                    // Update active state in navigation
                    sidebarLinks.forEach(link => {
                        link.parentElement.classList.remove('active');
                    });
                    this.parentElement.classList.add('active');
                    
                    // Hide sidebar on mobile after clicking a link
                    if (window.innerWidth <= 576) {
                        sidebar.classList.remove('show');
                    }
                }
            });
        });
        
        // Mobile navigation toggle
        if (mobileNavToggle) {
            mobileNavToggle.addEventListener('click', function() {
                sidebar.classList.toggle('show');
                
                // Toggle icon
                const icon = this.querySelector('i');
                if (sidebar.classList.contains('show')) {
                    icon.className = 'fas fa-times';
                } else {
                    icon.className = 'fas fa-bars';
                }
            });
        }
    }
    
    // Create placeholder chart until real data is available
    function createPlaceholderChart() {
        if (typeof d3 !== 'undefined') {
            // Create a simple placeholder visualization using D3.js
            const width = chartContainer.clientWidth;
            const height = 260;
            const margin = { top: 20, right: 20, bottom: 40, left: 50 };
            
            // Sample data for the placeholder
            const sampleData = [
                { time: 0, density: 0.2, risk: 'low' },
                { time: 1, density: 0.3, risk: 'low' },
                { time: 2, density: 0.5, risk: 'medium' },
                { time: 3, density: 0.7, risk: 'medium' },
                { time: 4, density: 0.9, risk: 'high' },
                { time: 5, density: 0.6, risk: 'medium' },
                { time: 6, density: 0.4, risk: 'low' },
                { time: 7, density: 0.3, risk: 'low' }
            ];
            
            // Remove placeholder text
            chartContainer.innerHTML = '';
            
            // Create SVG
            const svg = d3.select(chartContainer)
                .append('svg')
                .attr('width', width)
                .attr('height', height)
                .attr('class', 'placeholder-chart');
                
            const innerWidth = width - margin.left - margin.right;
            const innerHeight = height - margin.top - margin.bottom;
            
            const g = svg.append('g')
                .attr('transform', `translate(${margin.left},${margin.top})`);
                
            // Create scales
            const xScale = d3.scaleLinear()
                .domain([0, sampleData.length - 1])
                .range([0, innerWidth]);
                
            const yScale = d3.scaleLinear()
                .domain([0, 1])
                .range([innerHeight, 0]);
                
            // Create a color scale for risk levels
            const colorScale = d3.scaleOrdinal()
                .domain(['low', 'medium', 'high'])
                .range(['#4CAF50', '#FFC107', '#FF5252']);
                
            // Create axes
            const xAxis = d3.axisBottom(xScale)
                .ticks(sampleData.length)
                .tickFormat(d => `T${d}`);
                
            const yAxis = d3.axisLeft(yScale)
                .ticks(5)
                .tickFormat(d => d.toFixed(1));
                
            // Add axes to chart
            g.append('g')
                .attr('class', 'x-axis')
                .attr('transform', `translate(0,${innerHeight})`)
                .call(xAxis)
                .selectAll('text')
                .style('font-size', '10px')
                .style('fill', 'rgba(255, 255, 255, 0.7)');
                
            g.append('g')
                .attr('class', 'y-axis')
                .call(yAxis)
                .selectAll('text')
                .style('font-size', '10px')
                .style('fill', 'rgba(255, 255, 255, 0.7)');
                
            // Add labels
            g.append('text')
                .attr('class', 'x-axis-label')
                .attr('x', innerWidth / 2)
                .attr('y', innerHeight + margin.bottom - 5)
                .attr('text-anchor', 'middle')
                .style('font-size', '12px')
                .style('fill', 'rgba(255, 255, 255, 0.7)')
                .text('Time');
                
            g.append('text')
                .attr('class', 'y-axis-label')
                .attr('transform', 'rotate(-90)')
                .attr('x', -innerHeight / 2)
                .attr('y', -margin.left + 15)
                .attr('text-anchor', 'middle')
                .style('font-size', '12px')
                .style('fill', 'rgba(255, 255, 255, 0.7)')
                .text('Crowd Density (people/m²)');
                
            // Create line generator
            const line = d3.line()
                .x((d, i) => xScale(i))
                .y(d => yScale(d.density))
                .curve(d3.curveMonotoneX);
                
            // Add the line path
            g.append('path')
                .datum(sampleData)
                .attr('class', 'line')
                .attr('d', line)
                .style('fill', 'none')
                .style('stroke', 'rgba(108, 99, 255, 0.7)')
                .style('stroke-width', 2);
                
            // Add dots for each data point with risk color
            g.selectAll('.dot')
                .data(sampleData)
                .enter()
                .append('circle')
                .attr('class', 'dot')
                .attr('cx', (d, i) => xScale(i))
                .attr('cy', d => yScale(d.density))
                .attr('r', 5)
                .style('fill', d => colorScale(d.risk))
                .style('stroke', '#14151A')
                .style('stroke-width', 2);
                
            // Add threshold lines for risk levels
            g.append('line')
                .attr('class', 'threshold')
                .attr('x1', 0)
                .attr('y1', yScale(0.4))
                .attr('x2', innerWidth)
                .attr('y2', yScale(0.4))
                .style('stroke', 'rgba(76, 175, 80, 0.5)')
                .style('stroke-dasharray', '5,5')
                .style('stroke-width', 1);
                
            g.append('line')
                .attr('class', 'threshold')
                .attr('x1', 0)
                .attr('y1', yScale(0.7))
                .attr('x2', innerWidth)
                .attr('y2', yScale(0.7))
                .style('stroke', 'rgba(255, 193, 7, 0.5)')
                .style('stroke-dasharray', '5,5')
                .style('stroke-width', 1);
        }
    }
    
    // Initialize event listeners
    function initEventListeners() {
        // Upload video button
        if (uploadVideoBtn) {
            uploadVideoBtn.addEventListener('click', handleVideoUpload);
        }
        
        // Analyze video button
        if (analyzeVideoBtn) {
            analyzeVideoBtn.addEventListener('click', analyzeVideo);
        }
        
        // Sliders for parameters
        if (frameSkipSlider) {
            frameSkipSlider.addEventListener('input', updateSliderValue);
        }
        
        if (maxWorkersSlider) {
            maxWorkersSlider.addEventListener('input', updateSliderValue);
        }

        // Add demo video selection
        createDemoVideoSelector();

        // Initialize sidebar navigation
        initSidebarNavigation();
        
        // Handle window resize
        window.addEventListener('resize', handleResize);
    }
    
    // Create a demo video selector for testing
    function createDemoVideoSelector() {
        // Create demo video selector
        const videoControls = document.querySelector('.video-controls');
        
        if (videoControls) {
            // Create a dropdown for demo videos
            const demoSelector = document.createElement('div');
            demoSelector.className = 'form-group demo-selector';
            demoSelector.innerHTML = `
                <button class="btn-secondary btn-sm" id="use-demo">
                    <i class="fas fa-film"></i> Use Demo Video
                </button>
                <div class="demo-dropdown" style="display: none;">
                    <div class="demo-option" data-video="DemoVideos/Crowd_Low_Density.mp4">Low Density Crowd</div>
                    <div class="demo-option" data-video="DemoVideos/FreeFlow_Crowd.mp4">Free Flow Crowd</div>
                    <div class="demo-option" data-video="DemoVideos/High_Crowd.mp4">High Density Crowd</div>
                </div>
            `;
            
            videoControls.appendChild(demoSelector);
            
            // Add event listeners for demo selector
            const useDemoBtn = document.getElementById('use-demo');
            const demoDropdown = document.querySelector('.demo-dropdown');
            const demoOptions = document.querySelectorAll('.demo-option');
            
            // Toggle dropdown
            useDemoBtn.addEventListener('click', function() {
                demoDropdown.style.display = demoDropdown.style.display === 'none' ? 'block' : 'none';
            });
            
            // Handle option selection
            demoOptions.forEach(option => {
                option.addEventListener('click', function() {
                    const videoPath = this.getAttribute('data-video');
                    loadDemoVideo(videoPath, this.textContent);
                    demoDropdown.style.display = 'none';
                });
            });
            
            // Close dropdown when clicking elsewhere
            document.addEventListener('click', function(e) {
                if (!demoSelector.contains(e.target)) {
                    demoDropdown.style.display = 'none';
                }
            });
        }
    }
    
    // Load a demo video from the path
    function loadDemoVideo(videoPath, videoName) {
        // Clear placeholder
        videoPlaceholder.innerHTML = '';
        
        // Create video element
        videoElement = document.createElement('video');
        videoElement.controls = true;
        videoElement.style.width = '100%';
        videoElement.style.height = '100%';
        videoElement.style.borderRadius = '8px';
        
        // Set video source
        videoElement.src = videoPath;
        
        // Add to placeholder
        videoPlaceholder.appendChild(videoElement);
        
        // Update status
        console.log('Demo video loaded:', videoName);
        
        // Enable analyze button
        analyzeVideoBtn.disabled = false;
        
        // Create a special flag to indicate this is a demo video
        uploadedVideo = {
            isDemo: true,
            path: videoPath,
            name: videoName
        };
    }
    
    // Handle window resize
    function handleResize() {
        // Reset mobile navigation when window is resized beyond mobile breakpoint
        if (window.innerWidth > 576 && sidebar.classList.contains('show')) {
            sidebar.classList.remove('show');
            if (mobileNavToggle) {
                mobileNavToggle.querySelector('i').className = 'fas fa-bars';
            }
        }
        
        // Redraw chart if needed
        if (typeof d3 !== 'undefined' && chartContainer) {
            // Update chart width based on new container size
            const chartSvg = d3.select(chartContainer).select('svg');
            if (!chartSvg.empty()) {
                const width = chartContainer.clientWidth;
                chartSvg.attr('width', width);
                
                // Update other chart dimensions if needed
                // This is a simplified version, you might need more adjustments
            }
        }
    }
    
    // Handle video upload
    function handleVideoUpload() {
        if (isProcessing) {
            alert('Please wait for the current analysis to complete.');
            return;
        }
        
        // Create file input element
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = 'video/*';
        fileInput.style.display = 'none';
        
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                uploadedVideo = file;
                displayVideoPreview(file);
            }
        });
        
        // Trigger file selection
        document.body.appendChild(fileInput);
        fileInput.click();
        document.body.removeChild(fileInput);
    }
    
    // Display video preview
    function displayVideoPreview(file) {
        // Clear placeholder
        videoPlaceholder.innerHTML = '';
        
        // Create video element
        videoElement = document.createElement('video');
        videoElement.controls = true;
        videoElement.style.width = '100%';
        videoElement.style.height = '100%';
        videoElement.style.borderRadius = '8px';
        
        // Create object URL for the file
        const videoURL = URL.createObjectURL(file);
        videoElement.src = videoURL;
        
        // Add to placeholder
        videoPlaceholder.appendChild(videoElement);
        
        // Update status
        console.log('Video loaded:', file.name);
        
        // Enable analyze button
        analyzeVideoBtn.disabled = false;
    }
    
    // Update slider value display
    function updateSliderValue(e) {
        // Get the range value display element
        const valueDisplay = e.target.nextElementSibling;
        if (valueDisplay && valueDisplay.classList.contains('range-value')) {
            valueDisplay.textContent = e.target.value;
        }
    }
    
    // Analyze video function
    function analyzeVideo() {
        if (!uploadedVideo) {
            alert('Please upload a video first.');
            return;
        }
        
        if (isProcessing) {
            alert('Analysis is already in progress.');
            return;
        }
        
        // Set processing state
        isProcessing = true;
        analyzeVideoBtn.disabled = true;
        analyzeVideoBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
        
        // Get parameters from sliders
        const frameSkip = parseInt(frameSkipSlider.value);
        const maxWorkers = parseInt(maxWorkersSlider.value);
        
        // Clear existing recommendation content
        aiRecommendations.innerHTML = '';
        
        // Show AI loading spinner
        aiLoading.style.display = 'flex';
        
        // Check if this is a demo video
        if (uploadedVideo.isDemo) {
            // For demo videos, we can directly use the path without uploading
            fetch('/api/predict', {
                method: 'POST',
                body: JSON.stringify({
                    video_url: uploadedVideo.path,
                    skip: frameSkip,
                    max_workers: maxWorkers
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    displayAnalysisResults(data.data);
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred during analysis: ' + error.message);
            })
            .finally(() => {
                // Reset processing state
                isProcessing = false;
                analyzeVideoBtn.disabled = false;
                analyzeVideoBtn.innerHTML = '<i class="fas fa-search"></i> Analyze';
                // Hide loading spinner
                aiLoading.style.display = 'none';
            });
            return;
        }
        
        // For user-uploaded videos, we need to upload them first
        const formData = new FormData();
        formData.append('video', uploadedVideo);
        
        // First, upload the video to our server
        fetch('/api/upload_video', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(uploadData => {
            if (uploadData.status === 'success') {
                console.log('Video uploaded successfully:', uploadData);
                
                // Now make the predict API call with the file path
                return fetch('/api/predict', {
                    method: 'POST',
                    body: JSON.stringify({
                        video_url: uploadData.video_url,
                        skip: frameSkip,
                        max_workers: maxWorkers
                    }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
            } else {
                throw new Error(uploadData.message || 'Failed to upload video');
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                displayAnalysisResults(data.data);
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred during analysis: ' + error.message);
        })
        .finally(() => {
            // Reset processing state
            isProcessing = false;
            analyzeVideoBtn.disabled = false;
            analyzeVideoBtn.innerHTML = '<i class="fas fa-search"></i> Analyze';
            // Hide loading spinner
            aiLoading.style.display = 'none';
        });
    }
    
    // Display analysis results
    function displayAnalysisResults(results) {
        console.log('Analysis results received:', results);
        
        // Check if the results are in the Gradio API format
        if (Array.isArray(results) && results.length >= 2) {
            // Get video and plot from Gradio response
            const videoResult = results[0];
            const plotResult = results[1];
            
            // Display annotated video if available
            if (videoResult && videoResult.video) {
                displayAnnotatedVideo(videoResult.video);
            }
            
            // Display plot if available
            if (plotResult && plotResult.type === 'matplotlib' && plotResult.plot) {
                displayPlot(plotResult.plot);
            }
            
            // Generate simple recommendations based on analysis
            const recommendations = [
                "Analysis complete. See annotated video and crowd density plot.",
                `Frame skip: ${frameSkipSlider.value}, Max workers: ${maxWorkersSlider.value}`,
                "Adjust parameters for different analysis results."
            ];
            
            displayAIRecommendations(recommendations);
            
            // Update stats cards with some placeholder values
            updateStatsFromAnnotation();
        } else {
            // Handle older format or custom format
            if (results.chart) {
                updateChart(results.chart);
            }
            
            if (results.heatmap) {
                updateHeatmap(results.heatmap);
            }
            
            if (results.recommendations && Array.isArray(results.recommendations)) {
                displayAIRecommendations(results.recommendations);
            } else {
                displayAIRecommendations(["No specific recommendations available for this analysis."]);
            }
            
            updateStatsFromResults(results);
        }
    }
    
    // Display annotated video from API response
    function displayAnnotatedVideo(videoUrl) {
        // Get video feed container
        const videoFeed = document.querySelector('.video-feed');
        if (!videoFeed) return;
        
        // Clear existing content
        videoFeed.innerHTML = '';
        
        // Create video element for the annotated video
        const annotatedVideo = document.createElement('video');
        annotatedVideo.controls = true;
        annotatedVideo.autoplay = false;
        annotatedVideo.style.width = '100%';
        annotatedVideo.style.height = 'auto';
        annotatedVideo.style.borderRadius = '8px';
        annotatedVideo.style.maxHeight = '300px';
        
        // Set source
        annotatedVideo.src = videoUrl;
        
        // Create container for the video
        const videoContainer = document.createElement('div');
        videoContainer.className = 'annotated-video-container';
        videoContainer.appendChild(annotatedVideo);
        
        // Add to video feed
        videoFeed.appendChild(videoContainer);
        
        // Add controls below the video
        const videoControls = document.createElement('div');
        videoControls.className = 'video-controls';
        videoControls.innerHTML = `
            <button class="btn-secondary btn-sm" id="download-video"><i class="fas fa-download"></i> Download Annotated Video</button>
            <button class="btn-primary btn-sm" id="analyze-again"><i class="fas fa-redo"></i> Analyze Again</button>
        `;
        videoFeed.appendChild(videoControls);
        
        // Add download event
        document.getElementById('download-video').addEventListener('click', () => {
            window.open(videoUrl, '_blank');
        });
        
        // Add analyze again event
        document.getElementById('analyze-again').addEventListener('click', () => {
            if (uploadedVideo) {
                analyzeVideo();
            } else {
                alert('Please upload a video first');
            }
        });
    }
    
    // Display plot from API response
    function displayPlot(plotData) {
        // Get chart container
        const chartContainer = document.getElementById('density-chart');
        if (!chartContainer) return;
        
        // Clear existing content
        chartContainer.innerHTML = '';
        
        // Create image element for the plot
        const plotImage = document.createElement('img');
        plotImage.src = plotData; // This should be the base64 data URL
        plotImage.alt = 'Crowd Density Analysis Plot';
        plotImage.style.width = '100%';
        plotImage.style.height = 'auto';
        plotImage.style.borderRadius = '8px';
        
        // Add to chart container
        chartContainer.appendChild(plotImage);
    }
    
    // Update stats based on the annotation
    function updateStatsFromAnnotation() {
        try {
            // Example of updating stats with estimation
            const statsCards = document.querySelectorAll('.stats-card .stats-value');
            
            // Current crowd - random number for demonstration
            if (statsCards[0]) {
                const crowd = Math.round(800 + Math.random() * 1000);
                statsCards[0].textContent = crowd.toLocaleString();
            }
            
            // Risk level based on the crowd number
            if (statsCards[1]) {
                const crowd = parseInt(statsCards[0].textContent.replace(/,/g, ''));
                let riskLevel = 'Low';
                if (crowd > 1500) riskLevel = 'High';
                else if (crowd > 1000) riskLevel = 'Medium';
                
                statsCards[1].textContent = riskLevel;
                
                // Update risk color
                const riskIcon = statsCards[1].closest('.stats-card').querySelector('.stats-icon');
                if (riskIcon) {
                    riskIcon.className = 'stats-icon';
                    if (riskLevel === 'Low') riskIcon.classList.add('green');
                    else if (riskLevel === 'Medium') riskIcon.classList.add('yellow');
                    else riskIcon.classList.add('red');
                }
            }
            
            // Active cameras
            if (statsCards[2]) {
                statsCards[2].textContent = '1'; // Since we're analyzing one video
            }
        } catch (e) {
            console.error('Error updating stats:', e);
        }
    }
    
    // Convert Gradio response to chart data format
    function convertToChartData(data) {
        // Handle different possible formats of the data
        console.log("Converting data format:", data);
        
        // If data is empty or undefined, return empty array
        if (!data) {
            return [];
        }
        
        // Handle string data (try to parse as JSON)
        if (typeof data === 'string') {
            try {
                data = JSON.parse(data);
            } catch (e) {
                console.error('Failed to parse chart data:', e);
                return [];
            }
        }
        
        // If data is already an array of objects with density property
        if (Array.isArray(data) && data.length && typeof data[0] === 'object' && data[0].hasOwnProperty('density')) {
            return data;
        }
        
        // If data is an array but doesn't have the right format, try to convert
        if (Array.isArray(data) && data.length) {
            try {
                // Try to convert each item to our format
                return data.map((item, index) => {
                    // If item is already in correct format
                    if (item && typeof item === 'object' && item.hasOwnProperty('density')) {
                        return item;
                    }
                    
                    // Try to extract density value
                    let density = 0;
                    if (typeof item === 'number') {
                        density = item;
                    } else if (typeof item === 'object') {
                        // Try to find a numeric property
                        for (const key in item) {
                            if (typeof item[key] === 'number') {
                                density = item[key];
                                break;
                            }
                        }
                    }
                    
                    // Determine risk level based on density
                    let risk = 'low';
                    if (density > 0.7) {
                        risk = 'high';
                    } else if (density > 0.4) {
                        risk = 'medium';
                    }
                    
                    return {
                        time: index * 10,
                        density: density,
                        risk: risk
                    };
                });
            } catch (e) {
                console.error('Failed to convert chart data array:', e);
            }
        }
        
        // Default mock data if we can't convert
        return [
            { time: 0, density: 0.3, risk: 'low' },
            { time: 10, density: 0.5, risk: 'medium' },
            { time: 20, density: 0.7, risk: 'high' },
            { time: 30, density: 0.4, risk: 'medium' },
            { time: 40, density: 0.2, risk: 'low' }
        ];
    }
    
    // Update stats cards with results data
    function updateStatsFromResults(results) {
        try {
            // Example of updating stats based on results
            const statsCards = document.querySelectorAll('.stats-card .stats-value');
            
            // Get max density from chart data if available
            if (results.chart && results.chart.data && results.chart.data.length) {
                const maxDensity = Math.max(...results.chart.data.map(d => d.density));
                const avgDensity = results.chart.data.reduce((sum, d) => sum + d.density, 0) / results.chart.data.length;
                const lastRisk = results.chart.data[results.chart.data.length - 1].risk;
                
                // Current crowd - random number scaled by density
                if (statsCards[0]) {
                    const crowd = Math.round(1000 + maxDensity * 1000);
                    statsCards[0].textContent = crowd.toLocaleString();
                }
                
                // Risk level
                if (statsCards[1]) {
                    statsCards[1].textContent = lastRisk.charAt(0).toUpperCase() + lastRisk.slice(1);
                }
            }
        } catch (e) {
            console.error('Error updating stats:', e);
        }
    }
    
    // Update the chart with new data
    function updateChart(chartData) {
        // Check if we have data
        if (!chartData || !chartData.data || !chartData.data.length) {
            console.log('No chart data available');
            return;
        }
        
        console.log('Updating chart with data:', chartData);
        
        // Clear any existing chart
        chartContainer.innerHTML = '';
        
        // Create new chart using D3.js
        const width = chartContainer.clientWidth;
        const height = 260;
        const margin = { top: 20, right: 20, bottom: 40, left: 50 };
        
        // Create SVG
        const svg = d3.select(chartContainer)
            .append('svg')
            .attr('width', width)
            .attr('height', height)
            .attr('class', 'density-chart');
            
        const innerWidth = width - margin.left - margin.right;
        const innerHeight = height - margin.top - margin.bottom;
        
        const g = svg.append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);
            
        // Create scales
        const xScale = d3.scaleLinear()
            .domain([0, chartData.data.length - 1])
            .range([0, innerWidth]);
            
        const yScale = d3.scaleLinear()
            .domain([0, d3.max(chartData.data, d => d.density) || 1])
            .range([innerHeight, 0]);
            
        // Create a color scale for risk levels
        const colorScale = d3.scaleOrdinal()
            .domain(['low', 'medium', 'high'])
            .range(['#4CAF50', '#FFC107', '#FF5252']);
            
        // Create axes
        const xAxis = d3.axisBottom(xScale)
            .ticks(Math.min(chartData.data.length, 10))
            .tickFormat(d => `T${d}`);
            
        const yAxis = d3.axisLeft(yScale)
            .ticks(5)
            .tickFormat(d => d.toFixed(1));
            
        // Add axes to chart
        g.append('g')
            .attr('class', 'x-axis')
            .attr('transform', `translate(0,${innerHeight})`)
            .call(xAxis)
            .selectAll('text')
            .style('font-size', '10px')
            .style('fill', 'rgba(255, 255, 255, 0.7)');
            
        g.append('g')
            .attr('class', 'y-axis')
            .call(yAxis)
            .selectAll('text')
            .style('font-size', '10px')
            .style('fill', 'rgba(255, 255, 255, 0.7)');
            
        // Add labels
        g.append('text')
            .attr('class', 'x-axis-label')
            .attr('x', innerWidth / 2)
            .attr('y', innerHeight + margin.bottom - 5)
            .attr('text-anchor', 'middle')
            .style('font-size', '12px')
            .style('fill', 'rgba(255, 255, 255, 0.7)')
            .text('Time Frame');
            
        g.append('text')
            .attr('class', 'y-axis-label')
            .attr('transform', 'rotate(-90)')
            .attr('x', -innerHeight / 2)
            .attr('y', -margin.left + 15)
            .attr('text-anchor', 'middle')
            .style('font-size', '12px')
            .style('fill', 'rgba(255, 255, 255, 0.7)')
            .text('Crowd Density (people/m²)');
            
        // Create line generator
        const line = d3.line()
            .x((d, i) => xScale(i))
            .y(d => yScale(d.density))
            .curve(d3.curveMonotoneX);
            
        // Add the line path
        g.append('path')
            .datum(chartData.data)
            .attr('class', 'line')
            .attr('d', line)
            .style('fill', 'none')
            .style('stroke', 'rgba(108, 99, 255, 0.7)')
            .style('stroke-width', 2);
            
        // Add dots for each data point with risk color
        g.selectAll('.dot')
            .data(chartData.data)
            .enter()
            .append('circle')
            .attr('class', 'dot')
            .attr('cx', (d, i) => xScale(i))
            .attr('cy', d => yScale(d.density))
            .attr('r', 5)
            .style('fill', d => colorScale(d.risk))
            .style('stroke', '#14151A')
            .style('stroke-width', 2);
            
        // Add threshold lines for risk levels
        g.append('line')
            .attr('class', 'threshold')
            .attr('x1', 0)
            .attr('y1', yScale(0.4))
            .attr('x2', innerWidth)
            .attr('y2', yScale(0.4))
            .style('stroke', 'rgba(76, 175, 80, 0.5)')
            .style('stroke-dasharray', '5,5')
            .style('stroke-width', 1);
            
        g.append('line')
            .attr('class', 'threshold')
            .attr('x1', 0)
            .attr('y1', yScale(0.7))
            .attr('x2', innerWidth)
            .attr('y2', yScale(0.7))
            .style('stroke', 'rgba(255, 193, 7, 0.5)')
            .style('stroke-dasharray', '5,5')
            .style('stroke-width', 1);
    }
    
    // Update heatmap visualization
    function updateHeatmap(heatmapData) {
        // Replace placeholder with actual heatmap
        heatmapContainer.innerHTML = '';
        
        // Add a mock heatmap image for demonstration
        const heatmapImage = document.createElement('img');
        heatmapImage.src = 'https://via.placeholder.com/500x260/000000/FFFFFF?text=Crowd+Heatmap';
        heatmapImage.alt = 'Crowd Density Heatmap';
        heatmapImage.style.width = '100%';
        heatmapImage.style.height = '100%';
        heatmapImage.style.borderRadius = '8px';
        heatmapImage.style.objectFit = 'cover';
        
        heatmapContainer.appendChild(heatmapImage);
        
        // Re-add the legend
        const legend = document.createElement('div');
        legend.className = 'heatmap-legend';
        legend.innerHTML = `
            <div class="legend-item">
                <span class="color-dot low"></span>
                <p>Low Risk</p>
            </div>
            <div class="legend-item">
                <span class="color-dot medium"></span>
                <p>Medium Risk</p>
            </div>
            <div class="legend-item">
                <span class="color-dot high"></span>
                <p>High Risk</p>
            </div>
        `;
        
        heatmapContainer.appendChild(legend);
    }
    
    // Display AI recommendations
    function displayAIRecommendations(recommendations) {
        // Hide loading spinner
        aiLoading.style.display = 'none';
        
        // Clear previous recommendations
        aiRecommendations.innerHTML = '';
        
        // Add each recommendation
        recommendations.forEach(rec => {
            const recItem = document.createElement('div');
            recItem.className = 'recommendation-item';
            recItem.innerHTML = `
                <p>${rec}</p>
            `;
            
            aiRecommendations.appendChild(recItem);
        });
    }
    
    // Mock analysis results for demonstration
    function mockAnalysisResults() {
        return {
            chart: {
                // Chart data would go here
                data: [
                    { time: 0, density: 0.3, risk: 'low' },
                    { time: 10, density: 0.5, risk: 'medium' },
                    { time: 20, density: 0.8, risk: 'high' },
                    { time: 30, density: 0.6, risk: 'medium' },
                    { time: 40, density: 0.3, risk: 'low' }
                ]
            },
            heatmap: {
                // Heatmap data would go here
            },
            recommendations: [
                "Redirect crowd from Entry Gate A to Entry Gate C to reduce density in the central area.",
                "Deploy 3 additional security personnel to the North section which has reached high risk level.",
                "Gradually reduce flow through East corridor which is approaching critical density threshold.",
                "Current crowd movement patterns suggest potential bottleneck forming at South exit within 5-7 minutes."
            ]
        };
    }
}); 