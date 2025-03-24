import { defineConfig } from "eslint/config";
import globals from "globals";
import js from "@eslint/js";
import tseslint from "typescript-eslint";
import pluginReact from "eslint-plugin-react";

export default defineConfig([
  { files: ["**/*.{js,mjs,cjs,ts,jsx,tsx}"] },
  { files: ["**/*.{js,mjs,cjs,ts,jsx,tsx}"], languageOptions: { globals: globals.browser } },
  { files: ["**/*.{js,mjs,cjs,ts,jsx,tsx}"], plugins: { js }, extends: ["js/recommended"] },
  tseslint.configs.recommended,
  pluginReact.configs.flat.recommended,
  {
    files: ["**/*.{js,mjs,cjs,ts,jsx,tsx}"],
    rules: {
      "semi": ["error", "always"],
      "prettier/prettier": [
        "error",
        {
          "singleQuote": true,
          "semi": true,
          "trailingComma": "all",
          "printWidth": 80,
          "tabWidth": 2,
          "endOfLine": "auto"
        }
      ],
      "no-console": "warn",
      "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }]
    }
  }
]);
