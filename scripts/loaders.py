from langchain_unstructured import UnstructuredLoader
from dotenv import load_dotenv

load_dotenv()

def document_loader(files):

    file_path = "../Loaded_Files/"
    
    files = [file_path + file for file in files]

    loader = UnstructuredLoader(
        files,
        chunking_strategy= 'basic',
        max_characters = 10000,
        include_orig_elements = False,
    )

    docs = loader.load()

    return docs


if __name__ == "__main__":
    files = ["Park_friend.docx", "Park_friend.pdf"]
    aa = document_loader(files)

    for a in aa:
        source = a.metadata['source']
        content = a.page_content
        print(f"Document {source}:\nPage Content:\n{content}")
