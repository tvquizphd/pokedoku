import backdropCSS from 'backdrop-css' assert { type: 'css' };
import globalCSS from 'global-css' assert { type: 'css' };
import { phaseMap, isPhase, nPhases } from 'phases';
import { testGuess, getMatches } from 'api';
import { reactive } from '@arrow-js/core';
import { toBackdrop } from 'backdrop';
import { toPokemonGrid } from 'grid';
import { toSearchModal } from 'search';
import { toNav } from 'nav';
import { toTag } from 'tag';

const phase_list = [...Array(nPhases).keys()];

// Choose 6 random types
const randomTypes = () => {
  const banned = [
    new Set(['Normal', 'Steel']),
    new Set(['Normal', 'Rock']),
    new Set(['Normal', 'Bug']),
    new Set(['Normal', 'Ice']),
    new Set(['Poison', 'Ice']),
    new Set(['Dragon', 'Bug']),
    new Set(['Ghost', 'Rock']),
    new Set(['Fairy', 'Fire']),
    new Set(['Fairy', 'Ground'])
  ]
  // Prevent banned type combinatons
  const is_banned = (out, col) => (set) => {
    return set.has(out) && col.some(o => set.has(o));
  }
  // All available types
  const types = [
    'Normal', 'Fire', 'Water', 'Grass', 'Electric', 'Ice', 'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dark', 'Dragon', 'Steel', 'Fairy'
  ];
  return [1,2,3,4,5,6].reduce((output, i) => {
    let out = null 
    // Random unique type not in output
    while (out === null) {
      out = types[Math.floor(Math.random() * types.length)];
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

const main = () => {
  
  const no_pokemon = JSON.stringify([
    0,1,2,3,4,5,6,7,8
  ].map(() => {
    return null; 
  }));

  const no_matches = JSON.stringify([]);

  const rand = randomTypes();
  const cols = [0,1,2].map(i => rand[i]);
  const rows = [3,4,5].map(i => rand[i]);

  const data = reactive({
    phaseMap,
    tries: 0,
    modal: null,
    content: '',
    cols, rows,
    phase: 0, err: 0,
    active_square: 0,
    pokemon: no_pokemon,
    matches: no_matches,
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
        data.cols[col], data.rows[row]
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
      return await testGuess(data.api_root, id, conditions);
    },
    selectPokemon: (mons, new_mon) => {
      return mons.map((mon, i) => {
        if (i != data.active_square) return mon;
        return new_mon;
      });
    },
    width: window.innerWidth,
    height: window.innerHeight,
    api_root: 'http://localhost:8000',
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
  const root = toTag('div')`
    ${nav}${pokemonGrid}${searchModal}
  `({
    class: 'centered root index'
  });
  return toTag('div')`${backdrop}${root}`({
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
