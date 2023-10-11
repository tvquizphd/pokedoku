import backdropCSS from 'backdrop-css' assert { type: 'css' };
import globalCSS from 'global-css' assert { type: 'css' };
import { phaseMap, isPhase, nPhases } from 'phases';
import { testGuess, getMatches, getRegions } from 'api';
import { reactive } from '@arrow-js/core';
import { toBackdrop } from 'backdrop';
import { toPokemonGrid } from 'grid';
import { toSearchModal } from 'search';
import { toNav } from 'nav';
import { toTag } from 'tag';

const phase_list = [...Array(nPhases).keys()];

// Choose 6 random types
const randomConditions = async (api_root) => {
  const regions = await getRegions(api_root);
  const last_used = localStorage['pokedoku-saved-conditions'] || "[]";
  const banned = [
    new Set(['Normal', 'Steel']),
    new Set(['Normal', 'Rock']),
    new Set(['Normal', 'Bug']),
    new Set(['Normal', 'Ice']),
    new Set(['Poison', 'Ice']),
    new Set(['Dragon', 'Bug']),
    new Set(['Ghost', 'Rock']),
    new Set(['Fairy', 'Fire']),
    new Set(['Fairy', 'Ground']),
    // Avoid combinations recently used
    ...JSON.parse(last_used).map(xy => new Set(xy)),
    // Avoid duplicate regions
    ...regions.reduce((o1,r1,i) => {
      return regions.slice(i+1).reduce((o2, r2) => {
        return [...o2, new Set([r1, r2])];
      }, o1);
    }, [])
  ];
  // Prevent banned type combinatons
  const is_banned = (out, col) => (set) => {
    return set.has(out) && col.some(o => set.has(o));
  }
  // All available types
  const types = [
    'Normal', 'Fire', 'Water', 'Grass', 'Electric', 'Ice', 'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dark', 'Dragon', 'Steel', 'Fairy'
  ];
  const conditions = [...types, ...regions];
  return [1,2,3,4,5,6].reduce((output, i) => {
    let out = null 
    // Random unique type not in output
    while (out === null) {
      out = conditions[
        Math.floor(Math.random() * conditions.length)
      ];
      // Ensure no duplication
      if (output.includes(out)) {
        out = null;
        continue;
      }
      // Ensure no clash between row/column
      const col = output.slice(0,3);
      if (i >= 3 && banned.some(is_banned(out, col))) {
        out = null;
      }
    }
    return [...output, out];
  }, []);
}

const remember = (new_pokemon, tries) => {
  // Prevent choices from being selected next time
  localStorage.setItem("pokedoku-saved-tries", `${tries}`);
  localStorage.setItem("pokedoku-saved-pokemon", JSON.stringify(
    new_pokemon
  ));
}

const has_saved_state = () => {
  const found = [
    'tries', 'pokemon', 'rows', 'cols'
  ].map(k => {
    return localStorage.getItem(`pokedoku-saved-${k}`);
  });
  const [tries, pokemon, rows, cols] = found;
  const saved = found.every(x => x !== null);
  console.log([
    'tries', 'pokemon', 'rows', 'cols'
  ])
  return [saved, parseInt(tries || 0), pokemon, rows, cols];
}

const initialize = async (api_root, reset) => {

  const saved = has_saved_state();
  if (saved[0] && reset === false) {
    const saved_state = saved.slice(1);
    const [tries, pokemon, rows, cols] = saved_state;
    return { tries, pokemon, rows, cols };
  }
  const pokemon = JSON.stringify([
    0,1,2,3,4,5,6,7,8
  ].map(() => {
    return null; 
  }));

  const rand = await randomConditions(api_root);
  const col_list = [0,1,2].map(i => rand[i]);
  const row_list = [3,4,5].map(i => rand[i]);
  const cols = JSON.stringify(col_list);
  const rows = JSON.stringify(row_list);

  // Prevent choices from being selected next time
  localStorage.removeItem("pokedoku-saved-tries");
  localStorage.removeItem("pokedoku-saved-pokemon");
  localStorage.setItem("pokedoku-saved-rows", rows);
  localStorage.setItem("pokedoku-saved-cols", cols);
  localStorage.setItem("pokedoku-saved-conditions", JSON.stringify(
    row_list.reduce((x,r) => {
      return col_list.reduce((y,c) => ([...y, [r,c]]), x);
    }, [])
  ));

  return { tries: 0, pokemon, rows, cols };
}

const main = async () => {
  
  const host = window.location.hostname;
  const api_root = `http://${host}:8000`;
  const no_matches = JSON.stringify([]);
  const {
    tries, rows, cols, pokemon
  } = await initialize(api_root, false);

  const data = reactive({
    phaseMap,
    tries: tries,
    modal: null,
    content: '',
    cols, rows,
    phase: 0, err: 0,
    active_square: 0,
    pokemon: pokemon,
    matches: no_matches,
    resetRevive: async () => {
        const {
          tries, rows, cols, pokemon
        } = await initialize(api_root, true);
        data.pokemon = pokemon;
        data.tries = tries;
        data.rows = rows;
        data.cols = cols;
    },
    closeModal: () => {
      data.modal = null;
    },
    toFormPngUrl: (id) => {
      const repo = 'https://raw.githubusercontent.com/PokeAPI/sprites';
      return `${repo}/master/sprites/pokemon/other/official-artwork//${id}.png`;
    },
    toMatches: async (guess) => {
      const root = data.api_root;
      const matches = getMatches(root, guess);
      return await matches;
    },
    testGuess: async (id) => {
      const col = data.active_square % 3; 
      const row = Math.floor(data.active_square / 3);
      const conditions = [
        JSON.parse(data.cols)[col], JSON.parse(data.rows)[row]
      ];
      // Show failure status
      const pokemon = JSON.parse(data.pokemon);
      const missing = pokemon.some(p => p === null);
      const failure = missing && data.tries >= 9;
      if (failure) {
        data.err = 1;
        return;
      }
      data.tries += 1;
      console.log(conditions);
      return await testGuess(data.api_root, id, conditions);
    },
    selectPokemon: (mons, new_mon) => {
      const new_pokemon = mons.map((mon, i) => {
        if (i != data.active_square) return mon;
        return new_mon;
      });
      remember(new_pokemon, data.tries);
      return new_pokemon;
    },
    api_root: api_root,
    width: window.innerWidth,
    height: window.innerHeight,
    skipInvalidPhase: (phase) => {
      return [ /* Phases to skip */ ].some(x => x);
    }
  });
  window.addEventListener('resize', handleResize(data));
  document.adoptedStyleSheets = [
    globalCSS, backdropCSS
  ];
  // Main Content 
  const nav = toNav(data);
  const pokemonGrid = toPokemonGrid(data, globalCSS);
  const searchModal = toSearchModal(data, globalCSS);
  // Animated Background
  const backdrop = toBackdrop(data);
  // Containers
  const centered = toTag('div')`
    ${nav}${pokemonGrid}
  `({
    class: 'centered root index'
  });
  return toTag('div')`${backdrop}${centered}${searchModal}`({
    class: 'centered root wrapper',
  })(document.body);
}

const parseDate = (date_string) => {
  if (date_string === null) return null;
  return new Date(Date.parse(date_string));
}

const handleResize = (d) => {
  return () => {
    d.height = window.innerHeight;
    d.width = window.innerWidth;
  }
}

export default main
