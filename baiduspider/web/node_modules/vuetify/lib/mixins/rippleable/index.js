// Directives
import ripple from '../../directives/ripple'; // Types

import Vue from 'vue';
export default Vue.extend({
  name: 'rippleable',
  directives: {
    ripple
  },
  props: {
    ripple: {
      type: [Boolean, Object],
      default: true
    }
  },
  methods: {
    genRipple(data = {}) {
      if (!this.ripple) return null;
      data.staticClass = 'v-input--selection-controls__ripple';
      data.directives = data.directives || [];
      data.directives.push({
        name: 'ripple',
        value: {
          center: true
        }
      });
      data.on = Object.assign({
        click: this.onChange
      }, this.$listeners);
      return this.$createElement('div', data);
    },

    onChange() {}

  }
});
//# sourceMappingURL=index.js.map