from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import BSHTMLLoader

from dotenv import load_dotenv
import os
from dataclasses import dataclass
from typing import Type

load_dotenv()

# Make sure the filenames are repeated

# Parent document loader class
@dataclass
class Document_loader:

    document_loader_class : Type    # Appropriate document loader class 

    # Versatile document loader
    def load_document(self, files, **kwargs):
        #Files uploaded by the user is stored in Loaded_Files folder.    
        file_path = "../Loaded_Files/"
        files = [file_path + file for file in files]

        # A dictionary of document lists
        # {Filename (str) : list[Document]}
        # Contain all other documents, in case where the number of file is more than one.
        total_doc = {}

        #Recursively load all files
        for file in files:
            loader = self.document_loader_class(file, **kwargs)
            docs = loader.load()

            total_doc[file] = docs

        return total_doc

# PDF loader
# Unstructured 
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

def load_all_files(files_by_filetype) -> dict:
    # A list of PDF documents
    pdf_files = files_by_filetype['pdf']
    docx_files = files_by_filetype['docx']
    txt_files = files_by_filetype['txt']
    html_files = files_by_filetype['html']

    # Document loader objects
    pdf_loader = Document_loader(document_loader_class=PyPDFLoader)         #PDF
    docx_loader = Document_loader(document_loader_class=Docx2txtLoader)     #DOCX
    txt_loader = Document_loader(document_loader_class=TextLoader)          #TXT
    html_loader = Document_loader(document_loader_class=BSHTMLLoader)       #HTML

    # Dictionaries
        # Contain all loaded documents
    # PDF, DOCX, TXT
    # HTML
    # {filename (str) : list[Document], ...}
    pdf_docs = pdf_loader.load_document(files=pdf_files)
    docx_docs = docx_loader.load_document(files=docx_files)
    txt_docs = txt_loader.load_document(files=txt_files)
    html_docs = html_loader.load_document(files=html_files, open_encoding = "utf-8")

    # Merged dictionary
    merged_dict = {**pdf_docs, **docx_docs, **txt_docs, **html_docs}

    return merged_dict

# Pretty print to see the load result to test
def pretty_print(docs_dict : dict):

    # Loop over all Document objects in the dictionary
    for _, documents in docs_dict.items():
        for document in documents:
            source = document.metadata['source']        # File location
            # page = document.metadata['page']            # No. Page
            content = document.page_content             # Actual text content
            if len(content) > 40:
                content = content[:40]
            pagebreak = "-" * 40
            print(f"Document {source}:\n\nPage Content:\n{content}\n\n{pagebreak}\n")

if __name__ == "__main__":

    # All uploaded documents are stored in Loaded_Files folder.
    document_folder_path = "../Loaded_Files"

    # Get the list of all files and directories
    files = os.listdir(document_folder_path)

    # dict
    # {extenstion(str) : [filename (str)]}
    # e.g) {"pdf" : [document, document1, document2], ...}
    files_by_filetype = file_type_filter(files)

    all_file_docs_dict = load_all_files(files_by_filetype)

    pretty_print(all_file_docs_dict)
