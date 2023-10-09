import searchCSS from 'search-css' assert { type: 'css' };
import globalCSS from 'global-css' assert { type: 'css' };
import { toTag, CustomTag } from 'tag';
import { getForms } from 'api';

const toSearchModal = (data, actions) => {

  class SearchModal extends CustomTag {

    static get setup() {
      return {
        pokemon: JSON.parse(data.pokemon),
        matches: JSON.parse(data.matches),
        updating_forms: [],
        updating_all: false,
        search: '',
      };
    }

    get mons() {
      const max_mons = 20;
      return [...this.data.matches].reduce((forms, p) => {
        if (p.forms.length == 0) {
          this.fetchPokemonForms(p.dex);
          return forms;
        }
        if (forms.length >= max_mons) {
          return forms;
        }
        return [
          ...forms, ...p.forms.map((f) => {
            return { 
              name: f.name, id: f.id, key: f.id,
              percentage: f.percentage
            };
          })
        ];
      }, []);
    }

    get root() {
      const to_accept = (mon) => {
        return toTag('div')`Guess`({
          class: 'accept',
          '@click': async () => {
            this.data.search = '';
            const ok = await data.testGuess(mon.id);
            if (ok) {
              data.pokemon = JSON.stringify(
                data.selectPokemon(
                  this.data.pokemon, mon
                )
              );
            }
            data.closeModal(); 
          }
        });
      }
      const items = () => { 
        return this.mons.map((mon) => {
          const to_url = () => data.toFormPngUrl(mon.id);
          const no_form = () => mon.id === null;
          const img = toTag('img')``({
            src: () => {
              return no_form() ? '' : to_url();
            }
          });
          return toTag('div')`
            ${img}${mon.name}
            <div>${to_accept(mon)}</div>
          `({
            key: mon.key
          });
        });
      }
      const results = toTag('div')`${() => items()}`({
        class: 'results'
      });
      const search = toTag('input')``({
        value: () => this.data.search,
        placeholder: 'Search Pokémon...',
        '@input': (event) => {
          this.data.search = event.target.value;
          // Don't update if updating or updating_forms
          const is_updating_forms = this.data.updating_forms.length > 0;
          if (this.data.updating_all || is_updating_forms) {
            return;
          }
          this.data.updating_all = true;
          // Recursive update function
          const update_matches = () => {
            const guess = this.data.search;
            data.toMatches(guess).then((new_matches) => {
              data.matches = JSON.stringify(new_matches);
              const need_refresh = this.data.search != guess;
              this.data.updating_all = need_refresh;
              if (need_refresh) {
                update_matches();
              }
            });
          }
          update_matches();
        },
        autofocus: "",
        class: 'search',
        type: 'text'
      })
      const center = toTag('div')`
      ${search}${results}
      `({
        class: 'center',
        '@click': (e) => {
          e.stopPropagation();
        }
      });
      return toTag('div')`
        ${center}`({
        class: () => {
          if (data.modal == 'search') {
            return 'shown modal wrapper';
          }
          return 'hidden modal wrapper';
        },
        '@click': () => {
          data.closeModal();
        }
      });
    }

    get styles() {
      const sheet = new CSSStyleSheet();
      sheet.replaceSync(`
      .todo {
      }`);
      return [globalCSS, searchCSS, sheet];
    }

    async fetchPokemonForms(dexn) {
      const { updating_forms } = this.data;
      if (updating_forms.includes(dexn)) {
        return;
      }
      this.data.updating_forms = [...updating_forms, dexn];
      // Request all regional forms for the pokemon
      const dexn_forms = await getForms(data.api_root, dexn);
      this.data.matches = this.data.matches.map((p) => {
        if (p.dex == dexn) {
          p.forms = dexn_forms;
        }
        return p;
      });
      this.data.updating_forms = this.data.updating_forms.filter((d) => {
        return d != dexn;
      });
    }

    attributeChangedCallback(name, _, v) {
      let parsed = v;
      try {
        parsed = JSON.parse(v)
      } catch {
      }
      super.attributeChangedCallback(name, _, parsed);
    }
  }

  return toTag('search', SearchModal)``({
    pokemon: () => data.pokemon,
    matches: () => data.matches,
    class: 'shown modal',
    search: '',
  });

}

export { toSearchModal };
