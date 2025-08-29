import { defineConfig } from "eslint/config";
import js from "@eslint/js";
import svelte from "eslint-plugin-svelte";
import importPlugin from "eslint-plugin-import";
import pluginPromise from "eslint-plugin-promise";
import globals from "globals";
import stylistic from "@stylistic/eslint-plugin";
import ts from "typescript-eslint";
import svelteConfig from "./svelte.config.js";

export default defineConfig([
  js.configs.recommended,
  importPlugin.flatConfigs.recommended,
  pluginPromise.configs["flat/recommended"],
  ...ts.configs.recommended,
  ...svelte.configs.recommended,
  {
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    plugins: {
      "@stylistic": stylistic,
    },
  },
  {
    files: ["**/*.svelte", "**/*.svelte.ts", "**/*.svelte.js"],
    languageOptions: {
      parserOptions: {
        projectService: true,
        extraFileExtensions: [".svelte"],
        parser: ts.parser,
        svelteConfig,
      },
    },
    plugins: {
      "@stylistic": stylistic,
    },
  },
]);
