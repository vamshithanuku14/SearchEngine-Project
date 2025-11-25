/**
 * Modern Search Engine Frontend
 * Professional implementation with real-world features
 */

class ModernSearchEngine {
    constructor() {
        this.searchInput = document.getElementById('searchInput');
        this.searchForm = document.getElementById('searchForm');
        this.suggestions = document.getElementById('suggestions');
        this.resultsContainer = document.getElementById('resultsContainer');
        this.loading = document.getElementById('loading');
        this.advancedToggle = document.getElementById('advancedToggle');
        this.advancedFields = document.getElementById('advancedFields');
        this.resultsCount = document.getElementById('resultsCount');
        this.resultsStats = document.getElementById('resultsStats');
        
        this.debounceTimer = null;
        this.currentQuery = '';
        this.isAdvancedVisible = false;
        this.lastSearchTime = 0;
        
        this.initializeEventListeners();
        this.initializeServiceWorker();
        this.initializeAnalytics();
    }
    
    initializeEventListeners() {
        // Search input events
        this.searchInput.addEventListener('input', (e) => this.handleInput(e));
        this.searchInput.addEventListener('focus', () => this.showSuggestions());
        this.searchInput.addEventListener('keydown', (e) => this.handleKeydown(e));
        
        // Form submission
        this.searchForm.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Advanced search toggle
        if (this.advancedToggle) {
            this.advancedToggle.addEventListener('click', () => this.toggleAdvanced());
        }
        
        // Click outside to hide suggestions
        document.addEventListener('click', (e) => {
            if (!this.searchInput.contains(e.target) && !this.suggestions.contains(e.target)) {
                this.hideSuggestions();
            }
        });
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleGlobalKeydown(e));
        
        // Load more results on scroll
        window.addEventListener('scroll', () => this.handleScroll());
        
