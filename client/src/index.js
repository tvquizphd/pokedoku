import backdropCSS from 'backdrop-css' assert { type: 'css' };
import globalCSS from 'global-css' assert { type: 'css' };
import { phaseMap, isPhase, nPhases } from 'phases';
import { reactive } from '@arrow-js/core';
import { toBackdrop } from 'backdrop';
import { toActions } from 'actions';
import { toEventForm } from 'form';
import { toNav } from 'nav';
import { toTag } from 'tag';

const phase_list = [...Array(nPhases).keys()];

const main = () => {
  const data = reactive({
    phaseMap,
    content: '',
    phase: 0, err: 0,
    width: window.innerWidth,
    height: window.innerHeight,
    api_root: 'http://localhost:8000',
    skipInvalidPhase: (phase) => {
      return [ /* Phases to skip */ ].some(x => x);
    }
  });
  const actions = toActions(data);
  window.addEventListener('resize', handleResize(data));
  document.adoptedStyleSheets = [
    globalCSS, backdropCSS
  ];
  // Date at the top
  const nav = toNav(data, actions);
  // Demo Form
  const eventForm = toEventForm(data, globalCSS);
  // Animated Background
  const backdrop = toBackdrop(data);
  // Containers
  const root = toTag('div')`
    ${nav}${eventForm}
  `({
    class: 'centered root index'
  });
  return toTag('div')`${backdrop}${root}`({
    class: 'centered root wrapper'
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
