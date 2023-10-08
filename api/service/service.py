import requests
import logging
import random
import json

THREE_GRAMS = {
    'bul': [1],
    'ivy': [2],
    'ven': [3, 48, 49, 543],
    'cha': [4, 5, 6, 113, 441, 609, 737, 935],
    'squ': [7, 931],
    'war': [8],
    'bla': [9, 257, 806],
    'cat': [10],
    'met': [11, 375, 376],
    'but': [12],
    'wee': [13, 70, 110],
    'kak': [14],
    'bee': [15],
    'pid': [16, 17, 18, 519],
    'rat': [19, 20],
    'spe': [21, 665, 897],
    'fea': [22],
    'eka': [23],
    'arb': [24, 930],
    'pik': [25, 731],
    'rai': [26, 243],
    'san': [27, 28, 551, 769, 844, 989],
    'nid': [29, 30, 31, 32, 33, 34],
    'cle': [35, 36, 173],
    'vul': [37, 629],
    'nin': [38, 290, 291],
    'jig': [39],
    'wig': [40, 960],
    'zub': [41],
    'gol': [42, 55, 76, 118, 622, 623, 768],
    'odd': [43],
    'glo': [44],
    'vil': [45],
    'par': [46, 47],
    'dig': [50, 660],
    'dug': [51],
    'meo': [52, 678, 908],
    'per': [53, 863],
    'psy': [54],
    'man': [56, 226, 310, 458, 490, 630],
    'pri': [57, 394, 730],
    'gro': [58, 253, 383, 388, 810],
    'arc': [59, 493, 566, 567, 881, 883, 997],
    'pol': [60, 61, 62, 186, 855, 1012],
    'abr': [63],
    'kad': [64],
    'ala': [65],
    'mac': [66, 67, 68],
    'bel': [69, 182, 374, 939],
    'vic': [71, 494],
    'ten': [72, 73],
    'geo': [74],
    'gra': [75, 210, 853, 945],
    'pon': [77],
    'rap': [78],
    'slo': [79, 80, 199],
    'mag': [81, 82, 126, 129, 219, 240, 462, 467, 801],
    'far': [83, 981],
    'dod': [84, 85],
    'see': [86, 273],
    'dew': [87, 502, 751],
    'gri': [88, 861],
    'muk': [89],
    'she': [90, 292, 372, 422, 616],
    'clo': [91, 852, 980],
    'gas': [92, 423],
    'hau': [93],
    'gen': [94, 649],
    'oni': [95],
    'dro': [96],
    'hyp': [97],
    'kra': [98],
    'kin': [99, 230, 983],
    'vol': [100, 313, 637, 721],
    'ele': [101, 125, 239, 309, 466],
    'exe': [102, 103],
    'cub': [104, 613],
    'mar': [105, 179, 183, 259, 556, 747, 802],
    'hit': [106, 107, 237],
    'lic': [108, 463],
    'kof': [109],
    'rhy': [111, 112, 464],
    'tan': [114, 465, 924],
    'kan': [115],
    'hor': [116],
    'sea': [117, 119, 364],
    'sta': [120, 121, 234, 396, 397, 398, 805],
    'mr-': [122, 866],
    'scy': [123],
    'jyn': [124],
    'pin': [127, 204, 871],
    'tau': [128],
    'gya': [130],
    'lap': [131],
    'dit': [132],
    'eev': [133],
    'vap': [134],
    'jol': [135, 595],
    'fla': [136, 180, 669, 841, 973],
    'por': [137, 233, 474],
    'oma': [138, 139],
    'kab': [140, 141],
    'aer': [142],
    'sno': [143, 361, 459, 872],
    'art': [144],
    'zap': [145],
    'mol': [146],
    'dra': [147, 148, 149, 452, 691, 780, 880, 882, 886, 887],
    'mew': [150, 151],
    'chi': [152, 170, 358, 390, 433, 1002, 1004],
    'bay': [153],
    'meg': [154],
    'cyn': [155],
    'qui': [156, 651],
    'typ': [157, 772],
    'tot': [158],
    'cro': [159, 169, 453, 910],
    'fer': [160, 597, 598],
    'sen': [161],
    'fur': [162, 676],
    'hoo': [163, 720],
    'noc': [164],
    'led': [165, 166],
    'spi': [167, 327, 442, 918],
    'ari': [168],
    'lan': [171, 645],
    'pic': [172],
    'igg': [174],
    'tog': [175, 176, 468, 777],
    'nat': [177],
    'xat': [178],
    'amp': [181],
    'azu': [184, 298],
    'sud': [185],
    'hop': [187],
    'ski': [188, 300, 672],
    'jum': [189],
    'aip': [190],
    'sun': [191, 192],
    'yan': [193, 469],
    'woo': [194, 527, 831],
    'qua': [195, 912, 913, 914],
    'esp': [196, 677, 956],
    'umb': [197],
    'mur': [198],
    'mis': [200, 429],
    'uno': [201],
    'wob': [202],
    'gir': [203, 487],
    'for': [205],
    'dun': [206],
    'gli': [207, 472, 969, 970],
    'ste': [208, 762],
    'snu': [209],
    'qwi': [211],
    'sci': [212],
    'shu': [213, 353],
    'her': [214, 507],
    'sne': [215, 903],
    'ted': [216],
    'urs': [217, 892, 901],
    'slu': [218, 685],
    'swi': [220, 684],
    'pil': [221],
    'cor': [222, 341, 822, 823],
    'rem': [223],
    'oct': [224],
    'del': [225, 301, 655],
    'ska': [227],
    'hou': [228, 229, 972],
    'pha': [231, 708],
    'don': [232, 977],
    'sme': [235],
    'tyr': [236, 248, 696, 697],
    'smo': [238, 928],
    'mil': [241, 350, 868],
    'bli': [242, 522, 824],
    'ent': [244],
    'sui': [245],
    'lar': [246, 636],
    'pup': [247],
    'lug': [249],
    'ho-': [250],
    'cel': [251, 797],
    'tre': [252, 709],
    'sce': [254],
    'tor': [255, 324, 389, 641, 726],
    'com': [256, 415, 764],
    'mud': [258, 749, 750],
    'swa': [260, 317, 333, 541, 581],
    'poo': [261],
    'mig': [262],
    'zig': [263],
    'lin': [264],
    'wur': [265],
    'sil': [266, 773, 843],
    'bea': [267, 614],
    'cas': [268, 351],
    'dus': [269, 355, 356, 477],
    'lot': [270],
    'lom': [271],
    'lud': [272],
    'nuz': [274],
    'shi': [275, 403, 410, 756],
    'tai': [276],
    'swe': [277],
    'win': [278],
    'pel': [279],
    'ral': [280],
    'kir': [281],
    'gar': [282, 445, 569, 934],
    'sur': [283],
    'mas': [284, 942],
    'shr': [285, 944],
    'bre': [286],
    'sla': [287, 289],
    'vig': [288],
    'whi': [293, 340, 544, 547],
    'lou': [294],
    'exp': [295],
    'mak': [296],
    'har': [297],
    'nos': [299],
    'sab': [302],
    'maw': [303],
    'aro': [304, 683],
    'lai': [305],
    'agg': [306],
    'med': [307, 308],
    'plu': [311],
    'min': [312, 572, 774],
    'ill': [314],
    'ros': [315, 407],
    'gul': [316],
    'car': [318, 455, 565, 703, 838],
    'sha': [319, 492],
    'wai': [320, 321],
    'num': [322],
    'cam': [323],
    'spo': [325],
    'gru': [326, 736],
    'tra': [328, 520],
    'vib': [329],
    'fly': [330],
    'cac': [331, 332],
    'alt': [334],
    'zan': [335],
    'sev': [336],
    'lun': [337, 792],
    'sol': [338, 577, 791],
    'bar': [339, 689, 847],
    'cra': [342, 346, 408, 739, 740, 845],
    'bal': [343],
    'cla': [344, 366, 692, 693],
    'lil': [345, 506, 549],
    'ano': [347],
    'arm': [348, 936],
    'fee': [349],
    'kec': [352],
    'ban': [354],
    'tro': [357],
    'abs': [359],
    'wyn': [360],
    'gla': [362, 431, 471, 896],
    'sph': [363],
    'wal': [365, 1009],
    'hun': [367],
    'gor': [368],
    'rel': [369, 953],
    'luv': [370],
    'bag': [371],
    'sal': [373, 757, 758],
    'reg': [377, 378, 379, 486, 894, 895],
    'lat': [380, 381],
    'kyo': [382],
    'ray': [384],
    'jir': [385],
    'deo': [386],
    'tur': [387, 776],
    'mon': [391],
    'inf': [392],
    'pip': [393],
    'emp': [395],
    'bid': [399],
    'bib': [400],
    'kri': [401, 402],
    'lux': [404, 405],
    'bud': [406],
    'ram': [409],
    'bas': [411, 550, 902],
    'bur': [412],
    'wor': [413],
    'mot': [414],
    'ves': [416],
    'pac': [417],
    'bui': [418],
    'flo': [419, 670, 671, 907],
    'che': [420, 421, 650, 652, 833],
    'amb': [424],
    'dri': [425, 426, 529, 817],
    'bun': [427, 659],
    'lop': [428],
    'hon': [430, 679],
    'pur': [432, 509],
    'stu': [434, 618, 759],
    'sku': [435],
    'bro': [436, 437],
    'bon': [438],
    'mim': [439, 778],
    'hap': [440],
    'gib': [443],
    'gab': [444],
    'mun': [446, 517, 1015],
    'rio': [447],
    'luc': [448],
    'hip': [449, 450],
    'sko': [451],
    'tox': [454, 748, 848, 849],
    'fin': [456, 963],
    'lum': [457],
    'abo': [460],
    'wea': [461],
    'lea': [470, 542],
    'mam': [473],
    'gal': [475, 596],
    'pro': [476],
    'fro': [478, 656, 657, 873],
    'rot': [479],
    'uxi': [480],
    'mes': [481],
    'aze': [482],
    'dia': [483, 719],
    'pal': [484, 536, 770, 964],
    'hea': [485, 631],
    'cre': [488],
    'phi': [489],
    'dar': [491, 554, 555, 723],
    'sni': [495],
    'ser': [496, 497],
    'tep': [498],
    'pig': [499],
    'emb': [500],
    'osh': [501],
    'sam': [503],
    'pat': [504],
    'wat': [505, 940],
    'sto': [508, 874],
    'lie': [510],
    'pan': [511, 513, 515, 674, 675],
    'sim': [512, 514, 516],
    'mus': [518],
    'unf': [521],
    'zeb': [523],
    'rog': [524],
    'bol': [525, 836],
    'gig': [526],
    'swo': [528],
    'exc': [530],
    'aud': [531],
    'tim': [532],
    'gur': [533],
    'con': [534],
    'tym': [535],
    'sei': [537],
    'thr': [538],
    'saw': [539, 586],
    'sew': [540],
    'sco': [545, 813, 952],
    'cot': [546],
    'pet': [548],
    'kro': [552, 553],
    'dwe': [557],
    'cru': [558],
    'scr': [559, 560, 985],
    'sig': [561],
    'yam': [562, 835],
    'cof': [563],
    'tir': [564],
    'tru': [568, 732],
    'zor': [570, 571],
    'cin': [573, 815],
    'got': [574, 575, 576],
    'duo': [578],
    'reu': [579],
    'duc': [580],
    'van': [582, 583, 584],
    'dee': [585],
    'emo': [587],
    'kar': [588, 798],
    'esc': [589],
    'foo': [590],
    'amo': [591],
    'fri': [592, 996],
    'jel': [593],
    'alo': [594],
    'kli': [599, 601],
    'kla': [600, 950],
    'tyn': [602],
    'eel': [603, 604],
    'elg': [605],
    'beh': [606],
    'lit': [607, 667, 725],
    'lam': [608],
    'axe': [610],
    'fra': [611],
    'hax': [612],
    'cry': [615],
    'acc': [617],
    'mie': [619, 620],
    'dru': [621],
    'paw': [624, 921, 922, 923],
    'bis': [625],
    'bou': [626, 761],
    'ruf': [627],
    'bra': [628, 654, 946, 947],
    'dur': [632, 884],
    'dei': [633],
    'zwe': [634],
    'hyd': [635],
    'cob': [638],
    'ter': [639],
    'vir': [640],
    'thu': [642],
    'res': [643],
    'zek': [644],
    'kyu': [646],
    'kel': [647],
    'mel': [648, 808, 809],
    'fen': [653],
    'gre': [658, 820, 971, 984],
    'fle': [661, 662],
    'tal': [663],
    'sca': [664],
    'viv': [666],
    'pyr': [668],
    'gog': [673],
    'dou': [680],
    'aeg': [681],
    'spr': [682, 906],
    'ink': [686],
    'mal': [687],
    'bin': [688],
    'skr': [690],
    'hel': [694, 695],
    'ama': [698],
    'aur': [699],
    'syl': [700],
    'haw': [701],
    'ded': [702],
    'goo': [704, 706],
    'sli': [705, 988],
    'kle': [707, 900],
    'pum': [710],
    'gou': [711],
    'ber': [712],
    'ava': [713],
    'noi': [714, 715],
    'xer': [716],
    'yve': [717],
    'zyg': [718],
    'row': [722],
    'dec': [724],
    'inc': [727],
    'pop': [728],
    'bri': [729],
    'tou': [733],
    'yun': [734],
    'gum': [735],
    'vik': [738],
    'ori': [741],
    'cut': [742],
    'rib': [743],
    'roc': [744],
    'lyc': [745],
    'wis': [746],
    'ara': [752],
    'fom': [753],
    'lur': [754],
    'mor': [755, 860, 877],
    'bew': [760],
    'tsa': [763],
    'ora': [765],
    'pas': [766],
    'wim': [767],
    'pyu': [771],
    'kom': [775, 784],
    'bru': [779, 986],
    'dhe': [781],
    'jan': [782],
    'hak': [783],
    'tap': [785, 786, 787, 788],
    'cos': [789, 790],
    'nih': [793],
    'buz': [794],
    'phe': [795],
    'xur': [796],
    'guz': [799],
    'nec': [800],
    'poi': [803],
    'nag': [804],
    'zer': [807],
    'thw': [811],
    'ril': [812],
    'rab': [814, 954],
    'sob': [816],
    'int': [818],
    'skw': [819],
    'roo': [821],
    'dot': [825],
    'orb': [826],
    'nic': [827],
    'thi': [828],
    'gos': [829],
    'eld': [830],
    'dub': [832],
    'dre': [834, 885],
    'rol': [837],
    'coa': [839],
    'app': [840, 842],
    'arr': [846],
    'siz': [850],
    'cen': [851],
    'sin': [854, 1013],
    'hat': [856, 857, 858],
    'imp': [859],
    'obs': [862],
    'cur': [864],
    'sir': [865],
    'run': [867],
    'alc': [869],
    'fal': [870],
    'eis': [875],
    'ind': [876],
    'cuf': [878],
    'cop': [879],
    'zac': [888],
    'zam': [889],
    'ete': [890],
    'kub': [891],
    'zar': [893],
    'cal': [898],
    'wyr': [899],
    'ove': [904],
    'ena': [905],
    'fue': [909],
    'ske': [911],
    'lec': [915],
    'oin': [916],
    'tar': [917],
    'nym': [919],
    'lok': [920],
    'mau': [925],
    'fid': [926],
    'dac': [927],
    'dol': [929],
    'nac': [932, 933],
    'cer': [937],
    'tad': [938],
    'kil': [941],
    'mab': [943],
    'toe': [948, 949],
    'cap': [951],
    'fli': [955],
    'tin': [957, 958, 959, 1003],
    'wug': [961],
    'bom': [962],
    'var': [965],
    'rev': [966],
    'cyc': [967],
    'ort': [968],
    'cet': [974, 975],
    'vel': [976],
    'tat': [978],
    'ann': [979],
    'dud': [982],
    'flu': [987],
    'iro': [990, 991, 992, 993, 994, 995, 1006, 1010],
    'bax': [998],
    'gim': [999],
    'gho': [1000],
    'wo-': [1001],
    'roa': [1005],
    'kor': [1007],
    'mir': [1008],
    'dip': [1011],
    'oki': [1014],
    'fez': [1016],
    'oge': [1017]
}
TWO_GRAMS = dict()
ONE_GRAMS = dict()
for k, v in THREE_GRAMS.items():
    two_list = TWO_GRAMS.get(k[:2], [])
    one_list = ONE_GRAMS.get(k[:1], [])
    TWO_GRAMS[k[:2]] = two_list + v
    ONE_GRAMS[k[:1]] = one_list + v

