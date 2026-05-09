import os
import re
import json
from bs4 import BeautifulSoup
import html2text
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

RAW_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'phase1_raw')
CLEAN_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'phase1_cleaned')

def clean_html_to_markdown(html_content):
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.ignore_emphasis = False
    h.body_width = 0
    return h.handle(html_content)

def split_markdown_table(table_text, max_rows=15):
    lines = table_text.strip().split('\n')
    header_idx = -1
    for i, line in enumerate(lines):
        if re.match(r'^[\-\s\|]+$', line) and i > 0 and '|' in lines[i-1]:
            header_idx = i - 1
            break
            
    if header_idx == -1:
        return [table_text]
        
    header_lines = lines[:header_idx+2]
    data_lines = lines[header_idx+2:]
    
    chunks = []
    for i in range(0, len(data_lines), max_rows):
        batch = data_lines[i:i+max_rows]
        chunks.append('\n'.join(header_lines + batch))
        
    return chunks

def clean_and_chunk_all():
    print("[Subphase 1.3] Starting Semantic Data Cleaning & Chunking...")
    os.makedirs(CLEAN_DIR, exist_ok=True)
    
    headers_to_split_on = [
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    
    if not os.path.exists(RAW_DIR):
        print(f"[Subphase 1.3] Raw directory not found: {RAW_DIR}")
        return
        
    for filename in os.listdir(RAW_DIR):
        if not filename.endswith('.html'):
            continue
            
        file_path = os.path.join(RAW_DIR, filename)
        meta_path = file_path.replace('.html', '_meta.json')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
            
        soup = BeautifulSoup(html_content, 'html.parser')
        
        for tag in soup(['header', 'footer', 'nav', 'aside', 'script', 'style', 'svg']):
            tag.decompose()
            
        main_content = soup.find('main') or soup.body
        if not main_content:
            continue
            
        markdown_text = clean_html_to_markdown(str(main_content))
        # Clean up whitespace
        markdown_text = re.sub(r'\n{3,}', '\n\n', markdown_text).strip()
            
        # 1. Semantic split by Headers
        md_header_splits = markdown_splitter.split_text(markdown_text)
        
        final_chunks = []
        seen_faq_headers = set()  # deduplicate FAQ sections with the same H3 question
        fund_manager_chunk = None  # synthesized fund manager FAQ chunk

        for split in md_header_splits:
            content = split.page_content
            split_meta = split.metadata
            
            # Filter pure noise sections
            h2 = split_meta.get("Header 2", "")
            h3 = split_meta.get("Header 3", "")
            if "Recently viewed" in h2 or "Recently viewed" in h3:
                continue
            if "Compare similar funds" in h2 or "Compare similar funds" in h3:
                continue

            # Filter empty-header nav/boilerplate chunks (no meaningful header)
            if not h2.strip() and not h3.strip():
                continue

            # Deduplicate FAQ chunks: same H3 question produces many sub-chunks
            # from table splitting — keep only the first occurrence
            if h2 == "FAQs" and h3:
                if h3 in seen_faq_headers:
                    continue
                seen_faq_headers.add(h3)

            # Extract fund manager info from the "About" section to synthesise
            # a dedicated FAQ chunk (Groww pages don't have a fund manager FAQ)
            if "About" in h3 and "Current Fund Manager" in content:
                fm_match = re.search(
                    r'([A-Z][a-z]+(?: [A-Z][a-z]+)+) is the Current Fund Manager',
                    content
                )
                if fm_match:
                    fm_name = fm_match.group(1)
                    fund_manager_chunk = {
                        "text": (
                            f"Scheme: {meta['scheme_name']} | Section: FAQs "
                            f"Who is the fund manager of {meta['scheme_name']}?\n"
                            f"{fm_name} is the Current Fund Manager of {meta['scheme_name']}."
                        ),
                        "metadata": {"Header 2": "FAQs", "Header 3": f"Who is the fund manager of {meta['scheme_name']}?"}
                    }

            # 2. Advanced Table Split for massive tables like "Holdings"
            if "Holdings" in h2 or "Holdings" in h3:
                table_chunks = split_markdown_table(content, max_rows=15)
                for t_chunk in table_chunks:
                    final_chunks.append({
                        "text": f"Scheme: {meta['scheme_name']} | Section: {h2} {h3}\n{t_chunk}".strip(),
                        "metadata": split_meta
                    })
            else:
                # 3. Fallback for other long texts
                if len(content) > 1000:
                    sub_chunks = text_splitter.split_text(content)
                    for sc in sub_chunks:
                        final_chunks.append({
                            "text": f"Scheme: {meta['scheme_name']} | Section: {h2} {h3}\n{sc}".strip(),
                            "metadata": split_meta
                        })
                else:
                    final_chunks.append({
                        "text": f"Scheme: {meta['scheme_name']} | Section: {h2} {h3}\n{content}".strip(),
                        "metadata": split_meta
                    })

        # Append the synthesised fund manager FAQ chunk if found
        if fund_manager_chunk:
            final_chunks.append(fund_manager_chunk)
        
        safe_name = filename.replace('.html', '')
        out_path = os.path.join(CLEAN_DIR, f"{safe_name}_chunks.json")
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump({
                "scheme_name": meta["scheme_name"],
                "source_url": meta["source_url"],
                "chunks": [c["text"] for c in final_chunks]
            }, f, indent=4, ensure_ascii=False)
            
        print(f"[Subphase 1.3] Semantically chunked {meta['scheme_name']} -> {len(final_chunks)} chunks saved.")
        
    print("[Subphase 1.3] Semantic Cleaning & Chunking Complete.\n")

if __name__ == "__main__":
    clean_and_chunk_all()
