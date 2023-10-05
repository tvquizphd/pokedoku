import pokemonGridCSS from 'grid-css' assert { type: 'css' };
import { toTag, CustomTag } from 'tag';
import { phases, phaseMap, isPhase } from 'phases';

const infos = {
  'play': () => `
    Welcome to Pokedoku
  `,
  'review': what => `Played ${what}?`
};

const toInfo = (what, phase) => {
  const info_text = infos[phases[phase]](what);
  const results = [
    toTag('div')`<strong>Chosen Pokemon</strong>`()
  ]
  if (isPhase(phase, 'review')) {
    const list = toTag('div')`${results}`();
    return toTag('div')`${info_text} ${list}`();
  }
  return toTag('div')`${info_text}`();
}

const toPokemonGrid = (data, globalCSS) => {

  class PokemonGrid extends CustomTag {

    static get setup() {
      return { };
    }

    get root() {
      const info = () => {
        const what = "Pokedoku"
        return toTag('div')`${() => {
          return toInfo(what, data.phase);
        }}`();
      }
      return toTag('form')`${info}`({
        class: 'pokemon-grid centered'
      });
    }

    get styles() {
      return [globalCSS, pokemonGridCSS];
    }
  }

  return toTag('pokemon-grid', PokemonGrid)``({
    class: 'grid-row2'
  });
}

export { toPokemonGrid };
