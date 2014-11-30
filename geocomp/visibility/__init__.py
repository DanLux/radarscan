#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Algoritmos para o Problema da visibilidade:

Dado um conjunto de segmentos e um ponto disjuntos, determinar os trechos
visíveis dos segmentos a partir do ponto.

Algoritmos disponíveis:
- Linha de varredura polar

algoritmo ótimo = executa em tempo O(n lg(n)), n = número de segmentos
"""

import scanline

# cada entrada deve ter:
#  [ 'nome-do-modulo', 'nome-da-funcao', 'nome do algoritmo' ]
children = (
	( 'scanline', 'radar_scan', 'Linha de Varredura' ),
)

__all__ = map (lambda a: a[0], children)
