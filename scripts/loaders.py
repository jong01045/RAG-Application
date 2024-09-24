from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
import os

load_dotenv()

# Make sure the filenames are repeated


# PDF loader
# PyPDFLoader
def pdf_document_loader(files : list[str]) -> dict:

    #Files uploaded by the user is stored in Loaded_Files folder.
    file_path = "../Loaded_Files/"
    files = [file_path + file for file in files]

    # A dictionary of document lists
    # {Filename (str) : list[Document]}
    # Contain all other documents, in case where the number of pdf file is more than one.
    total_doc = {}

    #Recursively load all pdf files uploaded.
    for file in files:
        loader = PyPDFLoader(file)
        docs = loader.load()

        #Add the list of documents to the total list.
        total_doc[file] = docs

    return total_doc

# Separate file types
# return dict
# {extenstion(str) : list[filename]}
def file_type_filter(files : list[str]) -> dict:

    # Dictionary to store files based on their extensions
    files_by_extension = {}

    for filename in files:
        # Use os.path.splitext() to split the file name and extension
        name, extension = os.path.splitext(filename)
        
        # Ensure extensions are consistent (removing the dot)
        extension = extension.lower().lstrip('.')
        
        # Add the file to the dictionary based on its extension
        if extension not in files_by_extension:
            files_by_extension[extension] = []
        
        files_by_extension[extension].append(filename)
    
    return files_by_extension


if __name__ == "__main__":

    # All uploaded documents are stored in Loaded_Files folder.
    document_folder_path = "../Loaded_Files"

    # Get the list of all files and directories
    files = os.listdir(document_folder_path)

    # dict
    # {extenstion(str) : [filename (str)]}
    # e.g) {"pdf" : [document, document1, document2], ...}
    files_by_filetype = file_type_filter(files)

    # A list of PDF documents
    pdf_files = files_by_filetype['pdf']

    # dict
    # {filename (str) : list[Document], ...}
    pdf_docs = pdf_document_loader(files = pdf_files)

    for filename, documents in pdf_docs.items():
        for document in documents:
            source = document.metadata['source']
            page = document.metadata['page']
            content = document.page_content
            pagebreak = "-" * 40
            print(f"Document {source}:\nPage:{page}\nPage Content:\n{content}\n\n{pagebreak}\n")