        // Handle browser back/forward
        window.addEventListener('popstate', (e) => this.handlePopState(e));
    }
    
    initializeServiceWorker() {
        // Register service worker for offline functionality
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/static/search-sw.js')
                .then(registration => {
                    console.log('ServiceWorker registered: ', registration);
                })
                .catch(error => {
                    console.log('ServiceWorker registration failed: ', error);
                });
        }
    }
    
    initializeAnalytics() {
        // Basic analytics tracking
        this.trackEvent('page_view', { page: 'search_home' });
    }
    
    handleInput(e) {
        const query = e.target.value.trim();
        this.currentQuery = query;
        
        // Clear previous debounce timer
        clearTimeout(this.debounceTimer);
        
        if (query.length === 0) {
            this.hideSuggestions();
            this.clearResults();
            return;
        }
        
        if (query.length < 2) {
            this.hideSuggestions();
            return;
        }
        
        // Debounce suggestions
        this.debounceTimer = setTimeout(() => {
            this.fetchSuggestions(query);
            this.trackEvent('search_suggest', { query: query });
        }, 200);
    }
    
    handleKeydown(e) {
        const suggestions = this.suggestions.querySelectorAll('.suggestion-item');
        const activeSuggestion = this.suggestions.querySelector('.suggestion-item.active');
        
        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                this.navigateSuggestions(1, suggestions, activeSuggestion);
                break;
            case 'ArrowUp':
                e.preventDefault();
                this.navigateSuggestions(-1, suggestions, activeSuggestion);
                break;
            case 'Enter':
                if (activeSuggestion) {
                    e.preventDefault();
                    this.selectSuggestion(activeSuggestion);
                }
                break;
            case 'Escape':
                this.hideSuggestions();
                break;
        }
    }
    
    navigateSuggestions(direction, suggestions, activeSuggestion) {
        let nextIndex = 0;
        
        if (activeSuggestion) {
            const currentIndex = Array.from(suggestions).indexOf(activeSuggestion);
            nextIndex = currentIndex + direction;
            
            if (nextIndex < 0) nextIndex = suggestions.length - 1;
            if (nextIndex >= suggestions.length) nextIndex = 0;
            
            activeSuggestion.classList.remove('active');
        }
        
        suggestions[nextIndex].classList.add('active');
        suggestions[nextIndex].scrollIntoView({ block: 'nearest' });
    }
    
    selectSuggestion(suggestionElement) {
        const query = suggestionElement.querySelector('.suggestion-query').textContent;
        this.searchInput.value = query;
        this.hideSuggestions();
        this.performSearch(query);
        this.trackEvent('suggestion_select', { query: query });
    }
    
    handleSubmit(e) {
        e.preventDefault();
        const query = this.searchInput.value.trim();
        
        if (query) {
            this.performSearch(query);
            this.trackEvent('search_submit', { query: query, method: 'form' });
        }
    }
    
    handleGlobalKeydown(e) {
        // Focus search input when '/' is pressed
        if (e.key === '/' && e.target !== this.searchInput) {
            e.preventDefault();
            this.searchInput.focus();
        }
        
        // Clear search with Escape when input is focused
        if (e.key === 'Escape' && document.activeElement === this.searchInput) {
            this.searchInput.value = '';
            this.hideSuggestions();
            this.clearResults();
        }
    }
    
    handleScroll() {
        // Implement infinite scroll or load more functionality
        const scrollPosition = window.innerHeight + window.scrollY;
        const pageHeight = document.documentElement.scrollHeight;
        const scrollThreshold = 500;
        
        if (pageHeight - scrollPosition < scrollThreshold) {
            // Load more results if available
            this.loadMoreResults();
        }
    }
    
    handlePopState(e) {
        // Handle browser navigation
        if (e.state && e.state.query) {
            this.searchInput.value = e.state.query;
            this.performSearch(e.state.query, false);
        }
    }
    
    async fetchSuggestions(query) {
        try {
            const response = await fetch(`/suggest?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            this.displaySuggestions(data.suggestions, query);
        } catch (error) {
            console.error('Error fetching suggestions:', error);
            this.hideSuggestions();
        }
    }
    
    displaySuggestions(suggestions, query) {
        if (!suggestions || suggestions.length === 0) {
            this.hideSuggestions();
            return;
        }
        
        this.suggestions.innerHTML = '';
        
        suggestions.forEach((suggestion, index) => {
            const suggestionElement = this.createSuggestionElement(suggestion, query, index);
            this.suggestions.appendChild(suggestionElement);
        });
        
        this.showSuggestions();
    }
    
    createSuggestionElement(suggestion, query, index) {
        const div = document.createElement('div');
        div.className = `suggestion-item ${index === 0 ? 'active' : ''}`;
        div.innerHTML = `
            <span class="suggestion-icon">🔍</span>
            <span class="suggestion-query">${this.highlightText(suggestion, query)}</span>
            <span class="suggestion-type">suggestion</span>
        `;
        
        div.addEventListener('click', () => {
            this.selectSuggestion(div);
        });
        
        return div;
    }
    
    highlightText(text, query) {
        if (!query) return text;
        
        const regex = new RegExp(`(${this.escapeRegex(query)})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }
    
    escapeRegex(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }
    
    showSuggestions() {
        this.suggestions.classList.add('show');
    }
    
    hideSuggestions() {
        this.suggestions.classList.remove('show');
        this.suggestions.querySelectorAll('.suggestion-item.active').forEach(item => {
            item.classList.remove('active');
        });
    }
    
    async performSearch(query, updateHistory = true) {
        this.showLoading();
        this.hideSuggestions();
        
        // Update browser history
        if (updateHistory) {
            window.history.pushState({ query: query }, '', `?q=${encodeURIComponent(query)}`);
        }
        
        this.lastSearchTime = Date.now();
        
        try {
            // Build query parameters
            const params = new URLSearchParams();
            params.append('q', query);
            
            // Add advanced options if visible and selected
            if (this.isAdvancedVisible) {
                const topK = document.getElementById('topK')?.value;
                const searchType = document.getElementById('searchType')?.value;
                
                console.log('Advanced options:', { topK, searchType }); // Debug log
                
                if (topK && topK !== '10') {
                    params.append('top_k', topK);
                }
                if (searchType && searchType !== 'standard') {
                    params.append('type', searchType);
                }
            }
            
            const response = await fetch(`/search?${params.toString()}`);
            const data = await response.json();
            
            this.displayResults(data);
            this.trackEvent('search_complete', { 
                query: query, 
                results: data.total_results,
                time: Date.now() - this.lastSearchTime,
                advanced_options: this.isAdvancedVisible
            });
            
        } catch (error) {
            this.displayError('Search failed: ' + error.message);
            this.trackEvent('search_error', { query: query, error: error.message });
        } finally {
            this.hideLoading();
        }
    }
    
    displayResults(data) {
        this.resultsContainer.innerHTML = '';
        
        if (data.error) {
            this.displayError(data.error);
            return;
        }
        
        // Update results count and stats with advanced options info
        if (this.resultsCount) {
            const topK = document.getElementById('topK')?.value || '10';
            this.resultsCount.textContent = `About ${data.total_results} results (showing ${Math.min(data.total_results, topK)})`;
        }
        
        if (this.resultsStats) {
            const searchType = document.getElementById('searchType')?.value || 'standard';
            this.resultsStats.innerHTML = `
                <div class="stat-item">
                    <span>⏱️ ${data.execution_time?.toFixed(3) || '0.000'}s</span>
                </div>
                <div class="stat-item">
                    <span>🔍 ${searchType.charAt(0).toUpperCase() + searchType.slice(1)} Search</span>
                </div>
                <div class="stat-item">
                    <span>📝 "${data.processed_query || data.query}"</span>
                </div>
            `;
        }
        
        // Display results
        if (data.results.length === 0) {
            this.displayNoResults();
            return;
        }
        
        data.results.forEach((result, index) => {
            const resultElement = this.createResultElement(result, index + 1);
            this.resultsContainer.appendChild(resultElement);
        });
        
        // Add fade-in animation
        setTimeout(() => {
            this.resultsContainer.querySelectorAll('.result-item').forEach((item, index) => {
                item.style.animationDelay = `${index * 0.1}s`;
                item.classList.add('fade-in');
            });
        }, 100);
    }
    
    createResultElement(result, rank) {
        const resultDiv = document.createElement('div');
        resultDiv.className = 'result-item';
        
        const scorePercent = Math.min(result.similarity_score * 100, 100);
        const wordCount = result.word_count || 0;
        const readingTime = Math.ceil(wordCount / 200); // Average reading speed
        
        resultDiv.innerHTML = `
            <div class="result-badge">#${rank}</div>
            <a href="${result.url}" class="result-title" target="_blank" rel="noopener">
                ${this.escapeHtml(result.title)}
            </a>
            <div class="result-url">
                <span class="url-favicon">🌐</span>
                ${this.escapeHtml(result.url)}
            </div>
            <div class="result-snippet">${result.snippet}</div>
            <div class="result-meta">
                <div class="meta-item">
                    <span>Relevance:</span>
                    <span class="score-value">${(result.similarity_score * 100).toFixed(1)}%</span>
                    <div class="score-bar">
                        <div class="score-fill" style="width: ${scorePercent}%"></div>
                    </div>
                </div>
                <div class="meta-item">
                    <span>📊 ${wordCount.toLocaleString()} words</span>
                </div>
                <div class="meta-item">
                    <span>⏱️ ${readingTime} min read</span>
                </div>
                <div class="meta-item">
                    <span>🔍 ${result.score.toFixed(4)}</span>
                </div>
            </div>
        `;
        
        // Add click tracking
        resultDiv.querySelector('.result-title').addEventListener('click', () => {
            this.trackEvent('result_click', {
                rank: rank,
                url: result.url,
                title: result.title,
                score: result.score
            });
        });
        
        return resultDiv;
    }
    
    displayError(message) {
        this.resultsContainer.innerHTML = `
            <div class="error">
                <span class="error-icon">⚠️</span>
                <strong>Error:</strong> ${message}
            </div>
        `;
    }
    
    displayNoResults() {
        this.resultsContainer.innerHTML = `
            <div class="no-results">
                <div class="no-results-icon">🔍</div>
                <h3 class="no-results-title">No results found</h3>
                <p>Try different keywords or check your spelling</p>
                <div class="mt-16">
                    <button class="search-button" onclick="searchEngine.clearSearch()">Clear Search</button>
                </div>
            </div>
        `;
    }
    
    clearSearch() {
        this.searchInput.value = '';
        this.clearResults();
        this.searchInput.focus();
    }
    
    clearResults() {
        this.resultsContainer.innerHTML = '';
        if (this.resultsCount) this.resultsCount.textContent = '';
        if (this.resultsStats) this.resultsStats.innerHTML = '';
    }
    
    showLoading() {
        this.loading.classList.remove('hidden');
        this.resultsContainer.innerHTML = '';
    }
    
    hideLoading() {
        this.loading.classList.add('hidden');
    }
    
    toggleAdvanced() {
        this.isAdvancedVisible = !this.isAdvancedVisible;
        this.advancedFields.classList.toggle('show', this.isAdvancedVisible);
        this.advancedToggle.textContent = this.isAdvancedVisible ? 'Hide Advanced' : 'Advanced Search';
        
        this.trackEvent('advanced_toggle', { state: this.isAdvancedVisible });
    }
    
    loadMoreResults() {
        // Implement pagination or infinite scroll
        console.log('Load more results triggered');
        
        // Example implementation:
        const currentResults = this.resultsContainer.querySelectorAll('.result-item').length;
        const totalResults = parseInt(this.resultsCount?.textContent?.match(/\d+/)?.[0]) || 0;
        
        if (currentResults < totalResults) {
            // In a real implementation, you would fetch the next page of results
            console.log(`Loading more results... (${currentResults} of ${totalResults})`);
        }
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    trackEvent(eventName, properties = {}) {
        // Basic analytics implementation
        console.log(`Event: ${eventName}`, properties);
        
        // In a real implementation, you would send this to Google Analytics, etc.
        if (typeof gtag !== 'undefined') {
            gtag('event', eventName, properties);
        }
        
        // Store search history
        if (eventName === 'search_complete') {
            this.addToSearchHistory(properties.query);
        }
    }
    
    // Public methods
    search(query) {
        this.searchInput.value = query;
        this.performSearch(query);
    }
    
    getSearchHistory() {
        return JSON.parse(localStorage.getItem('searchHistory') || '[]');
    }
    
    addToSearchHistory(query) {
        const history = this.getSearchHistory();
        
        // Remove duplicates
        const filteredHistory = history.filter(item => item.query !== query);
        
        // Add to beginning
        filteredHistory.unshift({
            query: query,
            timestamp: Date.now(),
            date: new Date().toISOString()
        });
        
        // Keep only last 50 searches
        const limitedHistory = filteredHistory.slice(0, 50);
        localStorage.setItem('searchHistory', JSON.stringify(limitedHistory));
    }
    
    // Method to handle advanced search options changes
    handleAdvancedOptionChange() {
        // If we have a current query, re-run the search with new options
        if (this.currentQuery && this.currentQuery.trim()) {
            this.performSearch(this.currentQuery, false);
        }
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    window.searchEngine = new ModernSearchEngine();
    
    // Handle search query from URL
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('q');
    if (query) {
        window.searchEngine.search(query);
    }
    
    // Add event listeners for advanced options changes
    const topKSelect = document.getElementById('topK');
    const searchTypeSelect = document.getElementById('searchType');
    
    if (topKSelect) {
        topKSelect.addEventListener('change', () => {
            window.searchEngine.handleAdvancedOptionChange();
        });
    }
    
    if (searchTypeSelect) {
        searchTypeSelect.addEventListener('change', () => {
            window.searchEngine.handleAdvancedOptionChange();
        });
    }
    
    // Add some example functionality
    console.log('Modern Search Engine initialized');
    
    // Example: Add keyboard shortcut hint
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.placeholder = 'Search the web... (Press / to focus)';
    }
});

// Utility functions
const SearchUtils = {
    formatNumber: (num) => {
        return new Intl.NumberFormat().format(num);
    },
    
    formatTime: (seconds) => {
        if (seconds < 1) {
            return `${(seconds * 1000).toFixed(0)}ms`;
        }
        return `${seconds.toFixed(3)}s`;
    },
    
    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    throttle: (func, limit) => {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    },
    
    // Helper to get advanced search options
    getAdvancedOptions: () => {
        return {
            topK: document.getElementById('topK')?.value || '10',
            searchType: document.getElementById('searchType')?.value || 'standard'
        };
    },
    
    // Helper to set advanced search options
    setAdvancedOptions: (options) => {
        if (options.topK && document.getElementById('topK')) {
            document.getElementById('topK').value = options.topK;
        }
        if (options.searchType && document.getElementById('searchType')) {
            document.getElementById('searchType').value = options.searchType;
        }
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ModernSearchEngine, SearchUtils };
}