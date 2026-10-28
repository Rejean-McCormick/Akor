# AKOR — Tandem Education P2

Extraire cette archive **à la racine** de `akor` (au même niveau que `src/akor/preflight.py`). L'extraction n'applique pas le correctif.

1. `TANDEM_EDU_P2_AKOR` : `PREVIEW_TANDEM_EDU_P2_AKOR.cmd`
2. `INSTALL_TANDEM_EDU_P2_AKOR.cmd`
3. `VERIFY_TANDEM_EDU_P2_AKOR.cmd`

Rollback facultatif: `ROLLBACK_TANDEM_EDU_P2_AKOR.cmd`.

Le P2 implémente seulement une **revue synthétique hors ligne**. Les certificats d'identité, ACL réelles de classe, WorldRelease et admissions Orgo ne sont pas raccordés à cette étape. Ne pas utiliser ces fixtures comme jetons ni comme permissions d'enfant.

Le gestionnaire refuse toute divergence SHA-256 des sources sélectionnées et des fichiers d'ancrage avant écriture, sauvegarde l'état antérieur hors dépôt et vérifie les tests sur une copie temporaire.
