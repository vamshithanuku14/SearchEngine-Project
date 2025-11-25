/**
 * Smart Search Engine Frontend with Enhanced Features
 * Real-time spell checking, query expansion, and suggestions
 */

class SmartSearchEngine {
    constructor() {
        this.searchInput = document.getElementById('searchInput');
        this.searchForm = document.getElementById('searchForm');
        this.suggestions = document.getElementById('suggestions');
        this.resultsContainer = document.getElementById('resultsContainer');
        this.loading = document.getElementById('loading');
        this.resultsCount = document.getElementById('resultsCount');
        this.resultsStats = document.getElementById('resultsStats');
        this.smartFeaturesPanel = document.getElementById('smartFeaturesPanel');
        
        this.debounceTimer = null;
        this.currentQuery = '';
        this.lastSearchTime = 0;
        this.smartFeaturesEnabled = true;
        
        this.initializeEventListeners();
        this.initializeSmartFeatures();
    }
    
    initializeEventListeners() {
        // Search input events
        this.searchInput.addEventListener('input', (e) => this.handleInput(e));
        this.searchInput.addEventListener('focus', () => this.showSuggestions());
        this.searchInput.addEventListener('keydown', (e) => this.handleKeydown(e));
        
        // Form submission
        this.searchForm.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Click outside to hide suggestions
        document.addEventListener('click', (e) => {
            if (!this.searchInput.contains(e.target) && !this.suggestions.contains(e.target)) {
                this.hideSuggestions();
            }
        });
    }
    
    initializeSmartFeatures() {
        // Create smart features panel if it doesn't exist
        if (!this.smartFeaturesPanel) {
            this.createSmartFeaturesPanel();
        }
        
        console.log('🔍 Smart search features initialized');
    }
    
    createSmartFeaturesPanel() {
        const panel = document.createElement('div');
        panel.id = 'smartFeaturesPanel';
        panel.className = 'smart-features-panel hidden';
        panel.innerHTML = `
            <div class="smart-features-header">
                <h4>🧠 Smart Search Features</h4>
                <button class="close-panel" onclick="searchEngine.hideSmartFeatures()">×</button>
            </div>
            <div class="smart-features-content">
                <div id="spellCheckInfo" class="feature-info hidden">
                    <div class="feature-icon">🔤</div>
                    <div class="feature-details">
                        <strong>Spell Check Applied</strong>
                        <div class="correction-details"></div>
                    </div>
                </div>
                <div id="expansionInfo" class="feature-info hidden">
                    <div class="feature-icon">🔍</div>
                    <div class="feature-details">
                        <strong>Query Expanded</strong>
                        <div class="expansion-details"></div>
                    </div>
                </div>
                <div id="suggestionsInfo" class="feature-info hidden">
                    <div class="feature-icon">💡</div>
                    <div class="feature-details">
                        <strong>Search Suggestions</strong>
                        <div class="suggestion-details"></div>
                    </div>
                </div>
            </div>
        `;
        
        // Insert after search form
        this.searchForm.parentNode.insertBefore(panel, this.searchForm.nextSibling);
        this.smartFeaturesPanel = panel;
    }
    
    handleInput(e) {
        const query = e.target.value.trim();
        this.currentQuery = query;
        
        // Clear previous debounce timer
        clearTimeout(this.debounceTimer);
        
        if (query.length === 0) {
            this.hideSuggestions();
            this.clearResults();
            this.hideSmartFeatures();
            return;
        }
        
        if (query.length < 2) {
            this.hideSuggestions();
            return;
        }
        
        // Debounce suggestions and real-time features
        this.debounceTimer = setTimeout(() => {
            this.fetchSuggestions(query);
            this.showRealTimeFeatures(query);
        }, 300);
    }
    
    async showRealTimeFeatures(query) {
        if (!this.smartFeaturesEnabled) return;
        
        try {
            // Show loading state for smart features
            this.showSmartFeaturesLoading();
            
            // Fetch spell check and expansion in parallel
            const [spellCheck, expansion] = await Promise.all([
                this.fetchSpellCheck(query),
                this.fetchExpansion(query)
            ]);
            
            this.displayRealTimeFeatures(spellCheck, expansion, query);
            
        } catch (error) {
            console.error('Error showing real-time features:', error);
        }
    }
    
