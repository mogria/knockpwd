let 
  pkgs = import <nixpkgs> { };
  stdenv = pkgs.stdenv;
  python = pkgs.python35;
  pythonPackages = pkgs.python35Packages;
in
  stdenv.mkDerivation rec {
    name = "knockd-env";
    buildInputs = [ python pythonPackages.pycrypto pythonPackages.nose pythonPackages.pylint];
  }
