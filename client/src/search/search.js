import searchCSS from 'search-css' assert { type: 'css' };
import globalCSS from 'global-css' assert { type: 'css' };
import { toTag, CustomTag } from 'tag';

const toSearchModal = (data, actions) => {

  class SearchModal extends CustomTag {

    static get setup() {
      return {
        matches: JSON.parse(data.matches),
        busy: false,
        search: '',
      };
    }

    get root() {
      const accept = toTag('div')`Guess`({
        class: 'accept',
        '@click': () => {
          this.data.search = '';
          data.closeModal(); 
        }
      })
      const actions = toTag('div')`
        ${accept}
      `({
        class: 'actions'
      });
      const items = () => {
        const mons = this.data.matches;
        console.log(mons.length);
        return mons.map((mon, i) => {
          const to_name = () => {
            return mon?.name;
          }
          return toTag('div')`
            ${to_name()}
          `({
            key: to_name()
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
          if (this.data.busy) {
            return;
          }
          this.data.busy = true;
          // Recursive update function
          const update_matches = () => {
            const guess = this.data.search;
            console.log('Searching ', guess);
            data.toMatches(guess).then((new_matches) => {
              data.matches = JSON.stringify(new_matches);
              const need_refresh = this.data.search != guess;
              this.data.busy = need_refresh;
              if (need_refresh) {
                update_matches();
              }
            });
          }
          update_matches();
        },
        class: 'search',
        type: 'text'
      })
      const center = toTag('div')`
      ${search}${results}${actions}
      `({
        class: 'center'
      });
      return toTag('div')`
        ${center}`({
        class: 'wrapper'
      });
    }

    get styles() {
      const sheet = new CSSStyleSheet();
      sheet.replaceSync(`
      .todo {
      }`);
      return [globalCSS, searchCSS, sheet];
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
    class: () => {
      if (data.modal == 'search') {
        return 'shown modal';
      }
      return 'hidden modal';
    },
    matches: () => data.matches,
    search: '',
  });

}

export { toSearchModal };