    async fetchSpellCheck(query) {
        const response = await fetch(`/spellcheck?q=${encodeURIComponent(query)}`);
        return await response.json();
    }
    
    async fetchExpansion(query) {
        const response = await fetch(`/expand?q=${encodeURIComponent(query)}`);
        return await response.json();
    }
    
    displayRealTimeFeatures(spellCheck, expansion, originalQuery) {
        this.showSmartFeaturesPanel();
        
        // Spell Check Information
        const spellCheckInfo = document.getElementById('spellCheckInfo');
        const spellCheckDetails = spellCheckInfo.querySelector('.correction-details');
        
        if (spellCheck.has_corrections) {
            spellCheckInfo.classList.remove('hidden');
            spellCheckDetails.innerHTML = `
                <div class="correction-item">
                    <span class="original">"${spellCheck.original_query}"</span>
                    <span class="arrow">→</span>
                    <span class="corrected">"${spellCheck.corrected_query}"</span>
                </div>
                <div class="confidence">Confidence: ${(spellCheck.confidence * 100).toFixed(0)}%</div>
            `;
        } else {
            spellCheckInfo.classList.add('hidden');
        }
        
        // Query Expansion Information
        const expansionInfo = document.getElementById('expansionInfo');
        const expansionDetails = expansionInfo.querySelector('.expansion-details');
        
        if (expansion.has_expansion && expansion.new_terms.length > 0) {
            expansionInfo.classList.remove('hidden');
            expansionDetails.innerHTML = `
                <div class="expansion-item">
                    <span class="original">"${expansion.original_query}"</span>
                    <span class="arrow">+</span>
                    <span class="new-terms">${expansion.new_terms.join(', ')}</span>
                </div>
                <div class="expanded-query">Expanded to: "${expansion.expanded_query}"</div>
            `;
        } else {
            expansionInfo.classList.add('hidden');
        }
        
        // Show suggestions info if we have any
        this.updateSuggestionsInfo();
    }
    
    updateSuggestionsInfo() {
        const suggestionsInfo = document.getElementById('suggestionsInfo');
        const suggestionDetails = suggestionsInfo.querySelector('.suggestion-details');
        
        const currentSuggestions = this.suggestions.querySelectorAll('.suggestion-item');
        if (currentSuggestions.length > 0) {
            suggestionsInfo.classList.remove('hidden');
            suggestionDetails.innerHTML = `
                <div>${currentSuggestions.length} suggestions available</div>
                <div class="suggestion-examples">
                    ${Array.from(currentSuggestions).slice(0, 3).map(s => 
                      `<span class="suggestion-example">"${s.querySelector('.suggestion-query').textContent}"</span>`
                    ).join('')}
                </div>
            `;
        } else {
            suggestionsInfo.classList.add('hidden');
        }
    }
    
    showSmartFeaturesPanel() {
        if (this.smartFeaturesPanel) {
            this.smartFeaturesPanel.classList.remove('hidden');
        }
    }
    
    hideSmartFeatures() {
        if (this.smartFeaturesPanel) {
            this.smartFeaturesPanel.classList.add('hidden');
        }
    }
    
    showSmartFeaturesLoading() {
        this.showSmartFeaturesPanel();
        const content = this.smartFeaturesPanel.querySelector('.smart-features-content');
        content.innerHTML = '<div class="loading-smart">Analyzing query...</div>';
    }
    
