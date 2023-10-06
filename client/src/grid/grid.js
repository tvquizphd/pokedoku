import pokemonGridCSS from 'grid-css' assert { type: 'css' };
import { toTag, CustomTag } from 'tag';
import { phases, phaseMap, isPhase } from 'phases';

const toPokemonSprite = (mon, phase) => {
  return toTag('img')``({
    class: 'full',
    'src': 'https://pokedoku.com/unknown.png'
  });
}

const displayPokemon = (mon, phase) => {

  if (isPhase(phase, 'review')) {
    return toTag('div')`Done`();
  }

  return toPokemonSprite(
    mon, phase
  );
//  return toTag('div')`${() => mon.name}`();
}

const toPokemonGrid = (data, globalCSS) => {

  class PokemonGrid extends CustomTag {

    static get setup() {
      return { };
    }

    get root() {
      const squares = data.pokemon.map((mon) => () => {
        return toTag('div')`
        <div class='right'>69%</div>
        ${displayPokemon(
          mon, data.phase
        )}
        <div class='full'>${() => mon.name}</div>
        `();
      });

      return toTag('div')`${squares}`({
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
