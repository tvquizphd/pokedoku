from urllib.parse import urlparse
import requests
import logging
import random
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

def random_dex(tried, three, two, one, ndex):
    new_3grams = list(set(three) - tried)
    new_2grams = list(set(two) - tried)
    new_1grams = list(set(one) - tried)
    # Try matching dex numbers
    if len(new_3grams):
        return random.choice(new_3grams)
    elif len(new_2grams):
        return random.choice(new_2grams)
    elif len(new_1grams):
        return random.choice(new_1grams)

    # Resort to random dex numbers
    rand = random.randint(1, ndex + 1)
    while rand in tried:
        rand = random.randint(1, ndex + 1)
    return rand

def quality(n, count, offset):
    is_first = offset == 0
    priority = [1000, 100, 1]
    values = [is_first, n, count]
    ranking = zip(priority, values)
    return sum([p*v for p,v in ranking])

# thresh based on tries and remaining
def to_thresh(found_some, tried_some, at_start):
    if at_start: return 2
    if not found_some and tried_some: return 2
    if found_some and not tried_some: return 4
    if found_some and tried_some: return 3
    return 3

def close_enough(
    guess, max_tries, min_out, n_tried, n_found, offset, n
):
    found_some = n_found > min_out/2
    tried_some = n_tried > max_tries/2
    at_start = offset == 0
    thresh = to_thresh(
        found_some, tried_some, at_start
    )
    matched = n >= min(len(guess), thresh)
    return (matched, thresh)

def str_dist(guess, target):
    def ngrams(s,n):
        for start in range(0, len(s) - n + 1):
            yield s[start:start+n]

    found = (0, 0, 0)

    for n in [2,3,4,5,6]:
        ngrams_guess = set(ngrams(guess, n))
        ngrams_target = set(ngrams(target, n))
        union = ngrams_guess & ngrams_target
        if len(union) == 0: continue
        offset = min(
            target.index(chars) for chars in union
        )
        found = (n, len(union), offset)

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

def to_ngrams(dex_dict):
    three_grams = dict()
    for dexn,name in dex_dict.items():
        dex_list = three_grams.get(name[:3], [])
        three_grams[name[:3]] = dex_list + [dexn]

    two_grams = dict()
    one_grams = dict()
    for k, v in three_grams.items():
        two_list = two_grams.get(k[:2], [])
        one_list = one_grams.get(k[:1], [])
        two_grams[k[:2]] = two_list + v
        one_grams[k[:1]] = one_list + v

    return (three_grams, two_grams, one_grams)

def parse_generations(games):
    gen_dict = dict()
    all_gen_ids = set([
       game.generation for game in games.values() 
    ])
    gen_dexes = {
        gen: [
            game for (gid, game) in games.items()
            if gen == game.generation
        ]
        for gen in list(all_gen_ids)
    }
    return gen_dexes


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
        (three_grams, two_grams, one_grams) = to_ngrams(
            config.dex_dict
        )
        self.gen_dict = parse_generations(
            config.game_dict
        )
        self.three_grams = three_grams
        self.two_grams = two_grams
        self.one_grams = one_grams

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

        guess = raw_guess.lower()

        if len(guess) < 2:
            return []

        out = []
        tried = set()

        log_tracking = (0, 0)
        # Only try few mon
        max_tries = 5
        min_out = 3

        # Sample pokemon that meet threshhold
        while len(tried) < max_tries and len(out) < min_out:
            three = self.three_grams.get(guess[:3], [])
            two = self.two_grams.get(guess[:2], [])
            one = self.one_grams.get(guess[:1], [])
            ndex = len(self.config.dex_dict)
            dexn = random_dex(tried, three, two, one, ndex)
            # Search for pokemon if not tried
            if dexn in tried: continue
            root = self.config.api_url
            pkmn = get_api(root, f'pokemon-species/{dexn}/', True)
            if pkmn is None:
                continue
            # Modify threshhold based on results
            (n, count, offset) = str_dist(guess, pkmn['name'])
            # Measure similarity in pokemon names
            (matched, thresh) = close_enough(
                guess, max_tries, min_out, len(tried), len(out), offset, n 
            )
            # Logging
            remaining = min_out - len(out)
            next_tracking = (thresh, remaining)
            if (next_tracking != log_tracking):
                log_tracking = next_tracking
                print(
                    f'Seeking {thresh}-gram matches for {remaining} pkmn'
                )
            if matched:
                out.append((pkmn, n, count, offset))
            tried.add(dexn)

        # Unfetched 2-grams (includes 3-grams)
        two = self.two_grams.get(guess[:2], [])
        unfetched_2grams = list(set(two) - tried)
        
        # Return with less information
        for dexn in unfetched_2grams:
            name = self.config.dex_dict.get(dexn, None)
            if name is None: continue
            pkmn = { 'name': name, 'id': dexn }
            (n, count, offset) = str_dist(guess, pkmn['name'])
            # Assume that unmatched 2-grams are close enough
            out.append((pkmn, n, count, offset))

        # Sort by match quality 
        out_pkmn = [
            x[0] for x in sorted(
                out, reverse=True, key=lambda x: quality(*x[1:])
            )
        ]

        return [format_pkmn(p) for p in out_pkmn]


def to_service(config):
    return Service(config)
