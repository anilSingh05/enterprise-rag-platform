import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


from app.ingestion.chuncking import TextChunker

sample_text = open("data/fintech/kyc_policy_v1.txt").read()

chunker = TextChunker()
chunks = chunker.chunk_text(sample_text)

print(f"Total chunks: {len(chunks)}")
print("First chunk:\n", chunks[0].text)
