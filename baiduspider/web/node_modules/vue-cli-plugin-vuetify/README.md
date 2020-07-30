# vue-cli-plugin-vuetify

> A [Vue CLI 3 Plugin](https://github.com/vuejs/vue-cli) for installing Vuetify

### 💿 Install

If you haven't yet installed vue-cli 3, first follow the install instructions here: https://github.com/vuejs/vue-cli

**Tip**: If you don't want to overwrite your current vue-cli because you still need `vue init`, [then try this](https://cli.vuejs.org/guide/creating-a-project.html#pulling-2-x-templates-legacy).

Generate a project using vue-cli 3.0:
```bash
vue create my-app
```

Before installing the vuetify plugin, make sure to commit or stash your changes in case you need to revert the changes.

To install the vuetify plugin simply navigate to your application folder and add Vuetify.
```bash
cd my-app

vue add vuetify
```

If you run into any issues, reach out to us in our [Discord Community server](https://community.vuetifyjs.com).

### 🚀 Usage

Here are some extra steps for setting up the old templates but using plugins from the new ecosystem.

#### Nuxt

```
# preset: default (babel, eslint)

vue add nuxt-starter-template
```

Todo

- Add vuetify Nuxt starter template


#### Electron

Just add [vue-cli-plugin-electron-builder](https://nklayman.github.io/vue-cli-plugin-electron-builder/)

```
vue add electron-builder
vue add vuetify
yarn electron:serve
```

#### PWA

If you already made a project with the PWA option selected, then just adding like above should do it.


#### Cordova

Use the [Cordova](https://github.com/m0dch3n/vue-cli-plugin-cordova) plugin.

```
npm install -g cordova # If cordova is not already installed
vue add cordova

npm run cordova-serve-android # Development Android
npm run cordova-build-android # Build Android
npm run cordova-serve-ios # Development IOS
npm run cordova-build-ios # Build IOS
npm run cordova-serve-browser # Development Browser
npm run cordova-build-browser # Build Browser
```

#### Capacitor

Use  the [Capacitor](https://github.com/nklayman/vue-cli-plugin-capacitor) plugin.

```
vue add @nklayman/capacitor
yarn capacitor:serve
```

Note: you may also want to hide to splashcreen when your app is ready to make your app load faster. See the [plugin installation docs](https://github.com/nklayman/vue-cli-plugin-capacitor#install) for instructions.

### 💪 Supporting Vuetify
<p>Vuetify is an open source MIT project that has been made possible due to the generous contributions by <a href="https://github.com/vuetifyjs/vuetify/blob/dev/BACKERS.md">community backers</a>. If you are interested in supporting this project, please consider:</p>

<ul>
  <li>
    <a href="https://github.com/users/johnleider/sponsorship">Becoming a sponsor on Github</a>
    <strong><small>(supports John)</small></strong>
  </li>
  <li>
    <a href="https://opencollective.com/vuetify">Becoming a backer on OpenCollective</a>
    <strong><small>(supports the Dev team)</small></strong>
  </li>
  <li>
    <a href="https://tidelift.com/subscription/npm/vuetify?utm_source=vuetify&utm_medium=referral&utm_campaign=readme">Become a subscriber on Tidelift</a>
  </li>
  <li>
    <a href="https://paypal.me/vuetify">Make a one-time payment with Paypal</a>
  </li>
  <li>
    <a href="https://vuetifyjs.com/getting-started/consulting-and-support?ref=github">Book time with John</a>
  </li>
</ul>

### 📑 License
[MIT](http://opensource.org/licenses/MIT)

Copyright (c) 2016-present Vuetify LLC
