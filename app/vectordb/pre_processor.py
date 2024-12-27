import logging

def replace_t_with_space(list_of_documents):
    """
    Replaces all tab characters ('\t') with spaces in the page content of each document.

    Args:
        list_of_documents: A list of document objects, each with a 'page_content' attribute.

    Returns:
        The modified list of documents with tab characters replaced by spaces.
    """

    for doc in list_of_documents:
        doc.page_content = doc.page_content.replace('\t', ' ')  # Replace tabs with spaces
    return list_of_documents

def replace_n_with_space(list_of_documents):
    """
    Replaces all tab characters ('\n') with spaces in the page content of each document.

    Args:
        list_of_documents: A list of document objects, each with a 'page_content' attribute.

    Returns:
        The modified list of documents with tab characters replaced by spaces.
    """
    for doc in list_of_documents:
        doc.page_content = doc.page_content.replace('\n', ' ')  # Replace tabs with spaces
    return list_of_documents

def clean_documents(list_of_documents):
    """
    Cleans the list_of_documents by executing clean-up process
    """
    try: 
        cleaned_list_of_documents = replace_t_with_space(list_of_documents=list_of_documents)
        cleaned_list_of_documents = replace_n_with_space(list_of_documents=cleaned_list_of_documents)
        return cleaned_list_of_documents
    except Exception as err:
        logging.info(f'Error in cleaning up the documents. Moving forward without cleanups. Error {err}')
        return list_of_documents