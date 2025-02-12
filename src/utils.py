import re
import json
from typing import List, Tuple, Dict
from datetime import datetime

def anonymize_text(text: str) -> Tuple[str, List[str], Dict]:
    """
    Anonymize sensitive information in text and generate embeddings with anonymized content.
    Returns tuple of (anonymized text, list of found sensitive items, dictionary of embedding data)
    """
    patterns = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'phone': r'\b(?:\+?34)?[\s.-]?[689]\d{2}[\s.-]?\d{3}[\s.-]?\d{3}\b',  # Spanish phone numbers
        'international_phone': r'\b(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',  # International format
        'address': r'\b(?:Calle|Avenida|Av\.|C/)\s+(?:[A-Za-zÀ-ÿ\s,]+\d*)+(?:,\s*\d{5})?\b',  # Spanish addresses
    }

    found_items = []
    anonymized = text
    replacements = []

    # First pass: collect all sensitive information and perform replacements
    for pattern_name, pattern in patterns.items():
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            found_text = match.group()
            found_items.append(f"{pattern_name}: {found_text}")
            anonymized_text = '*' * len(found_text)
            replacements.append({
                'type': pattern_name,
                'original': found_text,
                'anonymized': anonymized_text,
                'position': match.span()
            })
            anonymized = anonymized.replace(found_text, anonymized_text)

    # Create embeddings data with optimization for LLM and RAG systems
    chunk_size = 1000
    chunks = [anonymized[i:i+chunk_size] for i in range(0, len(anonymized), chunk_size)]

    embeddings_data = {
        'metadata': {
            'timestamp': datetime.now().isoformat(),
            'document_length': len(text),
            'anonymized_length': len(anonymized),
            'sensitive_items_count': len(found_items),
            'language': 'es',  # Spanish content
            'version': '1.0',
            'embeddings_model': 'text-embedding-3-large',  # Latest OpenAI embeddings model
            'content_type': 'text/plain',
            'anonymization_level': 'partial',  # Only specific patterns are anonymized
            'charset': 'utf-8'
        },
        'embedding_config': {
            'chunk_size': chunk_size,
            'overlap': 0,  # No overlap between chunks
            'total_chunks': len(chunks),
            'model_max_tokens': 8191  # Standard context window for embeddings
        },
        'content': {
            'text': anonymized,  # Full anonymized text
            'chunks': chunks,  # Text divided into chunks for embedding
            'chunk_metadata': [{
                'index': i,
                'length': len(chunk),
                'start_char': i * chunk_size,
                'end_char': min((i + 1) * chunk_size, len(anonymized))
            } for i, chunk in enumerate(chunks)]
        },
        'sensitive_data': [{
            'type': r['type'],
            'position': r['position'],
            'length': len(r['original']),
            'replacement': r['anonymized']
        } for r in replacements],
        'rag_metadata': {
            'document_type': 'anonymized_text',
            'processing_type': 'privacy_enhanced',
            'embedding_ready': True,
            'anonymization_patterns': list(patterns.keys()),
            'vector_dimensions': 3072,  # Matches text-embedding-3-large dimensions
            'similarity_metric': 'cosine',
            'preprocessing': ['anonymization', 'chunking'],
            'usage': 'document_retrieval'
        }
    }

    return anonymized, found_items, embeddings_data

def format_found_items(items: List[str]) -> str:
    """Format the list of found sensitive items for display"""
    if not items:
        return "No se ha detectado información sensible"
    return "\n".join(sorted(items))

def get_embeddings_json(embeddings_data: Dict) -> str:
    """Convert embeddings data to JSON string"""
    return json.dumps(embeddings_data, ensure_ascii=False, indent=2)