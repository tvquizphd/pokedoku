from urllib.parse import urlparse
import requests
import logging
import json
import time

def get_api(root, endpoint, unsure=False):
    headers = {'content-type': 'application/json'}
    try:
        r = requests.get(root + endpoint, headers=headers)
        return r.json() 
    except Exception as e:
        if not unsure:
            logging.critical(e, exc_info=True)
        return None

def get_pages(root, endpoint, offset=None):
    off = f"&offset={offset}" if offset else ""
    page_list = get_api(root, f'/{endpoint}/?limit=1000{off}')
    while page_list["next"] is not None:
        next_list = get_api(
            root, f'/{endpoint}/?{urlparse(page_list["next"]).query}'
        )
        page_list["results"].append(next_list["results"])
        page_list["next"] = next_list["next"]

    return page_list

def id_from_url(url):
    split_url = urlparse(url).path.split('/')
    return int([s for s in split_url if s][-1])

def quality(offset, n, count):
    is_first = offset == 0
    scales = [
        [0, 0], [10*2**n, n]
    ][+(n>0)]
    values = [is_first, count]
    ranking = zip(scales, values)
    return sum([p*v for p,v in ranking])

def to_ngrams(s,n):
    for start in range(0, len(s) - n + 1):
        yield s[start:start+n]

def to_ngram_union(guess, target, n):
    ngrams_guess = set(to_ngrams(guess, n))
    ngrams_target = set(to_ngrams(target, n))
    union = ngrams_guess & ngrams_target
    offset = 0 if not len(union) else min(
        target.index(un) for un in union
    )
    return (union, offset)

def fast_dist(guess, target):

    found = (0, 0, 0)

    for n in [1,2,3]:
        (union, offset) = to_ngram_union(guess, target, n)
        if len(union) == 0: continue
        found = (offset, n, len(union))

    return found 

def str_dist(guess, target):

    found = (0, 0, 0)

    for n in [1,2,3,4,5,6]:
        (union, offset) = to_ngram_union(guess, target, n)
        if len(union) == 0: continue
        found = (offset, n, len(union))

    return found 

def format_form(v):
    pid = id_from_url(v['url'])
    form = {
        'name': v['name'], 'id': pid,
        'percentage': 42,
    }
    return { 'form': form }

def format_pkmn(p):
    varieties = [v['pokemon'] for v in p.get('varieties', [])]
    forms = [format_form(v)['form'] for v in varieties]
    pokemon = {
        'forms': forms,
        'name': p['name'],
        'dex': p['id']
    }
    return { 'pokemon': pokemon }

def clamp(v, low, high):
    return min(high, max(low, v))

class RegionalDex():

    def __init__(self, gen_id, game, did, dex):
        self.generation = gen_id;
        self.game = game.name;
        self.game_id = game.id;
        self.dex_id = did;
        self.dex = dex

    def __repr__(self):
        return f'''\
Generation {self.generation}; \
Game {self.game_id}: {self.game}; \
Dex {self.dex_id}: {self.dex}'''

