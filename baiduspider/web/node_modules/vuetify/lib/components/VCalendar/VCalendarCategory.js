// Styles
import "../../../src/components/VCalendar/VCalendarCategory.sass"; // Mixins

import VCalendarDaily from './VCalendarDaily'; // Util

import { getSlot } from '../../util/helpers';
import props from './util/props';
/* @vue/component */

export default VCalendarDaily.extend({
  name: 'v-calendar-category',
  props: props.category,
  computed: {
    classes() {
      return {
        'v-calendar-daily': true,
        'v-calendar-category': true,
        ...this.themeClasses
      };
    },

    parsedCategories() {
      return typeof this.categories === 'string' && this.categories ? this.categories.split(/\s*,\s*/) : Array.isArray(this.categories) ? this.categories : [];
    }

  },
  methods: {
    genDayHeader(day, index) {
      const data = {
        staticClass: 'v-calendar-category__columns'
      };
      const scope = {
        week: this.days,
        ...day,
        index
      };
      const children = this.parsedCategories.map(category => this.genDayHeaderCategory(day, this.getCategoryScope(scope, category)));
      return [this.$createElement('div', data, children)];
    },

    getCategoryScope(scope, category) {
      return { ...scope,
        category: category === this.categoryForInvalid ? null : category
      };
    },

    genDayHeaderCategory(day, scope) {
      return this.$createElement('div', {
        staticClass: 'v-calendar-category__column-header',
        on: this.getDefaultMouseEventHandlers(':day-category', e => {
          return this.getCategoryScope(this.getSlotScope(day), scope.category);
        })
      }, [getSlot(this, 'category', scope) || this.genDayHeaderCategoryTitle(scope.category), getSlot(this, 'day-header', scope)]);
    },

    genDayHeaderCategoryTitle(category) {
      return this.$createElement('div', {
        staticClass: 'v-calendar-category__category'
      }, category === null ? this.categoryForInvalid : category);
    },

    genDayBody(day) {
      const data = {
        staticClass: 'v-calendar-category__columns'
      };
      const children = this.parsedCategories.map(category => this.genDayBodyCategory(day, category));
      return [this.$createElement('div', data, children)];
    },

    genDayBodyCategory(day, category) {
      const data = {
        staticClass: 'v-calendar-category__column',
        on: this.getDefaultMouseEventHandlers(':time-category', e => {
          return this.getCategoryScope(this.getSlotScope(this.getTimestampAtEvent(e, day)), category);
        })
      };
      const children = getSlot(this, 'day-body', () => this.getCategoryScope(this.getSlotScope(day), category));
      return this.$createElement('div', data, children);
    }

  }
});
//# sourceMappingURL=VCalendarCategory.js.map