import utils  # Make sure utils.py is in the same directory or in PYTHONPATH

def main():
    # Load your PDF or TXT file text
    text = utils.load_pdf_text("path/to/your/document.pdf")  # Change to your file path
    # Or for TXT file:
    # text = utils.load_txt_text("path/to/your/document.txt")

    # Chunk your text
    chunks = utils.get_text_chunks(text)

    # Get embeddings for all chunks
    embeddings = utils.get_embeddings(chunks)

    print(f"Got {len(embeddings)} embeddings.")
    print("First embedding vector snippet:", embeddings[0][:5])

if __name__ == "__main__":
    main()
