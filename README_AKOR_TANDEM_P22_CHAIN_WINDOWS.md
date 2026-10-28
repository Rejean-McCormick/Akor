# Akor P2.2 — correctif du lanceur transversal Windows

**Cause constatée :** l'ancien `CHECK_TANDEM_EDU_P2_CHAIN.cmd` transmettait `--akor "%~dp0"`.
La variable `%~dp0` se termine par `\` ; le `\"` final peut absorber le guillemet dans la
conversion Windows des arguments Python, supprimant ainsi `--worlds` et `--orgo`.

**Solution :** racine Akor `%~dp0.` sans antislash terminal et transmission explicite de
`--akor`, `--worlds` et `--orgo`. Vérification préalable des manifestes P2 voisins.

Extraction a la racine `C:\mycode\Ekole\Akor\Akor` (ne jamais extraire ailleurs).
Puis :

```powershell
cd 'C:\mycode\Ekole\Akor\Akor'
.\PREVIEW_AKOR_TANDEM_P22_CHAIN_WINDOWS.cmd
.\INSTALL_AKOR_TANDEM_P22_CHAIN_WINDOWS.cmd
.\VERIFY_AKOR_TANDEM_P22_CHAIN_WINDOWS.cmd
.\CHECK_TANDEM_EDU_P2_CHAIN.cmd
```

Rollback facultatif : `.\ROLLBACK_AKOR_TANDEM_P22_CHAIN_WINDOWS.cmd`.
Sauvegarde automatique sous `C:\mycode\Ekole\Akor\Tandem_Local\akor_tandem_education_p22_chain_cmd`.

Le correctif modifie **uniquement** `CHECK_TANDEM_EDU_P2_CHAIN.cmd`. Aucun contenu
Orgo, Orgo_Worlds, Akor applicatif, base, service ni VPS n'est modifié.

La validation de chaine est une **revue synthetique hors ligne**, pas une admission runtime.
