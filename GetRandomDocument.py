# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 13:40:39 2024

@author: gowtham.balachan
"""
class RandomDocumentRetriever:
    def __init__(self, client, db_name, collection_name):
        self.client = client
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_random_document(self):
        random_documents = self.collection.aggregate([
            {"$sample": {"size": 1}}
        ])
        # Convert the cursor to a list
        random_documents_list = list(random_documents)
        # Check if the list is empty
        if random_documents_list:
            # Extract the random document from the list
            random_document = random_documents_list[0]
            return random_document
        else:
            # If the list is empty, return None
            return None
