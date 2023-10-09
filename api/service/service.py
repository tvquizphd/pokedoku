from urllib.parse import urlparse
import requests
import logging
import random
import json
import time

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
    split_url = urlparse(v['url']).path.split('/')
    pid = [s for s in split_url if s][-1]
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


class Service():
    def __init__(self, config):
        self.config = config

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

    def get_api(self, endpoint, unsure=False):
        target = self.config.api_url + endpoint
        headers = {'content-type': 'application/json'}
        try:
            r = requests.get(target, headers=headers)
            return r.json() 
        except Exception as e:
            if not unsure:
                logging.critical(e, exc_info=True)
            return None

    def run_test(self, identifier, fns):
        pkmn = self.get_api(f'pokemon/{identifier}/', True)
        types = [t['type']['name'] for t in pkmn.get('types', [])]
        # All conditions met within all types
        return { 'ok': all([fn(s,types) for (s,fn) in fns]) }

    def get_forms(self, dexn):
        pkmn = self.get_api(f'pokemon-species/{dexn}/', True)
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
            three = self.config.three_grams.get(guess[:3], [])
            two = self.config.two_grams.get(guess[:2], [])
            one = self.config.one_grams.get(guess[:1], [])
            dexn = random_dex(tried, three, two, one, self.config.ndex)
            # Search for pokemon if not tried
            if dexn in tried: continue
            pkmn = self.get_api(f'pokemon-species/{dexn}/', True)
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
        two = self.config.two_grams.get(guess[:2], [])
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
