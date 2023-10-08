import pokemonGridCSS from 'grid-css' assert { type: 'css' };
import { toTag, CustomTag } from 'tag';
import { phases, phaseMap, isPhase } from 'phases';

const toPokemonSprite = (no_mon, to_dex) => {
  const to_png = () => {
    const base = 'https://raw.githubusercontent.com/PokeAPI'
    const prefix = `${base}/sprites/master/sprites/pokemon`
    return `${prefix}/${to_dex()}.png`
  }
  return toTag('img')``({
    class: () => {
      if (no_mon()) return 'full placeholder';
      return 'full';
    },
    src: () => {
      return no_mon() ? '' : to_png();
    }
  });
}

function* addHeaders (squares, cols, rows) {
  yield toTag('div')``({
    class: 'corner header'
  });

  const mod = rows.length;
  for (const col of cols) {
      yield toTag('div')`
      <div class="${() => col}">${() => col}</div>
      `({
        class: 'column header'
      });
  }
  for (const i in squares) {
    const square = squares[i];
    const row = rows[Math.floor(i / mod)];
    if (i % mod == 0) {
      yield toTag('div')`
      <div class="${() => row}">${() => row}</div>
      `({
        class: 'row header'
      });
    }
    yield square;
  }
}

const types = [
  'Normal', 'Fire', 'Water', 'Grass', 'Electric', 'Ice', 'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dark', 'Dragon', 'Steel', 'Fairy'
];

// Function to choose random from array
const randomTypes = () => {
  return [1,2,3,4,5,6].reduce((output) => {
    let out = undefined
    // Random unique type not in output
    while (!out || output.includes(out)) {
      out = types[Math.floor(Math.random() * types.length)];
    }
    return [...output, out];
  }, []);
}

const toPokemonGrid = (data, globalCSS) => {

  class PokemonGrid extends CustomTag {

    static get setup() {
      return {
        pokemon: JSON.parse(data.pokemon)
      };
    }

    get root() {
      const mons = [0,1,2,3,4,5,6,7,8].map((i) => {
        return () => this.data.pokemon[i];
      });
      const squares = mons.map((to_mon, i) => () => {
        const no_mon = () => to_mon() == null;
        const to_dex = () => to_mon()?.dex;
        const to_name = () => to_mon()?.name;
        const to_prob = () => to_mon()?.probability;
        const pokemon = toPokemonSprite(no_mon, to_dex);
        const prob = toTag('div')`${
          () => no_mon()? '' : to_prob()+'%'
        }`({
          class: 'top right'
        });
        const name = toTag('div')`${
          () => to_name() || ''
        }`({
          class: 'bottom full'
        })
        return toTag('div')`
          ${pokemon}${prob}${name}
        `({
          '@click': () => {
            const mons = this.data.pokemon;
            const new_mon = no_mon() ? {
              name: 'Pikachu',
              probability: 0,
              dex: 25
            } : null;
            const new_mons = data.selectPokemon(mons, new_mon, i);
            data.pokemon = JSON.stringify(new_mons);
          }
        });
      });

      const rand = randomTypes();
      const cols = [0,1,2].map(i => rand[i]);
      const rows = [3,4,5].map(i => rand[i]);
      const items = [...addHeaders(squares, cols, rows)];

      return toTag('div')`${items}`({
        'class': 'pokemon-grid centered'
      });
    }

    get styles() {
      return [globalCSS, pokemonGridCSS];
    }

    attributeChangedCallback(name, _, v) {
      super.attributeChangedCallback(name, _, JSON.parse(v));
    }
  }

  return toTag('pokemon-grid', PokemonGrid)``({
    pokemon: () => data.pokemon,
    class: 'grid-row2'
  });
}

export { toPokemonGrid };
