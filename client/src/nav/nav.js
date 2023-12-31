import navCSS from 'nav-css' assert { type: 'css' };
import globalCSS from 'global-css' assert { type: 'css' };
import { backPhase, isFirstPhase } from 'phases';
import { nextPhase, isLastPhase } from 'phases';
import { phaseMap } from 'phases';
import { toTag, CustomTag } from 'tag';

const toNav = (data) => {

  const colors = [
    [
      '--chosen-background', '--dark-text-color',
      '--chosen-box-shadow', '--main-text-shadow',
      'pointer'
    ],
    [
      '--error-background', '--error-text-color',
      '--error-box-shadow', '--error-text-shadow',
      'default'
    ]
  ];

  class Nav extends CustomTag {

    static get setup() {
      return {
        tries: 0, text: '', err: data.err
      };
    }

    get root() {
      const back = () => {
        const first = () => isFirstPhase(data.phase);
        const text = `${['← Back', data.tries+'/9'][+first()]}`;
        return toTag('div')`${data.err ? 'Sorry!' : text}`({
          data: data,
          'class': 'button',
          '@click': () => {
            if (first()) return;
            // Three atempts at skipping phases
            data.phase = [...'...'].reduce(n => {
              if (!data.skipInvalidPhase(n)) return n;
              return backPhase(n);
            }, backPhase(data.phase));
          }
        });
      }
      const github_root = 'https://raw.githubusercontent.com/PokeAPI/sprites/master'
      const revive = toTag('div')`
      <img src="${github_root}/sprites/items/max-revive.png">
      </img><div>Reset</div>`({
          class: 'revive button',
          '@click': () => {
            data.resetRevive();
          }
      });
      const header = () => {
        return toTag('div')`${d => d.text}`({
          class: 'centered-content main-title',
          data: this.data
        });
      }
      const nav = toTag('div')`${revive}${header}`({
        class: 'nav centered grid-row1'
      });
      const buttons = toTag('div')`${back}`({
        class: 'nav centered grid-row3'
      });
      return toTag('div')`${nav}${buttons}`({
        class: 'content'
      });
    }

    get styles() {
      const i = data.err % colors.length;
      const [
        background, color, shadow, text_shadow, cursor
      ] = colors[i];
      const sheet = new CSSStyleSheet();
      const last = isLastPhase(data.phase);
      sheet.replaceSync(`
      .nav {
        background-color: var(${background});
        text-shadow: var(${text_shadow});
        box-shadow: var(${shadow});
        color: var(${color});
        cursor: ${cursor};
      }`);
      return [globalCSS, navCSS, sheet];
    }
  }

  return toTag('nav', Nav)``({
    class: 'content',
    err: () => data.err,
    tries: () => data.tries,
    text: () => {
      return [
        'Pokedoku',
        'Good Job!'
      ][data.phase];
    },
    data 
  });
}

export { toNav };