def random_dex(tried, three, two, one, ndex):
    new_3grams = list(set(three) - tried)
    new_2grams = list(set(two) - tried)
    new_1grams = list(set(one) - tried)
    # Try matching dex numbers
    if len(new_3grams):
        print('from 3gram')
        return random.choice(new_3grams)
    elif len(new_2grams):
        print('from 2gram')
        return random.choice(new_2grams)
    elif len(new_1grams):
        print('from 1gram')
        return random.choice(new_1grams)

    print('from random')
    # Resort to random dex numbers
    rand = random.randint(1, ndex + 1)
    while rand in tried:
        rand = random.randint(1, ndex + 1)
    return rand

def quality(n, count, offset):
    return n * (count - offset)

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

def format_pkmn(p):
    pokemon = {
        'percentage': 99,
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

    def get_matches(self, raw_guess):

        guess = raw_guess.lower()

        if len(guess) < 2:
            return []

        out = []
        tried = set()

        log_tracking = (0, 0)
        # Only try few mon
        max_tries = 3
        min_out = 2

        # Sample pokemon that meet threshhold
        while len(tried) < max_tries and len(out) < min_out:
            three = THREE_GRAMS.get(guess[:3], [])
            two = TWO_GRAMS.get(guess[:2], [])
            one = ONE_GRAMS.get(guess[:1], [])
            rand = random_dex(tried, three, two, one, self.config.ndex)
            # Search for pokemon if not tried
            if rand in tried: continue
            pkmn = self.get_api(f'pokemon-species/{rand}/', True)
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
            tried.add(rand)

        # Sort by match quality 
        out_pkmn = [
            x[0] for x in sorted(
                out, reverse=True, key=lambda x: quality(*x[1:])
            )
        ]

        return [format_pkmn(p) for p in out_pkmn]


def to_service(config):
    return Service(config)
