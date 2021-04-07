

WIKI_BASE = 'https://en.wikipedia.org'
# This pages houses (by type) all Wikipedia Pages to be scraped
# Overarching Page reference: https://en.wikipedia.org/wiki/Lists_of_foods

PAGES_TO_SCRAPE = {
    # for pages with several <table>s, each being a category
    'table_categories': [
        # tuple[2] is the column index of the food
        ('Fruit', '/wiki/List_of_culinary_fruits', 1),
        ('Vegitables', '/wiki/List_of_vegetables', 1),
        ('Pasta', '/wiki/List_of_pasta', 2),
    ],
    # for pages with several <ul>s, each being a category
    'ul_categories': [
        ('Nuts', '/wiki/List_of_culinary_nuts'),
        ('Breads', '/wiki/List_of_American_breads'),
        ('Condiments', '/wiki/List_of_condiments'),
        ('Spreads', '/wiki/List_of_spreads'),
        ('Common Dips', '/wiki/Dipping_sauce'),
        ('Sauces', '/wiki/List_of_sauces'),
        ('Mushrooms', '/wiki/Edible_mushroom'),
        ('Breakfast', 'wiki/List_of_breakfast_foods'),
    ],
    # for pages with 1 <table> of 1 category
    'single_table_category':  [
        ('Breads', '/wiki/List_of_breads'),
        ('Fried Dough', '/wiki/List_of_fried_dough_foods'),
        ('Dairy', '/wiki/List_of_dairy_products'),
        ('Cheese', '/wiki/List_of_cheeses'),
        ('Cakes', '/wiki/List_of_cakes'),
        ('Pastries', '/wiki/List_of_pastries'),
    ],
    # manually contructed hierarchy of cargoriesa and foods
    'manual_categories': {
        # 'Meat': {},
        'Poultry': {
            'page_url': '/wiki/Poultry',
            'foods': [
                '/wiki/Egg_as_food',
                '/wiki/Chicken_as_food',
                '/wiki/Duck_as_food',
                '/wiki/Turkey_as_food',
            ]
        },
        'Livestock': {
            'page_url': '/wiki/Livestock',
            'foods': [
                '/wiki/Beef',
                '/wiki/Lamb_and_mutton',
                '/wiki/Pork',
                '/wiki/Veal',
            ]
        },
        'Game': {
            'page_url': '/wiki/Game_(hunting)',
            'foods': ['/wiki/Venison']
        },
        'Fish': {
            'page_url': '/wiki/Fish_as_food',
            'foods': [
                '/wiki/Anchovies_as_food',
                '/wiki/Catfish',
                '/wiki/Halibut',
                '/wiki/Mackerel_as_food',
                '/wiki/Pollock',
                '/wiki/Salmon_as_food',
                '/wiki/Sardines_as_food',
                '/wiki/Tilapia',
                '/wiki/Trout',
                '/wiki/Tuna',
                '/wiki/Walleye'
            ]
        },
        'Seafood': {
            'page_url': '/wiki/Seafood',
            'foods': [
                '/wiki/Squid_as_food',
                '/wiki/Clams',
                '/wiki/Lobster',
                '/wiki/Crayfish_as_food',
                '/wiki/Oyster',
                '/wiki/Mussel',
                '/wiki/Octopus_as_food',
                '/wiki/Scallop',
                '/wiki/Shrimp_and_prawn_as_food',
                '/wiki/Sea_urchin'
            ]
        },
    },
    'dishes': [
        ('Egg Dishes', '/wiki/List_of_egg_dishes'),
        ('Cheese Dishes', '/wiki/List_of_cheese_dishes'),
        ('Meat Dishes', '/wiki/List_of_meat_dishes'),
        ('Fish Dishes', '/wiki/List_of_fish_dishes'),
        ('Seafood Dishes', '/wiki/List_of_seafood_dishes'),
        ('Noodle Dishes', '/wiki/List_of_noodle_dishes'),
        ('Desserts', '/wiki/List_of_desserts'),
        ('Stews', '/wiki/List_of_stews'),
        ('Soups', '/wiki/List_of_soups'),
        ('Snack Foods', '/wiki/List_of_snack_foods'),
        ('Sandwiches', '/wiki/List_of_sandwiches'),
        ('Salads', '/wiki/List_of_salads'),
        ('Tarts & Flans', '/wiki/List_of_pies,_tarts_and_flans'),
        ('Noodles', '/wiki/List_of_noodles'),
        ('Fermented Foods', '/wiki/List_of_fermented_foods'),
        ('Food Pastes', '/wiki/List_of_food_pastes'),
        ('Porridges', '/wiki/List_of_porridges'),
        ('Dumplings', '/wiki/List_of_dumplings'),
        ("Hors D'oeuvre", '/wiki/List_of_hors_d%27oeuvre'),
        ('Rice Cakes', '/wiki/Rice_cake'),
    ]
}
