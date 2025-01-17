{ pkgs, lib, config, inputs, ... }:

{
  packages = [
    pkgs.git
  ];

  languages = {
    javascript = {
      enable = true;
      pnpm = {
        enable = true;
        install.enable = true;
      };
    };

    python = {
      enable = true;
      poetry = {
        enable = true;
        install.enable = true;
        activate.enable = true;
      };
    };
  };

  processes = {
    flask.exec = "flask --debug --app server/server run";
    tailwind.exec = "dev-tailwind";
  };

  scripts.dev-tailwind.exec = "pnpm exec tailwindcss -i ./server/styles/main.css -o ./server/static/styles/main.css --watch";
  scripts.build-tailwind.exec = "pnpm exec tailwindcss -i ./server/styles/main.css -o ./server/static/styles/main.css --minify";

  scripts.cp-htmx.exec = "cp -f node_modules/htmx.org/dist/htmx.min.js server/static/scripts/htmx.min.js";

  git-hooks.hooks = {
    black.enable = true;
    biome.enable = true;
  };
}
