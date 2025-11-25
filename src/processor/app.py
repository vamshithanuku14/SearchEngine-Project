from flask import Flask, request, jsonify, render_template
import pandas as pd
from common.config import Config
from common.logger import setup_logger
from .query_validator import EnhancedQueryValidator
from .results_generator import EnhancedResultsGenerator

logger = setup_logger(__name__)

def create_app():
    """Create and configure enhanced Flask application."""
    app = Flask(__name__)
    config = Config()
    
    # Initialize enhanced components
    query_validator = EnhancedQueryValidator()
    results_generator = EnhancedResultsGenerator()
    
    @app.route('/')
    def index():
        """Render main search page."""
        return render_template('modern_index.html')
    
    @app.route('/search', methods=['GET', 'POST'])
    def search():
        """Handle enhanced search queries."""
        try:
            # Get query parameters
            if request.method == 'GET':
                query = request.args.get('q', '')
                top_k = request.args.get('top_k', default=config.get('processor.top_k_results', 10), type=int)
                search_type = request.args.get('type', 'standard')
                use_spell_check = request.args.get('spell_check', default=True, type=bool)
                use_expansion = request.args.get('expansion', default=True, type=bool)
            else:
                data = request.json if request.is_json else request.form
                query = data.get('query', '')
                top_k = data.get('top_k', config.get('processor.top_k_results', 10))
                search_type = data.get('type', 'standard')
                use_spell_check = data.get('spell_check', True)
                use_expansion = data.get('expansion', True)
            
            if not query:
                return jsonify({
                    'error': 'Query parameter is required',
                    'error_code': 'MISSING_QUERY'
                }), 400
            
            # Enhanced query validation with smart features
            validation_result = query_validator.validate_query(query)
            
            # Determine which query to use based on settings
            if use_spell_check and validation_result['has_corrections']:
                search_query = validation_result['corrected_query']
                correction_used = True
            else:
                search_query = validation_result['cleaned_query']
                correction_used = False
            
            # Apply query expansion if enabled
            if use_expansion and validation_result['has_expansions']:
                final_query = validation_result['expanded_query']
                expansion_used = True
            else:
                final_query = search_query
                expansion_used = False
            
            # Process query and get results
            search_results = results_generator.search(
                final_query, 
                top_k=top_k, 
                use_enhanced_ranking=True
            )
            
            # Prepare enhanced response with smart features info
            response = {
                'query': query,
                'processed_query': final_query,
                'cleaned_query': validation_result['cleaned_query'],
                'corrected_query': validation_result.get('corrected_query', ''),
                'expanded_query': validation_result.get('expanded_query', ''),
                'results': search_results,
                'total_results': len(search_results),
                'smart_features': {
                    'spell_check_used': correction_used,
                    'query_expansion_used': expansion_used,
                    'original_query': query,
                    'corrections_applied': validation_result['spelling'].get('corrections', []),
                    'expansions_applied': validation_result['expansion'].get('new_terms', [])
                },
                'validation_result': {
                    'valid': validation_result['valid'],
                    'analysis': validation_result.get('analysis', {}),
                    'spelling_corrections': validation_result.get('spelling', {}).get('corrections', []),
                    'query_expansion': validation_result.get('expansion', {}).get('new_terms', [])
                },
                'search_metadata': {
                    'top_k': top_k,
                    'search_type': search_type,
                    'spell_check_enabled': use_spell_check,
                    'expansion_enabled': use_expansion,
                    'execution_time': search_results[0].get('execution_time', 0) if search_results else 0
                }
            }
            
            # Log smart features usage
            if correction_used:
                logger.info(f"Spell correction applied: '{query}' -> '{search_query}'")
            if expansion_used:
                logger.info(f"Query expansion applied: '{search_query}' -> '{final_query}'")
            
            logger.info(f"Enhanced search completed for query: '{query}' -> '{final_query}', found {len(search_results)} results")
            
            return jsonify(response)
            
        except Exception as e:
            logger.error(f"Error processing search request: {str(e)}")
            return jsonify({
                'error': 'Internal server error',
                'error_code': 'INTERNAL_ERROR'
            }), 500
    
    @app.route('/suggest', methods=['GET'])
    def suggest():
        """Provide enhanced query suggestions."""
        try:
            query = request.args.get('q', '')
            max_suggestions = request.args.get('max', default=5, type=int)
            
            if not query:
                return jsonify({'suggestions': []})
            
            suggestions = query_validator.get_enhanced_suggestions(query, max_suggestions)
            
            # Format suggestions for frontend
            formatted_suggestions = [s['suggestion'] for s in suggestions]
            
            return jsonify({
                'query': query,
                'suggestions': formatted_suggestions,
                'detailed_suggestions': suggestions,
                'total_suggestions': len(suggestions)
            })
            
        except Exception as e:
            logger.error(f"Error generating suggestions: {str(e)}")
            return jsonify({'suggestions': []})
    
    @app.route('/validate', methods=['POST'])
    def validate_query():
        """Endpoint specifically for query validation."""
        try:
            data = request.json
            query = data.get('query', '')
            
            if not query:
                return jsonify({'error': 'Query parameter is required'}), 400
            
            validation_result = query_validator.validate_query(query)
            
            return jsonify(validation_result)
            
        except Exception as e:
            logger.error(f"Error validating query: {str(e)}")
            return jsonify({
                'valid': False,
                'message': 'Validation error',
                'error': str(e)
            }), 500
    
    @app.route('/spellcheck', methods=['GET'])
    def spell_check():
        """Endpoint specifically for spell checking."""
        try:
            query = request.args.get('q', '')
            
            if not query:
                return jsonify({'corrections': []})
            
            validation_result = query_validator.validate_query(query)
            spell_result = validation_result.get('spelling', {})
            
            return jsonify({
                'original_query': query,
                'corrected_query': spell_result.get('corrected_query', query),
                'has_corrections': spell_result.get('has_corrections', False),
                'corrections': spell_result.get('corrections', []),
                'confidence': spell_result.get('confidence_score', 1.0)
            })
            
        except Exception as e:
            logger.error(f"Error in spell check: {str(e)}")
            return jsonify({
                'original_query': query,
                'corrected_query': query,
                'has_corrections': False,
                'corrections': [],
                'error': str(e)
            })
    
    @app.route('/expand', methods=['GET'])
    def expand_query():
        """Endpoint specifically for query expansion."""
        try:
            query = request.args.get('q', '')
            
            if not query:
                return jsonify({'expanded_query': '', 'new_terms': []})
            
            validation_result = query_validator.validate_query(query)
            expansion_result = validation_result.get('expansion', {})
            
            return jsonify({
                'original_query': query,
                'expanded_query': expansion_result.get('expanded_query', query),
                'new_terms': expansion_result.get('new_terms', []),
                'expansion_details': expansion_result.get('expansion_details', []),
                'has_expansion': len(expansion_result.get('new_terms', [])) > 0
            })
            
        except Exception as e:
            logger.error(f"Error in query expansion: {str(e)}")
            return jsonify({
                'original_query': query,
                'expanded_query': query,
                'new_terms': [],
                'has_expansion': False,
                'error': str(e)
            })
    
    @app.route('/batch_search', methods=['POST'])
    def batch_search():
        """Handle enhanced batch search queries from CSV file."""
        try:
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            if not file.filename.endswith('.csv'):
                return jsonify({'error': 'File must be in CSV format'}), 400
            
            # Read CSV file
            df = pd.read_csv(file)
            if 'query' not in df.columns:
                return jsonify({'error': 'CSV must contain "query" column'}), 400
            
            queries = df['query'].tolist()
            results = []
            stats = {
                'total_queries': len(queries),
                'successful_queries': 0,
                'failed_queries': 0,
                'total_results': 0,
                'queries_with_corrections': 0,
                'queries_with_expansion': 0
            }
            
            for query in queries:
                validation_result = query_validator.validate_query(query)
                if validation_result['valid']:
                    processed_query = validation_result.get('suggested_query', query)
                    search_results = results_generator.search(processed_query)
                    
                    # Track smart features usage
                    has_corrections = validation_result.get('has_corrections', False)
                    has_expansions = len(validation_result.get('expansion', {}).get('new_terms', [])) > 0
                    
                    if has_corrections:
                        stats['queries_with_corrections'] += 1
                    if has_expansions:
                        stats['queries_with_expansion'] += 1
                    
                    results.append({
                        'original_query': query,
                        'processed_query': processed_query,
                        'results': search_results,
                        'validation_details': validation_result,
                        'smart_features_used': {
                            'spell_check': has_corrections,
                            'query_expansion': has_expansions
                        },
                        'status': 'success'
                    })
                    
                    stats['successful_queries'] += 1
                    stats['total_results'] += len(search_results)
                else:
                    results.append({
                        'original_query': query,
                        'error': validation_result['message'],
                        'error_code': validation_result.get('error_code'),
                        'results': [],
                        'status': 'failed'
                    })
                    stats['failed_queries'] += 1
            
            return jsonify({
                'batch_results': results,
                'statistics': stats
            })
            
        except Exception as e:
            logger.error(f"Error processing batch search: {str(e)}")
            return jsonify({'error': 'Error processing batch search'}), 500
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Enhanced health check endpoint."""
        try:
            # Check if index is loaded
            index_status = 'loaded' if results_generator.inverted_index.total_documents > 0 else 'empty'
            validator_status = 'ready'
            
            return jsonify({
                'status': 'healthy',
                'service': 'enhanced_search_engine',
                'components': {
                    'query_validator': validator_status,
                    'results_generator': index_status,
                    'index_documents': results_generator.inverted_index.total_documents
                },
                'smart_features': {
                    'spell_check': 'enabled',
                    'query_expansion': 'enabled',
                    'suggestions': 'enabled'
                },
                'version': '2.0.0'
            })
        except Exception as e:
            return jsonify({
                'status': 'degraded',
                'error': str(e)
            }), 500
    
    return app