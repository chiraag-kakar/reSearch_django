from rest_framework.decorators import api_view
from rest_framework.response import Response
import re


class Found:
    """
    Represents the appearance of a term in a given document, along with the
    frequency of appearances in the same one.
    """
    def _init_(self, docId, frequency):
        self.docId = docId
        self.frequency = frequency  

    def _repr_(self):
        """
        String representation of the Appearance object
        """
        return str(self._dict_)


class Database:
    """
    In memory database representing the already indexed documents.
    """
    def _init_(self):
        self.db = dict()

    def _repr_(self):
        """
        String representation of the Database object
        """
        return str(self._dict_)

    def get(self, id):
        return self.db.get(id, None)

    def add(self, document):
        """
        Adds a document to the DB.
        """
        return self.db.update({document['id']: document})

    def remove(self, document):
        """
        Removes document from DB.
        """
        return self.db.pop(document['id'], None)


class Invert:
    """
    Inverted Index class.
    """
    def _init_(self, db):
        self.index = dict()
        self.db = db

    def _repr_(self):
        """
        String representation of the Database object
        """
        return str(self.index)   

    def index_document(self, document):
        """
        Process a given document, save it to the DB and update the index.
        """
        # Remove punctuation from the text.
        clean_text = re.sub(r'[^\w\s]', '', document['text'])
        terms = re.split(' |\n', clean_text)
        appearances_dict = dict() 
        # Dictionary with each term and the frequency it appears in the text.
        for term in terms:
            term = term.lower()
            term_frequency = appearances_dict[term].frequency if term in appearances_dict else 0
            appearances_dict[term] = Found(document['id'], term_frequency + 1)

        # Update the inverted index
        update_dict = {key: [appearance]
                       if key not in self.index
                       else self.index[key] + [appearance]
                       for (key, appearance) in appearances_dict.items()}
        self.index.update(update_dict)        
        # Add the document into the database
        self.db.add(document)        
        return document

    def lookup_query(self, query):
        """
        Returns the dictionary of terms with their correspondent Appearances. 
        This is a very naive search since it will just split the terms and show
        the documents where they appear.
        """
        if query in self.index:
            result = []
            count = 0
            for x in self.index[query]:
                count += 1
                result.append([x.frequency, x.docId])
                if count == 10:
                    break
            return sorted(result, reverse=True)
        else:
            return []


#global variables used throughout the program
db = Database()
index = Invert(db)
uid = 0


@api_view(['GET', 'POST'])
def indexes(request):
    global uid, db, index
    uid = 0
    db = Database()
    index = Invert(db)
    return Response({"info": "All the indexes has been cleared."})


@api_view(['GET', 'POST'])
def indexing_document(request):
    global uid, index
    try:
        docs = request.data['data']
        docs = docs.split('\n\n')
        print(docs)
        for par in docs:
            doc = {
                'id': uid,
                'text': par
            }
            index.index_document(doc)
            uid += 1
    except Exception as e:
        return Response({"status": 0})
    return Response({"status": 1})


@api_view(['GET', 'POST'])
def search(request):
    global index, db
    result = index.lookup_query(request.data['word'].lower())
    print(result)
    for r in result:
        r.append(db.db[r[1]]['text'])
    return Response({"docs": result})

@api_view(['GET'])
def retrieve_doc(request, id):
    global db
    if id not in db.db.keys():
        return Response({"text": ""})
    print(db.db[id])
    return Response({"text": db.db[id]['text']})

@api_view(['GET'])
def retrieve_all(request):
    global db
    res = [[db.db[x]['id'], db.db[x]['text']] for x in db.db.keys()]
    return Response({"docs": res})