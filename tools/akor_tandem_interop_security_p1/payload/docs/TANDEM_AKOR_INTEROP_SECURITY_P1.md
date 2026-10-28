# Akor / Tandem P1 — frontiere d'integration, pas un nouveau moteur

## Autorites (immuables pour cette livraison)

- **Kontexte** possede le scenario, les etapes, roles et fragments narratifs.
- **Kompose** compile/simule et verifie le contrat de projection Ekole P1.
- **Akor** fait le controle croise **lecture seule** entre les trois depots; il ne decide pas de la progression, n'assigne aucun role reel et ne devient pas un moteur de workflow.
- **Orgo / Orgo_Worlds** conservent les transitions, autorisations et la WorldRelease canonique. Les UUID du P1 ne prouvent **aucune** release valide.
- **Ekole** conserve la projection enseignant et les preuves scolaires; completude d'une tache != competence acquise.

## Porte verifiable

La commande `run_akor_tandem.py` :

1. Charge les **modules sources existants** de Kompose V3 (`tandem_handoff.py`) et d'Ekole P1 (`projection.py`); refuse leurs absences.
2. Verifie l'aperçu synthetique **avec les deux validateurs proprietaires**, sans recoder leurs schemas.
3. Compare tenant, World, WorldRelease aux UUID **fournis explicitement par l'operateur**. Ce sont des etiquettes synthetiques declarees, **pas** une preuve de permission.
4. Verifie que le scenario et la correspondance des etapes/roles existent dans les sources synthetiques Kontexte.
5. Produit exclusivement un bilan de conformite sans contenu pedagogique prive, avec empreintes SHA-256. Aucun fichier ou service n'est modifie.

## Exemple de revue (UUID **fictifs**, ne pas reutiliser dans une vraie seance)

Depuis `C:\mycode\Ekole\akor`, avec les autres depots a leur emplacement habituel :

```powershell
py -3 run_akor_tandem.py `
  --kontexte 'C:\mycode\Ekole\Kontexte' `
  --kompose 'C:\mycode\Ekole\Kompose' `
  --ekole 'C:\mycode\Ekole\ekole' `
  --preview 'C:\mycode\Ekole\Kompose\examples\integrations\ekole-fete-sorciere.synthetic.json' `
  --tenant-id '11111111-1111-4111-8111-111111111111' `
  --world-id '22222222-2222-4222-8222-222222222222' `
  --world-release-id '33333333-3333-4333-8333-333333333333'
```

Le resultat doit inclure `runtime_admitted=false`, `teacher_authorized=false`, `permissions_verified=false`, `world_release_verified=false`, `dispatch_allowed=false` et `may_publish_to_child=false`.

## Exclusions explicites

- Aucun HTTP vers Orgo, aucune injection `--apply`, aucun Signal/Case/Task reel.
- Aucune prise en charge d'identites enfant, de permissions scolaires, de consentements ou d'approbation reelle.
- Aucune preuve de WorldRelease immuable ou de droit de divulguer les fragments.
- Aucun changement de `run_akor.py` (prequalification Boulangerie historique) ou des autres depots.
- Aucun appel a un fournisseur d'identite, a un reseau, a Docker ou au VPS.

## Qualification ulterieure

Authentification enseignant, approbation/audit serveur, controle scope et appartenance tenant/World/WorldRelease par les autorites canoniques, projections individuelles et fuites inter-groupes, commandes Orgo idempotentes et controles de versions, gestion de replis et evaluation pedagogique independante.
