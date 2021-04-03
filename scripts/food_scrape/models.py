class WikiCategory:
    ''' An object for storing food categories scraped from Wikipedia'''

    count = 0
    _id = None

    def __init__(self, name, description, wiki_url = None, foods = None, child_categories=None):
        WikiCategory.count += 1
        self.name = name
        self.description = description
        self.wiki_url = wiki_url
        self.foods = foods
        self.child_categories = child_categories
        print(self)

    def __str__(self):
        return f'''
    {WikiCategory.count}) {self.name}
    _id: {self._id}
    Description: {self.description[:40] if self.description else ''}...
    Wikipedia: {self.wiki_url[:42] if self.wiki_url else ''}...
    Food Count: {len(self.foods)}
    ------------------------
    '''

    def insert_cmd(self, parent_category_id=None):
        # creates an SQL insert command
        return (
            "INSERT INTO wiki_category VALUES(NULL, ?, ?, ?, ?)",
            (self.name, self.description, self.wiki_url, parent_category_id)
        )

    def update_id(self, _id):
        self._id = _id

class WikiFood:
    ''' An object for storing food metadata scraped from Wikipedia'''
    count = 0
    _id = None

    def __init__(self, name, description, image_src, wiki_url):
        WikiFood.count += 1
        self.name = name
        self.description = description
        self.image_src = image_src
        self.wiki_url = wiki_url
        print(self)

    def __str__(self):
        return f'''
    {WikiFood.count}) {self.name}
    Description: {self.description[:40] if self.description else ''}...
    src: {self.image_src[:48] if self.image_src else ''}...
    Wikipedia: {self.wiki_url[:42]if self.wiki_url else ''}...
    ------------------------
    '''

    def insert_cmd(self):
        # cretes an SQL insert command
        return (
            "INSERT INTO wiki_food VALUES(NULL, ?, ?, ?, ?)",
            (self.name, self.description, self.wiki_url, self.image_src)
        )

    def update_id(self, _id):
        self._id = _id
