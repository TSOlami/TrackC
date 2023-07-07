![TE Logo](https://tecdn.b-cdn.net/img/logo/te-transparent-noshadows.webp)

# Tailwind-Elements Vite Starter

**[>> Support Tailwind-Elements with a STAR](https://github.com/mdbootstrap/Tailwind-Elements)**

**[>> Tailwind Docs](https://tailwind-elements.com/docs/standard/getting-started/quick-start/)**

<a href="https://www.npmjs.com/package/tw-elements"> <img src="https://img.shields.io/npm/dt/tw-elements.svg" alt="Total Downloads"></a>
<a href="https://github.com/mdbootstrap/Tailwind-Elements/releases"><img src="https://img.shields.io/npm/v/tw-elements.svg" alt="Latest Release"></a>
<a href="https://twitter.com/intent/tweet/?text=Thanks+@TailwindElement+for+creating+an+amazing+collection+of+open+source+components+for+@tailwindcss%20https://tailwind-elements.com/&hashtags=tailwindCSS,bootstrap,webdesign,javascript,100DaysOfCode,DevCommunity"><img src="https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Let%20us%20know%20you%20were%20here%21&"></a>
<a href="https://www.youtube.com/watch?v=c9B4TPnak1A&t=6s"><img alt="YouTube Video Views" src="https://img.shields.io/youtube/views/c9B4TPnak1A?label=Bootstrap%205%20Tutorial%20Views&style=social"></a>

---

> `warning:` The use of this Starter is at your own risk and assumes basic knowledge of Vite, JavaScript and CSS preprocessors. We recommend creating custom versions of Tailwind-Elements and themes only for advanced developers.

---

### Installation

```
npm install
```

### Dev Server

```
npm start
```

### Build

```
npm run build
```

### Features:

- Bundling and ES6+ Support via [vite](https://github.com/vitejs/vite)
- SASS Support via [sass-loader](https://github.com/jtangelder/sass-loader)
- Linting via [eslint-loader](https://github.com/MoOx/eslint-loader)
- Unit Testing via [jest](https://github.com/facebook/jest)
- Code Formatting via [prettier](https://github.com/prettier/prettier)

### Files structure:

```
.
├── src
│   ├── img/
│   ├── js/
│   └── scss/
├── dist/
├── tailwind.config.cjs
├── vite.config.js
└── index.html
```

<br><br>

---

# Tailwind-Elements

### Importing JS modules

If you want to use the power of ES modules, import the component you need and init it with `initTE` method

```
import { Carousel, initTE } from "tw-elements";
initTE({ Carousel });
```

If you are using an UMD format you can import the entire library:

```
import 'tw-elements';
```

### Importing TE plugin

To add Tailwind-Elements plugin, please add the following code to tailwind.config.cjs:

```
plugins: [require('tw-elements/dist/plugin.js')]
```

<br><br>

---

# CUSTOM VERSION OF TAILWIND-ELEMENTS

It is possible to prepare a custom version of Tailwind-Elements. It can be useful when the project uses only several modules of our library and you want to reduce the size of the compiled files. To achieve this, follow the steps:

```
npm install
```

### Importing JS components

Copy the content from node_modules/tw-elements/dist/src to the src directory. Pick only the components you need and update necessary paths. Here's an example:

```
import Input from ./src/js/forms/input';
```

Some components may require additional dependencies to be installed. Vite should report this after starting a devServer.

### Configuration

Vite config for TE development and index.html file is located in root directory.

### Dev Server

```
npm start
```

### Build

```
npm run build
```
