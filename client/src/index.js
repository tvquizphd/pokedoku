import backdropCSS from 'backdrop-css' assert { type: 'css' };
import globalCSS from 'global-css' assert { type: 'css' };
import { phaseMap, isPhase, nPhases } from 'phases';
import { reactive } from '@arrow-js/core';
import { toBackdrop } from 'backdrop';
import { toPokemonGrid } from 'grid';
import { toSearchModal } from 'search';
import { getMatches } from 'api';
import { toNav } from 'nav';
import { toTag } from 'tag';

const phase_list = [...Array(nPhases).keys()];

const main = () => {
  
  const no_pokemon = JSON.stringify([
    0,1,2,3,4,5,6,7,8
  ].map(() => {
    return null; 
  }));

  const no_matches = JSON.stringify([]);

  const data = reactive({
    phaseMap,
    modal: null,
    content: '',
    phase: 0, err: 0,
    pokemon: no_pokemon,
    matches: no_matches,
    closeModal: () => {
      data.modal = null;
    },
    toMatches: async (guess) => {
      const root = data.api_root;
      const matches = getMatches(root, guess);
      return await matches;
    },
    selectPokemon: (mons, new_mon, i) => {
      if (data.modal == null) {
        data.modal = 'search';
      }
      return mons.map((mon, j) => {
        if (i != j) return mon;
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
