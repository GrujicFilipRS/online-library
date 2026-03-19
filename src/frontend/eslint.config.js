import js from "@eslint/js";
import prettier from "eslint-config-prettier";
import vue from "eslint-plugin-vue";
import tseslint from "typescript-eslint";

export default [
  js.configs.recommended,
  ...tseslint.configs.recommended,
  ...vue.configs["flat/recommended"],

  {
    files: ["**/*.vue"],
    languageOptions: {
      parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module"
      }
    }
  },

  {
    rules: {
      "no-console": "warn",
      "no-unused-vars": "warn",

      // Vue
      "vue/multi-word-component-names": "off"
    }
  },

  prettier
];
