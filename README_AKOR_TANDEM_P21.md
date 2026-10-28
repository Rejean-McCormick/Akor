# Akor Tandem P2.1 — Verifications strictes (Windows)

**Portee:** correction de l'installateur P2 deja installe. Aucun fichier applicatif Akor,
aucune donnee, aucun service, aucune base, ni aucun depot voisin n'est modifie.

**Cause:** le test isolé apres INSTALL n'incluait pas `run_akor_tandem_intent.py`.
La commande `compileall` affichait `Can't list` sans retourner d'erreur.

**Correctif unique:** `tools/tandem_education_p2/manifest.json` :
- `test_copy` inclut desormais `run_akor_tandem_intent.py`;
- une commande `python -m py_compile run_akor_tandem_intent.py` executee dans la copie isolee
  retourne une erreur si le lanceur est absent.

Extraire le ZIP a la racine `C:\mycode\Ekole\Akor\Akor`.
Puis, depuis PowerShell:

```powershell
.\PREVIEW_AKOR_TANDEM_P21.cmd
.\INSTALL_AKOR_TANDEM_P21.cmd
.\VERIFY_AKOR_TANDEM_P21.cmd
```

Option de retour arriere sur ce manifeste: `.\ROLLBACK_AKOR_TANDEM_P21.cmd`.
La sauvegarde est sous `..\Tandem_Local\akor_tandem_education_p21\backups`.

**Etape distincte, facultative:** `.\CHECK_TANDEM_EDU_P2_CHAIN.cmd` lance les outils
P2 existants des trois depots en lecture seule, sans credentiels, reseau, DB ni Orgo apply.
C'est une qualification des CONTRATS SYNTHETIQUES, pas une admission runtime.