class Service():
    def __init__(self, config):
        self.config = config
        self.dex_dict = config.dex_dict
        self.gen_dict = config.gen_dict
        self.three_grams = config.three_grams
        self.two_grams = config.two_grams

    @property
    def all_regions(self):
        all_region_names = list(set(
            region for games in self.gen_dict.values()
            for game in games
            for region in game.regions.values()
        ))
        return [{'region': r} for r in all_region_names]

    async def delete_api(self, endpoint):
        #target = self.config.api_url + endpoint
        #session.delete(target)
        pass

    async def put_api(self, endpoint, data):
        #target = self.config.api_url + endpoint
        headers = {'content-type': 'application/json'}
        #session.put(target, json=data, headers=headers)
        pass

    async def post_api(self, endpoint, data):
        #target = self.config.api_url + endpoint
        headers = {'content-type': 'application/json'}
        #session.post(target, json=data, headers=headers)
        pass

    @staticmethod 
    def update_games(root, games):
        off = max(games.keys()) if len(games) else 0
        ver_list = get_pages(root, 'version-group', off)
        ver_dict = { **games }
        for ver_info in ver_list["results"]:
            ver_id = id_from_url(ver_info['url'])
            ver = get_api(root, f'/version-group/{ver_id}')
            ver_dict[ver_id] = {
                "name": ver["name"],
                "generation": id_from_url(ver["generation"]["url"]),
                "dexes": {
                    id_from_url(dex["url"]): dex["name"]
                    for dex in ver["pokedexes"]
                },
                "regions": {
                    id_from_url(region["url"]): region["name"]
                    for region in ver["regions"]
                }
            }
            print('Adding', ver['name'])
        return { k: {"id": k, **v} for (k,v) in ver_dict.items() }

    def form_to_species(self, pkmn):
        root = self.config.api_url
        species_id = id_from_url(pkmn["species"]["url"])
        return get_api(root, f'pokemon-species/{species_id}/')

    def to_regional_dex_list(self, pkmn):
        species = self.form_to_species(pkmn)
        gen_id = id_from_url(species["generation"]["url"])
        gen_list = self.gen_dict[gen_id]
        dex_list = [
            RegionalDex(gen_id, game, did, dex)
            for game in gen_list
            for (did, dex) in game.dexes.items()
        ]
        sid = species["id"]
        return (sid, sorted(dex_list, key=lambda d: d.game_id))

    def to_first_region(self, pkmn, sid, dex_list):
        all_regions = set([r['region'] for r in self.all_regions])
        split_name = set(pkmn['name'].split('-'))
        pkmn_name_regions = split_name & all_regions
        # Use any region found in name
        if len(pkmn_name_regions):
            return pkmn_name_regions.pop()
        # Search pokedex if no region in name
        root = self.config.api_url
        for regional_dex in dex_list:
            did = regional_dex.dex_id
            dex = get_api(root, f'pokedex/{did}/')
            dex_species = [
                id_from_url(d['pokemon_species']['url'])
                for d in dex['pokemon_entries']
            ]
            if sid in dex_species:
                return dex['region']['name']

    def run_test(self, identifier, fns):
        root = self.config.api_url
        pkmn = get_api(root, f'pokemon/{identifier}/')
        # Find all dexes for all games in generation
        (sid, dex_list) = self.to_regional_dex_list(pkmn)
        # Find first region that contains pokemon
        first_region = self.to_first_region(pkmn, sid, dex_list)
        
        # All conditions met within all types
        pkmn_types = pkmn.get('types', [])
        types = [t['type']['name'] for t in pkmn_types]
        valid = types + [first_region]
        ok = all([fn(s,valid) for (s,fn) in fns])
        return { 'ok': ok }

    def get_forms(self, dexn):
        root = self.config.api_url
        pkmn = get_api(root, f'pokemon-species/{dexn}/', True)
        varieties = [v['pokemon'] for v in pkmn.get('varieties', [])]
        return [format_form(v) for v in varieties]

    def get_matches(self, raw_guess):

        start_request = time.time()
        guess = raw_guess.lower()

        min_chars = 2
        n_chars = len(guess)
        bonus_chars = n_chars - min_chars
        if bonus_chars < 0:
            return []

        # Example trigrams: cha, mag, dra, iro
        two = self.two_grams.get(guess[:2], [])
        three = self.three_grams.get(guess[:3], [])

        # Sort two-gram pokemon by match quality
        favored = sorted(
            two, reverse=True,
            key=lambda k: quality(*str_dist(guess, self.dex_dict[k]))
        )
        # List of all other pokemon
        ndex = len(self.dex_dict)
        full_dex = set(range(1, ndex + 1))
        etc = list(full_dex - set(two))
        # Sort other pokemon less exactly
        other = sorted(
            etc, reverse=True,
            key=lambda k: quality(*fast_dist(guess, self.dex_dict[k]))
        )

        out = []
        ntri = len(three)
        # Increase results by string length
        defaults = (2, clamp(ntri, 2, 12))
        (n_fetches, n_partial) = ({
            0: (1, 2),
            1: (1, 4),
            2: (2, clamp(ntri, 1, 8)),
        }).get(bonus_chars, defaults)

        root = self.config.api_url
        # Fetch some favored pokemon
        for _ in favored[:n_fetches]:
            dexn = favored[0]
            # Search for pokemon if not tried
            pkmn = get_api(root, f'pokemon-species/{dexn}/', True)
            if pkmn is None: continue
            favored = favored[1:]
            out.append(pkmn)

        main_out = len(out)
        print(f'Fully added {main_out} matches for {guess}')

        # Pad out results with other matches
        for dexn in (favored + other)[:n_partial]:
            name = self.dex_dict[dexn]
            pkmn = { 'name': name, 'id': dexn }
            out.append(pkmn)
        
        print(f'Partially added {n_partial} others for {guess}')

        end_request = time.time()
        print(end_request - start_request)

        return [format_pkmn(p) for p in out]


def to_service(config):
    return Service(config)
