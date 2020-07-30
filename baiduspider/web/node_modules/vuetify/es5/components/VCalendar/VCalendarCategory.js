"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

require("../../../src/components/VCalendar/VCalendarCategory.sass");

var _VCalendarDaily = _interopRequireDefault(require("./VCalendarDaily"));

var _helpers = require("../../util/helpers");

var _props = _interopRequireDefault(require("./util/props"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(source, true).forEach(function (key) { _defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(source).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

/* @vue/component */
var _default = _VCalendarDaily.default.extend({
  name: 'v-calendar-category',
  props: _props.default.category,
  computed: {
    classes: function classes() {
      return _objectSpread({
        'v-calendar-daily': true,
        'v-calendar-category': true
      }, this.themeClasses);
    },
    parsedCategories: function parsedCategories() {
      return typeof this.categories === 'string' && this.categories ? this.categories.split(/\s*,\s*/) : Array.isArray(this.categories) ? this.categories : [];
    }
  },
  methods: {
    genDayHeader: function genDayHeader(day, index) {
      var _this = this;

      var data = {
        staticClass: 'v-calendar-category__columns'
      };

      var scope = _objectSpread({
        week: this.days
      }, day, {
        index: index
      });

      var children = this.parsedCategories.map(function (category) {
        return _this.genDayHeaderCategory(day, _this.getCategoryScope(scope, category));
      });
      return [this.$createElement('div', data, children)];
    },
    getCategoryScope: function getCategoryScope(scope, category) {
      return _objectSpread({}, scope, {
        category: category === this.categoryForInvalid ? null : category
      });
    },
    genDayHeaderCategory: function genDayHeaderCategory(day, scope) {
      var _this2 = this;

      return this.$createElement('div', {
        staticClass: 'v-calendar-category__column-header',
        on: this.getDefaultMouseEventHandlers(':day-category', function (e) {
          return _this2.getCategoryScope(_this2.getSlotScope(day), scope.category);
        })
      }, [(0, _helpers.getSlot)(this, 'category', scope) || this.genDayHeaderCategoryTitle(scope.category), (0, _helpers.getSlot)(this, 'day-header', scope)]);
    },
    genDayHeaderCategoryTitle: function genDayHeaderCategoryTitle(category) {
      return this.$createElement('div', {
        staticClass: 'v-calendar-category__category'
      }, category === null ? this.categoryForInvalid : category);
    },
    genDayBody: function genDayBody(day) {
      var _this3 = this;

      var data = {
        staticClass: 'v-calendar-category__columns'
      };
      var children = this.parsedCategories.map(function (category) {
        return _this3.genDayBodyCategory(day, category);
      });
      return [this.$createElement('div', data, children)];
    },
    genDayBodyCategory: function genDayBodyCategory(day, category) {
      var _this4 = this;

      var data = {
        staticClass: 'v-calendar-category__column',
        on: this.getDefaultMouseEventHandlers(':time-category', function (e) {
          return _this4.getCategoryScope(_this4.getSlotScope(_this4.getTimestampAtEvent(e, day)), category);
        })
      };
      var children = (0, _helpers.getSlot)(this, 'day-body', function () {
        return _this4.getCategoryScope(_this4.getSlotScope(day), category);
      });
      return this.$createElement('div', data, children);
    }
  }
});

exports.default = _default;
//# sourceMappingURL=VCalendarCategory.js.map