#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ponto de entrada do Protocolo Sombra"""

import sys
import os

# Adicionar o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from protocolo_sombra.engine.motor import MotorJogo
from protocolo_sombra.ui.terminal import C, mensagem_eva


def main():
    try:
        jogo = MotorJogo()
        jogo.iniciar()
    except KeyboardInterrupt:
        print(f"\n\n{C.DIM}  Conexão interrompida.{C.RESET}")
        mensagem_eva("Fuga não é uma opção. Apenas um adiamento.")
        print()
    except Exception as e:
        print(f"\n{C.VERM_CLARO}  [ERRO CRÍTICO] {e}{C.RESET}")
        import traceback
        traceback.print_exc()
        print(f"{C.MAGENTA}  EVA-9: 'Até os erros são intencionais.'{C.RESET}")


if __name__ == "__main__":
    main()
