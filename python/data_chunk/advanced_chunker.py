from semantic_chunker.core import SemanticChunker

chunks = [
    {"text": "Artificial intelligence is a growing field."},
    {"text": "Machine learning is a subset of AI."},
    {"text": "Photosynthesis occurs in plants."},
    {"text": "Deep learning uses neural networks."},
    {"text": "Plants convert sunlight into energy."},
]

chunker = SemanticChunker(max_tokens=512)
merged_chunks = chunker.chunk(chunks)

for i, merged in enumerate(merged_chunks):
    print(f"Chunk {i}:")
    print(merged["text"])
    print()

# Response

Merged Chunk 1
Text: Artificial intelligence is a growing field. Machine learning is a subset of AI. Deep learning uses n...
Metadata: [{'text': 'Artificial intelligence is a growing field.'}, {'text': 'Machine learning is a subset of AI.'}, {'text': 'Deep learning uses neural networks.'}]

Merged Chunk 2
Text: Photosynthesis occurs in plants. Plants convert sunlight into energy....
Metadata: [{'text': 'Photosynthesis occurs in plants.'}, {'text': 'Plants convert sunlight into energy.'}]