    async fetchSuggestions(query) {
        try {
            const response = await fetch(`/suggest?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            this.displaySuggestions(data.suggestions, query);
            this.updateSuggestionsInfo();
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
        
        // Determine icon based on suggestion type
        const icon = this.getSuggestionIcon(suggestion);
        
        div.innerHTML = `
            <span class="suggestion-icon">${icon}</span>
            <span class="suggestion-query">${this.highlightText(suggestion, query)}</span>
            <span class="suggestion-type">suggestion</span>
        `;
        
        div.addEventListener('click', () => {
            this.selectSuggestion(div);
        });
        
        return div;
    }
    
    getSuggestionIcon(suggestion) {
        // Simple heuristic for suggestion types
        if (suggestion.includes(' ')) {
            return '💡'; // Multi-word suggestions
        } else if (suggestion.length <= 5) {
            return '🔤'; // Short words
        } else {
            return '🔍'; // General suggestions
        }
    }
    
    highlightText(text, query) {
        if (!query) return text;
        
        const regex = new RegExp(`(${this.escapeRegex(query)})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }
    
    escapeRegex(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }
    
    selectSuggestion(suggestionElement) {
        const query = suggestionElement.querySelector('.suggestion-query').textContent;
        this.searchInput.value = query;
        this.hideSuggestions();
        this.performSearch(query);
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
                this.hideSmartFeatures();
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
    
    handleSubmit(e) {
        e.preventDefault();
        const query = this.searchInput.value.trim();
        
        if (query) {
            this.performSearch(query);
        }
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
            const response = await fetch(`/search?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            this.displayResults(data);
            this.showSmartFeaturesSummary(data);
            
        } catch (error) {
            this.displayError('Search failed: ' + error.message);
        } finally {
            this.hideLoading();
        }
    }
    
    showSmartFeaturesSummary(data) {
        if (!data.smart_features) return;
        
        const features = data.smart_features;
        let summary = [];
        
        if (features.spell_check_used) {
            summary.push(`🔤 Corrected "${features.original_query}" to "${data.processed_query}"`);
        }
        
        if (features.query_expansion_used) {
            summary.push(`🔍 Expanded with: ${features.expansions_applied.join(', ')}`);
        }
        
        if (summary.length > 0) {
            this.showNotification(summary.join(' | '));
        }
    }
    
    showNotification(message) {
        // Create or update notification element
        let notification = document.getElementById('smartFeatureNotification');
        if (!notification) {
            notification = document.createElement('div');
            notification.id = 'smartFeatureNotification';
            notification.className = 'smart-feature-notification';
            document.body.appendChild(notification);
        }
        
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">🧠</span>
                <span class="notification-text">${message}</span>
                <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;
        
        notification.classList.add('show');
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            notification.classList.remove('show');
        }, 5000);
    }
    
    displayResults(data) {
        this.resultsContainer.innerHTML = '';
        
        if (data.error) {
            this.displayError(data.error);
            return;
        }
        
        // Update results count with smart features info
        if (this.resultsCount) {
            let countText = `About ${data.total_results} results`;
            
            if (data.smart_features) {
                if (data.smart_features.spell_check_used || data.smart_features.query_expansion_used) {
                    countText += ' (with smart features)';
                }
            }
            
            this.resultsCount.textContent = countText;
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
    }
    
    createResultElement(result, rank) {
        const resultDiv = document.createElement('div');
        resultDiv.className = 'result-item';
        
        const scorePercent = Math.min(result.similarity_score * 100, 100);
        
        resultDiv.innerHTML = `
            <div class="result-badge">#${rank}</div>
            <a href="${result.url}" class="result-title" target="_blank" rel="noopener">
                ${this.escapeHtml(result.title)}
            </a>
            <div class="result-url">${this.escapeHtml(result.url)}</div>
            <div class="result-snippet">${result.snippet}</div>
            <div class="result-meta">
                <div class="meta-item">
                    <span>Relevance: ${(result.similarity_score * 100).toFixed(1)}%</span>
                    <div class="score-bar">
                        <div class="score-fill" style="width: ${scorePercent}%"></div>
                    </div>
                </div>
            </div>
        `;
        
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
            </div>
        `;
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
    
    showLoading() {
        this.loading.classList.remove('hidden');
        this.resultsContainer.innerHTML = '';
    }
    
    hideLoading() {
        this.loading.classList.add('hidden');
    }
    
    clearResults() {
        this.resultsContainer.innerHTML = '';
        if (this.resultsCount) this.resultsCount.textContent = '';
        if (this.resultsStats) this.resultsStats.innerHTML = '';
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    window.searchEngine = new SmartSearchEngine();
    
    // Handle search query from URL
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('q');
    if (query) {
        window.searchEngine.searchInput.value = query;
        window.searchEngine.performSearch(query);
    }
});