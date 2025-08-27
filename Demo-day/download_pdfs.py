import arxiv
import requests
import json
import os
from pathlib import Path

def download_arxiv_pdfs():
    """Download real PDFs from ArXiv"""
    
    print("🔍 Searching for credit risk papers on ArXiv...")
    
    # Search for credit risk papers
    search = arxiv.Search(
        query="credit risk modeling machine learning",
        max_results=3,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    downloaded_papers = []
    
    for result in search.results():
        try:
            # Create filename from title
            filename = result.title.replace(" ", "_").replace(":", "").replace(",", "")[:50] + ".pdf"
            filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.')).rstrip()
            
            print(f"📥 Downloading: {result.title[:60]}...")
            
            # Download PDF
            response = requests.get(result.pdf_url, stream=True)
            response.raise_for_status()
            
            filepath = Path("data/pdfs") / filename
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ Downloaded: {filename}")
            
            # Save metadata
            metadata = {
                "title": result.title,
                "authors": [author.name for author in result.authors],
                "summary": result.summary,
                "published_date": result.published.strftime("%Y-%m-%d") if result.published else None,
                "arxiv_id": result.entry_id,
                "pdf_filename": filename
            }
            
            downloaded_papers.append(metadata)
            
            # Save individual metadata
            metadata_file = Path("data/research_papers") / f"{result.entry_id.split('/')[-1]}.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
                
        except Exception as e:
            print(f"❌ Failed to download {result.title[:30]}...: {e}")
    
    # Save all metadata together
    with open("data/research_papers/all_papers.json", 'w') as f:
        json.dump(downloaded_papers, f, indent=2)
    
    print(f"✅ Downloaded {len(downloaded_papers)} PDFs successfully!")

if __name__ == "__main__":
    download_arxiv_pdfs()
