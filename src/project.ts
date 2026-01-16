import {makeProject} from '@motion-canvas/core';

import intro from './scenes/intro?scene';
import apiIntegration from './scenes/apiIntegration?scene';
import agentAction from './scenes/agentAction?scene';
import selfCustodial from './scenes/selfCustodial?scene';
import callToAction from './scenes/callToAction?scene';

export default makeProject({
  scenes: [intro, apiIntegration, agentAction, selfCustodial, callToAction],
});
