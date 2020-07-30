// Styles
import "../../../src/components/VWindow/VWindow.sass"; // Directives

import Touch from '../../directives/touch'; // Components

import VBtn from '../VBtn';
import VIcon from '../VIcon';
import { BaseItemGroup } from '../VItemGroup/VItemGroup';
/* @vue/component */

export default BaseItemGroup.extend({
  name: 'v-window',

  provide() {
    return {
      windowGroup: this
    };
  },

  directives: {
    Touch
  },
  props: {
    activeClass: {
      type: String,
      default: 'v-window-item--active'
    },
    continuous: Boolean,
    mandatory: {
      type: Boolean,
      default: true
    },
    nextIcon: {
      type: [Boolean, String],
      default: '$next'
    },
    prevIcon: {
      type: [Boolean, String],
      default: '$prev'
    },
    reverse: {
      type: Boolean,
      default: undefined
    },
    showArrows: Boolean,
    showArrowsOnHover: Boolean,
    touch: Object,
    touchless: Boolean,
    value: {
      required: false
    },
    vertical: Boolean
  },

  data() {
    return {
      changedByDelimiters: false,
      internalHeight: undefined,
      transitionHeight: undefined,
      transitionCount: 0,
      isBooted: false,
      isReverse: false
    };
  },

  computed: {
    isActive() {
      return this.transitionCount > 0;
    },

    classes() {
      return { ...BaseItemGroup.options.computed.classes.call(this),
        'v-window--show-arrows-on-hover': this.showArrowsOnHover
      };
    },

    computedTransition() {
      if (!this.isBooted) return '';
      const axis = this.vertical ? 'y' : 'x';
      const reverse = this.$vuetify.rtl && axis === 'x' ? !this.internalReverse : this.internalReverse;
      const direction = reverse ? '-reverse' : '';
      return `v-window-${axis}${direction}-transition`;
    },

    hasActiveItems() {
      return Boolean(this.items.find(item => !item.disabled));
    },

    hasNext() {
      return this.continuous || this.internalIndex < this.items.length - 1;
    },

    hasPrev() {
      return this.continuous || this.internalIndex > 0;
    },

    internalIndex() {
      return this.items.findIndex((item, i) => {
        return this.internalValue === this.getValue(item, i);
      });
    },

    internalReverse() {
      return this.reverse ? !this.isReverse : this.isReverse;
    }

  },
  watch: {
    internalIndex: 'updateReverse'
  },

  mounted() {
    window.requestAnimationFrame(() => this.isBooted = true);
  },

  methods: {
    genContainer() {
      const children = [this.$slots.default];

      if (this.showArrows) {
        children.push(this.genControlIcons());
      }

      return this.$createElement('div', {
        staticClass: 'v-window__container',
        class: {
          'v-window__container--is-active': this.isActive
        },
        style: {
          height: this.internalHeight || this.transitionHeight
        }
      }, children);
    },

    genIcon(direction, icon, fn) {
      return this.$createElement('div', {
        staticClass: `v-window__${direction}`
      }, [this.$createElement(VBtn, {
        props: {
          icon: true
        },
        attrs: {
          'aria-label': this.$vuetify.lang.t(`$vuetify.carousel.${direction}`)
        },
        on: {
          click: () => {
            this.changedByDelimiters = true;
            fn();
          }
        }
      }, [this.$createElement(VIcon, {
        props: {
          large: true
        }
      }, icon)])]);
    },

    genControlIcons() {
      const icons = [];
      const prevIcon = this.$vuetify.rtl ? this.nextIcon : this.prevIcon;
      /* istanbul ignore else */

      if (this.hasPrev && prevIcon && typeof prevIcon === 'string') {
        const icon = this.genIcon('prev', prevIcon, this.prev);
        icon && icons.push(icon);
      }

      const nextIcon = this.$vuetify.rtl ? this.prevIcon : this.nextIcon;
      /* istanbul ignore else */

      if (this.hasNext && nextIcon && typeof nextIcon === 'string') {
        const icon = this.genIcon('next', nextIcon, this.next);
        icon && icons.push(icon);
      }

      return icons;
    },

    getNextIndex(index) {
      const nextIndex = (index + 1) % this.items.length;
      const item = this.items[nextIndex];
      if (item.disabled) return this.getNextIndex(nextIndex);
      return nextIndex;
    },

    getPrevIndex(index) {
      const prevIndex = (index + this.items.length - 1) % this.items.length;
      const item = this.items[prevIndex];
      if (item.disabled) return this.getPrevIndex(prevIndex);
      return prevIndex;
    },

    next() {
      this.isReverse = this.$vuetify.rtl;
      /* istanbul ignore if */

      if (!this.hasActiveItems || !this.hasNext) return;
      const nextIndex = this.getNextIndex(this.internalIndex);
      const item = this.items[nextIndex];
      this.internalValue = this.getValue(item, nextIndex);
    },

    prev() {
      this.isReverse = !this.$vuetify.rtl;
      /* istanbul ignore if */

      if (!this.hasActiveItems || !this.hasPrev) return;
      const lastIndex = this.getPrevIndex(this.internalIndex);
      const item = this.items[lastIndex];
      this.internalValue = this.getValue(item, lastIndex);
    },

    updateReverse(val, oldVal) {
      if (this.changedByDelimiters) {
        this.changedByDelimiters = false;
        return;
      }

      this.isReverse = val < oldVal;
    }

  },

  render(h) {
    const data = {
      staticClass: 'v-window',
      class: this.classes,
      directives: []
    };

    if (!this.touchless) {
      const value = this.touch || {
        left: () => {
          this.$vuetify.rtl ? this.prev() : this.next();
        },
        right: () => {
          this.$vuetify.rtl ? this.next() : this.prev();
        },
        end: e => {
          e.stopPropagation();
        },
        start: e => {
          e.stopPropagation();
        }
      };
      data.directives.push({
        name: 'touch',
        value
      });
    }

    return h('div', data, [this.genContainer()]);
  }

});
//# sourceMappingURL=VWindow.js.map