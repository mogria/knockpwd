let 
  pkgs = import <nixpkgs> { };
  stdenv = pkgs.stdenv;
in
  stdenv.mkDerivation rec {
    name = "knockd-env";
    buildInputs = with pkgs; [ python36 ];
  }
