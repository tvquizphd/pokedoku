import eventFormCSS from 'form-css' assert { type: 'css' };
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

const toEventForm = (data, globalCSS) => {

  class EventForm extends CustomTag {

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
        class: 'event-form centered'
      });
    }

    get styles() {
      return [globalCSS, eventFormCSS];
    }
  }

  return toTag('event-form', EventForm)``({
    class: 'grid-row2'
  });
}

export { toEventForm };
