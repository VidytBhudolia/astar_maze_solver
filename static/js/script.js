document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const sizeSlider = document.getElementById('maze-size');
    const sizeValueElem = document.getElementById('size-value');
    const generateBtn = document.getElementById('generate-btn');
    const solveBtn = document.getElementById('solve-btn');
    const mazeContainer = document.getElementById('maze-container');
    const resultsContainer = document.getElementById('results-container');
    const resultCards = document.getElementById('result-cards');
    
    // Chart
    let comparisonChart = null;
    
    // Current maze state
    let currentMaze = null;
    let startPos = [1, 1];
    let endPos = [1, 1];
    
    // Update size value display when slider changes
    sizeSlider.addEventListener('input', function() {
        // Ensure size is odd (for maze generation)
        let size = parseInt(this.value);
        if (size % 2 === 0) size--;
        this.value = size;
        
        sizeValueElem.textContent = size;
    });
    
    // Generate maze button click
    generateBtn.addEventListener('click', function() {
        const size = parseInt(sizeSlider.value);
        
        // Disable the button during fetch
        generateBtn.disabled = true;
        generateBtn.textContent = "Generating...";
        
        // Make API request to generate maze
        fetch('/generate_maze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ size: size })
        })
        .then(response => response.json())
        .then(data => {
            // Store maze data
            currentMaze = data.maze;
            startPos = data.start;
            endPos = data.end;
            
            // Display the maze
            displayMaze(currentMaze, startPos, endPos);
            
            // Enable solve button
            solveBtn.disabled = false;
            
            // Hide results if shown
            resultsContainer.style.display = 'none';
        })
        .catch(error => {
            console.error('Error generating maze:', error);
            alert('Error generating maze. Please try again.');
        })
        .finally(() => {
            // Re-enable button
            generateBtn.disabled = false;
            generateBtn.textContent = "Generate Maze";
        });
    });
    
    // Solve maze button click
    solveBtn.addEventListener('click', function() {
        // Disable button during fetch
        solveBtn.disabled = true;
        solveBtn.textContent = "Solving...";
        
        // Make API request to solve maze
        fetch('/solve_maze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                maze: currentMaze,
                start: startPos,
                end: endPos
            })
        })
        .then(response => response.json())
        .then(data => {
            // Display results
            displayResults(data);
            
            // Show results section
            resultsContainer.style.display = 'block';
        })
        .catch(error => {
            console.error('Error solving maze:', error);
            alert('Error solving maze. Please try again.');
        })
        .finally(() => {
            // Re-enable button
            solveBtn.disabled = false;
            solveBtn.textContent = "Solve Maze";
        });
    });
    
    // Function to display the maze
    function displayMaze(maze, start, end, solution = null) {
        // Clear existing maze
        mazeContainer.innerHTML = '';
        
        // Set CSS grid size
        mazeContainer.style.gridTemplateColumns = `repeat(${maze[0].length}, 15px)`;
        mazeContainer.style.gridTemplateRows = `repeat(${maze.length}, 15px)`;
        
        // Create maze cells
        for (let i = 0; i < maze.length; i++) {
            for (let j = 0; j < maze[i].length; j++) {
                const cell = document.createElement('div');
                cell.className = 'maze-cell';
                
                // Determine cell type
                if (i === start[0] && j === start[1]) {
                    cell.classList.add('start');
                } else if (i === end[0] && j === end[1]) {
                    cell.classList.add('end');
                } else if (solution && solution[i][j] === 2) {
                    cell.classList.add('solution');
                } else if (maze[i][j] === 1) {
                    cell.classList.add('wall');
                } else {
                    cell.classList.add('path');
                }
                
                mazeContainer.appendChild(cell);
            }
        }
    }
    
    // Function to display results
    function displayResults(results) {
        // Clear previous results
        resultCards.innerHTML = '';
        
        // Define fixed order and color mapping
        const heuristicOrder = ['manhattan', 'KNN', 'decision_tree'];
        const colorMapping = {
            'manhattan': '#FF6384',
            'KNN': '#36A2EB',
            'decision_tree': '#FFCE56'
        };
        
        // Prepare data for chart
        const labels = [];
        const times = [];
        const backgroundColors = [];
        
        // Find the fastest heuristic
        let fastestHeuristic = '';
        let fastestTime = Infinity;
        
        // Convert results object to array and sort by custom order
        const sortedResults = Object.entries(results)
            .sort((a, b) => {
                const indexA = heuristicOrder.indexOf(a[0]);
                const indexB = heuristicOrder.indexOf(b[0]);
                return indexA - indexB;
            });
        
        // Create result cards and collect data for chart
        for (const [heuristic, data] of sortedResults) {
            const executionTime = data.time;
            const solvedMaze = data.solved_maze;
            
            // Check if this is the fastest
            if (executionTime < fastestTime) {
                fastestTime = executionTime;
                fastestHeuristic = heuristic;
            }
            
            // Create result card
            const card = document.createElement('div');
            card.className = `result-card ${heuristic}`;
            
            // Format heuristic name for display
            const displayName = heuristic
                .split('_')
                .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                .join(' ');
            
            // Add a fastest flag attribute to be used later    
            card.setAttribute('data-fastest', 'false');
            
            card.innerHTML = `
                <div class="result-card-info" style="display: flex; flex-direction: column; flex-grow: 1; overflow: hidden;">
                    <div style="display: flex; align-items: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                        <h3 style="margin: 0; display: inline-block;">${displayName}</h3>
                        <span class="fastest-label" style="color:#4CAF50; margin-left: 5px; display: none;">(Fastest)</span>
                    </div>
                    <p style="margin: 5px 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Time: ${executionTime.toFixed(6)} seconds</p>
                </div>
                <button class="view-solution-btn" data-heuristic="${heuristic}" style="padding: 5px 10px; font-size: 0.85em; align-self: center; margin-left: 5px; width: 120px; color: white; border: none; border-radius: 4px; cursor: pointer;">View Solution</button>
            `;
            
            resultCards.appendChild(card);
            
            // Add event listener for view solution button
            card.querySelector('.view-solution-btn').addEventListener('click', function() {
                // Remove active class from all cards
                document.querySelectorAll('.result-card').forEach(c => {
                    c.classList.remove('active');
                });
                
                // Add active class to this card
                card.classList.add('active');
                
                // Display this solution
                displayMaze(currentMaze, startPos, endPos, solvedMaze);
            });
            
            // Add data for chart
            labels.push(displayName);
            times.push(executionTime);
            backgroundColors.push(colorMapping[heuristic]);
        }
        
        // Mark the fastest heuristic
        const fastestCard = document.querySelector(`.result-card.${fastestHeuristic}`);
        if (fastestCard) {
            fastestCard.classList.add('fastest');
            fastestCard.setAttribute('data-fastest', 'true');
            const fastestLabel = fastestCard.querySelector('.fastest-label');
            if (fastestLabel) {
                fastestLabel.style.display = 'inline';
            }
        }
        
        // Display the fastest solution by default
        displayMaze(currentMaze, startPos, endPos, results[fastestHeuristic].solved_maze);
        
        // Create comparison chart
        createComparisonChart(labels, times, backgroundColors);
    }
    
    // Function to create comparison chart
    function createComparisonChart(labels, times, backgroundColors) {
        const ctx = document.getElementById('comparison-chart').getContext('2d');
        
        // Destroy existing chart if it exists
        if (comparisonChart) {
            comparisonChart.destroy();
        }
        
        // Create new chart
        comparisonChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Execution Time (seconds)',
                    data: times,
                    backgroundColor: backgroundColors
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Time (seconds)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Heuristic Function'
                        }
                    }
                }
            }
        });
    }
});
