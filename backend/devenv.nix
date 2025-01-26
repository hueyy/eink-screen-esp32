{ pkgs, lib, config, inputs, ... }:

{
  packages = [
    pkgs.git
    pkgs.ngrok
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
    flask.exec = "cp-htmx && dev-flask";
    tailwind.exec = "dev-tailwind";
    tailwind.process-compose = {
      availability = {
        restart = "always";
      };
    };
  };

  scripts.dev-flask.exec = "flask --debug --app server/server run";

  scripts.dev-tailwind.exec = "pnpm dlx @tailwindcss/cli -i ./server/styles/main.css -o ./server/static/styles/main.css --watch";
  scripts.build-tailwind.exec = "pnpm dlx @tailwindcss/cli -i ./server/styles/main.css -o ./server/static/styles/main.css --minify";

  scripts.cp-htmx.exec = "cp -f node_modules/htmx.org/dist/htmx.min.js server/static/scripts/htmx.min.js";

  services.caddy = {
    enable = true;
    config = ''
      {
        debug
      }

      :8000 {
        handle_path /healthcheck {
          respond "OK"
        }

        handle /static/current {
          uri strip_prefix /static/current
          root server/static/current
          file_server
        }

        handle /static/* {
          encode zstd gzip
          uri strip_prefix /static
          root server/static
          file_server
        }

        handle {
          encode zstd gzip
          reverse_proxy localhost:5000
        }
      }
    '';
  };

  git-hooks.hooks = {
    black.enable = true;
    biome.enable = true;
    nixpkgs-fmt.enable = true;
  };
}
