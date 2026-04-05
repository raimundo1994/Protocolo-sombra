#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Executa Protocolo Sombra v3.0"""

import sys
import os

# Garante que o diretório pai está no path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from protocolo_sombra_v3.__main__ import main

if __name__ == "__main__":
    main()
