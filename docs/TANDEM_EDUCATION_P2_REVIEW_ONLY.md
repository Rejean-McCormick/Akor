# Akor P2 — intention synthétique, sans admission

Akor génère une **intention de revue** à partir d'un handoff déjà accepté par ses validateurs Kompose V3 et Ekole P1. Il vérifie aussi la correspondance avec les étapes de Kontexte.

Commande (depuis la racine Akor, avec les dépôts voisins disponibles) :

```powershell
py -3 run_akor_tandem_intent.py --kontexte C:\mycode\Ekole\Kontexte --kompose C:\mycode\Ekole\Kompose --ekole C:\mycode\Ekole\ekole --preview C:\chemin\preview.json --tenant-id 11111111-1111-4111-8111-111111111111 --world-id 22222222-2222-4222-8222-222222222222 --world-release-id 33333333-3333-4333-8333-333333333333
```

Le JSON de sortie peut être donné aux **outils locaux** `scripts/tandem-education/scope-review.mjs` (Orgo_Worlds) et `tools/tandem-education/review-plan.mjs` (Orgo). La fixture 11 étapes a été vérifiée avec les modules réels de Kontexte, Kompose et Ekole.

Ce document **n'est pas un jeton**, ne contient pas d'identité d'enfant ni de fragment privé et ne démontre aucune approbation enseignante. Il n'a **aucune valeur d'autorisation**. Les véritables admissions exigent un contrôle d'identité, de permissions, d'appartenance de classe et de WorldRelease dans les services autoritaires, qui restent à implémenter et à qualifier.
