let 
  pkgs = import <nixpkgs> { };
  stdenv = pkgs.stdenv;
  python = pkgs.python36;
  pythonPackages = pkgs.python36Packages;
in
  stdenv.mkDerivation rec {
    name = "knockd-env";
    buildInputs = [ python pythonPackages.pycrypto pythonPackages.nose ];
  }
